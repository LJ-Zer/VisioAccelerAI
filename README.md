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
5. (UBUNTU 22.04) Install Vitis-AI libraries

	```sh 
	https://xilinx-wiki.atlasssian.net/wiki/spaces/A/pages/2072838191/Building+Vitis-AI+Sample+Applications+on+Certified+Ubuntu+20.04+LTS+for+Xilinx+Devices
	```

	```sh
	sudo snap install xlnx-config --classic
	```

	```sh
	xlnx-config.sysinit
	```

	```sh
	sudo apt -y update
 	```

	```sh
	sudo apt -y install libopencv-dev
	```

	```sh
	sudo apt -y install libgoogle-glog-dev
	```
6. (UBUNTU 22.04) Load the sample nlp-smartvision DPU

	```sh 
	https://xilinx.github.io/kria-apps-docs/kv260/2022.1/build/html/docs/nlp-smartvision/docs/app_deployment_nlp.html
	```

	```sh
	sudo apt search xlnx-firmware-kv260
	```

	```sh
	sudo apt install xlnx-firmware-kv260-nlp-smartvision
	```

	```sh
	sudo xmutil listapps
 	```

	```sh
	sudo xmutil unloadapp
	```

	```sh
	sudo xmutil loadapp kv260-nlp-smartvision
	```

7. (UBUNTU 20.04) Install Opencv.hpp files and other dependencies for the C++ file compilations
	```sh
	sudo apt-get update
	```
	```sh
	sudo apt-get upgrade
	```
	```sh
	sudo apt install libopencv-dev
	```
	```sh
	sudo apt install libgoogle-glog-dev
	```

8. (UBUNTU 22.04) Install Opencv.hpp files and other dependencies for the C++ file compilations
	```sh
	sudo apt -y update
	```
	```sh
	sudo apt -y install libopencv-dev
	```
	```sh
	sudo apt -y install libgoogle-glog-dev
	```
	```sh
	sudo apt -y install vitis-ai-library
	```
	```sh
	sudo apt -y install libjson-c-dev
	```

9. Install Vitis-AI Library Samples
	```sh
	cd ~
	```
	```sh
	git clone https://github.com/Xilinx/Vitis-AI.git
	```
	```sh
	cd Vitis-AI
	```
	```sh
	git checkout tags/v1.3.2
	```

10. Also clone this repository. This repo is the existing architecture of VisioAccelerAI
	```sh
	cd ~/Desktop
	```
	```sh
	git clone https://github.com/Ze-r000/Visio_FPGA.git
	```

11. Place the Densebox_640_360 model. 
	```sh
	cd Visio_FPGA
	```
	```sh
	mkdir /usr/share/vitis_ai_library/models
	```
	```sh
	cp densebox_640_360 /usr/share/vitis_ai_library/models -r
	```

12. Clone the Face-Detected Folder for Git_Upload Repository
	```sh
	git clone https://github.com/Ze-r000/Face-Detected.git
	```

13. Download and Install Miniforge3 for facial recognition model inferencing. Just follow the steps in the GitHub instructions. Choose the Linux aarrch64 for Ubuntu 20.04
	```sh
	https://github.com/conda-forge/miniforge
	```

14. It is an bash file to install it, go to the directory where the .sh file located.
	```sh
	bash <filename.sh>
	```

15. To make conda default to your terminal execute this command
	```sh
	cd ~/
	```
	```sh
	export PATH="$HOME/miniforge3/bin:$PATH"
	```
16. Create Anaconda environment
	```sh
	conda create --name visio-env python=3.9
	```

17. Activate Visio Environment
	```sh
	conda activate visio-env
	```

18. Install Dependencies for VisioAccelerAI Facial Recognition
	```sh
	pip install h5py --only-binary h5py
	```
	```sh
	pip install tensorflow opencv-python
	```

### DPU Design Flow
_All libraries and dependencies should have the same version when cloning from GitHub. Since the commands in TCL and Makefiles are designed for Unix, the file paths follow the Linux format. So, update the paths accordingly if you're on Windows, or just use Linux instead._

1. Generate this four files from Xilinx Vivado
	```sh
	*Reference: https://xilinx.github.io/kria-apps-docs/kv260/2021.1/build/html/docs/build_vivado_design.html*
	```
	```sh
	*Other Flow: https://github.com/Xilinx/Vitis-AI-Tutorials/tree/2.0/Tutorials/Vitis-AI-Vivado-TRD*
	```

	```sh
	Generated file should be the following:
        * .bit
        * .dtsi
        * xclbin
        * .json
	```

2. Sample bash command translated from Unix to Windows
	```sh
	* LOCATION: AI@DESKTOP-N3NL671 MINGW64 ~/Desktop/Kria-HW/kria-vitis-platforms/platforms/vivado/kv260_ispMipiRx_DP (release-2021.1)
	```
	```sh
	* Translated: /f/Vivado/Vivado/2021.2/bin/vivado.bat -mode batch -source scripts/main.tcl
	```

3. Location of the Boards in Xilinx 
	```sh
	Use the 2021.1 version of the boards. Download the repo to the 2021.1 specific branch and replace the directory of your xilinxboardstore files.
	```
	```sh
	https://github.com/Xilinx/XilinxBoardStore
	```
	```sh
	F:\Vivado\Vivado\2021.2\data\xhub\boards\XilinxBoardStore\boards\Xilinx
	```

4. To extract the HWA, follow this steps.
	```sh
	*Reference: https://xilinx.github.io/kria-apps-docs/kv260/2021.1/build/html/docs/build_vivado_design.html?fbclid=IwAR1wRQREIKzEFVgk-2hexwwO_AdSWL624k9fzrkRHklcJKnyJXUP6O3WD94*
	```

5. This command is for other work flow in extracting the HWA
	```sh
	export TRD_HOME=C:/Users/AI/Desktop/Kria-HW/Vitis-AI
	```
	```sh
	source F:/Vivado/Vivado/2021.2/settings64.sh
	```
	```sh
	C:/Users/AI/Desktop/Kria-HW/Vitis-AI/dsa/DPU-TRD/prj/Vivado/scripts/trd_prj.tcl
	```

6. After Generating this files flash it to the FPGA xlnx-config listapps
	```sh
	*Reference: https://xilinx.github.io/kria-apps-docs/kv260/2022.1/build/html/docs/generating_custom_firmware.html*
	```
	```sh
	sudo apt install bootgen-xlnx
	```
	```sh
	sudo make -C boards/ install
	```
	```sh
	LOCATION OF DPU's | /usr/lib/firmware/xilinx/kv260-nlp-smartvision
	```
	```sh
	I used the git clone | --branch xlnx_rel_v2021.2 https://github.com/Xilinx/kria-apps-firmware.git
	```
7. used this repo to make DPU installed in Kria
	```sh
	git clone --branch xlnx_rel_v2022.2 https://github.com/Xilinx/kria-apps-firmware.git
	```

8. I used this repo to open the HWA of the Kria
	```sh
	git clone --branch xlnx_rel_v2022.2 https://github.com/Xilinx/kria-vitis-platforms.git
	```

9. I used this boards
	```sh
	- git clone --branch 2022.2 https://github.com/Xilinx/XilinxBoardStore.git
	```

10. Inside the Platforms/overlays/Vitis_Libraries
	```sh
	git clone --branch 2022.2 https://github.com/Xilinx/Vitis_Libraries.git
	```

11. Modify the IP Cores of Xilinx from extracted hardware architecture using Xilinx Vivado
	```sh
	*Atleast 32 GB of RAM to run synthesis*
	```

### Inferencing using modified DPU

1. Unload existing Accelerator and Load the Hardware Accelerator DPU
	```sh
	sudo xlnx-config --xmutil unloadapp
	```
	```sh
	sudo xlnx-config --xmutil loadapp Visio_DPU
	```

2. From the directory of your model.
	```sh
	source ~/miniforge3/bin/activate
	```
	```sh
	conda activate visio-env
	```
3. Inference Facial Recognition
	```sh
	python inference_image.py --modeldir"" --imagedir="../Face_Detect/face_detected"
	```

4. Inference Face Detection
	```sh	
	source build.sh
	```
	```sh
	/usr/bin/g++ -std=c++17 -I. -I/usr/include/opencv4 -o test_video_facedetect test_video_facedetect.cpp -lopencv_core 
	```
	```sh
	lopencv_video -lopencv_videoio -lopencv_imgproc -lopencv_imgcodecs -lopencv_highgui -lvitis_ai_library-facedetect 
	-lvitis_ai_library-dpu_task -pthread -lglog
	```
	```sh
	./Visio-FD densebox_640_360.xmodel 0
	```

5. Note for bash build.sh
	```sh
	*This file should be came from the original file location not from GitHub. If it is from GitHub, this would not run, so take note for the original build.sh file. *
	```

### Vitis-AI Installation

*References: https://xilinx.github.io/Vitis-AI/3.0/html/docs/quickstart/mpsochtmlfbclid=IwAR0ah9oX4Zd8f9ifqja1FZjk_2vhF4aItGtAxA6qU55ktKqE7Q9UgzY6bh8*
	
1. Installation of Ubuntu 20.04 LTS. Go to powershell run in administrator, then execute this code. 
	```sh
	- wsl --install -d Ubuntu-20.04
	```

2. Installation of Docker, download and install this link.
	```sh
	https://docs.docker.com/desktop/install/windows-install/
	```

3. Create accound and sign in the docker. 

4. Go to the settings, enable the integration of WSL.

5. Setup Vitis AI
	```sh
	source /home/lj/petalinux_sdk_2023.1/environment-setup-cortexa72-cortexa53-xilinx-linux
	```
	```sh
	source /home/lj/petalinux_sdk_2023.1/environment-setup-cortexa72-cortexa53-xilinx-linux
	```
	```sh
	./docker_run.sh xilinx/vitis-ai-pytorch-cpu:latest
	```

### Common Issues during development

1. Solution for won't download the Git 
*https://stackoverflow.com/questions/35821245/github-server-certificate-verification-failed* 
	```sh
	sudo mkdir /usr/local/share/ca-certificates/cacert.org
	```
	```sh
	sudo wget -P /usr/local/share/ca-certificates/cacert.org http://www.cacert.org/certs/root.crt http://www.cacert.org/certs/class3.crt
	```
	```sh
	sudo update-ca-certificates
	```

2. Problem installing the Anaconda TF dependencies H5py 
*https://github.com/h5py/h5py/issues/2035*
	```sh
	pip install h5py --only-binary h5py
	```

3. Problem in EOF in Git clone. Solution is to increase the buffer size
	```sh
	git config --global http.postBuffer 524288000
	```
	```sh	
	Or download the whole repository in USB from PC
	```
	```sh
	- Or download using tar.gz
	```
4. (UBUNTU 22.04) If build.sh command not found, try this one
	```sh
	sudo install g++
	```
	```sh 
	/usr/bin/g++ -std=c++17 -I. -I/usr/include/opencv4 -o test_video_facedetect test_video_facedetect.cpp -lopencv_core -lopencv_video -lopencv_videoio -lopencv_imgproc -lopencv_imgcodecs -lopencv_highgui -lvitis_ai_library-facedetect -lvitis_ai_library-dpu_task -pthread -lglog
	```

5. Issues for the script for face detection. If the bounding box is at the corner the script automatically terminated

6. For the Facial recognition 
    ```sh
	The model continously to inference images even it is already inference. So the solution is to create a command that the processed images will move to other folder so that the script wont process it again.
	```
7. Pushing local repo from Ubuntu
*https://www.youtube.com/watch?v=ePCBuIQJAUc*


### Using Digilent Arty Z7 20T (For further development hehe)

*This is instruction for accessing the Hardware design for Digilent Arty Z7 20T based on Zynq 7000 SoC.*

#### ***Installation for Vivado 2022.1***

```sh
*https://www.xilinx.com/member/forms/download/xef.html?filename=Xilinx_Unified_2022.1_0420_0327_Win64.exe*
```
```sh
*Note: Fill up the necessary information and scroll down for the download button. It requires 150 GB of storage.*
```

1. ***Zynq Files***
	```sh
	git clone https://github.com/Xilinx/PYNQ.git
	```

2. Steps
```sh
1. From the folder of the Pynq, go to Pynq/boards/Pynq-Z1/base. And copy the address of that folder.
```
```sh 
1. Open the Vivado 2022.1
```
```sh
2. In the main page of the Vivado, go to the "window" tab, and click the TCL Console.
```
```sh
3. In the console, type "cd {paste/the/address/of/the/folder}"
```
```sh
4. Enter, and wait for the loading time.
```
```sh
5. In the console again, type "source ./build_ip.tcl"
```
```sh
6. Enter, and wait for the loading time.
```
```sh
7. In the console again,  type "source ./base.tcl"
```
```sh
8. And wait for the loading time, it takes a lot of time to see the hardware design.
```