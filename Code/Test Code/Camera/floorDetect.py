import cv2
import numpy as np

# Set the lower and upper bounds of the color range for the floor (adjust these values)
lower_floor_color = np.array([90, 90, 90])
upper_floor_color = np.array([150, 150, 150])

# Set the camera index (0 for default camera)
camera_index = 0
cap = cv2.VideoCapture(camera_index)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Resize the frame to a fixed width for faster processing
    frame = cv2.resize(frame, (300, 300))

    # Convert the frame from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask based on the defined color range for the floor
    mask = cv2.inRange(hsv, lower_floor_color, upper_floor_color)

    # Bitwise AND to get the result within the color range
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Display the original frame and the result
    cv2.imshow("Original Frame", frame)
    cv2.imshow("Floor Detection", result)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
