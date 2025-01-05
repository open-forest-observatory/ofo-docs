# Using Jetstream2 for OFO development

## Getting set up

### New users

These steps are required once per new user.

1. Create an [ACCESS](https://access-ci.org/) account and provide your username to your supervisor,
   so they can add you to our project. Before performing the next steps, wait until your supervisor
   confirms you are added to our ACCESS project.
1. Create (or locate an existing) SSH key. You can google instructions for your operating system, or
   follow [this suggested
   guide](https://medium.com/@mbohlip/generating-ssh-key-pairs-on-a-windows-mac-linux-0e9993bf2985).
   If you'd like more detail, here's [more detailed tutorial](https://happygitwithr.com/ssh-keys) (read
   sections 10.1 through 10.4). Note: this detailed tutorial is designed for R and RStudio users, but you can
   ignore all the refenreces to R and RStudio and focus on the shell instructions.
1. Add your public SSH key in [Exosphere](https://jetstream2.exosphere.app/): Log in with your ACCESS credentials (once added to our project), go to our project/allocation (BIO220124), click Create in the top right, and click SSH Public Key. Enter a public key name (e.g. `derek-laptop01`) and paste in the key text.

If you will need CACAO to create Kubernetes clusters (such as if you are helping with infrastructure engineering--your supervisor will tell you if so), you should also do the following:

1. Add credentials in [CACAO](https://cacao.jetstream-cloud.org/):
   1. Log in to [CACAO](https://cacao.jetstream-cloud.org/) with your ACCESS credentials.
   2. Add a credential for the OFO ACCESS project (BIO220124): go to Credentials (key icon), click Add Credential in the top right, and click Cloud Credential. Choose Jetstream2, log in at the ACCESS prompt, and select the project BIO220124.
   3. Add your public SSH key: go to Credentials (key icon), click Add Credential in the top right, and click SSH Public Key. Enter a public key name (e.g. `derek-laptop01`) and paste in the key text .


### New VMs

These steps are required once for each new VM that a user desires. This should be done during initial onboarding (after the new user steps above), and it can also be done whenever an updated or additional VM is desired. There are several events that may trigger users to want a new VM:

- OFO updates its [development VM template](https://github.com/open-forest-observatory/ofo-ansible) (which is applied on top of a Jetstream2 featured Ubuntu image)
- You need more compute nodes
- You screwed up your VM configuration and want to start fresh

Follow these steps to create and configure a new instance:

1. Go to [Exosphere](https://jetstream2.exosphere.app/exosphere/) and select our project/allocation (BIO220124).
2. Click **Create** -> **Instance** in the top right.
3. Click the **By Image** tab, search for `ofo-dev`, find the newest image (should be at the bottom), and click *Create Instance*.
4. For **Name**, enter a name that's descriptive to you and starts with your name. For example, `derek-01`.
5. For **Flavor**, select **m3.small** to start, unless you know you will need more compute immediately. You can resize later when you need more compute. Exception: If you will need a g3.xl (unlikely for new OFO members), you may need to create it now, because the GPU drivers are different for this specific flavor (though JS2 may have resolved this).
6. For **Choose a root disk size**, select **Custom** and enter `50` (GB) unless you know you will need something larger. Normally you won't because most data is stored on `/ofo-share` which is not part of this 60 GB. [This selection actually does not affect the instance creation, which uses the image's disk size.]
7. For **Enable web desktop**, select **Yes**, unless you know you will not need it (unlikely for new OFO members).
8. For **Choose an SSH public key**, select the key you added in the previous section.
9. Click **Create**.
10. Pull up the instance's page by clicking on the **Instances** box and then clicking on the instance name. Wait for the status in the top-right to change to **Ready** in green (2-3 min).

Note that others in our project can access the instances you create, so *do not store unencrypted credentials* or other private or sensitive information on them. See the [Security](#security) section below for solutions.

## Basic instance access and management

### SSH access

SSH into your instance using `ssh exouser@<ip address>`. You can find the IP address of your instance on the instance's page in [Exosphere](https://jetstream2.exosphere.app/exosphere/).

### Remote desktop access

To access a graphical remote desktop in a browser tab, navigate to that instance's page in [Exosphere](https://jetstream2.exosphere.app/exosphere/) and click the **Web Desktop** button.

### Shelving and unshelving

It is **very important** that you shelve your instances when not using them, especially the larger instances. 

The easiest way to shelve and unshelve is via the instance's page in [Exosphere](https://jetstream2.exosphere.app/exosphere/):

1. Go to our project/allocation (BIO220124)
1. Click on Instances
1. Click on your instance
1. In the top right under "Actions", select "Shelve"

Note that this has the same effect as powering off a computer: all unsaved work will be lost, and next time you will start from a fresh boot. Use this same approach to unshelve your instance when you're ready to resume work, and to resize your instance if you need more compute or memory (see below). Note that after unshelving, there may be a brief delay before the web desktop becomes available or before you can SSH in.


### Resizing

Resizing is super useful to enable you do do simple tasks like coding and low-compute testing with a small instance (uses less of our allocation budget) and then sizing up when necessary for large compute jobs. Note that resizing involves a reboot, so any unsaved work will be lost. The `m2.small` instance size is sufficient for code development with lightweight processing.

Resize the instance via the instance's [Exosphere](https://jetstream2.exosphere.app/) page, using the Actions menu on the top right of the instance page.

### More details

More details on instance access and management can be found in the [Jetstream2 documentation](https://docs.jetstream-cloud.org/), including:

- [Instance Management Actions](https://docs.jetstream-cloud.org/ui/exo/manage/#instance-management-actions)

## Using instances

### `/ofo-share/`

Instances have very limited storage specific to the instance, but they are set up to mount an 8 TB shared volume at `/ofo-share/`. This is where all project data and code should be stored. For each project you work on, create (or use an existing) subfolder of `/ofo-share/` to hold the data.

#### Code repositories: development

For code development, each person should create a subfolder `/ofo-share/repos-<firstname>` to hold all their code repositories. Doing it this way (rather than everyone accessing the same code files) allows each person to work in their own branch and make their own changes that don't affect other people. The code you modify will be accessible to other people (via their own copies of the repo) when you push your commits.

In contrast to **code** development, the **data** that the repo operates on should be in a general project data folder so that everyone can access it (so we don't need multiple copies of the data on `/ofo-share/`).

#### Code repositories: production

The folder `/ofo-share/utils` is intended to hold the current public, production code (generally the most recent commit in the `main` branch) of our code libraries. Use the code here if you need to use some of our OFO functions for an analysis (as opposed to actively developing/testing them, in which case they should be in your own `repos-<firstname>` folder). We can regularly `git pull` in these repos to keep them up to date with the remote, but don't directly edit the code in this folder or push from it.

#### Temporary data

For temporary data that you don't want to store in a project's data folder, you can use a folder `/ofo-share/scratch-<firstname>` or `/ofo-share/tmp/`.

### Data transfer

For data files on cloud storage such as Box or CyVerse, an incredibly value command line tool is `rclone`. To set up an account, use `rclone config` and follow the instructions. Assuming you set up a Box account with the name `box_myname`, you'd transfer data with a command like: `rclone sync box_myname:projects/myproject_data/ /ofo-share/myproject_data --progress --transfers 16`.

Please note that it is essential that you **encrypt your rclone configuration file**, as it will contain your login credentials to cloud storage providers. To do this, run `rclone config` and select the option "Set configuration password".

### Jupyter Notebook / Jupyter Lab

You can get Jupyter Lab in a browser tab (accessible from anywhere on the internet) using Jupyter server on your instance. It's best if you start the server from the root of the `/ofo-share` folder so you have easy access to all files there. Run:

```
cd /ofo-share/
/ofo-share/utils/environments/jetstream/jupyter-lab.sh
```

then copy the last URL shown in the terminal and paste it into a browser. Inside a notebook you should be able to choose different kernels (conda environments) that are configured for the user account running the server. When you're done, shut down the notebook server (either from the notebook, or from the terminal by doing Control-C twice) to prevent access to the server by others. If you want a basic Jupyter notebook instead of Jupyter Lab, you can use `/ofo-share/utils/environments/jetstream/jupyter-notebook.sh`.

### RStudio

Use RStudio Server; don't use RStudio GUI via a remote desktop. RStudio Server has all the same functionality and many conveniences. RStudio Server is a version of RStudio that runs in a browser tab on your local machine, but all the data and compute comes from your remote VM. Access RStudio from the browser on your local computer at `https://<ip address>`. Log in using username `exouser` and the passphrase found on your instance's page in [Exosphere](https://jetstream2.exosphere.app/). The first time you access RStudio Server via HTTPS, you will likely get a warning about an unsigned SSL certificate, but that is OK; it's the certificate installed upon VM creation and it enables a secure connection even though it's not signed.

#### RStudio and git

To interface with `git` for code development in RStudio, you can use the command line or use RStudio's built-in git functionality under the Git tab in the top right pane (shows up when you've opened a project that is a git repo). However, we recommend that you use VS Code for git (either via its graphical tools or its terminal) because it does not require storing your credentials on the VM. If you do want to use RStudio's git functionality or the VM's native terminal (not via VS Code), you need to set up a private encrypted folder to store your git credentials so they cannot be accessed by others on our project. See the [Security](#security) section below for instructions.

#### RStudio and `/ofo-share`

The RStudio Server file browser defaults to the `~/` directory. To access a higher-level directory on the instance (and specifically the `/ofo-share/` folder), you need to click the `...` in the top  right of the file browser and enter `/` at the prompt. Then you will see all top-level directories on the instance and you can navigate to `/ofo-share/`.

### VS Code

[VS Code](https://code.visualstudio.com/) is a very powerful and flexible code editor that can be run on your local machine. It is strong for both Python and R (though its debugging features are more finnicky than those in RStudio). Your local instance of VS Code can easily connect to JS2 VMs to edit and execute code remotely, so you only need to install VS Code locally.

#### Connecting to remote server from VS Code: first time

- Install the the VS Code extension "Remote - SSH"
- Connect to the remote VM by clicking the '><' button in the bottom left
- Click 'Connect to host'.
- Click 'Add new SSH host'. Type `ssh exouser@<vm_ip_address>`.
- When prompted, choose to update the SSH config in `/home/<username>/.ssh/config`
- Click the '><' button again, then 'Connect to host...', then select the host you just added. You may need to repond 'Yes' to accept the fingerprint of the host.

#### Connecting to remote server from VS Code: after first time

- Click the '><' button, then 'Connect to host...', then select the host IP (or name) you want to connect to.
- Open a code folder on the remote host by clicking 'Open folder...'. You'll probably want to navigate up the directories (`..`) and into `/ofo-share/repos-<yourname>/`.

#### Setting up VS Code for R

Note that if you want to set up your local machine for R editing too, the steps below are not complete because some additional steps have already been completed on the OFO VM image. For full steps, [see here](https://code.visualstudio.com/docs/languages/r).

- Open the plugins pane (click on the 4 blocks icon in the left)
- Find the `R` plugin. Install it locally. Then click 'Install in SSH'.
- Find the `R Debugger` plugin. Install it locally. Then click 'Install in SSH'.
- **Set up the radian R terminal** (it has autocompletion, syntax highlighting, etc): 
    - In the extensions pane, click the gear next to the R extension, and click 'Extension settings'. Find the setting 'Rterm: Linux'. In the box, enter `/opt/radian`. NOTE: If your local machine is linux, this setting will also apply there. Therefore I recommend you put a symlink to your local radian binary (likely located at `~/.local/bin/radian`) at `/opt/radian`. This is how the VM is set up.
    - Enable the extension's "bracketed paste" option: In the extension settings, find the setting 'Bracketed Paste' and check the box.
- Code linting is enabled by default. To change what types of issues get flagged by the linter, [see here](https://code.visualstudio.com/docs/languages/r#_linting).

### Run command line processes without staying connected

Many types of command line processes are long-running and you don't want to have to stay signed in via an SSH connection to keep them running. Examples include large `rclone` data transfers and long data processing runs. To create processes that stay running even when your SSH connection closes, one approach is to use the [`tmux`](https://github.com/tmux/tmux/wiki) or [`screen`](https://www.gnu.org/software/screen/manual/screen.html) tools.

To use `tmux`, in a SSH session, type `tmux` and hit enter at the prompt. Now you can run commands like usual, except that if you are disconnected (e.g. you close your terminal window), they continue running. You can reconnect by starting another SSH session and typing `tmux attach`. You can also run multiple processes ("windows") within one SSH session via `tmux`. To start a new one, type `Control-B C`. To move between windows, type `Control-B #`, where `#` is the index of the window (indicated in the bottom panel; starts at 0). To close one, switch to it and then type `Control-B &`.

To use `screen`, in a SSH session, type `screen` and hit enter at the prompt. Now you can run commands like usual, except that if you are disconnected (e.g. you close your terminal window), they continue running. You can reconnect by starting another SSH session and typing `screen -dr`. You can also run multiple processes ("windows") within one SSH session via `screen`. To start a new one, type `Control-A C`. To toggle between that one and the original, type `Control-A Control-A`. If you create more than two, select from them by typing `Control-A Shift-"`. To close one, make it active (by selecting it from the menu that appears after typing `Control-A Shift-"`) and then type `Control-A K`.

### Use GUI software via remote desktop

Instances support a remote desktop that you access via a browser tab. To access it, navigate to the instance's page in CACAO and then click the Web Desktop icon. (If it does not load properly, try first opening a "Web Shell" from CACAO and closing it, and/or waiting 1 minute after unshelving.) Most software can be started via the "Activities" menu, which you can access with the Activities button in the top right (and then searching for the software name) or via the "9 dots" button in the bottom panel. Note that as configured, the bottom panel gets hidden when software windows overlap it, in which case you have to use the "Activities" button.

**Web browser:** Firefox browser comes preinstalled as part of the JS2 featured image.

## Metashape

The Metashape GUI is installed on the OFO dev image.

The Metashape python module is also installed, specifically in the conda environment `meta`. For running Metashape and the `automate-metashape` repo code from the command line, switch to the environment using `conda activate meta`. We aim to keep the `meta` environment updated with the current version of Metashape.

## Security

Anyone in our Jetstream project can access the instances you create, so *do not store unencrypted credentials* or other private or sensitive information on them. Here are some solutions for common credentials.

### Rclone

To store your rclone configuration file securely, you can encrypt it using `rclone config`. Run `rclone config` and select the option "Set configuration password". This will encrypt your configuration file so that it cannot be read by others. You will need to enter the password you set each time you run `rclone`.

### git

VS Code's Remote SSH extension is magic for working with git: it forwards your local machine's git credentials to the VM whenever necessary, without ever storing your credentials on the VM. This applies to terminals opened in VS Code as well as VS Code's graphical git tools. Therefore, the top recommendation is to use VS Code for performing all git operations. If you do not normally use VS Code for your project, you can still use it just for git operations. Follow the [instructions above](#vs-code) for connecting your local VS Code to your remote VM. Then just click the "open folder" button and navigate to the folder containing your cloned git repo. It will open the folder, and the left sidebar will contain options for browsing and opening the repo's files, as well as for performing git operations. You can also open a terminal inside VS Code and interact with git via the command line.

If you must use the VM's command line (outside VS Code) or RStudio's git functionality, you must set up a private encrypted folder to store your git credentials so they cannot be accessed by others on our project. Please see the [private encrypted folder](#private-encrypted-folder) section below.

### Browser logins

Sometimes the easiest way to access files is via the Firefox browser in the VM's remote desktop, but often you will need to enter passwords to log in to websites. Don't use the Firefox's built-in password store; use a password manager extension such as [Bitwarden](https://bitwarden.com/). The password manager will store your passwords securely in the cloud (encrypted with a master password) and allow you to log in to websites without typing your password. The password manager will not store your passwords on the VM, so they will not be accessible to others in our project.

### Other credentials

If you must store other credentials on the VM, you should use a private encrypted folder. See the [private encrypted folder](#private-encrypted-folder) section below. Let Derek know what other use cases you have for storing credentials on the VM, and he can help you set up a secure solution, such as better integration with the private encrypted folder described below.

### Private encrypted folder

There is a shell script automatically loaded onto the OFO dev image that will create a private encrypted folder for you. This folder will be mounted at ~/Private and will be encrypted with a passphrase that only you know. You can store your credentials in this folder, decrypt them when needed, and they will only be accessible to your current login session.

After set up, there are a few ways to decrypt your private folder:
- When you open the web desktop, after about a minute, you will get a prompt box with a button "Run this action now". Click the button and enter your passphrase.
- When connected to a terminal (SSH or web shell), you can run the command `dec` (which is an alias for the `ecryptfs-mount-privage` and enter your passphrase.

When your private folder is decrypted, you will see all the files in it. When it is decrypted, it will just show a readme.txt file explaining that it is a private folder and how to decrypt it. When you are done with the files in the folder, you can run the command `enc` (which is an alias for `ecryptfs-umount-private`) to re-encrypt the folder, or simply log out or close your SSH session or web shell and it will be automatically re-encrypted.

Part of the configuration around the private folder (which is handled automatically -- for git credentials only -- by the setup script referenced below) involves putting your credentials file in the ~/Private folder and symlinking to it from the place where the credentials file is expected. For git credentials, the file `~/.git-credentials` is moved to `~/Private/.git-credentials` and a symlink to this location is placed in the original location. This way, the git credential helper will read the credentials from the symlinked file, which is decrypted when you run `dec` and encrypted when you run `enc`. When the private folder is encrypted, the symlinked file will be empty and the git credential helper will not be able to read any credentials.

To set up this folder, run the following command in a terminal on the VM: `/opt/setup-private-folder.sh` and provide a password at the prompt.
