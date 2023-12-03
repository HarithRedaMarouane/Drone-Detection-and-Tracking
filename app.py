import sys
import cv2 
import imutils
from yoloDet import YoloTRT

def gstreamer_pipeline(device=0):
    return (
        "v4l2src device=/dev/video%d ! "
        "videoconvert ! "
        "videoscale ! "
        "video/x-raw, width=1280, height=720, format=(string)BGR ! appsink"
        % device
    )
# use path for library and engine file
model = YoloTRT(library="yolov5/build/libmyplugins.so", engine="yolov5/build/best_yolov5_300.engine", conf=0.5, yolo_ver="v5")

# Start video capture with USB camera
cap = cv2.VideoCapture(gstreamer_pipeline(),cv2.CAP_GSTREAMER)


while True:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=600)
    detections, t = model.Inference(frame)
    # for obj in detections:
    #    print(obj['class'], obj['conf'], obj['box'])
    # print("FPS: {} sec".format(1/t))
    fps = 1.0 / t
    fps_text = "FPS: {:.2f}".format(fps)
    cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255,0),2)
    cv2.imshow("Output", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
