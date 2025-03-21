import cv2
import csv
import os
from ultralytics import YOLO


def get_available_cameras():
    available_cameras = []
    for i in range(10):  # Try up to 10 camera indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    return available_cameras


def select_camera():
    available_cameras = get_available_cameras()
    if not available_cameras:
        print("No cameras found.")
        return -1

    print("Select the camera you want to use:")
    for i, camera in enumerate(available_cameras):
        print(f"{i + 1}. Camera {camera}")

    while True:
        choice = int(input("Enter the camera number: "))
        if 1 <= choice <= len(available_cameras):
            return available_cameras[choice - 1]
        else:
            print("Invalid choice. Please select a valid camera number.")


def format_time(time_str):
    if not (len(time_str) == 8 or len(time_str) == 9) or not time_str.isdigit():
        raise ValueError("Input should be a string of 7 or 8 digits.")

    if len(time_str) == 8:
        hours = time_str[0]
        minutes = time_str[1:3]
        seconds = time_str[3:5]
        milliseconds = time_str[5:]
    else:
        hours = time_str[0]
        minutes = time_str[1:3]
        seconds = time_str[3:5]
        milliseconds = time_str[5:]

    if len(time_str) == 9:
        formatted_time = f"{hours.zfill(1)}:{minutes.zfill(2)}:{seconds.zfill(2)}:{milliseconds.zfill(3)}"

    return formatted_time


def detect_numbers(frame, digit_model, screen_model, mapping, change_counts, time_detected, foto, names):
    detection_screen = screen_model(frame)[0]
    screen_boxes = detection_screen.boxes.data.tolist()

    # Limit to maximum 2 stopwatch
    for idx, screen in enumerate(screen_boxes[:2], start=1):
        x1, y1, x2, y2, score, class_id = screen
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        print(f"Box {idx} Coordinates: {(x1, y1, x2, y2)}")

        if x1 >= 0 and y1 >= 0 and x2 > x1 and y2 > y1:
            screen_frame = frame[y1:y2, x1:x2]
            time_per_frame = []

            detections = digit_model(screen_frame)[0]
            for detection in sorted(detections.boxes.data.tolist(), key=lambda x: x[0]):
                x1_d, y1_d, x2_d, y2_d, score_d, class_id_d = detection
                if int(class_id_d) in mapping:
                    print(f"Class ID: {class_id_d}")
                    print(f"Detection: {mapping[int(class_id_d)]}")
                    time_per_frame.append(mapping[int(class_id_d)])

            if len(time_per_frame) in [8, 8]:  # Check for 7 or 8 digits
                if time_per_frame == time_detected[-1] and time_per_frame != ['0'] * len(time_per_frame):
                    change_counts[idx] += 1
                    if change_counts[idx] == 3:
                        print(f"SAVE SUCCESSFULLY for Stopwatch {idx}")
                        time_per_frame = []
                        formatted_time = format_time(''.join(time_detected[-1]))
                        csv_file = "./result/result.csv"
                        save_path = "./frames"
                        photo_files = [file for file in os.listdir(save_path) if file.endswith('.jpg')]
                        photo_length = len(photo_files)
                        new_filename = f'{photo_length + 1}.jpg'
                        cv2.imwrite(os.path.join(save_path, new_filename), screen_frame)

                        with open(csv_file, mode='a+', newline='') as file:
                            writer = csv.writer(file)
                            if os.path.getsize(csv_file) == 0:
                                writer.writerow([photo_length + 1, formatted_time, f"Stopwatch {idx}", names[idx-1]])
                                foto += 1
                            else:
                                writer.writerow([photo_length + 1, formatted_time, f"Stopwatch {idx}", names[idx-1]])
                                foto += 1
                elif time_per_frame == ['0'] * len(time_per_frame):
                    print(f"RESET for Stopwatch {idx}")
                    change_counts[idx] = 0
                time_detected.append(time_per_frame)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, names[idx-1], (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return change_counts, time_detected, foto


def main():
    source_path = './model/best.pt'
    screen_model_source_path = './model/kotak_stopwatch.pt'
    digit_model = YOLO(source_path)
    screen_model = YOLO(screen_model_source_path)

    mapping = {
        0: '-', 1: '.', 2: '0', 3: '1', 4: '2', 5: '3',
        6: '4', 7: '5', 8: '6', 9: '7', 10: '8', 11: '9', 12: 'D'
    }

    change_counts = {1: 0, 2: 0}
    # Initialize with 6-digit time
    time_detected = [['0', '0', '0', '0', '0', '0']]
    foto = 0
    names = ["1", "2"]  # Names for Box 1 and Box 2

    camera_index = select_camera()
    if camera_index == -1:
        return

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error opening camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        change_counts, time_detected, foto = detect_numbers(
            frame, digit_model, screen_model, mapping, change_counts, time_detected, foto, names)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
