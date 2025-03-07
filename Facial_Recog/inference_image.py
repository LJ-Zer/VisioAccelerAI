import os
import argparse
import cv2
import numpy as np
import sys
import glob
import importlib.util
import datetime
import shutil  # Import the shutil module for file operations
import time
# Define and parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--modeldir', help='Folder the .tflite file is located in',
                    required=True, default='')
parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                    default='detect.tflite')
parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt',
                    default='labelmap.txt')
parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
                    default=0.5)
parser.add_argument('--imagedir', help='Name of the folder containing images to perform detection on. Folder must contain only images.',
                    required=True, default='../Face_Detect/face_detected')
parser.add_argument('--save_results', help='Save labeled images and annotation data to a results folder',
                    action='store_true')
parser.add_argument('--noshow_results', help='Don\'t show result images (only use this if --save_results is enabled)',
                    action='store_false')
parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                    action='store_true')

args = parser.parse_args()

# Parse user inputs
MODEL_NAME = args.modeldir
GRAPH_NAME = args.graph
LABELMAP_NAME = args.labels

min_conf_threshold = float(args.threshold)
use_TPU = args.edgetpu

save_results = args.save_results  # Defaults to False
show_results = args.noshow_results  # Defaults to True

IM_DIR = args.imagedir

# Import TensorFlow libraries
# If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
# If using Coral Edge TPU, import the load_delegate library
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
    if use_TPU:
        from tflite_runtime.interpreter import load_delegate
else:
    from tensorflow.lite.python.interpreter import Interpreter
    if use_TPU:
        from tensorflow.lite.python.interpreter import load_delegate

# If using Edge TPU, assign filename for Edge TPU model
if use_TPU:
    # If the user has specified the name of the .tflite file, use that name, otherwise use the default 'edgetpu.tflite'
    if GRAPH_NAME == 'detect.tflite':
        GRAPH_NAME = 'edgetpu.tflite'

# Get path to the current working directory
CWD_PATH = os.getcwd()

# Define path to images and grab all image filenames
PATH_TO_IMAGES = os.path.join(CWD_PATH, IM_DIR)
images = glob.glob(PATH_TO_IMAGES + '/*.jpg') + glob.glob(PATH_TO_IMAGES + '/*.png') + glob.glob(PATH_TO_IMAGES + '/*.bmp')

# Create results directory if the user wants to save results
if save_results:
    RESULTS_DIR = IM_DIR + '_results'
    RESULTS_PATH = os.path.join(CWD_PATH, RESULTS_DIR)
    if not os.path.exists(RESULTS_PATH):
        os.makedirs(RESULTS_PATH)

# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_NAME, LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Have to do a weird fix for the label map if using the COCO "starter model" from
# https://www.tensorflow.org/lite/models/object_detection/overview
# The first label is '???', which has to be removed.
if labels[0] == '???':
    del labels[0]

# Load the TensorFlow Lite model
# If using Edge TPU, use the special load_delegate argument
if use_TPU:
    interpreter = Interpreter(model_path=PATH_TO_CKPT,
                              experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    print(PATH_TO_CKPT)
else:
    interpreter = Interpreter(model_path=PATH_TO_CKPT)

interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5

save_folder1 = '../../Face-Detected'  # Folder name to store captured images
if not os.path.exists(save_folder1):
    os.makedirs(save_folder1)

lord_john_perucho_counter = 0
lord_john_perucho_detected = False  
num_images_to_process_lord = 1  
total_lord_john_perucho_detected = 0  
lord_john_perucho_cooldown = time.monotonic()
lord_john_perucho_cooldowns = 0

leo_delen_counter = 0
leo_delen_detected = False  
num_images_to_process_leo = 1  
total_leo_delen_detected = 0  
leo_delen_cooldown = time.monotonic()
leo_delen_cooldowns = 0

frank_castillo_counter = 0
frank_castillo_detected = False  
num_images_to_process_frank = 1  
total_frank_castillo_detected = 0  
frank_castillo_cooldown = time.monotonic()
frank_castillo_cooldowns = 0

queenie_amargo_counter = 0
queenie_amargo_detected = False  
num_images_to_process_queenie = 1  
total_queenie_amargo_detected = 0  
queenie_amargo_cooldown = time.monotonic()
queenie_amargo_cooldowns = 0

outname = output_details[0]['name']

if 'StatefulPartitionedCall' in outname:  # This is a TF2 model
    boxes_idx, classes_idx, scores_idx = 1, 3, 0
else:  # This is a TF1 model
    boxes_idx, classes_idx, scores_idx = 0, 1, 2

image_paths = "../Face_Detect/face_detected"

processed_images = set()
processed_images_folder = 'processed_images'  # Folder name for processed images
if not os.path.exists(processed_images_folder):
    os.makedirs(processed_images_folder)

def get_image_paths(image_paths):
  """Gets a list of image paths from the specified folder."""
  return [os.path.join(image_paths, f) for f in os.listdir(image_paths) if f.endswith((".jpg", ".jpeg", ".png"))]  # Filter for image formats

while True:
    images = get_image_paths("../Face_Detect/face_detected")

    for image_path in images:
        images = get_image_paths("../Face_Detect/face_detected")
        # Check if the image has already been processed
        if image_path in processed_images:
            continue  
        time.sleep(1)
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        imH, imW, _ = image.shape
        image_resized = cv2.resize(image_rgb, (width, height))
        input_data = np.expand_dims(image_resized, axis=0)

        if floating_model:
            input_data = (np.float32(input_data) - input_mean) / input_std

        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0]  # Bounding box coordinates of detected objects
        classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0]  # Class index of detected objects
        scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0]  # Confidence of detected objects
        
        for i in range(len(scores)):
            if 0 <= int(classes[i]) < len(labels) and (scores[i] > min_conf_threshold) and (scores[i] <= 1.0):
                object_name = labels[int(classes[i])]  # Look up object name from the "labels" array using the class index

                if object_name == "Lord John Perucho" and not lord_john_perucho_detected and lord_john_perucho_counter < num_images_to_process_lord:
                        now = datetime.datetime.now()
                        timestamp = now.strftime("%Y-%m-%d_%H-%M")  # YYYY-MM-DD_HH-MM-SS format
                        ymin = int(max(1, (boxes[i][0] * imH)))
                        xmin = int(max(1, (boxes[i][1] * imW)))
                        ymax = int(min(imH, (boxes[i][2] * imH)))
                        xmax = int(min(imW, (boxes[i][3] * imW)))
                        cropped_image = image[ymin:ymax, xmin:xmax]
                        cropped_image_resized = cv2.resize(cropped_image, (320, 320))
                        image_name = f"{timestamp}_TI_{object_name} ({lord_john_perucho_counter}).jpg"
                        image_path_processed = os.path.join(save_folder1, image_name)
                        cv2.imwrite(image_path_processed, cropped_image_resized)  # Capture the frame
                        lord_john_perucho_counter += 1
                        lord_john_perucho_detected = True  # Set flag to True after first detection
                        lord_john_perucho_cooldown = time.monotonic()# Store start time for cooldown
                        print ("Time In Detection: Lord John Perucho")
                        images = get_image_paths("../Face_Detect/face_detected")
                if object_name == "Lord John Perucho" and lord_john_perucho_counter > 5 and (time_lapse > 60): ##time.localtime().tm_hour == 17 and time.localtime().tm_min >= 12
                        now = datetime.datetime.now()
                        timestamp = now.strftime("%Y-%m-%d_%H-%M")  # YYYY-MM-DD_HH-MM-SS format
                        ymin = int(max(1, (boxes[i][0] * imH)))
                        xmin = int(max(1, (boxes[i][1] * imW)))
                        ymax = int(min(imH, (boxes[i][2] * imH)))
                        xmax = int(min(imW, (boxes[i][3] * imW)))
                        cropped_image = image[ymin:ymax, xmin:xmax]
                        cropped_image_resized = cv2.resize(cropped_image, (320, 320))
                        image_name = f"{timestamp}_TO_{object_name} ({lord_john_perucho_counter}).jpg"
                        image_path_processed = os.path.join(save_folder1, image_name)
                        cv2.imwrite(image_path_processed, cropped_image_resized)  # Capture the frame
                        lord_john_perucho_detected = True 
                        lord_john_perucho_cooldown = time.monotonic()# Store start time for cooldown
                        time_lapse = int(time.monotonic() - lord_john_perucho_cooldown)
                        # print ("Mid_IF", time_lapse)
                        print ("Time Out Detection: Lord John Perucho")
                        images = get_image_paths("../Face_Detect/face_detected")
                elif object_name == "Lord John Perucho":
                    now = datetime.datetime.now()
                    timestamp = now.strftime("%Y-%m-%d_%H-%M")  # YYYY-MM-DD_HH-MM-SS format
                    ymin = int(max(1, (boxes[i][0] * imH)))
                    xmin = int(max(1, (boxes[i][1] * imW)))
                    ymax = int(min(imH, (boxes[i][2] * imH)))
                    xmax = int(min(imW, (boxes[i][3] * imW)))
                    cropped_image = image[ymin:ymax, xmin:xmax]
                    lord_john_perucho_counter += 1
                    shutil.move(image_path, os.path.join(processed_images_folder, os.path.basename(image_path)))
                    processed_images.add(image_path)
                    time_lapse = int(time.monotonic() - lord_john_perucho_cooldown)
                    # print ("Actual Time: ", (time.monotonic() - lord_john_perucho_cooldown))
                    # print ("Time set: ", lord_john_perucho_cooldown)
                    print("Dump Images: Lord John Perucho")
                    images = get_image_paths("../Face_Detect/face_detected")

                if object_name == "Leo Delen" and not leo_delen_detected and leo_delen_counter < num_images_to_process_leo:
                        now = datetime.datetime.now()
                        timestamp = now.strftime("%Y-%m-%d_%H-%M")  # YYYY-MM-DD_HH-MM-SS format
                        ymin = int(max(1, (boxes[i][0] * imH)))
                        xmin = int(max(1, (boxes[i][1] * imW)))
                        ymax = int(min(imH, (boxes[i][2] * imH)))
                        xmax = int(min(imW, (boxes[i][3] * imW)))
                        cropped_image = image[ymin:ymax, xmin:xmax]
                        cropped_image_resized = cv2.resize(cropped_image, (320, 320))
                        image_name = f"{timestamp}_TI_{object_name} ({leo_delen_counter}).jpg"
                        image_path_processed = os.path.join(save_folder1, image_name)
                        cv2.imwrite(image_path_processed, cropped_image_resized)  # Capture the frame
                        leo_delen_counter += 1
                        leo_delen_detected = True  # Set flag to True after first detection
                        leo_delen_cooldown = time.monotonic()# Store start time for cooldown
                        print ("Time In Detection: Leo Delen")
                        images = get_image_paths("../Face_Detect/face_detected")
                if object_name == "Leo Delen" and leo_delen_counter > 5 and (time_lapse > 60): ##time.localtime().tm_hour == 17 and time.localtime().tm_min >= 12
                        now = datetime.datetime.now()
                        timestamp = now.strftime("%Y-%m-%d_%H-%M")  # YYYY-MM-DD_HH-MM-SS format
                        ymin = int(max(1, (boxes[i][0] * imH)))
                        xmin = int(max(1, (boxes[i][1] * imW)))
                        ymax = int(min(imH, (boxes[i][2] * imH)))
                        xmax = int(min(imW, (boxes[i][3] * imW)))
                        cropped_image = image[ymin:ymax, xmin:xmax]
                        cropped_image_resized = cv2.resize(cropped_image, (320, 320))
                        image_name = f"{timestamp}_TO_{object_name} ({leo_delen_counter}).jpg"
                        image_path_processed = os.path.join(save_folder1, image_name)
                        cv2.imwrite(image_path_processed, cropped_image_resized)  # Capture the frame
                        leo_delen_detected = True 
                        leo_delen_cooldown = time.monotonic()# Store start time for cooldown
                        time_lapse = int(time.monotonic() - leo_delen_cooldown)
                        print ("Time Out Detection: Leo Delen")
                        images = get_image_paths("../Face_Detect/face_detected")
                elif object_name == "Leo Delen":
                    now = datetime.datetime.now()
                    timestamp = now.strftime("%Y-%m-%d_%H-%M")  # YYYY-MM-DD_HH-MM-SS format
                    ymin = int(max(1, (boxes[i][0] * imH)))
                    xmin = int(max(1, (boxes[i][1] * imW)))
                    ymax = int(min(imH, (boxes[i][2] * imH)))
                    xmax = int(min(imW, (boxes[i][3] * imW)))
                    cropped_image = image[ymin:ymax, xmin:xmax]
                    leo_delen_counter += 1
                    shutil.move(image_path, os.path.join(processed_images_folder, os.path.basename(image_path)))
                    processed_images.add(image_path)
                    time_lapse = int(time.monotonic() - leo_delen_cooldown)
                    print("Dump Images: Leo Delen")
                    images = get_image_paths("../Face_Detect/face_detected")

                if object_name == "Frank Lester castillo" and not frank_castillo_detected and frank_castillo_counter < num_images_to_process_frank:
                        now = datetime.datetime.now()
                        timestamp = now.strftime("%Y-%m-%d_%H-%M")  # YYYY-MM-DD_HH-MM-SS format
                        ymin = int(max(1, (boxes[i][0] * imH)))
                        xmin = int(max(1, (boxes[i][1] * imW)))
                        ymax = int(min(imH, (boxes[i][2] * imH)))
                        xmax = int(min(imW, (boxes[i][3] * imW)))
                        cropped_image = image[ymin:ymax, xmin:xmax]
                        cropped_image_resized = cv2.resize(cropped_image, (320, 320))
                        image_name = f"TI_{timestamp}_{object_name} ({frank_castillo_counter}).jpg"
                        image_path_processed = os.path.join(save_folder1, image_name)
                        cv2.imwrite(image_path_processed, cropped_image_resized)  # Capture the frame
                        frank_castillo_counter += 1
                        frank_castillo_detected = True  # Set flag to True after first detection
                        frank_castillo_cooldown = time.monotonic()# Store start time for cooldown
                        print ("Time In Detection: Frank Lester Castillo")
                        images = get_image_paths("../Face_Detect/face_detected")
                if object_name == "Frank Lester castillo" and frank_castillo_counter > 5 and (time_lapse > 60): ##time.localtime().tm_hour == 17 and time.localtime().tm_min >= 12
                        now = datetime.datetime.now()
                        timestamp = now.strftime("%Y-%m-%d_%H-%M")  # YYYY-MM-DD_HH-MM-SS format
                        ymin = int(max(1, (boxes[i][0] * imH)))
                        xmin = int(max(1, (boxes[i][1] * imW)))
                        ymax = int(min(imH, (boxes[i][2] * imH)))
                        xmax = int(min(imW, (boxes[i][3] * imW)))
                        cropped_image = image[ymin:ymax, xmin:xmax]
                        cropped_image_resized = cv2.resize(cropped_image, (320, 320))
                        image_name = f"{timestamp}_TO_{object_name} ({frank_castillo_counter}).jpg"
                        image_path_processed = os.path.join(save_folder1, image_name)
                        cv2.imwrite(image_path_processed, cropped_image_resized)  # Capture the frame
                        frank_castillo_detected = True 
                        frank_castillo_cooldown = time.monotonic()# Store start time for cooldown
                        time_lapse = int(time.monotonic() - frank_castillo_cooldown)
                        # print ("Mid_IF", time_lapse)
                        print ("Time Out Detection: Frank Lester Castillo")
                        images = get_image_paths("../Face_Detect/face_detected")
                elif object_name == "Frank Lester castillo":
                    now = datetime.datetime.now()
                    timestamp = now.strftime("%Y-%m-%d_%H-%M")  # YYYY-MM-DD_HH-MM-SS format
                    ymin = int(max(1, (boxes[i][0] * imH)))
                    xmin = int(max(1, (boxes[i][1] * imW)))
                    ymax = int(min(imH, (boxes[i][2] * imH)))
                    xmax = int(min(imW, (boxes[i][3] * imW)))
                    cropped_image = image[ymin:ymax, xmin:xmax]
                    frank_castillo_counter += 1
                    shutil.move(image_path, os.path.join(processed_images_folder, os.path.basename(image_path)))
                    processed_images.add(image_path)
                    time_lapse = int(time.monotonic() - frank_castillo_cooldown)
                    print("Dump Images: Frank Lester Castillo")
                    images = get_image_paths("../Face_Detect/face_detected")

                if object_name == "Queenie Rose Amargo" and not queenie_amargo_detected and queenie_amargo_counter < num_images_to_process_queenie:
                        now = datetime.datetime.now()
                        timestamp = now.strftime("%Y-%m-%d_%H-%M")  # YYYY-MM-DD_HH-MM-SS format
                        ymin = int(max(1, (boxes[i][0] * imH)))
                        xmin = int(max(1, (boxes[i][1] * imW)))
                        ymax = int(min(imH, (boxes[i][2] * imH)))
                        xmax = int(min(imW, (boxes[i][3] * imW)))
                        cropped_image = image[ymin:ymax, xmin:xmax]
                        cropped_image_resized = cv2.resize(cropped_image, (320, 320))
                        image_name = f"{timestamp}_TI_{object_name} ({queenie_amargo_counter}).jpg"
                        image_path_processed = os.path.join(save_folder1, image_name)
                        cv2.imwrite(image_path_processed, cropped_image_resized)  # Capture the frame
                        queenie_amargo_counter += 1
                        queenie_amargo_detected = True  # Set flag to True after first detection
                        queenie_amargo_cooldown = time.monotonic()# Store start time for cooldown
                        print ("Time In Detection: Queenie Rose Amargo")
                        images = get_image_paths("../Face_Detect/face_detected")
                if object_name == "Queenie Rose Amargo" and queenie_amargo_counter > 5 and (time_lapse > 60): ##time.localtime().tm_hour == 17 and time.localtime().tm_min >= 12
                        now = datetime.datetime.now()
                        timestamp = now.strftime("%Y-%m-%d_%H-%M")  # YYYY-MM-DD_HH-MM-SS format
                        ymin = int(max(1, (boxes[i][0] * imH)))
                        xmin = int(max(1, (boxes[i][1] * imW)))
                        ymax = int(min(imH, (boxes[i][2] * imH)))
                        xmax = int(min(imW, (boxes[i][3] * imW)))
                        cropped_image = image[ymin:ymax, xmin:xmax]
                        cropped_image_resized = cv2.resize(cropped_image, (320, 320))
                        image_name = f"{timestamp}_TO_{object_name} ({queenie_amargo_counter}).jpg"
                        image_path_processed = os.path.join(save_folder1, image_name)
                        cv2.imwrite(image_path_processed, cropped_image_resized)  # Capture the frame
                        queenie_amargo_detected = True 
                        queenie_amargo_cooldown = time.monotonic()# Store start time for cooldown
                        time_lapse = int(time.monotonic() - frank_castillo_cooldown)
                        print ("Time Out Detection: Queenie Rose Amargo")
                        images = get_image_paths("../Face_Detect/face_detected")
                elif object_name == "Queenie Rose Amargo":
                    now = datetime.datetime.now()
                    timestamp = now.strftime("%Y-%m-%d_%H-%M")  # YYYY-MM-DD_HH-MM-SS format
                    ymin = int(max(1, (boxes[i][0] * imH)))
                    xmin = int(max(1, (boxes[i][1] * imW)))
                    ymax = int(min(imH, (boxes[i][2] * imH)))
                    xmax = int(min(imW, (boxes[i][3] * imW)))
                    cropped_image = image[ymin:ymax, xmin:xmax]
                    queenie_amargo_counter += 1
                    shutil.move(image_path, os.path.join(processed_images_folder, os.path.basename(image_path)))
                    processed_images.add(image_path)
                    time_lapse = int(time.monotonic() - queenie_amargo_cooldown)
                    print("Dump Images: Queenie Rose Amargo")
                    images = get_image_paths("../Face_Detect/face_detected")
                
        images = get_image_paths("../Face_Detect/face_detected")

        if not images:
            # images = get_image_paths("../Face_Detect/face_detected")
            print("No images to process")
            time.sleep(2)
            continue

# Clean up
cv2.destroyAllWindows()