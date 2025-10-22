---
---

# Installation

## Where to get Tangerine?

Contact us at jb@citrus-software.com or ask a demo on our [website](https://citrus-software.com)

## Software installation

>  This is the fastest way to get Tangerine up and running for everyday use.

### Prerequisites
- Intel Xeon recommended
- NVIDIA card that supports OpenGL 4.6 (GeForce GT 640 minimum)
- Recent NVIDIA drivers (431.60 or above)
- Windows (7 64 bits, 10, 11) or Rocky 9.x or Ubuntu 24.x
- 32 Gb RAM or more (preferably 64 Gb)

### 🚀 Windows install

Double-click on Tangerine-x.x.xx-win64.exe to install it and follow the different steps.
Your admin may prefer to install it silently with the command line:
`C:\Tangerine-x.x.xx-win64.exe /S /D=C:\Any Folder\Tangerine`

Please note the /D option should always be the last of the command line, and no quote nor double quote should be used even if there are spaces in the path.

ffmpeg.exe is required to create playblast videos in Tangerine and to use video references in the viewport. Anyone is free to download and use it but we can’t legally pack it into our installer. An internet connexion is required to download it automatically, use the /offline switch in the command line to disable it (before the /D=...), and proceed to a manual installation of:
https://github.com/GyanD/codexffmpeg/releases/download/6.1.1/ffmpeg-6.1.1-essentials_build.zip

Extract ffmpeg.exe and place it here:
`C:\Install Folder\Tangerine\third_parties\bin\ffmpeg.exe`
If you have no internet connection and if /offline is not defined, the installer will attempt to download but will just fail on this, and Tangerine will still be installed.

The license file can be installed in the “MyDocuments” folder, in the “Tangerine” subfolder.
If you install Tangerine on multiple computers, you may prefer to share the license file on a server, to do so define on each computer the environment variable TANG_LIC_FILE, for example : TANG_LIC_FILE=\\my_server\some_folder\tangerine.lic

### 🚀 Rocky 9.x install

Tangerine for Rocky uses AppImage, and fuse libs are required to make AppImage work:
```
	sudo dnf install fuse-libs
```
ffmpeg is required to create playblast videos in Tangerine and to use video references in the viewport:
```
	sudo dnf install epel-release
	sudo dnf install https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-9.noarch.rpm
	sudo dnf install ffmpeg
```

### 🚀 Ubuntu 24.x install

TODO

