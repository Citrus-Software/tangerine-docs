---
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Installation

## Where to get Tangerine?

Contact us at jb@citrus-software.com or ask a demo on our [website](https://citrus-software.com)

## Software installation

>  This is the fastest way to get Tangerine up and running for everyday use.

### Prerequisites
- Intel Xeon recommended
- NVIDIA card that supports OpenGL 4.6 (GeForce GT 640 minimum)
- Recent NVIDIA drivers (431.60 or above)
- Windows (7 64 bits, 10, 11) or Linux (Rocky 9.x or Ubuntu 24.x)
- 32 Gb RAM or more (preferably 64 Gb)

### The License File

The license file is like your personal serial number to use Tangerine, and must remain confidential (see our End User License Agreement). It has been sent to you by email from our team.

The license file can be installed in the "MyDocuments" folder (the user folder on Linux), in the "Tangerine" subfolder.
If you install Tangerine on multiple computers, you may prefer to share the license file on a server, to do so define on each computer the environment variable `TANG_LIC_FILE`, for example : `TANG_LIC_FILE=\\my_server\some_folder\tangerine.lic`


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

### 🚀 Linux install

Tangerine for Linux uses AppImage, and fuse libs are required to make AppImage work:
<Tabs>
  <TabItem value="Rocky" label="Rocky 9" default>
```
sudo dnf install fuse-libs
```
  </TabItem>
  <TabItem value="Ubuntu" label="Ubuntu 24" default>
```
sudo apt install libfuse2
```
  </TabItem>  
</Tabs>

ffmpeg is required to create playblast videos in Tangerine and to use video references in the viewport:
<Tabs>
  <TabItem value="Rocky" label="Rocky 9" default>
```
sudo dnf install epel-release
sudo dnf install https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-9.noarch.rpm
sudo dnf install ffmpeg
```
  </TabItem>
  <TabItem value="Ubuntu" label="Ubuntu 24" default>
```
sudo apt install ffmpeg
```  
  </TabItem>  
</Tabs>

If Tangerine is the first OpenGL software you bring on your system, you need to install the OpenGL libraries:
<Tabs>
  <TabItem value="Rocky" label="Rocky 9" default>
```
sudo dnf install libglvnd-opengl mesa-libGLU
```
  </TabItem>
  <TabItem value="Ubuntu" label="Ubuntu 24" default>
```
sudo apt install libgl1 libglx0 libglu1-mesa
```  
  </TabItem>  
</Tabs>

