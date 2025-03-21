import cv2
from ultralytics import YOLO
import csv
import os

# MODEL DECLARATION
digit_model = YOLO('./model/best.pt')

# LOAD VIDEO
cap = cv2.VideoCapture('./assets/stopwatch_test_2.mp4')

# READ FRAMES
ret = True
frame_number = -1
time_detected = []
time_per_frame = []

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

frame_number = -1
change_count = 0
ret, frame = cap.read()

frame_path = 'frames'

while ret:
    frame_number += 1
        
    detections = digit_model(frame)[0]
    time_per_frame = []
    
    for detection in sorted(detections.boxes.data.tolist(), key=lambda x: x[0]):
        x1, y1, x2, y2, score, class_id = detection
        
        time_per_frame.append(mapping[int(class_id)])

    maxlen = 5

    # Pastikan panjang time_per_frame sesuai dengan apa yang Anda butuhkan
    if len(time_per_frame) != maxlen:
        continue
    print(time_per_frame)
    if frame_number > 1:
        if time_per_frame == time_detected[-1][1] and time_per_frame != ['0', '0', '0', '0', '0']:
            change_count += 1
        else:
            change_count = 0
            
        if change_count > 5:
            cv2.imwrite('./frames/last_frame.jpg', frame)
            ret = False

    # Simpan informasi ke dalam variabel atau struktur data yang sesuai
    time_detected.append([frame_number,time_per_frame])
    
formatted_time = f"{time_detected[-1][1][0]}:{time_detected[-1][1][1]}{time_detected[-1][1][2]}:{time_detected[-1][1][3]}{time_detected[-1][1][4]}"

# Nama file CSV
csv_file = "./result/result.csv"

# Menuliskan formatted_time ke dalam file CSV
if os.path.isfile(csv_file) and os.path.getsize(csv_file) > 0:
    # Jika file CSV tidak kosong, gunakan mode 'a' untuk append
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([formatted_time])
else:
    # Jika file CSV kosong, gunakan mode 'w' untuk menulis dari awal
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([formatted_time])
