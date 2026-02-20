# *Animal Detection Model* 

## 📌 Overview

This project implements a **real-time Animal Intrusion Detection System** using YOLOv3 for object detection. The system detects specific animals through a live camera feed and automatically triggers alerts via voice notification and Telegram messaging.

The application is designed for surveillance scenarios such as farms, rural properties, or restricted areas where animal intrusion may cause damage or safety concerns.

---

## 🚀 Key Features

- 🎥 Real-time object detection using YOLOv3
- 🐄 Detects selected animals (cow, dog, elephant, bear, sheep, horse)
- 🔊 Voice alert using Text-to-Speech (pyttsx3)
- 📸 Automatic image capture on detection
- 📤 Telegram message and photo alerts
- ⏳ Cooldown mechanism to prevent alert spamming
- 📁 Automatic storage of detected images

---

## 🏗️ System Architecture

### 1️⃣ Object Detection
- Uses **YOLOv3 (You Only Look Once)** model
- Pre-trained on COCO dataset
- Processes webcam input in real-time
- Applies Non-Max Suppression (NMS) for accurate bounding boxes

### 2️⃣ Animal Filtering
Only specific animal classes are monitored:
- Cow
- Dog
- Elephant
- Bear
- Sheep
- Horse

### 3️⃣ Alert Mechanism

When an animal is detected:

- The frame is saved locally
- A voice alert is generated
- A Telegram message is sent
- The detected image is sent via Telegram
- A cooldown timer prevents repeated alerts within 10 seconds

---

## 📡 Telegram Integration

The system integrates with the Telegram Bot API to:

- Send detection alerts
- Share captured intrusion images
- Provide remote monitoring capability

⚠️ Sensitive credentials such as `BOT_TOKEN` and `CHAT_ID` must be stored securely (e.g., environment variables).

---

## 🛠️ Technologies Used

- Python
- OpenCV (cv2)
- YOLOv3
- NumPy
- pyttsx3 (Text-to-Speech)
- Telegram Bot API
- Requests library

---

## 📂 Project Structure

- `animal.py` – Main detection and alert system
- `test_telegram.py` – Telegram message test script
- `yolov3.cfg` – YOLO configuration file
- `coco.names` – COCO class labels
- `yolov3.weights` – Pre-trained YOLO weights (not included in repo)
- `README.md` – Project documentation

---

## ⚙️ Setup Instructions

1. Install dependencies:
   ```bash
   pip install opencv-python numpy pyttsx3 requests
   ```

2. Download YOLOv3 weights file:<br>
`Place yolov3.weights in project directory`

3. Configure Telegram Bot:<br>
    Replace `BOT_TOKEN`<br>
    Replace `CHAT_ID`
   
4. Run the program:
```python
python animal.py
```

5. Press `q` to exit the application.

---

## Conclusion

This project demonstrates how computer vision and real-time messaging systems can be combined to create a practical, automated surveillance solution. It highlights the use of deep learning models in real-world safety and monitoring applications.
