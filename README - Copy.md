## About The Project

VisioAccelerAI is a capstone project aimed at deploying a facial recognition system on an FPGA board to enhance the model's computational capability for real-time attendance monitoring. This repository contains scripts, documentation, and instructions from various sources.

## Getting Started

Please refer to the instructions below. 

Note for the following folders.
* Face_Detect
  ```sh
  This folder contains the face detection model, just follow the steps below to run the scripts inside.
  ``
* Facial_Recog
  ```sh
  his folder contains the facial recognition detection model, just follow the steps below to run the scripts inside.
  ``
* Layers Counter
  ```sh
  This folder used to have analyzation for each model layers, this contains Jupyter notebook to run the breakdown of model layers.
  ``
* Results
  ```sh
  Contains the results from Xilinx Vivado and the results from models.
  ``
* Visio_DPU
  ```sh
  Contains the important files to run the hardware accelerator to Xilinx. Just follow the steps below.
  ``
* Face_Detect.sh -- Facial Recog.sh -- executes.sh
  ```sh
  This scripts is only used to automate tasks upon the board's startup. Don't worry about it.
  ``
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
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```
5. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
   ``