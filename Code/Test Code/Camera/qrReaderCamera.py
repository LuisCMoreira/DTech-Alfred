import cv2
import numpy as np
from pyzbar.pyzbar import decode

def locate_qr_code(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    qr_codes = decode(gray)

    if qr_codes:
        qr_code = qr_codes[0]
        print(f"QR Code Found: {qr_code.data}")
        return qr_code.rect
    else:
        print("No QR Code Found")
        return None

def capture_qr_code_frame(cap):
    ret, frame = cap.read()
    qr_code_location = locate_qr_code(frame)

    if qr_code_location:
        x, y, w, h = qr_code_location
        qr_code_frame = frame[y:y+h, x:x+w]
        print("Captured QR Code Frame")
        return qr_code_frame
    else:
        return None

def estimate_qr_code_tilt(reference_image, actual_frame):
    reference_qr = decode(reference_image)
    actual_qr = decode(actual_frame)

    if reference_qr and actual_qr:
        reference_points = np.array([(point.x, point.y) for point in reference_qr[0].polygon], dtype=np.float32)
        actual_points = np.array([(point.x, point.y) for point in actual_qr[0].polygon], dtype=np.float32)

        matrix, _ = cv2.findHomography(reference_points, actual_points, cv2.RANSAC)

        angle_rad = -np.arctan2(matrix[0, 1], matrix[0, 0])
        angle_deg = np.degrees(angle_rad)

        print(f"QR Code Tilt Angle: {angle_deg} degrees")
        return angle_deg
    else:
        print("QR Code not detected in one of the frames.")
        return None


def run_continuous_qr_code_reader(reference_image):
    cap = cv2.VideoCapture(0)

    while True:
        qr_code_frame = capture_qr_code_frame(cap)

        if qr_code_frame is not None:
            cv2.imshow("QR Code Frame", qr_code_frame)
            key = cv2.waitKey(0) & 0xFF

            if key == ord('q'):
                break

            tilt_angle = estimate_qr_code_tilt(reference_image, qr_code_frame)

            if tilt_angle is not None:
                print(f"QR Code Tilt Angle: {tilt_angle} degrees")

    cap.release()
    cv2.destroyAllWindows()


# Provide path to the reference image
reference_image_path = r"C:\Users\LuisC\Desktop\githubProjects\DTech-Alfred\Code\Test Code\Camera\100e20.png"
reference_image = cv2.imread(reference_image_path)

# Run the continuous QR code reader
run_continuous_qr_code_reader(reference_image)






