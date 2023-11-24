

import cv2
import os
from pyzbar.pyzbar import decode
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

##
import threading
global distToQR, xToQR, yToQR
lock = threading.Lock()
distToQR = 0
xToQR = 0
yToQR = 0


def get_distance_to_qr():
    global distToQR, xToQR, yToQR
    with lock:
        return distToQR, xToQR, yToQR

def locate_qr_code(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    qr_codes = decode(gray)

    if qr_codes:
        qr_code = qr_codes[0]
        print(f"QR Code Found: {qr_code.data}")
        return qr_code
    else:
        print("No QR Code Found")
        return None

def estimate_qr_code_position_and_distance(qr_code, actual_size, image_center):
    if qr_code is not None:
        # Assuming actual_size is the real-world size of the QR code
        actual_width, actual_height = actual_size

        # Extracting QR code information
        qr_code_rect = qr_code.rect
        qr_code_center = (qr_code_rect.left + qr_code_rect.width / 2, qr_code_rect.top + qr_code_rect.height / 2)

        # Calculate distance to QR code in x and y directions
        # Assuming known focal length and camera sensor size
        # You may need to calibrate these parameters based on your camera setup
        focal_length = 1000  # Example focal length in pixels
        sensor_width = 36.0  # Example camera sensor width in mm

        distance_to_qr_x = (actual_width * focal_length) / (qr_code_rect.width * sensor_width)
        distance_to_qr_y = (actual_height * focal_length) / (qr_code_rect.height * sensor_width)
        

        # Calculate distance to the center point of the image in x and y directions
        distance_to_center_x = qr_code_center[0] - image_center[0]
        distance_to_center_y = qr_code_center[1] - image_center[1]

        print(f"QR Code Center: {qr_code_center}")
        print(f"Distance to QR Code (X): {distance_to_qr_x:.2f} units")
        print(f"Distance to QR Code (Y): {distance_to_qr_y:.2f} units")
        print(f"Distance to Image Center (X): {distance_to_center_x:.2f} pixels")
        print(f"Distance to Image Center (Y): {distance_to_center_y:.2f} pixels")
        
        


        return qr_code_center, (distance_to_qr_x, distance_to_qr_y), (distance_to_center_x, distance_to_center_y), qr_code.data
    else:
        return None, None, None, None


def run_continuous_qr_code_reader(image_folder, actual_size, save_folder):
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        print(f"No images found in {image_folder}")
        return

    with PiCamera() as camera:
        camera.resolution = (640, 480)  # Adjust the resolution as needed
        camera.framerate = 30
        raw_capture = PiRGBArray(camera, size=(640, 480))

        time.sleep(0.1)  # Allow the camera to warm up

        for image_file in image_files:
            image_path = os.path.join(image_folder, image_file)
            reference_image = cv2.imread(image_path)

            # Calculate the center point of the image
            image_center = (reference_image.shape[1] / 2, reference_image.shape[0] / 2)

            print(f"Processing image: {image_path}")

            for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
                img = frame.array
                qr_code = locate_qr_code(img)

                # Save the frame with the fixed name "snapshot.png"
                save_path = os.path.join(save_folder, "snapshot.png")
                cv2.imwrite(save_path, img)
                print(f"Saved snapshot: {save_path}")
                time.sleep(0.2)

                if qr_code is not None:
                    qr_code_center, distance_to_qr, distance_to_center, qr_code_data = estimate_qr_code_position_and_distance(qr_code, actual_size, image_center)
                    print(f"QR Code Data: {qr_code_data}")
                    global distToQR, xToQR, yToQR
                    with lock:
                        distToQR=distance_to_qr[1]
                        xToQR=distance_to_center[0]
                        yToQR=distance_to_center[1]
                    
                else:
                    print("No QR Code Found")

                key = cv2.waitKey(1) & 0xFF
                raw_capture.truncate(0)

                if key == ord('q'):
                    break

    cv2.destroyAllWindows()




