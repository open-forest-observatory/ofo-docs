---
weight: 1
---

# Resources for Open Forest Observatory workshop at FOSS4G NA

9 AM - 12 PM, Monday, November 2, 2026 @ Bondi Room, Downtown Sheraton Grand, Sacramento, CA

## Workshop overview

The workshop will walk you through two [Open Forest Observatory tutorials](/tutorials/):

- [Detecting, mapping, and classifying trees](/tutorials/itd/1_detection.md)
- [Evaluating tree detection accuracy](/tutorials/itd/2_evaluation.md)

We will provide demonstrations and additional context around each task. We encourage you to bring your own laptop and follow along in running the tools yourself.

## Computing options

There are two options:

1. **Remote cloud computing environment**: We will provide a remote cloud computing environment for the workshop, preloaded with all the necessary data and software. You will be able to access this environment from your own laptop via `ssh` (instructions provided).
2. **Local compute on your laptop**: We provide instructions for running the tools locally, but you will need to install the necessary software and download the data to your laptop in advance. See [Advance preparation](#advance-preparation), below, for details.

## Advance preparation

Required preparation depends on how you plan to run the software (remotely or locally).

### Everyone

Install a graphical GIS software like [QGIS](https://qgis.org/en/site/forusers/download.html) to inspect data inputs and outputs.

### Remote computing environment

If you plan to use the remote computing environment, you must have at least *one* of the following installed on your laptop:

- (Recommended) [VS Code](https://code.visualstudio.com/) with the [Remote - SSH extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)
- SSH client (confirm access with `ssh -V` in a terminal)

### Local computing environment

If you plan to run the OFO tools on your laptop, you must download the workshop example data (~6 GB) and prepare to run either Docker containers or Conda environments. Due to expected slow connection speeds at the venue, you will need to download the Docker images or Conda libraries in advance (~20 GB). Follow the OFO [tutorial preparation instructions](/tutorials/preparation/) for all setup in advance of the workshop.

## Using the remote computing environment

You will be assigned a username like `user01`. We will provide you with the password during the workshop. The remote machine (VM) is at IP address `149.165.169.185`.

### Connecting

#### Terminal

To connect to the VM, in a terminal run:

```bash
ssh YOUR_USERNAME@149.165.169.185
```

Then enter the password.

#### VS Code

Alternatively, in VS Code, click the "><" icon in the lower left corner, select "Connect to Host...", click "+ Add New SSH Host", and enter:

```bash
ssh YOUR_USERNAME@149.165.169.185
```

Press Enter again to save to the default SSH config file. Then (and for all future connections) just click the "><" icon, select "Connect to Host...", and select the host you just added. Enter the password when prompted.

### Data

The tutorial demo data lives at `~/ofo-tutorial-data` on the VM. The subfolders are all read-only because they are shared across all users. The exception is `~/ofo-tutorial-data/output`, which is unique to you and begins empty. We recommend saving your outputs to this folder. All examples here and in the tutorials assume you will be saving to this folder.

### Transferring files from the remote VM to your laptop

#### Terminal

To transfer files from the VM to your laptop, _open a new terminal window_ and use the `scp` command. For example, to copy everything in the `~/ofo-tutorial-data/output` VM folder to `~/ofo-tutorial-data/output` on your local machine, run:

```bash
scp -r YOUR_USERNAME@149.165.169.185:~/ofo-tutorial-data/output ~/ofo-tutorial-data/output
```

To transfer a single file, run:

```bash
scp YOUR_USERNAME@149.165.169.185:~/ofo-tutorial-data/output/EXAMPLE_FILE.txt ~/ofo-tutorial-data/output/
```

#### VS Code

After connecting to the VM, click the "Open Folder" button in the left sidebar and select the folder `ofo-tutorial-data` and click "OK". You can then use the VS Code file explorer in the left pane, and right-click on any file or folder to download it to your local machine.
