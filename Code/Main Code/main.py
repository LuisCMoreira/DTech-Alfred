
import keyboard
import keyControl
import motionControl
import time
import threading

from qrFinder import run_continuous_qr_code_reader, get_distance_to_qr  # Import the QR code reader function
from snapOutput import app as flask_app  # Import the Flask app

# Lock for protecting shared resources, if needed
motion_control_lock = threading.Lock()


simpleCamera=True

testMode = False
keyMode = True

if simpleCamera:
    from http.server import HTTPServer
    
    # Import the VideoStreamHandler class from your previous code
    from cameraServer import VideoStreamHandler
    
    # Flag to indicate whether the video streaming server is running
    video_streaming_running = False

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



    try:
    
        if simpleCamera:
            # Start the video streaming server in a separate thread
            video_streaming_thread = threading.Thread(target=start_video_stream_server)
            video_streaming_thread.start()
            video_streaming_running = True
        else:
            # Run the QR code reader in a separate thread
            qr_thread = threading.Thread(target=run_continuous_qr_code_reader, args=("./qrimages", (10.0, 10.0), "./snapshots"))
            qr_thread.start()
    
            # Run the Flask server in a separate thread
            flask_thread = threading.Thread(target=flask_app.run, kwargs={'host': '0.0.0.0', 'port': 5001, 'debug': False})
            flask_thread.start()

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



        if simplesCamera:
            # Stop the video streaming server thread
            video_streaming_running = False
            video_streaming_thread.join()
        
        else:

            # Stop the QR code reader thread
            qr_thread.join()
    
            # Stop the Flask server thread
            flask_thread.join()

if __name__ == '__main__':
    main()

