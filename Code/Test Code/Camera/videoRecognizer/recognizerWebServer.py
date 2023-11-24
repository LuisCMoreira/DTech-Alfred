

import cv2
import numpy as np
import time

# Load pre-trained MobileNet SSD model
net = cv2.dnn.readNetFromCaffe(
    r'C:\Users\LuisC\Desktop\githubProjects\DTech-Alfred\Code\Test Code\Camera\MobileNetSSD_deploy.prototxt',
    r'C:\Users\LuisC\Desktop\githubProjects\DTech-Alfred\Code\Test Code\Camera\MobileNetSSD_deploy.caffemodel'
)

# Define classes for detection
classes = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor", "hand", "door"]

# Set the camera index (0 for default camera)
camera_index = 0
cap = cv2.VideoCapture(camera_index)

while True:
    try:
        # Capture a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture a frame. Exiting...")
            break

        # Resize the frame to a fixed width for faster processing
        frame = cv2.resize(frame, (300, 300))

        # Convert the frame to a blob
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)

        # Set the input to the network
        net.setInput(blob)

        # Run forward pass to get the detections
        detections = net.forward()

        # Loop over the detections
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            # Filter out detections with confidence lower than 75%
            if confidence > 0.75:
                class_id = int(detections[0, 0, i, 1])

                # Get the coordinates of the bounding box
                box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (startX, startY, endX, endY) = box.astype(int)

                # Draw the bounding box and label on the frame
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                label = f"{classes[class_id]}: {confidence:.2f}"
                cv2.putText(frame, label, (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save a snapshot every second
        time.sleep(0.2)
        snapshot_filename = f"snapshot.jpg"
        cv2.imwrite(snapshot_filename, frame)
        print(f"Snapshot saved: {snapshot_filename}")

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except KeyboardInterrupt:
        break

# Release the camera
cap.release()
