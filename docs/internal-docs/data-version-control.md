# Data version control

Notes and tips as we develop our data version control practices. **This is still a work in progress!**

## Datalad

### Clone a code repository containing a version-controlled (Datalad/git-annex) dataset as a submodule

To clone a code repo and also obtain datalad data submodules ("subdatasets" in Datalad terms) (just the data file pointers, not actual data):

`datalad install -r <repo url>`

This appears to clone the data submodules at the state (commit) referenced from the parent repository, even if there are more recent commits to the submodules. Optionally, add `-g` to get the actual data underlying the data file pointers from the remote repositories, if auto-enabled.

(The above appears to be the same as `git clone --recursive <repo url>`.)

If the code repository has already been cloned *without* the data submodules (e.g. via `git clone` without `--recursive`, or `datalad install` without `-r`), you can obtain the submodules from witihn the parent repo with:

`datalad install -r .`
or from within the (empty) submodule folder with
`datalad install .` or `datalad get -n`.

(These both appear to clone the data submodules at the state (commit) referenced from the parent repository.)

To check if your dataset (submodule) state is current with its remote:
`git status`

(You can use `datalad status` but it does not check status relative to the remote, just checks for changes to local files.)

To pull the most recent version (commit) of the dataset (submodule) (useful, for example, if you cloned a code repo that contained a data submodule frozen at a specific commit that has since been update):

`datalad update --how merge`
or
`git pull`

If you checked out a different commit of the dataset submodule and want to restore it to the version that is tagged in the parent code repo (assuming you haven't made a commit there to update the dataset version tag): `cd` to the parent code repo and run `git submodule update`, possibly with the `--init` option.

(The following does not seem to work [as documented](https://docs.datalad.org/en/stable/generated/man/datalad-update.html): to pull the version (commit) of the dataset registered in the parent repo, run
`datalad update --how merge --follow parentds` or potentially instead of `merge`, use `checkout`. )

To enable access to the data files (in cloud storage) underlying a Datalad/git-annex dataset, see [this section](#enable-access-to-the-data-files-in-cloud-storage-underlying-a-dataladgit-annex-dataset).


### Clone existing remote dataset (with metadata on GitHub and files on CyVerse), not inside a code repository

* `datalad clone <github url>`
* Enable the 'siblings' (data storage remotes): run the `datalad siblings ...` command suggested in output of the `clone` command. For CyVerse WebDAV, enter username and password when prompted.
    * Note: Once I got an error `Failed to create the collection: Prompt dismissed..` and the solution (I'm not clear on why) was to first run `export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring` per [this post](https://github.com/python-poetry/poetry/issues)
* Check that the siblings were added: `datalad siblings`. You should see `origin`, `here`, and `cyverse`. `(+)` means it contains data files, not just pointers/metadata.
* Set up your repo to push data to cyverse whenever you commit metadata changes to github (from the root of the repo): `datalad create-sibling-github -d . <name-of-repo> --publish-depends cyverse --existing reconfigure`
    * It would be great if we could find a way to have this setting saved in the DataLad settings in the GitHub repo so all clones use it by default.
* Locally download a file/folder/glob: `datalad get <file/folder/glob>`
* Modify the data locally
* Push your changes datalad push --to origin
    * Note: I haven't figured out why it doesn't work to push data with `datalad push --to cyverse` the way it does if you're the one who created the dataset. (This is only relevant if you have not set up the repo to push to cyverse whenever committing to github as instructed above. However, a workaround appears to be `datalad push --data anything` though I'm not completely sure what this is intended for.
* Pull remote changes from GitHub (pointers/metadata only): `datalad update --how merge`


### Enable access to the data files (in cloud storage) underlying a Datalad/git-annex dataset

To enable access to a "data remote" ("data sibling" in datalad terms; "special remote" in git-annex terms), `cd` to the repo and run `datalad siblings enable -s <name of sibling>`. To get a list of remotes that can be initialized, use `git annex initremote`. If you need to change anything about the data remote, or re-authenticate, see the docs for [datalad sibling update](https://docs.datalad.org/en/stable/generated/man/datalad-siblings.html) or the docs for [git-annex configremote](https://git-annex.branchable.com/git-annex-configremote/).

For the CyVerse WebDAV special remote, enter username and password when prompted.
    * Note: Once I got an error `Failed to create the collection: Prompt dismissed..` and the solution (I'm not clear on why) was to first run `export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring` per [this post](https://github.com/python-poetry/poetry/issues).

If the data remote that you want to use is configured as an "rclone remote", you will need to [install rclone](https://rclone.org/install/), configure it to access the data remote as instructed by the dataset provider, and install the [rclone special remote package](https://github.com/git-annex-remote-rclone/git-annex-remote-rclone) for git-annex.

### Create and publish a Datalad/git-annex dataset

* Create a dataset (git repo): `datalad create -c text2git <name-of-dataset>` and `cd` into it
* Optionally make larger text files be stored outside the git repo, in the 'annex' (by default the `text2git` config makes all text files be stored in the git repo): `nano .gitattributes` and change `...(mimeencoding=binary)and(largerthan=0)...` to `(mimeencoding=binary)or(largerthan=10kb)`
    * Then commit this change to the git repo
* Consider [setting the hashing backend](https://git-annex.branchable.com/backends/) to be BLAKE2B160E for > 2x faster hashing
* Copy data files into the repo (can use `datalad download-url` to track provenance in metadata)
    * Note to self: download raw imagery: `rclone copy gdrive:Natural_Reserves_Bucciarelli/KMZs original/KMZs --transfers 16 --progress --drive-shared-with-me`
* Check status: `datalad status`
* Save (commit) its state: `datalad save -m "<message>"` (optionally specific specific files/folders to save)
    * It took about 30 min to save a dataset of ~6000 drone images. Interested to know if plain git-annex would be faster.
* [Option 1] Create Cyverse remote ('sibling') for data: `WEBDAV_USERNAME=<username> WEBDAV_PASSWORD=<password> git annex initremote cyverse type=webdav url=https://data.cyverse.org/dav/iplant/projects/ofo/datalad-testing2 chunk=100mb encryption=none` (you can alternatively set the username and password env vars in advance of this call)
* [Option 2] Create a Box (or other `rclone`-enabled) remote for data:
    * Install rclone via `sudo apt install rclone`
    * Set up rclone for your Box account via `rclone config`
    * Run `sudo apt install git-annex-remote-rclone`
    * Run `git annex initremote box type=external externaltype=rclone chunk=100MiB encryption=none target=<name of your remote in rclone> prefix=<path to the data folder in your Box account>`
* Create github remote repo ('sibling') for metadata and small files: `datalad create-sibling-github -d . -s github-ofo ucnrs-data --github-organization open-forest-observatory --publish-depends cyverse <optionally: another --publish-depends for other data remotes>`. The `--publish-depends` part sets it up to trigger data upload to cyverse whenever the metadata is committed to github; otherwise you'd need two commands every time.
    * Note: Once I got an error `Failed to create the collection: Prompt dismissed..` and the solution (I'm not clear on why) was to first run `export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring` per [this post](https://github.com/python-poetry/poetry/issues/1917#issuecomment-1380429197).
* To set it up to autoenable the remotes upon `datalad install` performed by collaborators (so they don't have to run `datalad siblings enable`, when doing `git annex initremote`, add `autoenable=true`. This probably only makes sense for remotes not needing authentication, like a public-readable remote. If you've already added a remote without autoenable and you want to turn on autoenable, use `git annex configremote <remote name> autoenable=true`.
* Push the data and metadata to cyverse & github: `datalad push --to github-ofo`

### Add a Datalad dataset as a subdataset within an existing git repo

* `cd` into your git repo
* Not sure if necessary: make your git repo a Datalad repo too: `datalad create --force --no-annex`
* Clone the existing dataset into your top-level repo as a 'subdataset': `datalad clone --dataset . <github url>`
* `cd` into the new subdataset
* Enable siblings as [described above](#enable-access-to-the-data-files-in-cloud-storage-underlying-a-dataladgit-annex-dataset)
* Continue in [above section](#clone-existing-remote-dataset-with-metadata-on-github-and-files-on-cyverse-not-inside-a-code-repository) at "Set up your repo to push data to cyverse whenever you commit metadata changes to github"

### Delete a remote

* Edit the `.git/config` file and delete the respective remote entries.

### Notes on transfer speeds

* With 40 GB of data, mostly individual drone images
    * Box rclone remote with -J16: ~120 MB/s
    * GIN remote with -J16: ~10 MB/s
    * Cyverse WebDAV remote with -J5: ~2 MB/s
* With 160 GB of data, composed of 4 zip archives (38G, 22G, 96G) and remotes set to use 100 MB chunks:
    * Box with -J16: ~180 MB/s (used one thread per original file, not chunk)
    * GIN with -J16: ~4 MB/s (same as ^)
    * Cyverse WebDav with -J5: ~45 MB/s (same as ^)
* Same as above but using 500 MB chunks:
    * Box: 210 MB/s
    * CyVerse: ~45 MB/s (each transfer -- of 3 total -- seemed to have only ~12 MB/s even excluding the per-file overhead, which is now a much smaller fraction of the total transfer time with the larger chunks)

Interrupted transfers properly resumed on all three remotes (at least from the last transferred chunk).

## DVC

### Notes on usage challenges

* `dvc pull` can be given paths inside tracked directories. You can specify the actual file you want (as opposed to the *.dvc file). But **how do you know the directory listing** in order to request them?
    * With git-annex you can see the file listing because all the files show up as broken symlinks (until you pull the data, when they become unbroken).
* When you use `dvc pull` on a granular data sub-component of a tracked directory and then modify that file, are the granular file-level changes tracked anywhere?
    * No. DVC will tell you that the tracked directory was changed, but it seems you have to know which file was change in order to do `dvc add <the-changed-file>` (or maybe you can do `dvc add <tracked-directory>` and it will add the changes to the file. Also, it will not tell you what sub-files were changed, it only knows that something changed in the directory.
* If you download part of the full data repo (even everything associated with one .dvc file) and then update it (or even don't update it), you can't just do a generic `dvc push` to push the changes and "sync" your local changes with the data storage remote. You get an "unexpected error" related to the data files that you never downloaded. Also, if the files you downloaded were a subset of the files within the directory tracked by, e.g., `folder1.dvc` and you then do `dvc push folder1`, this will have the unintended consequences of permanently deleting all the files in that folder other than the ones you did download. The only way to download, modify, and push a subset of files in a tracked folder is to explicitly push those files.
* When you add files/dirs to the repo, you have to explicitly `dvc add` each one (at whatever level you want them to be tracked), whereas git-annex can automatically track all of them; there are no separate units that are tracked, just all files.
* Added all images in a directory individually to DVC tracking with `dvc add *` but then could not find an equivalent `dvc remove *` to remove them all. Clearly adding all images individually is not the intended use method.

### Notes to self for config

* `git init`, `dvc init`, add files to repo.
* dvc remote add -d cyverse webdavs://data.cyverse.org/dav/iplant/projects/ofo/datalad-testing4
* dvc remote modify --local cyverse_public user <cyverse username>
* dvc remote modify --local cyverse_public password <cyverse password>
* Mostly followed [this](https://dvc.org/doc/start/data-management/data-versioning)
