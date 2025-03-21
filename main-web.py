# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import csv
import os
from ultralytics import YOLO
import base64
import numpy as np
import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)
socketio = SocketIO(app)


def decode_image(img_data):
    # Pisahkan tipe MIME dan data gambar dari URL
    img_data_url_parts = img_data.split(',')
    # Contoh: 'data:image/jpeg;base64'
    img_data_mime_type = img_data_url_parts[0]

    # Ambil data gambar yang diencoded dalam base64
    img_data_base64 = img_data_url_parts[1]

    # Dekode data base64 ke bentuk biner
    img_data_binary = base64.b64decode(img_data_base64)

    # Baca data biner menggunakan OpenCV
    img_array = np.frombuffer(img_data_binary, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    return img


@socketio.on('connect')
def handle_connect():
    print('Client connected to the stream')


change_count = 0
time_detected = [['0', '0', '0', '0', '0']]
foto = 0


@socketio.on('stream')
def handle_stream(img_data):
    global change_count, time_detected, foto

    # print('Received image data', img_data[:50])

    # MODEL DECLARATION
    source_path = './model/best.pt'
    screen_model_source_path = './model/kotak_stopwatch.pt'
    digit_model = YOLO(source_path)
    screen_model = YOLO(screen_model_source_path)

    mapping = {
        0: '-',
        1: '.',
        2: '0',
        3: '1',
        4: '2',
        5: '3',
        6: '4',
        7: '5',
        8: '6',
        9: '7',
        10: '8',
        11: '9',
        12: 'D'
    }

    frame = decode_image(img_data)

    # Process the frame using YOLO model

    time_per_frame = []

    detection_screen = screen_model(frame)[0]

    for screen in detection_screen.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = screen
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        screen_frame = frame[y1:y2, x1:x2]

        detections = digit_model(screen_frame)[0]

        for detection in sorted(detections.boxes.data.tolist(), key=lambda x: x[0]):
            x1, y1, x2, y2, score, class_id = detection
            print(f"Class ID: {class_id}")
            print(f"Detection: {mapping[int(class_id)]}")
            time_per_frame.append(mapping[int(class_id)])

        maxlen = 5

        if len(time_per_frame) == maxlen:
            if time_per_frame == time_detected[-1] and time_per_frame != ['0', '0', '0', '0', '0']:
                change_count += 1
                if change_count == 3:
                    print("SAVE SUCCESSFULLY")
                    time_per_frame = []
                    formatted_time = f"{time_detected[-1][0]}:{time_detected[-1][1]}{time_detected[-1][2]}:{time_detected[-1][3]}{time_detected[-1][4]}"
                    csv_file = "./result/result.csv"
                    save_path = "./frames"
                    photo_files = [file for file in os.listdir(
                        save_path) if file.endswith('.jpg')]
                    photo_length = len(photo_files)
                    new_filename = f'{photo_length + 1}.jpg'
                    cv2.imwrite(os.path.join(
                        './frames', new_filename), screen_frame)

                    with open(csv_file, mode='a+', newline='') as file:
                        if os.path.getsize(csv_file) == 0:
                            # If the CSV file is empty, use mode 'w' to write from scratch
                            writer = csv.writer(file)
                            writer.writerow([photo_length + 1, formatted_time])
                            foto += 1
                        else:
                            # If the CSV file is not empty, use mode 'a' to append
                            writer = csv.writer(file)
                            writer.writerow([photo_length + 1, formatted_time])
                            foto += 1
            elif time_per_frame == ['0', '0', '0', '0', '0']:
                print("RESET")
                change_count = 0

            time_detected.append(time_per_frame)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)
