# Contributing to documentation

Thanks for your interest in contributing to the OFO documentation. This guide will help you get started.

The docs are written in [Markdown](https://www.markdownguide.org/), with some extensions for tabs and other features. See the [MkDocs documentation](https://www.mkdocs.org/user-guide/writing-your-docs/) for details.

There are two main options for contributing: via the GitHub web interface or by editing a local copy of the documentation files.

## GitHub web interface

This is the easiest way to contribute immediately with no setup (just a GitHub account), but for large changes or numerous successive changes, it can become tedious and end up taking more time.

To edit a page, navigate to that page on the docs site and click the "Edit this page" :material-note-edit-outline: button in the top right corner. This will take you to the GitHub record for that file, in editing mode. (You need to be logged in to GitHub.) Make your changes and then click the "Commit changes..." button in the top right. You will get a pop-up box that asks for a commit message describing your change. Enter a message.

=== "External contributors"

    Click "Propose changes". This will take you to a page where you can review your changes ("diffs") and create a pull request. If you want to make more edits, the easiest way is to go back to the documentation site and click the "Edit this page" button again. You will return to the GitHub editing page with your previous changes still there. Once your changes look good, click "Create pull request". Optionally customize the pull request title and description to summarize your changes for the docs maintainers, and then click "Create pull request" again. You will be taken to the pull request page, where you can see the status of the automated tests and any comments from the maintainers. If the tests pass, a maintainer will review your changes and merge them into the documentation. For detailed background on pull requests, see the [GitHub documentation](https://help.github.com/articles/about-pull-requests/).

=== "Internal contributors"

    **For simple changes**, you can click "Commit changes" to commit directly to the main branch. The live docs website should update within a few minutes to reflect your changes.
    
    **For more complex changes** or those you want someone to review, select "Create a new branch for this commit" then click "Propose changes". This will create a new branch in the docs repo with your changes committed, and will take you to a page where you can review your changes ("diffs") and create a pull request. If you want to make more edits before submitting the pull request, you would then need to find that page in the GitHub repo, make sure you're in your new branch, and click the "Edit this file" button in the top right. Once your changes look good, click "Create pull request" and then tag someone to review it.

## Local clone or fork of docs repository

If you're going to make more than a simple change or two, it will probably be easier to set up a local clone or fork of the docs repository, so that you can edit the docs files on your local computer, preview them locally, and push your changes to GitHub when you're ready.

=== "External contributors"

    Create a "fork" of the docs repository in your own GitHub account by clicking the "Fork" :octicons-repo-forked-16: button in the top right of the [docs repository home page on GitHub](https://github.com/open-forest-observatory/ofo-docs). This will create a copy of the docs repo in your own GitHub account. Then clone your fork to your local computer using `git` from the command line or the git GUI of your choice.

    Make your edits locally to the relevant markdown files in the `docs` folder, using the text editor or IDE of your choice.

    When you're happy with your changes, commit them to your local clone and push them to your fork on GitHub. Then go to your fork of the OFO Docs repository on GitHub and click the "New pull request" button in the top right. Click "Create pull request". Optionally customize the pull request title and description to summarize your changes for the docs maintainers, and then click "Create pull request" again. You will be taken to the pull request page, where you can see the status of the automated tests and any comments from the maintainers. If the tests pass, a maintainer will review your changes and merge them into the documentation. For detailed background on pull requests, see the [GitHub documentation](https://help.github.com/articles/about-pull-requests/).

=== "Internal contributors"

    Clone the [docs repo](https://github.com/open-forest-observatory/ofo-docs) locally
    
    **For simple changes**, you can commit directly to the main branch and push directly to main on GitHub. The live docs website should update within a few minutes to reflect your changes.
    
    **For more complex changes** or those you want someone to review, in your local clone of the docs repo, create a new branch for your changes.

    Make your edits locally to the relevant markdown files in the `docs` folder.

    When you're happy with your changes, commit them to your local branch and push them to your branch of the OFO Docs repository on GitHub. Then [create a pull request](https://github.com/open-forest-observatory/ofo-docs/pulls) and either merge it yourself or request a review.

### Previewing the docs site locally as you edit

Installation: `pip install mkdocs mkdocs-material mkdocs-awesome-pages-plugin mkdocs-nav-weight mkdocs-git-revision-date-localized-plugin mkdocs-git-committers-plugin-2`

From your local docs repository directory, run `mkdocs serve`. This will start a local web server that you can access at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser. It updates every time you save your changes to a docs file locally.