import cv2
import argparse
import numpy as np

# # handle command line arguments
# ap = argparse.ArgumentParser()
# ap.add_argument('-i', '--image', required=True,
#                 help = 'path to input image')
# ap.add_argument('-c', '--config', required=True,
#                 help = 'path to yolo config file')
# ap.add_argument('-w', '--weights', required=True,
#                 help = 'path to yolo pre-trained weights')
# ap.add_argument('-cl', '--classes', required=True,
#                 help = 'path to text file containing class names')
# args = ap.parse_args()


# function to get the output layer names
# in the architecture
def get_output_layers(net):
    layer_names = net.getLayerNames()

    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers

def draw_all_box(boxes, indices, class_ids, confidences, classes_file):

    # read class names from text file
    classes = None
    with open(classes_file, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    # generate different colors for different classes
    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

    # go through the detections remaining
    # after nms and draw bounding box
    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]

        draw_bounding_box(frame, class_ids[i], confidences[i], classes, round(x), round(y), round(x + w),
                          round(y + h), COLORS)

# function to draw bounding box on the detected object with class name
def draw_bounding_box(img, class_id, confidence, classes, x, y, x_plus_w, y_plus_h, COLORS):
    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)

    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def yolo_detection(frame, classes_file):
    Width = frame.shape[1]
    Height = frame.shape[0]
    scale = 0.00392


    # read pre-trained model and config file
    net = cv2.dnn.readNet(weights, config_file)

    # create input blob
    blob = cv2.dnn.blobFromImage(frame, scale, (416, 416), (0, 0, 0), True, crop=False)

    # set input blob for the network
    net.setInput(blob)

    # run inference through the network
    # and gather predictions from output layers
    outs = net.forward(get_output_layers(net))

    # initialization
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    # for each detetion from each output layer
    # get the confidence, class id, bounding box params
    # and ignore weak detections (confidence < 0.5)
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    # apply non-max suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    return boxes, indices, class_ids, confidences


def tracking(frame):
    print(history)


# Global history [ {{}, {}, {}}, {{}, {}}, {{}, {}} ]
history = list(dict(dict()))

# [
# { {'id': 0, 'box': [7, 211, 269, 580], 'feature' : [1, 1]}, {'id': 1, 'box': [x, y, w, h], 'feature' : [ ... ]} },  1st
# { {'id': 0,'box': [7, 211, 269, 580], 'feature' : [1, 1]}}                                                          2nd
# ]

if __name__ == '__main__':

    filename = "6767_7_v1.avi"
    classes_file = "obj.names"
    weights = "yolov2.weights"
    config_file = "yolo-obj.cfg"

    cap = cv2.VideoCapture(filename)

    cont = 1
    skip_frames = 0
    pause_frames = False
    while(cap.isOpened()):

        if not pause_frames:
            skip_frames -= 1
            ret, frame = cap.read()

            if skip_frames > 0:
                continue

            if cont % 1 == 0 and cont > 383:
                # Detection step
                boxes, indices, class_ids, confidences = yolo_detection(frame, classes_file)

                tracking(frame)

                # Draw the detected boxes
                draw_all_box(boxes, indices, class_ids, confidences, classes_file)




                # display output image
                cv2.imshow("object detection", frame)


        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('s'):
            skip_frames = 50
        if key == ord('p'):
            # toggle pause
            if pause_frames is True:
                pause_frames = False
            else:
                pause_frames = True

        cont = cont + 1

    # release resources
    cap.release()
    cv2.destroyAllWindows()