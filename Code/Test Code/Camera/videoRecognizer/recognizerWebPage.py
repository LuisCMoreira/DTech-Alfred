from flask import Flask, render_template, send_file
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image')
def get_image():
    # Specify the filename you want to serve
    filename = 'snapshot.jpg'
    image_path = os.path.join(os.getcwd(), filename)

    # Check if the file exists
    if not os.path.exists(image_path):
        return 'No image available'

    return send_file(image_path, mimetype='image/jpeg')

if __name__ == '__main__':
    # Listen on all network interfaces
    app.run(host='0.0.0.0', port=5001, debug=False)
