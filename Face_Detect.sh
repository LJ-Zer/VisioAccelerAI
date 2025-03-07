sudo xmutil unloadapp
sudo xmutil loadapp kv260-Visio-DPU
cd Face_Detect
/usr/bin/g++ -std=c++17 -I. -I/usr/include/opencv4 -o Visio-FD Visio-FD.cpp -lopencv_core -lopencv_video -lopencv_videoio -lopencv_imgproc -lopencv_imgcodecs -lopencv_highgui -lvitis_ai_library-facedetect -lvitis_ai_library-dpu_task -pthread -lglog
sudo ./Visio-FD Visio_640_360.xmodel 0
