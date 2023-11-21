'''
import keyControl
import motionControl
import time
from cameraServer import VideoStreamHandler
import threading


def main():
    # Your main script logic here
    print("This is the main script.")



    # Start the video stream server in a separate thread
    video_thread = threading.Thread(target=VideoStreamHandler)
    video_thread.start()

    testMode = False
    keyMode = True

    try:
        while True:
            if keyMode:
                keyControl.keyBoardCommand()

            if testMode:
                motionControl.moveL(0.34)
                time.sleep(10)
                motionControl.moveSTOP()
                time.sleep(5)

    except KeyboardInterrupt:
        print("end")
        motionControl.motorRT.cleanup()
        motionControl.motorLF.cleanup()

if __name__ == '__main__':
    main()


'''

import keyControl
import motionControl
import time
import threading
from http.server import HTTPServer

# Import the VideoStreamHandler class from your previous code
from cameraServer import VideoStreamHandler

# Flag to indicate whether the video streaming server is running
video_streaming_running = False

# Lock for protecting shared resources, if needed
motion_control_lock = threading.Lock()

def start_video_stream_server():
    global video_streaming_running
    try:
        server = HTTPServer(('', 80), VideoStreamHandler)
        print('Starting video stream server on port 80...')
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()
        video_streaming_running = False

def main():
    print("This is the main script.")

    testMode = False
    keyMode = True

    # Start the video streaming server in a separate thread
    video_streaming_thread = threading.Thread(target=start_video_stream_server)
    video_streaming_thread.start()
    video_streaming_running = True

    try:
        while True:
            if keyMode:
                keyControl.keyBoardCommand()

            if testMode:
                # Acquire the lock before calling motion control functions
                with motion_control_lock:
                    motionControl.moveL(0.34)
                time.sleep(10)
                with motion_control_lock:
                    motionControl.moveSTOP()
                time.sleep(5)

    except KeyboardInterrupt:
        print("End")

        # Acquire the lock before calling cleanup operations
        with motion_control_lock:
            motionControl.motorRT.cleanup()
            motionControl.motorLF.cleanup()

        # Stop the video streaming server thread
        video_streaming_running = False
        video_streaming_thread.join()

if __name__ == '__main__':
    main()


