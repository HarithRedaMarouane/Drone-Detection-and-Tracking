import cv2
import serial
import time
from yoloDet import YoloTRT

# Constants for camera and image
IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720
CAMERA_FOV = 105
CENTER_DEADZONE_RADIUS = 5  # Center deadzone radius in degrees
SLOW_ZONE_RADIUS = 10  # Slow zone radius in degrees

# Calculate pixels per degree based on the camera's FOV
PIXELS_PER_DEGREE = IMAGE_WIDTH / CAMERA_FOV

# Constants for servo control
SERVO_CENTER_X = 90  # Assuming 0-180 degrees range for the servo
SERVO_CENTER_Y = 90

# Initialize the serial connection to the ESP32
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
time.sleep(2)  # Wait for the connection to establish

def send_servo_angles(servo_x, servo_y):
    command = '{},{}\n'.format(servo_x, servo_y)
    ser.write(command.encode('utf-8'))

# Define the GStreamer pipeline
def gstreamer_pipeline(device=0):
    return (
        "v4l2src device=/dev/video%d ! "
        "videoconvert ! "
        "videoscale ! "
        "video/x-raw, width=(int)1280, height=(int)720, format=(string)BGR ! appsink"
        % device
    )

# Initialize the camera and YOLO model
cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
model = YoloTRT(library="yolov7/build/libmyplugins.so", engine="yolov7/build/yolov7.engine", conf=0.5, yolo_ver="v7")

# Center of the video frame
frame_center = (IMAGE_WIDTH // 2, IMAGE_HEIGHT // 2)

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Draw zones on the frame
    cv2.circle(frame, frame_center, int(CENTER_DEADZONE_RADIUS * PIXELS_PER_DEGREE), (0, 255, 0), 2)  # Green circle for center deadzone
    cv2.circle(frame, frame_center, int(SLOW_ZONE_RADIUS * PIXELS_PER_DEGREE), (0, 255, 255), 2)  # Yellow circle for slow zone

    detections, _ = model.Inference(frame)

    for det in detections:
        # Get the bounding box coordinates
        x1, y1, x2, y2 = det["box"]

        # Calculate the center of the bounding box
        bbox_center_x = int((x1 + x2) / 2)
        bbox_center_y = int((y1 + y2) / 2)

        # Draw a point at the center of the bounding box
        cv2.circle(frame, (bbox_center_x, bbox_center_y), 5, (0, 0, 255), -1)  # Red point at the center

        # Draw a line from the center of the bounding box to the center of the video frame
        cv2.line(frame, (bbox_center_x, bbox_center_y), frame_center, (255, 0, 0), 2)  # Blue line representing the offset

        # Calculate offset in pixels
        offset_x_pixels = bbox_center_x - frame_center[0]
        offset_y_pixels = bbox_center_y - frame_center[1]

        # Convert pixel offsets to angles
        angle_x = offset_x_pixels / PIXELS_PER_DEGREE
        angle_y = offset_y_pixels / PIXELS_PER_DEGREE

        # Calculate servo angles
        servo_x = SERVO_CENTER_X - angle_x
        servo_y = SERVO_CENTER_Y - angle_y

        # Ensure the servo angles are within the valid range
        servo_x = max(0, min(180, servo_x))
        servo_y = max(0, min(180, servo_y))

        # Send the angles to the ESP32
        send_servo_angles(servo_x, servo_y)

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
