---
weight: 1
---

# Data processing tutorials

Here we provide step-by-step tutorials covering common tasks related to automated forest invntory. The tutorials use OFO datasets and rely primraily on OFO software tools. The tutorials demonstrate basic software usage and point to separate documentation for more advanced functionality.

<div class="grid cards" markdown>

- :material-quadcopter: __Processing raw drone photos__ using structure-from-motion photogrammetry (coming soon!)
- :material-forest: __[Detecting, mapping, and classifying trees]__ from processed drone data
- :material-table-check: __[Evaluating tree detection accuracy]__ against ground reference data

</div>

<!-- [Processing raw drone photos]: photogrammetry.md -->
[Detecting, mapping, and classifying trees]: itd/
[Evaluating tree detection accuracy]: itd-eval/


## Preparing to follow the tutorials

TODO: Text on things to keep in mind that apply to all tutorials, such as where to get the data, etc.

### Docker

TODO: Text describing what Docker is and why we use it, how to install it (links to Docker docs?), and how to run generic docker containers. Need to make sure covers windows, linux, mac.


#### Docker Installation

=== "Linux/Mac"

    TODO

=== "Windows"


    Install Windows Subsystem for Linux (WSL2):
    `wsl --install`

    Reboot your computer, then download the [Docker Desktop installer](https://www.docker.com/get-started/). If you don't know whether you have AMD64 or ARM64 architecture, you can check by opening a PowerShell window and running the command `systeminfo | findstr /B /C:"System Type"`. If it says "x64-based PC", you have AMD64 architecture. If it says "ARM-based PC", you have ARM64 architecture.
    
    Run the installer, using the recommended settings.



### Podman

TODO: Derek's notes below

Run as administrator in PowerShell:

`winget install RedHat.Podman`

Then in a normal PowerShell:

``` powershell
podman machine init
podman machine set --rootful
```




### TODO

TODO: Other things to keep in mind. Perhaps:

* Explain we give raw python code examples but Jupyter notebooks are also available (if true)
* Where to get the example data
* More?