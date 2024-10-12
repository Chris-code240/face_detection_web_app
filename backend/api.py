from flask import Flask, Response
from flask_cors import CORS
import cv2
from mtcnn import MTCNN

#Initialize a flask app
app = Flask(__name__)


CORS(app)  # To allow cross origin for the frontend

# Initialize an instance of MTCNN
detector = MTCNN()

# Get capture source, in this case the webcam
cap = cv2.VideoCapture(0)

def generate_frames():
    frame_count = 0
    while True:
        success, frame = cap.read()  # Read frame from webcam
        if not success:
            break

        # MTCNN expects RGB, the frame is therefore converted to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform face detection
        #Instead of analyzing single frame, for covenience, lets use those at `multiples-of-5` position
        if frame_count % 5 == 0: 
            faces = detector.detect_faces(rgb_frame)
        frame_count += 1

        # Draw bounding boxes and key points on the frame
        for face in faces:
            x, y, width, height = face['box']
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)

            keypoints = face['keypoints']
            #Put red dots on eyes, nose, and mouth
            cv2.circle(frame, keypoints['left_eye'], 5, (0, 0, 255), -1)
            cv2.circle(frame, keypoints['right_eye'], 5, (0, 0, 255), -1)
            cv2.circle(frame, keypoints['nose'], 5, (0, 0, 255), -1)
            cv2.circle(frame, keypoints['mouth_left'], 5, (0, 0, 255), -1)
            cv2.circle(frame, keypoints['mouth_right'], 5, (0, 0, 255), -1)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame to be sent to the client
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
