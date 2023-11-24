import cv2
import os
import numpy as np
from pyzbar.pyzbar import decode

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

def run_continuous_qr_code_reader(image_folder, actual_size):
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        print(f"No images found in {image_folder}")
        return

    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        reference_image = cv2.imread(image_path)

        # Calculate the center point of the image
        image_center = (reference_image.shape[1] / 2, reference_image.shape[0] / 2)

        print(f"Processing image: {image_path}")

        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            qr_code = locate_qr_code(frame)

            if qr_code is not None:
                qr_code_center, distance_to_qr, distance_to_center, qr_code_data = estimate_qr_code_position_and_distance(qr_code, actual_size, image_center)

                # Display the frame with the QR code information
                cv2.putText(frame, f"Distance to QR Code (X): {distance_to_qr[0]:.2f} units", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Distance to QR Code (Y): {distance_to_qr[1]:.2f} units", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Distance to Center (X): {distance_to_center[0]:.2f} pixels", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Distance to Center (Y): {distance_to_center[1]:.2f} pixels", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"QR Code Data: {qr_code_data}", (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("QR Code Frame", frame)
            else:
                cv2.imshow("QR Code Frame", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

# Provide path to the folder containing images
image_folder_path = "./qrimages"

# Actual size of the QR code in the real world (width, height) in your chosen units
actual_size = (10.0, 10.0)  # Example: 10x10 units

# Run the continuous QR code reader on images in the folder
run_continuous_qr_code_reader(image_folder_path, actual_size)
