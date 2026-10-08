"""
MkDocs hook: automatically link glossary terms to their definitions.

Terms are declared in the front matter of the glossary page, mapping each
heading anchor to the phrases that should link to it:

    glossary:
      chm: [canopy height model, CHM]

Every occurrence of a phrase on any other page becomes
`<a class="term" data-preview href=".../glossary.md#chm">`, which Material for
MkDocs renders as a hover preview of the definition. Text inside links, code,
headings, and math is left alone. A page can opt out with `glossary_links: false`
in its front matter.
"""

import logging
import posixpath
import re
import xml.etree.ElementTree as etree

from markdown import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import AtomicString
from mkdocs.structure.pages import _RelativePathTreeprocessor
from mkdocs.utils.meta import get_data

log = logging.getLogger("mkdocs.hooks.glossary")

# Path of the glossary page, relative to docs_dir
GLOSSARY = "tutorials/glossary.md"

# Link only the first occurrence of each term per page, instead of all of them
FIRST_ONLY = False

# Elements whose text is never annotated
SKIP_TAGS = {"a", "code", "pre", "kbd", "abbr", "script", "style",
             "h1", "h2", "h3", "h4", "h5", "h6"}

# Built in on_files: compiled pattern with one named group per phrase, and the
# anchor each group links to
_pattern = None
_anchors = {}


def on_config(config):
    config.markdown_extensions.append(GlossaryExtension())
    return config


def on_files(files, config):
    global _pattern, _anchors
    _pattern, _anchors = None, {}

    file = files.get_file_from_path(GLOSSARY)
    if file is None:
        log.warning(f"Glossary page '{GLOSSARY}' not found; terms will not be linked")
        return files

    source, meta = get_data(file.content_string)
    terms = meta.get("glossary") or {}

    # Warn about anchors with no matching heading, e.g. after a rename
    ids = set(re.findall(r"\{[^}\n]*#([\w-]+)", source))
    for anchor in terms:
        if anchor not in ids:
            log.warning(f"Glossary term '{anchor}' has no heading with id '#{anchor}' in {GLOSSARY}")

    # Longest phrases first, so "canopy height model" wins over "canopy"
    phrases = sorted(
        ((str(p), a) for a, ps in terms.items() for p in ([ps] if isinstance(ps, str) else ps)),
        key=lambda item: -len(item[0]),
    )
    groups = []
    for i, (phrase, anchor) in enumerate(phrases):
        body = r"\s+".join(re.escape(word) for word in phrase.split())
        # Acronyms (all caps) match case-sensitively, everything else doesn't
        if not phrase.isupper():
            body = rf"(?i:{body})"
        groups.append(rf"(?P<t{i}>{body}s?)")
        _anchors[f"t{i}"] = anchor
    if groups:
        _pattern = re.compile(r"(?<!\w)(?:" + "|".join(groups) + r")(?!\w)")
    return files


class GlossaryTreeprocessor(Treeprocessor):

    def run(self, root):
        if _pattern is None:
            return

        # Python Markdown doesn't know which page it's rendering, but MkDocs'
        # relpath treeprocessor does (same approach as material.extensions.preview)
        relpath = self.md.treeprocessors["relpath"]
        if not isinstance(relpath, _RelativePathTreeprocessor):
            return
        file = relpath.file
        if file.src_uri == GLOSSARY:
            return
        if file.page is not None and file.page.meta.get("glossary_links") is False:
            return

        self.href = posixpath.relpath(GLOSSARY, posixpath.dirname(file.src_uri) or ".")
        self.seen = set()
        self._walk(root)

    def _walk(self, el):
        for child in list(el):
            if not self._skip(child):
                self._walk(child)
            split = self._split(child.tail)
            if split:
                child.tail, links = split
                index = list(el).index(child) + 1
                el[index:index] = links
        split = self._split(el.text)
        if split:
            el.text, links = split
            el[0:0] = links

    def _skip(self, el):
        return (
            not isinstance(el.tag, str)
            or el.tag in SKIP_TAGS
            or "arithmatex" in el.get("class", "")
        )

    def _split(self, text):
        """Return (leading text, [link elements with tails]) or None."""
        if not text or isinstance(text, AtomicString):
            return None
        lead, links, pos = text, [], 0
        for match in _pattern.finditer(text):
            anchor = _anchors[match.lastgroup]
            if FIRST_ONLY:
                if anchor in self.seen:
                    continue
                self.seen.add(anchor)
            link = etree.Element("a", {
                "href": f"{self.href}#{anchor}",
                "class": "term",
                "data-preview": "",
            })
            link.text = AtomicString(match.group(0))
            if links:
                links[-1].tail = text[pos:match.start()]
            else:
                lead = text[:match.start()]
            links.append(link)
            pos = match.end()
        if not links:
            return None
        links[-1].tail = text[pos:]
        return lead, links


class GlossaryExtension(Extension):

    def extendMarkdown(self, md):
        # After inline processing (20), so code spans etc. are real elements,
        # and before relpath (0), so MkDocs resolves and validates our links
        md.treeprocessors.register(GlossaryTreeprocessor(md), "glossary", 15)
