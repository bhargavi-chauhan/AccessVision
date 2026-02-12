# Real-time YOLO detection

# Direction awareness (left / center / right)

# Distance estimation (far → very close)

# Scene change narration

# Speech cooldown control

# Smooth webcam performance
# -------------------------------


import cv2
import time
import subprocess
from ultralytics import YOLO

# ---------------- CONFIG ----------------

important_objects = ["person", "chair", "bottle", "car"]
confidence_threshold = 0.5
speech_cooldown = 2  # seconds between speeches

far_threshold = 0.02
medium_threshold = 0.06
near_threshold = 0.12
emergency_threshold = 0.20

# ----------------------------------------

model = YOLO("yolov8n.pt")
model.fuse()

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Webcam error")
    exit()

print("Press 'q' to quit")

last_scene_signature = ""
last_spoken_time = 0

# ---------------- WINDOWS SPEECH ----------------

def speak(text):
    command = f'''
    Add-Type -AssemblyName System.Speech;
    $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    $speak.Rate = 1;
    $speak.Speak("{text}");
    '''
    subprocess.Popen(["powershell", "-Command", command],
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)

# ---------------- MAIN LOOP ----------------

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_h, frame_w, _ = frame.shape
    frame_area = frame_h * frame_w

    results = model(frame, verbose=False)
    result = results[0]

    scene_descriptions = []

    if result.boxes is not None:
        for box in result.boxes:
            conf = float(box.conf[0])
            if conf < confidence_threshold:
                continue

            class_id = int(box.cls[0])
            class_name = result.names[class_id]

            if class_name not in important_objects:
                continue

            x1, y1, x2, y2 = box.xyxy[0]
            box_area = float((x2 - x1) * (y2 - y1))
            area_ratio = box_area / frame_area

            center_x = (x1 + x2) / 2

            # Direction
            if center_x < frame_w / 3:
                direction = "left"
            elif center_x > frame_w * 2 / 3:
                direction = "right"
            else:
                direction = "center"

            # Distance
            if area_ratio > emergency_threshold:
                distance = "very close"
            elif area_ratio > near_threshold:
                distance = "near"
            elif area_ratio > medium_threshold:
                distance = "at medium distance"
            else:
                distance = "far"

            description = f"{class_name} on your {direction} {distance}"
            scene_descriptions.append(description)

    # Remove duplicates
    scene_descriptions = list(set(scene_descriptions))

    if scene_descriptions:
        sentence = "I see " + " and ".join(scene_descriptions) + "."
    else:
        sentence = "I cannot see anything important."

    print("Scene:", sentence)

    current_time = time.time()

    # Speak if scene meaningfully changed
    if sentence != last_scene_signature and (current_time - last_spoken_time) > speech_cooldown:
        speak(sentence)
        last_scene_signature = sentence
        last_spoken_time = current_time

    annotated = result.plot()
    cv2.imshow("AccessVision - Smart Mode", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
