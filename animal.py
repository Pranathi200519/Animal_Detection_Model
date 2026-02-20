import cv2
import numpy as np
import pyttsx3
import time
import os
import requests

# ===========================================
# 🔥 TELEGRAM DETAILS — INSERT YOUR VALUES
# ===========================================
BOT_TOKEN = "<your_bot_token_here>"  # Replace with your bot token
CHAT_ID = "<your_chat_id_here>"  # Replace with your chat ID 

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
TELEGRAM_PHOTO_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

# Load YOLOv3
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# Load COCO class names
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Text-to-Speech engine
engine = pyttsx3.init()

# Animal classes to detect
animal_list = ["cow", "dog", "elephant", "bear", "sheep", "horse"]

# Create folder to save detections
os.makedirs("detections", exist_ok=True)

cap = cv2.VideoCapture(0)

# Per-animal cooldown
last_alert_time = {}
COOLDOWN = 10  # seconds

while True:
    ret, frame = cap.read()
    height, width, channels = frame.shape

    # YOLO input
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416),
                                 (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    # Loop through detections
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Count animals
    animal_count = {}

    if len(indexes) > 0:
        for i in indexes.flatten():
            label = str(classes[class_ids[i]])

            if label in animal_list:

                # Counting
                if label not in animal_count:
                    animal_count[label] = 1
                else:
                    animal_count[label] += 1

                # Draw box
                x, y, w, h = boxes[i]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, label.upper(), (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 255, 0), 2)

    # Show counts on screen
    y_pos = 30
    for animal, count in animal_count.items():
        cv2.putText(frame, f"{animal.upper()}: {count}", (10, y_pos),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        y_pos += 30

    # ================================
    # 🔥 ALERT + SAVE + TELEGRAM SEND
    # ================================
    if animal_count:
        for animal, count in animal_count.items():

            if animal not in last_alert_time:
                last_alert_time[animal] = 0

            if time.time() - last_alert_time[animal] > COOLDOWN:

                message = f"{animal.upper()} detected! Count: {count}"
                print(message)

                # Save image
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = f"detections/{animal}_{timestamp}.jpg"
                cv2.imwrite(filename, frame)
                print(f"Image saved: {filename}")

                # Voice alert
                engine.say(message)
                engine.runAndWait()

                # ================================
                # 📤 SEND MESSAGE TO TELEGRAM
                # ================================
                try:
                    requests.post(TELEGRAM_URL, data={
                        "chat_id": CHAT_ID,
                        "text": message
                    })

                    # 📤 SEND PHOTO
                    with open(filename, "rb") as img:
                        requests.post(TELEGRAM_PHOTO_URL, data={
                            "chat_id": CHAT_ID
                        }, files={"photo": img})

                    print("Telegram alert sent!")

                except Exception as e:
                    print("Telegram error:", e)

                last_alert_time[animal] = time.time()

    cv2.imshow("Animal Detection (YOLOv3)", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
