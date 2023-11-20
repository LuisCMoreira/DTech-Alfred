import cv2
import numpy as np
from pyzbar.pyzbar import decode

def estimate_qr_code_tilt(reference_image, actual_image):
    # Read images
    reference = cv2.imread(reference_image, cv2.IMREAD_GRAYSCALE)
    actual = cv2.imread(actual_image, cv2.IMREAD_GRAYSCALE)

    # Detect QR codes in both images
    reference_qr = decode(reference)
    actual_qr = decode(actual)

    # Assuming only one QR code is present in both images
    reference_points = np.array([(point.x, point.y) for point in reference_qr[0].polygon], dtype=np.float32)
    actual_points = np.array([(point.x, point.y) for point in actual_qr[0].polygon], dtype=np.float32)

    # Estimate transformation matrix (rotation + translation)
    matrix = cv2.estimateAffine2D(reference_points, actual_points)[0]

    # Extract rotation angle
    angle_rad = -np.arctan2(matrix[0, 1], matrix[0, 0])
    angle_deg = np.degrees(angle_rad)

    return angle_deg




def estimate_qr_code_pose(reference_image, actual_image):
    # Read images
    reference = cv2.imread(reference_image, cv2.IMREAD_GRAYSCALE)
    actual = cv2.imread(actual_image, cv2.IMREAD_GRAYSCALE)

    # Detect QR codes in both images
    reference_qr = decode(reference)
    actual_qr = decode(actual)

    # Assuming only one QR code is present in both images
    reference_points = np.array([(point.x, point.y) for point in reference_qr[0].polygon], dtype=np.float32)
    actual_points = np.array([(point.x, point.y) for point in actual_qr[0].polygon], dtype=np.float32)

    # Known size of the QR code
    qr_code_size = 10.0  # Replace with the actual size of your QR code

    # Placeholder values (replace with actual calibration parameters)
    focal_length_x = 1000.0
    focal_length_y = 1000.0
    principal_point_x = actual.shape[1] / 2.0
    principal_point_y = actual.shape[0] / 2.0

    # Camera matrix and distortion coefficients
    camera_matrix = np.array([[focal_length_x, 0, principal_point_x],
                              [0, focal_length_y, principal_point_y],
                              [0, 0, 1]], dtype=np.float32)

    dist_coeffs = np.zeros((4, 1))  # Distortion coefficients

    # Estimate 3D pose using solvePnP
    success, rotation_vector, translation_vector = cv2.solvePnP(
        np.array([[-qr_code_size / 2, -qr_code_size / 2, 0],
                  [qr_code_size / 2, -qr_code_size / 2, 0],
                  [qr_code_size / 2, qr_code_size / 2, 0],
                  [-qr_code_size / 2, qr_code_size / 2, 0]], dtype=np.float32),
        actual_points, camera_matrix, dist_coeffs)

    # Extract euler angles from rotation vector
    rotation_matrix, _ = cv2.Rodrigues(rotation_vector)

    # Extract yaw angle
    yaw = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0]) * 180 / np.pi

    return translation_vector, rotation_vector, yaw


# Provide paths to the untilted reference image and the actual image
reference_image_path = r"C:\Users\LuisC\Desktop\githubProjects\DTech-Alfred\Code\Test Code\Camera\100e20.png"
actual_image_path = r"C:\Users\LuisC\Desktop\githubProjects\DTech-Alfred\Code\Test Code\Camera\tiltedAll.png"

tilt_angle = estimate_qr_code_tilt(reference_image_path, actual_image_path)
print(f"QR Code Tilt Angle: {tilt_angle} degrees")

translation, rotation, yaw = estimate_qr_code_pose(reference_image_path, actual_image_path)
print(f"Translation: {translation}")
print(f"Rotation Vector: {rotation}")
print(f"Yaw: {yaw} degrees")
