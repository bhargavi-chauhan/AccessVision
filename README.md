# AccessVision
Real-Time Context-Aware Object Detection with Voice Feedback. 

## Features:
✅ Real-Time Object Detection using YOLOv8 (Nano model)
✅ Important Object Filtering (person, car, chair, bottle, door)
✅ Scene-Aware Speech Output via Edge-TTS
✅ Non-Blocking Speech (speaks while detecting continuously)
✅ Stable Detection (requires objects to remain in frame for multiple frames)
✅ Distance Estimation (far / medium / near / very close) using bounding box area
✅ Direction Detection (left / center / right)
✅ Scene Change Detection (speaks only when scene changes significantly)
✅ No Repetitive Speech
✅ No Webcam Freezing or delays during detection

## Requirements:
1. Python: 3.12
2. Libraries:
  ```bash
  pip install ultralytics opencv-python torch torchvision edge-tts playsound
  ```
4. Hardware -> Webcam

## Setup:
1️⃣ Clone or download the repository.
2️⃣ Install required Python packages (see above).
3️⃣ Ensure your webcam is connected.
4️⃣ Run the main script:
   ```bash
   python main.py
   ```

## Usage:
1. Once the script starts, the webcam opens.
2. AccessVision detects objects in real-time.
3. When objects appear, move, or disappear, the system speaks a contextual sentence.
4. Press q to quit the program.
