#include "opencv2/opencv.hpp"
#include <iostream>
#include <glog/logging.h>
#include <memory>
#include <chrono>
#include <vitis/ai/demo.hpp>
#include <vitis/ai/facedetect.hpp>
#include <ctime>  // For filename generation
#include <filesystem>  // For folder creation

using namespace cv;
using namespace std::filesystem;

int main(int argc, char** argv) {
    VideoCapture cap(0);  // Open default camera (0)
    if (!cap.isOpened()) {
        std::cerr << "Error opening camera!" << std::endl;
        return -1;
    }

    auto network = vitis::ai::FaceDetect::create("densebox_640_360", true);
    if (!network) {
        std::cerr << "Failed to create face detection network." << std::endl;
        return -1;
    }

    int frame_width = cap.get(CAP_PROP_FRAME_WIDTH);
    int frame_height = cap.get(CAP_PROP_FRAME_HEIGHT);

    // Create the "face_detected" folder if it doesn't exist
    create_directory("face_detected");  // Using std::filesystem
    
    // Variables for FPS calculation

    
        while (true) {

            double fps = 0.0;
            auto start = std::chrono::steady_clock::now();

            Mat frame;
            bool frame_read_success = cap.read(frame);  // Flag for read success
            if (!frame_read_success) {
            std::cerr << "Error reading frame from camera!" << std::endl;
            }
            // Resize for network input if necessary
            Mat resized_frame;
            if (frame.cols != 5120 || frame.rows != 2880) {
            resize(frame, resized_frame, Size(5120, 2880));
            } else {
            resized_frame = frame; // Avoid unnecessary copy if sizes match
            }

            // Face detection
            auto face_results = network->run(resized_frame);

            // Update FPS after processing each frame
            auto end = std::chrono::steady_clock::now();
            std::chrono::duration<double, std::milli> elapsed_ms = end - start;
            fps = 1.0 / (elapsed_ms.count() / 1000.0);
            start = end;

            for (const auto& r : face_results.rects) {
                // Scale bounding box coordinates to original frame size
                int x1 = r.x * frame_width;
                int y1 = r.y * frame_height;
                int x2 = x1 + (r.width * frame_width);
                int y2 = y1 + (r.height * frame_height);

                Mat face_roi;
                try {
                    face_roi = frame(Rect(x1, y1, x2 - x1, y2 - y1));
                } catch (const cv::Exception& ex) {
                // Handle OpenCV exception if coordinates are out-of-bounds (optional)
                    // std::cerr << "Warning: ROI coordinates outside frame (" << ex.what() << ")" << std::endl;
                    continue;
                }
                
                // Save cropped face image with timestamp-based filename
                time_t now = time(0);
                tm *ltm = localtime(&now);
                char filename[80];
                strftime(filename, 80, "face_%Y-%m-%d_%H-%M-%S.jpg", ltm);

                // Create the full path including "face_detected" folder
                std::string full_path = "face_detected/" + std::string(filename);

                imwrite(full_path, face_roi);
                //LOG(INFO) << "Face cropped and saved to: " << full_path;
            }
            
            // Draw FPS text on the frame
            std::stringstream fps_text;
            fps_text << "FPS: " << std::fixed << std::setprecision(1) << fps;
            putText(frame, Point(10, 50), FONT_HERSHEY_SIMPLEX, 2.0, Scalar(0, 255, 0), 2);

            resize(frame, frame, Size(640, 360));
            imshow("VisioAccelerAI", frame);
            if (waitKey(10) == 27) { // Exit on ESC key press
            break;
            }
        }

        cap.release();
        return 0;
    }
