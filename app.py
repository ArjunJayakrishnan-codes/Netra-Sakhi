from flask import Flask, render_template, Response
import cv2
from utils.yolo_model import load_model
from utils.tts import speak
import time

app = Flask(__name__)
model = load_model()
cap = cv2.VideoCapture(0)
spoken = {}
COOLDOWN = 5  # seconds

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            results = model(frame)[0]
            now = time.time()
            for box in results.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]
                if label not in spoken or now - spoken[label] > COOLDOWN:
                    speak(f"I see a {label}")
                    spoken[label] = now

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
