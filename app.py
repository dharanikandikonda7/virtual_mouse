import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

process = None  # Global variable to store the subprocess


def start_finalvm():
    global process
    if process is None:
        # Ask for camera permission
        if not messagebox.askyesno("Camera Permission", "Allow camera access to start?"):
            return
        # Run finalvm.py as a separate process
        process = subprocess.Popen([sys.executable, "finalvm.py"], cwd=os.getcwd())
    else:
        messagebox.showinfo("Already Running", "Virtual Gesture Controller is already running.")


def stop_finalvm():
    global process
    if process:
        process.terminate()  # Stop the subprocess
        process = None
        messagebox.showinfo("Stopped", "Virtual Gesture Controller stopped.")
    else:
        messagebox.showinfo("Not Running", "Virtual Gesture Controller is not running.")


def exit_app():
    stop_finalvm()
    root.destroy()


# ---------------- GUI ----------------
root = tk.Tk()
root.title("Virtual Gesture Controller GUI")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(root, text="Virtual Gesture Controller", font=("Arial", 18, "bold")).pack(pady=30)

tk.Button(root, text="Start", font=("Arial", 14),
          width=15, bg="green", fg="white",
          command=start_finalvm).pack(pady=15)

tk.Button(root, text="Stop", font=("Arial", 14),
          width=15, bg="orange", fg="white",
          command=stop_finalvm).pack(pady=15)

tk.Button(root, text="Exit", font=("Arial", 14),
          width=15, bg="red", fg="white",
          command=exit_app).pack(pady=15)

root.mainloop()
