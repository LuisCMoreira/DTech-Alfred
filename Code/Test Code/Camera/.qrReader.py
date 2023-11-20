import cv2
import numpy as np
from pyzbar.pyzbar import decode

def read_qr_code(image_path):
    # Read the input image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use the decode function from pyzbar to decode QR codes
    qr_codes = decode(gray)

    # Print the data contained in the QR code(s)
    for qr_code in qr_codes:
        data = qr_code.data.decode('utf-8')
        print(f"QR Code Data: {data}")

        # Draw a rectangle around the QR code
        rect_points = qr_code.polygon
        if rect_points is not None and len(rect_points) == 4:
            # Convert rect_points to NumPy array of integers
            pts = np.array([(point.x, point.y) for point in rect_points], dtype=np.int32)
            
            cv2.polylines(image, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

            # Calculate the center of the QR code
            center = np.mean(pts, axis=0)

            # Calculate the rotation of the QR code
            rect = cv2.minAreaRect(pts)
            angle = rect[-1]

            # Print the coordinates of the center and rotation angle
            print(f"QR Code Center Coordinates: {center}")
            print(f"QR Code Rotation Angle: {angle} degrees")

    # Display the image with the detected QR codes
    cv2.imshow("QR Code Reader", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Provide the path to the image containing the QR code
image_path = r"C:\Users\LuisC\Desktop\githubProjects\DTech-Alfred\Code\Test Code\Camera\tiltedAll.png"
read_qr_code(image_path)
