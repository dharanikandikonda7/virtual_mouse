# 🖐️ Virtual Mouse & Gesture-Based System Control

## 🎯 Overview  
This project implements a **Virtual Mouse System** that allows users to interact with their computer using **hand gestures** instead of a physical mouse. Using **OpenCV**, **MediaPipe**, and **system control libraries** like `pyautogui`, `pycaw`, and `screen_brightness_control`, it enables control over:
- **Mouse movement**
- **Left & right clicks**
- **Scrolling**
- **System brightness**
- **System volume**

All operations are performed in **real-time** through webcam input.

> ⚠️ **Note:** There are two ways to run this project:  
> 1. **Directly:** Using `finalvm.py` (full-featured, console/OpenCV window).  
> 2. **GUI Frontend:** Using `app.py` (Tkinter interface). The `app.py` frontend **depends on `finalvm.py`**, so `finalvm.py` must be in the same folder.

---

## ⚙️ Features

| Feature | Gesture | Description |
|----------|----------|-------------|
| 🖱️ **Mouse Movement** | Show thumb, index, and middle fingers | Moves the mouse pointer according to the index finger |
| ⏸️ **Mouse Pause** | Bend middle finger down | Freezes mouse movement |
| 👆 **Left Click** | Bend only index finger | Triggers left click |
| ✌️ **Right Click** | Bend only middle finger | Triggers right click |
| ⬆️ **Scroll Up** | Show index, middle, and pinky fingers up | Scrolls the screen upward |
| ⬇️ **Scroll Down** | Show index and middle fingers up and close together | Scrolls the screen downward |
| 💡 **Brightness Control** | Use **left hand** (thumb & index distance) | Controls screen brightness |
| 🔊 **Volume Control** | Use **right hand** (thumb & index distance) | Controls system volume |
| ❌ **Quit Application** | Press `q` on keyboard | Gracefully exits the program |

---

## ✋ Two-Hand vs One-Hand Logic

- **Single Hand (Right Hand)** → Performs **mouse actions** (move, click, scroll).  
- **Two Hands Visible** → Activates **brightness and volume control**.  
  - **Left Hand:** Adjusts **brightness**.  
  - **Right Hand:** Adjusts **volume**.  
- If only one hand is visible, brightness and volume control **remain disabled** to prevent accidental triggers.

---

## 🧠 How It Works

1. **Hand Detection:**  
   Uses **MediaPipe Hands** to detect hand landmarks in real time.  

2. **Gesture Recognition:**  
   The program interprets the relative positions of fingers (index, middle, thumb) to map them to predefined actions.  

3. **Action Execution:**  
   - **OpenCV** displays live video with feedback.  
   - **pyautogui** handles mouse movement, click, and scroll.  
   - **pycaw** controls system volume.  
   - **screen_brightness_control** adjusts screen brightness.  

> ⚠️ **GUI Frontend (`app.py`)** simply launches `finalvm.py` as a subprocess and provides **Start/Stop controls** along with a basic Tkinter interface.

---

## 🧩 Dependencies

Install all dependencies with:
```bash
pip install -r requirements.txt
