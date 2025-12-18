import tkinter as tk
from tkinter import messagebox
import threading

# ---------------- BACKEND IMPORTS ----------------
import cv2
import numpy as np
import pyautogui
import math
from cvzone.HandTrackingModule import HandDetector
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# ---------------- GLOBAL CONTROL ----------------
running = False

# ---------------- HUD DRAW FUNCTION ----------------
def draw_hud(img, text, x, y, color=(0, 255, 0)):
    overlay = img.copy()
    (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)

    cv2.rectangle(
        overlay,
        (x - 10, y - h - 15),
        (x + w + 10, y + 5),
        (0, 0, 0),
        -1
    )

    cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)

    cv2.putText(
        img,
        text,
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2
    )

# ---------------- SIDEBAR PANEL ----------------
def draw_sidebar(img, mode, brightness, volume):
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (220, 480), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)

    draw_hud(img, "STATUS PANEL", 20, 40, (0, 255, 255))
    draw_hud(img, f"Mode: {mode}", 20, 90)
    draw_hud(img, f"Brightness: {brightness}%", 20, 140, (255, 200, 0))
    draw_hud(img, f"Volume: {volume}%", 20, 190, (100, 100, 255))

# ---------------- BACKEND ----------------
def start_gesture_controller():
    global running
    running = True

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Camera permission denied.")
        running = False
        return

    detector = HandDetector(detectionCon=0.85, maxHands=2)

    cam_w, cam_h = 640, 480
    cap.set(3, cam_w)
    cap.set(4, cam_h)

    screen_w, screen_h = pyautogui.size()

    box_w, box_h = 500, 300
    box_x = (cam_w - box_w) // 2
    box_y = (cam_h - box_h) // 2

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_control = cast(interface, POINTER(IAudioEndpointVolume))

    def get_distance(p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    mode = "Idle"
    brightness = 0
    volume = 0

    while running:
        success, img = cap.read()
        if not success:
            continue

        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        # Gesture Box
        cv2.rectangle(img, (box_x, box_y), (box_x + box_w, box_y + box_h), (0, 255, 0), 2)
        draw_hud(img, "Gesture Box", box_x + 10, box_y - 10)

        mode = "Idle"

        if hands:
            if len(hands) == 1:
                hand = hands[0]
                lmList = hand["lmList"]
                fingers = detector.fingersUp(hand)

                ind_x, ind_y = lmList[8][:2]
                mid_x, mid_y = lmList[12][:2]

                # Mouse Move
                if fingers == [1, 1, 1, 0, 0]:
                    if box_x <= ind_x <= box_x + box_w and box_y <= ind_y <= box_y + box_h:
                        screen_x = np.interp(ind_x, [box_x, box_x + box_w], [0, screen_w])
                        screen_y = np.interp(ind_y, [box_y, box_y + box_h], [0, screen_h])
                        pyautogui.moveTo(screen_x, screen_y)
                        mode = "Mouse Move"

                # Scroll Down
                elif fingers == [0, 1, 1, 0, 0]:
                    pyautogui.scroll(-20)
                    mode = "Scroll Down"

                # Scroll Up
                elif fingers == [0, 1, 1, 0, 1]:
                    pyautogui.scroll(20)
                    mode = "Scroll Up"

            elif len(hands) == 2:
                hand1, hand2 = hands
                left = hand1 if hand1["type"] == "Left" else hand2
                right = hand2 if left == hand1 else hand1

                lmL = left["lmList"]
                lmR = right["lmList"]

                brightness = int(np.interp(get_distance(lmL[4], lmL[8]), [30, 200], [0, 100]))
                sbc.set_brightness(brightness)

                volume = int(np.interp(get_distance(lmR[4], lmR[8]), [30, 200], [0, 100]))
                volume_control.SetMasterVolumeLevelScalar(volume / 100, None)

                mode = "Brightness / Volume"

        # Sidebar + HUD
        draw_sidebar(img, mode, brightness, volume)
        draw_hud(img, "Use APP Exit button to quit", 240, 30, (0, 0, 255))

        cv2.imshow("Virtual Gesture Controller", img)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()

# ---------------- FRONTEND ----------------
def start_app():
    if messagebox.askyesno("Camera Permission", "Allow camera access to start?"):
        threading.Thread(target=start_gesture_controller, daemon=True).start()

def exit_app():
    global running
    running = False
    root.destroy()

root = tk.Tk()
root.title("Virtual Gesture Controller")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(root, text="Virtual Gesture Controller", font=("Arial", 18, "bold")).pack(pady=30)

tk.Button(root, text="Start", font=("Arial", 14),
          width=15, bg="green", fg="white",
          command=start_app).pack(pady=15)

tk.Button(root, text="Exit", font=("Arial", 14),
          width=15, bg="red", fg="white",
          command=exit_app).pack(pady=15)

root.mainloop()
