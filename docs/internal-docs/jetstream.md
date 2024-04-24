# Using Jetstream2 for OFO development

## Getting set up

### New users

These steps are required once per new user.

1. Create an [ACCESS](https://access-ci.org/) account and provide your username to your supervisor, so they can add you to our project.
1. Create (or locate an existing) SSH key. Here's [a detailed tutorial](https://happygitwithr.com/ssh-keys) with some good context (read sections 10.1 through 10.4). Note: this tutorial is designed for R and RStudio users, but you can ignore all the refenreces to R and RStudio and focus on the shell instructions.
1. [Once added to our ACCESS project:] Add credentials in [CACAO](https://cacao.jetstream-cloud.org/) (after logging in with your ACCESS credentials):
    1. The OFO ACCESS project (BIO220124):  go to Credentials (key icon), click Add Credential in the top right, and click Cloud Credential. Choose Jetstream2, log in at the ACCESS prompt, and select the project BIO220124.
    1. Your public SSH key: go to Credentials (key icon), click Add Credential in the top right, and click SSH Public Key. Enter a public key name (e.g. `derek-laptop01`) and paste in the key text.
1. Add your public SSH key in [Exosphere](https://jetstream2.exosphere.app/): Log in with your ACCESS credentials (once added to our project), go to our project/allocation (BIO220124), click Create in the top right, and click SSH Public Key. Enter a public key name (e.g. derek-laptop01) and paste in the key text.

### New VMs

These steps are required once for each new VM that a user desires. This should be done during initial onboarding (after the new user steps above), and it can also be done whenever an updated VM is desired. There are several events that may trigger users to want a new VM:

- Jetstream2 updates their featured Ubuntu image
- OFO updates its [development VM template](https://github.com/open-forest-observatory/cacao-terraform-ofo) (which is applied on top of the current Jetstream2 featured Ubuntu image)
- You need more compute nodes
- You screwed up your VM configuration and want to start fresh

The steps to create a new instance(s) are:

1. Go to [CACAO](https://cacao.jetstream-cloud.org) and select the Deployments tab on the left. Click Add Deployment, select the OFO dev template from the list, and click Next.
    1. For Instance Name, enter a name that's descriptive to you and starts with your name. For example, `derek-dev` or simply `derek`.
    1. For Boot Image Name, choose the most recent featured Ubuntu image.
    1. Enter the desired number of instances (usually 1).
    1. Enter a flavor (size). Start with m3.small or m3.quad, as you can always resize later when you need more compute.
    1. Enter the Manila share key and Metashape license server IP address found in the [OFO Credentials](https://docs.google.com/document/d/155AP0P3jkVa-yT53a-QLp7vBAfjRa78gdST1Dfb4fls/edit?usp=sharing) google doc shared with all OFO members.
    1. Click Advanced, enable Configure Boot Disk, change Boot Type to Volume, and enter 60 GB unless you know you will need something larger. Normally you won't because most data is stored on `/ofo-share` which is not part of this 60 GB.
1. [Only necessary if you want to access RStudio Server; can be done at a later time:] SSH into the machine and change your password
    1. `ssh <username>@<ip address>`
    1. Your username is the same as your [ACCESS-CI](https://access-ci.org/) username.
    1. If you lose track of the IP address, you can find it in [CACAO](https://cacao.jetstream-cloud.org/): go to Deployments and select the deployment you want to access.
    1. Set a password for your user: `sudo passwd <username>`. Choose a secure password because if others can guess it they could access our VMs and shared data volume.

You should be the only one who can access this instance/VM, so it should be safe to store credentials on. Examples of credentials you might store are: a Box account login (stored in `rclone`; see below), so you can transfer files between the VM and Box; GitHub credentials, so you can push to repos without entering a password every time.

## Basic instance access and management

### SSH access

SSH into your instance using `ssh <username>@<ip address>`. You can find the IP address of your instance in [CACAO](https://cacao.jetstream-cloud.org/) under Deployments. Your username is the same as your [ACCESS-CI](https://access-ci.org/) username.

### Remote desktop access

To access a graphical remote desktop in a browser tab, navigate to that instance's page in [CACAO](https://cacao.jetstream-cloud.org/) under Deployments and click the  "Web Desktop" button.

### Shelving and unshelving

It is **very important** that you shelve your instances when not using them, especially the larger instances. 

It's fastest to this via the instance's page in [Jetstream Exosphere](https://jetstream2.exosphere.app/exosphere/):

1. Go to our project/allocation (BIO220124)
1. Click on Instances
1. Clear the filter
1. Click on your instance
1. In the top right under "Actions", select "Shelve"

Note that this has the same effect as powering off a computer; i.e. all unsaved work will be lost, and next time you will start from a fresh boot. Use this same approach to unshelve your instance when you're ready to resume work, and to resize your instance if you need more compute or memory (see below). Note that when unshelving via Exosphere, you may need to wait ~1 minute before you can open the remote desktop via CACAO.

Shelving/unshelving can also be done via the [CACAO](https://cacao.jetstream-cloud.org/home) interface under Deployments, by pressing the square Stop button to shelve it (or triangle Play button to unshelve it). Using this method though, unshelving takes much longer because it does a check that the VM has all the configurations specified by our template, a generally unnecessary step.


### Resizing

Resizing is super useful to enable you do do simple tasks like coding and low-compute testing with a small instance (uses less of our allocation budget) and then sizing up when necessary for large compute jobs. Note that resizing involves a reboot, so any unsaved work will be lost. The `m2.small` instance size is sufficient for code development with lightweight processing.

Resizing is not currently available in CACAO, but you can resize using an alternative interface called [Exosphere](https://jetstream2.exosphere.app/). You will need to select our allocation (BIO220124), go to Instances, clear the filter, find your instance by name, and select it. Resize it via the Actions menu on the top right of the instance page.

### More details

More details on instance access and management can be found in the [Jetstream2 documentation](https://docs.jetstream-cloud.org/), including:

- [Instance Management Actions](https://docs.jetstream-cloud.org/ui/exo/manage/#instance-management-actions)

Note that some instance interactions available via the Exosphere interface are not available for instances created via CACAO.
 

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

For data files on cloud storage such as Box, an incredibly value command line tool is `rclone`. To set up an account, use `rclone config` and follow the instructions. Assuming you set up a Box account with the name `box_myname`, you'd transfer data with a command like: `rclone sync box_myname:projects/myproject_data/ /ofo-share/myproject_data --progress --transfers 16`.

### Jupyter Notebook / Jupyter Lab

You can get Jupyter Lab in a browser tab (accessible from anywhere on the internet) using Jupyter server on your instance. It's best if you start the server from the root of the `/ofo-share` folder so you have easy access to all files there. Run:

```
cd /ofo-share/
/ofo-share/utils/environments/jetstream/jupyter-lab.sh
```

then copy the last URL shown in the terminal and paste it into a browser. Inside a notebook you should be able to choose different kernels (conda environments) that are configured for the user account running the server. The `base` conda environment is called `root` here. When you're done, shut down the notebook server (either from the notebook, or from the terminal by doing Control-C twice) to prevent access to the server by others. If you want a basic Jupyter notebook instead of Jupyter Lab, you can use `/ofo-share/utils/environments/jetstream/jupyter-notebook.sh`.

### RStudio

Use RStudio Server; don't use RStudio GUI via a remote desktop. RStudio Server has all the same functionality and many conveniences. RStudio Server is a version of RStudio that runs in a browser tab on your local machine, but all the data and compute comes from your remote VM. Access RStudio from the browser on your local computer at `https://<ip address>`. Log in using your ACCESS-CI username and the password you set up for it (in the "Getting set up" section above). The first time you access RStudio Server via HTTPS, you will likely get a warning about an unsigned SSL certificate, but that is OK; it's the certificate installed by CACAO upon VM creation and it enables a secure connection even though it's not signed. To interface with `git` for code development in RStudio, you can use the command line or use RStudio's built-in git functionality under the Git tab in the top-right pane (shows up when you've opened a project that is a git repo).

**Accessing `/ofo-share/` from the RStudio Server file browser:** The RStudio Server file browser defaults to the `~/` directory. To access a higher-level directory on the instance (and specifically the `/ofo-share/` folder), you need to click the `...` in the top  right of the file browser and enter `/` at the prompt. Then you will see all top-level directories on the instance and you can navigate to `/ofo-share/`.

### VS Code for R

#### Connecting to remote server from VS Code: first time

- Install the the VS Code extension "Remote - SSH"
- Connect to the remote VM by clicking the '><' button in the bottom left
- Click 'Connect to host'.
- Click 'Add new SSH host'. Type `ssh <your_access_username>@<vm_ip_address>`.
- When prompted, choose to update the SSH config in `/home/<username>/.ssh/config`
- Click the '><' button again, then 'Connect to host...', then select the host you just added. You may need to repond 'Yes' to accept the fingerprint of the host.

#### Connecting to remote server from VS Code: after first time

- Click the '><' button, then 'Connect to host...', then select the host IP (or name) you want to connect to.
- Open a code folder on the remote host by clicking 'Open folder...'. You'll probably want to navigate up the directories (`..`) and into `/ofo-share/repos-<yourname>/`.

#### Setting up VS Code for R

Note that if you want to set up your local machine for R editing too, the steps below are not complete because some of them have already been completed on the OFO VM image. For full steps, [see here](https://code.visualstudio.com/docs/languages/r).

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
