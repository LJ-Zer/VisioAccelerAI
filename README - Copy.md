## About The Project

VisioAccelerAI is a capstone project aimed at deploying a facial recognition system on an FPGA board to enhance the model's computational capability for real-time attendance monitoring. This repository contains scripts, documentation, and instructions from various sources.

## Getting Started

Please refer to the instructions below. 

Note for the following folders.
* Face_Detect
  ```sh
  This folder contains the face detection model, just follow the steps below to run the scripts inside.
  ```
* Facial_Recog
  ```sh
  This folder contains the facial recognition detection model, just follow the steps below to run the scripts inside.
  ```
* Layers Counter
  ```sh
  This folder used to have analyzation for each model layers, this contains Jupyter notebook to run the breakdown of model layers.
  ```
* Results
  ```sh
  Contains the results from Xilinx Vivado and the results from models.
  ```
* Visio_DPU
  ```sh
  Contains the important files to run the hardware accelerator to Xilinx. Just follow the steps below.
  ```
* Face_Detect.sh -- Facial Recog.sh -- executes.sh
  ```sh
  This scripts is only used to automate tasks upon the board's startup. Don't worry about it.
  ```
### Xilinx Kria Configuration

_Below is the installation process how to install operating system to XIlinx Kria SoC._

1. Install BalenaEtcher or Win32Diskmanager to flash the Ubuntu 20.04 in Xilinx Kria. 
   ```sh
   https://www.amd.com/en/products/system-on-modules/kria/k26/kv260-vision-starter-kit/getting-started-ubuntu/setting-up-the-sd-card-image.html
   ```
   ```sh
   (other support) https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/2037317633/Getting+Started+with+Certified+Ubuntu+20.04+LTS+for+Xilinx+Devices
   ```
   ```sh
   (other support) https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/1641152513/Kria+SOMs+Starter+Kits#Vitis-Platforms
   ```	
2. After Flashing the OS 
   ```sh
   Follow the steps from the documentation. Set up the Ubuntu user account.
   ```	
3. (UBUNTU 22.04 and 20.04) Update the system using this command in terminal
   ```sh
   sudo apt-get update
   ```	
   ```sh
   sudo apt-get upgrade
   ```	
3. Documentation to run the accelerator and face detection on Kria
   ```sh
   https://www.xilinx.com/developer/articles/building-running-vitis-ai-on-kria-with-ubuntu.html
   ```	
4. Install the xlnx-config libraries
   ```sh
   sudo snap install xlnx-config --classic
   ```	
   ```sh
   sudo snap install xlnx-config --classic --channel=1.x
   ```	
   ```sh
   xlnx-config.sysinit
   ```	
   ```sh
   sudo xlnx-config --snap --install xlnx-nlp-smartvision
   ```	