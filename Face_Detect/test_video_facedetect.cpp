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
        cerr << "Error opening camera!" << endl;
        return -1;
    }

    auto network = vitis::ai::FaceDetect::create("densebox_640_360", true);
    if (!network) {
        cerr << "Failed to create face detection network." << endl;
        return -1;
    }

    int frame_width = cap.get(CAP_PROP_FRAME_WIDTH);
    int frame_height = cap.get(CAP_PROP_FRAME_HEIGHT);

    // Create the "face_detected" folder if it doesn't exist
    create_directory("face_detected");  // Using std::filesystem

    while (true) {
        Mat frame;
        cap >> frame;
        if (frame.empty()) {
            cerr << "Error reading frame from camera!" << endl;
            break;
        }

        // Resize for network input if necessary
        Mat resized_frame;
        if (frame.cols != 640 || frame.rows != 360) {
            resize(frame, resized_frame, Size(640, 360));
        } else {
            resized_frame = frame; // Avoid unnecessary copy if sizes match
        }

        // Face detection
        auto face_results = network->run(resized_frame);

        if (!face_results.rects.empty()) {
            for (const auto& r : face_results.rects) {
                // Scale bounding box coordinates to original frame size
                int x1 = r.x * frame_width;
                int y1 = r.y * frame_height;
                int x2 = x1 + (r.width * frame_width);
                int y2 = y1 + (r.height * frame_height);

                // Extract ROI (Region of Interest)
                Mat face_roi = frame(Rect(x1, y1, x2 - x1, y2 - y1));

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
        }

        // Display frame with bounding boxes (optional)
        // You can uncomment this if you want to see the bounding boxes
        // for (const auto& r : face_results.rects) {
        //     cv::rectangle(frame, Point(x1, y1), Point(x2, y2), cv::Scalar(0, 5, 0));
        // }
        resize(frame, frame, Size(320,320));
        imshow("VisioAccelerAI", frame);
        if (waitKey(10) == 27) {  // Exit on ESC key press
            break;
        }
    }

    cap.release();
    return 0;
}
