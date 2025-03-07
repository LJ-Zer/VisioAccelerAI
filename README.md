# DPU Design Flow

### 1. Generate this four files from Xilinx Vivado
	- Reference: https://xilinx.github.io/kria-apps-docs/kv260/2021.1/build/html/docs/build_vivado_design.html
	- Other Flow: https://github.com/Xilinx/Vitis-AI-Tutorials/tree/2.0/Tutorials/Vitis-AI-Vivado-TRD
	- Generated file should be the following:
        * .bit
        * .dtsi
        * xclbin
        * .json

### 1.1. Other Git bash command translated from Unix to Windows
	* LOCATION: AI@DESKTOP-N3NL671 MINGW64 ~/Desktop/Kria-HW/kria-vitis-platforms/platforms/vivado/kv260_ispMipiRx_DP (release-2021.1)
		- /f/Vivado/Vivado/2021.2/bin/vivado.bat -mode batch -source scripts/main.tcl

### 1.2. Location of the Boards in Xilinx 
	- Use the 2021.1 version of the boards. Download the repo to the 2021.1 specific branch and replace the directory of your xilinxboardstore files.
		- https://github.com/Xilinx/XilinxBoardStore
	- F:\Vivado\Vivado\2021.2\data\xhub\boards\XilinxBoardStore\boards\Xilinx

### 1.2.1. To extract the HWA, follow this steps.
	- https://xilinx.github.io/kria-apps-docs/kv260/2021.1/build/html/docs/build_vivado_design.html?fbclid=IwAR1wRQREIKzEFVgk-2hexwwO_AdSWL624k9fzrkRHklcJKnyJXUP6O3WD94

### 1.3. THIS COMMAND IS FOR OTHER WORK FLOW IN EXTRACTING THE HWA OF KRIA
	- export TRD_HOME=C:/Users/AI/Desktop/Kria-HW/Vitis-AI
	- source F:/Vivado/Vivado/2021.2/settings64.sh
	- C:/Users/AI/Desktop/Kria-HW/Vitis-AI/dsa/DPU-TRD/prj/Vivado/scripts/trd_prj.tcl

### 2. After Generating this files flash it to the FPGA xlnx-config listapps. Find the design flow of this.
	- Reference: https://xilinx.github.io/kria-apps-docs/kv260/2022.1/build/html/docs/generating_custom_firmware.html
	- sudo apt install bootgen-xlnx
	- sudo make -C boards/ install
	- LOCATION OF DPU's /usr/lib/firmware/xilinx/kv260-nlp-smartvision
	- I used the git clone --branch xlnx_rel_v2021.2 https://github.com/Xilinx/kria-apps-firmware.git
	
### 2.1. I used this repo to make DPU installed in Kria
	- git clone --branch xlnx_rel_v2022.2 https://github.com/Xilinx/kria-apps-firmware.git

### 2.1.2 I used this repo to open the HWA of the Kria
	- git clone --branch xlnx_rel_v2022.2 https://github.com/Xilinx/kria-vitis-platforms.git

### 2.1.3 I used this boards
	- git clone --branch 2022.2 https://github.com/Xilinx/XilinxBoardStore.git

### 2.1.4. Inside the Platforms/overlays/Vitis_Libraries
	- git clone --branch 2022.2 https://github.com/Xilinx/Vitis_Libraries.git

NOTE: 
	All libraries and dependencies should have the same version when cloning from GitHub. Since the commands in TCL and Makefiles are designed for Unix, the file paths follow the Linux format. So, update the paths accordingly if you're on Windows, or just use Linux instead.

# Common Issues during development

### 1. Solution for wont download the git clone 
	- https://stackoverflow.com/questions/35821245/github-server-certificate-verification-failed
		*sudo mkdir /usr/local/share/ca-certificates/cacert.org
		*sudo wget -P /usr/local/share/ca-certificates/cacert.org http://www.cacert.org/certs/root.crt http://www.cacert.org/certs/class3.crt
		*sudo update-ca-certificates

### 2. Problem installing the Anaconda TF dependencies H5py 
	- https://github.com/h5py/h5py/issues/2035
	- pip install h5py --only-binary h5py

### 3. Problem in EOF in Git clone. Solution is to increase the buffer size.
	- git config --global http.postBuffer 524288000
	- Or download the whole repository in USB from PC
	- Or download using tar.gz

### 4. (UBUNTU 22.04) If build.sh command not found, try this one. 	
	- sudo install g++
	- /usr/bin/g++ -std=c++17 -I. -I/usr/include/opencv4 -o test_video_facedetect test_video_facedetect.cpp -lopencv_core -lopencv_video -lopencv_videoio -lopencv_imgproc -lopencv_imgcodecs -lopencv_highgui -lvitis_ai_library-facedetect -lvitis_ai_library-dpu_task -pthread -lglog

### 5. Issues for the script for face detection. If the bounding box is at the corner the script automatically terminated.

### 6. For the facial recognition. 
    - The model continously to inference images even it is already inference. So the solution is to create a command that the processed images will move to other folder so that the script wont process it again.

### 7. Git push from Ubuntu
	- https://www.youtube.com/watch?v=ePCBuIQJAUc

# Inferencing using your DPU

### 0. Unload existing Accelerator and Load the Hardware Accelerator DPU
	- sudo xlnx-config --xmutil unloadapp
	- sudo xlnx-config --xmutil loadapp Visio_DPU
	
### 1. From the directory of your model.
	- source ~/miniforge3/bin/activate
	- conda activate visio-env

### 2. Inference Facial Recognition
	- python inference_image.py --modeldir"" --imagedir="../Face_Detect/face_detected"

### 3. Inference Face Detection
	- source build.sh
	- /usr/bin/g++ -std=c++17 -I. -I/usr/include/opencv4 -o test_video_facedetect test_video_facedetect.cpp -lopencv_core -lopencv_video -lopencv_videoio -lopencv_imgproc -lopencv_imgcodecs -lopencv_highgui -lvitis_ai_library-facedetect -lvitis_ai_library-dpu_task -pthread -lglog
	- ./Visio-FD densebox_640_360.xmodel 0

### 4. Note for bash build.sh
	- This file should be came from the original file location not from GitHub.
	- If it is from GitHub, this would not run, so take note for the original build.sh file.

# Vitis-AI Installation
- References: https://xilinx.github.io/Vitis-AI/3.0/html/docs/quickstart/mpsoc.htmlfbclid=IwAR0ah9oX4Zd8f9ifqja1FZjk_2vhF4aItGtAxA6qU55ktKqE7Q9UgzY6bh8

***Installation of Ubuntu 20.04 LTS***

### 1. Go to powershell run in administrator, then execute this code. 
	- wsl --install -d Ubuntu-20.04

### 2. Installation of Docker, download and install this link.
	- https://docs.docker.com/desktop/install/windows-install/

### 3. Create accound and sign in the docker. 

### 4. Go to the settings, enable the integration of WSL.

### 5. Setup Vitis AI
	- source /home/lj/petalinux_sdk_2023.1/environment-setup-cortexa72-cortexa53-xilinx-linux
	- source /home/lj/petalinux_sdk_2023.1/environment-setup-cortexa72-cortexa53-xilinx-linux
	- ./docker_run.sh xilinx/vitis-ai-pytorch-cpu:latest

# Xilinx Kria Configuration

### 1. Install BalenaEtcher or Win32Diskmanager to flash the Ubuntu 20.04 in Xilinx Kria. Follow the steps in the link.
	- https://www.amd.com/en/products/system-on-modules/kria/k26/kv260-vision-starter-kit/getting-started-ubuntu/setting-up-the-sd-card-image.html
	- (other support) https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/2037317633/Getting+Started+with+Certified+Ubuntu+20.04+LTS+for+Xilinx+Devices
	- (other support) https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/1641152513/Kria+SOMs+Starter+Kits#Vitis-Platforms

### 2. After flashing 
	- Follow the steps from the documentation. Set up the Ubuntu user account.

### 2.1. (UBUNTU 22.04 and 20.04) Update the system using this command in terminal
	- sudo apt-get update
	- sudo apt-get upgrade

### 3. Follow the steps here: This documentation will run the accelerator and face detection in Kria
	- https://www.xilinx.com/developer/articles/building-running-vitis-ai-on-kria-with-ubuntu.html

### 3.1. Install the xlnx-config libraries
	- sudo snap install xlnx-config --classic
	- sudo snap install xlnx-config --classic --channel=1.x
	- xlnx-config.sysinit
	- sudo xlnx-config --snap --install xlnx-nlp-smartvision

### 3.1.2. (UBUNTU 22.04) Install Vitis-AI libraries 
	- Reference: https://xilinx-wiki.atlasssian.net/wiki/spaces/A/pages/2072838191/Building+Vitis-AI+Sample+Applications+on+Certified+Ubuntu+20.04+LTS+for+Xilinx+Devices
	- sudo snap install xlnx-config --classic
	- xlnx-config.sysinit
	- sudo apt -y update
 	- sudo apt -y install libopencv-dev
	- sudo apt -y install libgoogle-glog-dev
	
### 3.1. (UBUNTU 22.04) 
	- Reference: https://xilinx.github.io/kria-apps-docs/kv260/2022.1/build/html/docs/nlp-smartvision/docs/app_deployment_nlp.html
	- sudo apt search xlnx-firmware-kv260
	- sudo apt install xlnx-firmware-kv260-nlp-smartvision
	- sudo xmutil listapps
	- sudo xmutil unloadapp
	- sudo xmutil loadapp kv260-nlp-smartvision

### 3.1.1. (UBUNTU 20.04) Install Opencv.hpp files and other dependencies for the C++ file compilations.
	- sudo apt-get update
	- sudo apt-get upgrade
	- sudo apt install libopencv-dev
	- sudo apt install libgoogle-glog-dev

### 3.1.2. (UBUNTU 22.04) Install Opencv.hpp files and other dependencies for the C++ file compilations.
	- sudo apt -y update
	- sudo apt -y install libopencv-dev
	- sudo apt -y install libgoogle-glog-dev
	- sudo apt -y install vitis-ai-library
	- sudo apt -y install libjson-c-dev

### 3.2. Install Vitis-AI Library Samples
	- cd ~
	- git clone https://github.com/Xilinx/Vitis-AI.git
	- cd Vitis-AI
	- git checkout tags/v1.3.2

### 4. Also clone this repository. This repo is the existing architecture of VisioAccelerAI
	- cd ~/Desktop
	- git clone https://github.com/Ze-r000/Visio_FPGA.git

### 4.1. Place the Densebox_640_360 model. 
	- cd Visio_FPGA
	- mkdir /usr/share/vitis_ai_library/models
	- cp densebox_640_360 /usr/share/vitis_ai_library/models -r

### 4.2. Clone the Face-Detected Folder for Git_Upload Repository
	- git clone https://github.com/Ze-r000/Face-Detected.git

### 5. Download and Install Miniforge3 for facial recognition model inferencing. Just follow the steps in the GitHub instructions. Choose the Linux aarrch64 for Ubuntu 20.04
	- https://github.com/conda-forge/miniforge

### 5.1. It is an .sh file to install it, go to the directory where the .sh file located.
	- bash <filename.sh>

### 5.2. To make conda default to your terminal execute this command
	- cd ~/
	- export PATH="$HOME/miniforge3/bin:$PATH"

### 6. Create Anaconda environment
	- conda create --name visio-env python=3.9

### 7. Activate Visio Environment
	- conda activate visio-env

### 8. Install Dependencies for VisioAccelerAI Facial Recognition
	- pip install h5py --only-binary h5py
	- pip install tensorflow opencv-python
