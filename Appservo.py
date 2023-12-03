import cv2
import imutils
import Jetson.GPIO as GPIO
from yoloDet import YoloTRT

# GPIO setup for Jetson Nano
servo_x_pin = 32  # Update with your PWM-capable pin number
servo_y_pin = 33  # Update with your PWM-capable pin number

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_x_pin, GPIO.OUT)
GPIO.setup(servo_y_pin, GPIO.OUT)

pwm_x = GPIO.PWM(servo_x_pin, 50)  # 50 Hz
pwm_y = GPIO.PWM(servo_y_pin, 50)
pwm_x.start(0)
pwm_y.start(0)

def update_servo_position(pwm, angle):
    duty_cycle = angle / 18 + 2
    pwm.ChangeDutyCycle(duty_cycle)

def control_servos(object_center, frame_center):
    x_error = object_center[0] - frame_center[0]
    y_error = object_center[1] - frame_center[1]

    update_servo_position(pwm_x, -x_error/20)
    update_servo_position(pwm_y, -y_error/20)

def gstreamer_pipeline(device=0):
    return (
        "v4l2src device=/dev/video%d ! "
        "videoconvert ! "
        "videoscale ! "
        "video/x-raw, width=1280, height=720, format=(string)BGR ! appsink"
        % device
    )


# Initialize YOLO model
model = YoloTRT(library="yolov5/build/libmyplugins.so", engine="yolov5/build/best_yolov5_300.engine", conf=0.5, yolo_ver="v5")

# Start video capture with USB camera
cap = cv2.VideoCapture(gstreamer_pipeline(),cv2.CAP_GSTREAMER)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = imutils.resize(frame, width=600)
    detections, t = model.Inference(frame)

    frame_center = (frame.shape[1] // 2, frame.shape[0] // 2)

    for obj in detections:
        x_center = (obj['box'][0] + obj['box'][2]) // 2
        y_center = (obj['box'][1] + obj['box'][3]) // 2

        control_servos((x_center, y_center), frame_center)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()

