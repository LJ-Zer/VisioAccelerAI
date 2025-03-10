#
# Copyright 2019 Xilinx Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#CXX=${CXX:-g++}
/usr/bin/g++ -std=c++17 -I. -I/usr/include/opencv4 -o Visio-FD Visio-FD.cpp -lopencv_core -lopencv_video -lopencv_videoio -lopencv_imgproc -lopencv_imgcodecs -lopencv_highgui -lvitis_ai_library-facedetect  -pthread -lglog 

#$CXX -std=c++17 -I. -I/usr/include/opencv4 -o test_accuracy_facedetect test_accuracy_facedetect.cpp -lopencv_core -lopencv_video -lopencv_videoio -lopencv_imgproc -lopencv_imgcodecs -lopencv_highgui -lvitis_ai_library-facedetect  -lvitis_ai_library-model_config -lvitis_ai_library-math -lvitis_ai_library-dpu_task -lglog 
#$CXX -std=c++17 -I. -I/usr/include/opencv4 -o test_jpeg_facedetect test_jpeg_facedetect.cpp -lopencv_core -lopencv_video -lopencv_videoio -lopencv_imgproc -lopencv_imgcodecs -lopencv_highgui -lvitis_ai_library-facedetect  -pthread -lglog 
#$CXX -std=c++17 -I. -I/usr/include/opencv4 -o test_performance_facedetect test_performance_facedetect.cpp -lopencv_core -lopencv_video -lopencv_videoio -lopencv_imgproc -lopencv_imgcodecs -lopencv_highgui -lvitis_ai_library-facedetect  -lvart-util -lvitis_ai_library-dpu_task -pthread -lglog 
#$CXX -std=c++17 -I. -I/usr/include/opencv4 -o test_video_facedetect test_video_facedetect.cpp -lopencv_core -lopencv_video -lopencv_videoio -lopencv_imgproc -lopencv_imgcodecs -lopencv_highgui -lvitis_ai_library-facedetect  -pthread -lglog 
