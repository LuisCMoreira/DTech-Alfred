import time
import picamera
import io
from http.server import BaseHTTPRequestHandler, HTTPServer

class VideoStreamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
            self.end_headers()
            with picamera.PiCamera() as camera:
                camera.resolution = (640, 480)
                camera.framerate = 30
                time.sleep(2)  # Let the camera warm up
                stream = io.BytesIO()
                for _ in camera.capture_continuous(stream, format='jpeg'):
                    self.wfile.write(b'--frame\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(stream.getvalue()))
                    self.end_headers()
                    self.wfile.write(stream.getvalue())
                    stream.seek(0)
                    stream.truncate()
        else:
            self.send_response(404)
            self.end_headers()
            return

def main():
    try:
        server = HTTPServer(('', 80), VideoStreamHandler)
        print('Starting video stream server on port 80...')
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

if __name__ == '__main__':
    main()
