# DPU Design Flow

## 1. Generate this four files from Xilinx Vivado
	- Reference: https://xilinx.github.io/kria-apps-docs/kv260/2021.1/build/html/docs/build_vivado_design.html
	- Other Flow: https://github.com/Xilinx/Vitis-AI-Tutorials/tree/2.0/Tutorials/Vitis-AI-Vivado-TRD
	1. .bit
	2. .dtsi
	3. xclbin
	4. .json

### 1.1. Other Git bash command translated from Unix to Windows
	* LOCATION: AI@DESKTOP-N3NL671 MINGW64 ~/Desktop/Kria-HW/kria-vitis-platforms/platforms/vivado/kv260_ispMipiRx_DP (release-2021.1)
		- /f/Vivado/Vivado/2021.2/bin/vivado.bat -mode batch -source scripts/main.tcl

### 1.2. Location of the Boards in Xilinx 
	- Use the 2021.1 version of the boards. Download the repo to the 2021.1 specific branch and replace the directory of your xilinxboardstore files.
		- https://github.com/Xilinx/XilinxBoardStore
	- F:\Vivado\Vivado\2021.2\data\xhub\boards\XilinxBoardStore\boards\Xilinx

### 1.2.1. To extract the HWA, follow this steps.
	- https://xilinx.github.io/kria-apps-docs/kv260/2021.1/build/html/docs/build_vivado_design.html?fbclid=IwAR1wRQREIKzEFVgk-2hexwwO_AdSWL624k9fzrkRHklcJKnyJXUP6O3WD94

## 1.3. THIS COMMAND IS FOR OTHER WORK FLOW IN EXTRACTING THE HWA OF KRIA
	- export TRD_HOME=C:/Users/AI/Desktop/Kria-HW/Vitis-AI
	- source F:/Vivado/Vivado/2021.2/settings64.sh
	- C:/Users/AI/Desktop/Kria-HW/Vitis-AI/dsa/DPU-TRD/prj/Vivado/scripts/trd_prj.tcl

## 2. After Generating this files flash it to the FPGA xlnx-config listapps. Find the design flow of this.
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

## 1. Solution for wont download the git clone 
	- https://stackoverflow.com/questions/35821245/github-server-certificate-verification-failed
		*sudo mkdir /usr/local/share/ca-certificates/cacert.org
		*sudo wget -P /usr/local/share/ca-certificates/cacert.org http://www.cacert.org/certs/root.crt http://www.cacert.org/certs/class3.crt
		*sudo update-ca-certificates

## 2. Problem installing the Anaconda TF dependencies H5py 
	- https://github.com/h5py/h5py/issues/2035
	- pip install h5py --only-binary h5py

## 3. Problem in EOF in Git clone. Solution is to increase the buffer size.
	- git config --global http.postBuffer 524288000
	- Or download the whole repository in USB from PC
	- Or download using tar.gz

## 4. (UBUNTU 22.04) If build.sh command not found, try this one. 	
	- sudo install g++
	- /usr/bin/g++ -std=c++17 -I. -I/usr/include/opencv4 -o test_video_facedetect test_video_facedetect.cpp -lopencv_core -lopencv_video -lopencv_videoio -lopencv_imgproc -lopencv_imgcodecs -lopencv_highgui -lvitis_ai_library-facedetect -lvitis_ai_library-dpu_task -pthread -lglog



