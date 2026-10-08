import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import datetime
import os

print("Initializing SAGE Clinical Care System (Fully Automated Telemetry)...")

# 1. Persistent TTS Worker Process
tts_worker_code = """
import sys
import pyttsx3
for line in sys.stdin:
    phrase = line.strip()
    if not phrase:
        continue
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(phrase)
        engine.runAndWait()
        engine.stop()
        del engine
    except Exception:
        pass
"""

tts_process = None
try:
    kwargs = {}
    if sys.platform == "win32":
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
    tts_process = subprocess.Popen(
        [sys.executable, '-c', tts_worker_code],
        stdin=subprocess.PIPE, text=True, **kwargs
    )
except Exception as e:
    print(f"TTS Worker Error: {e}")

# Shared App State for Telemetry & Dashboard
app_state = {
    "history": [],
    "fatigue_state": "Normal (Low Fatigue)",
    "fatigue_color": "#27ae60",  # Green
    "hardware_status": "ONLINE (Edge Pi 5)",
    "cpu_temp": "41.2 °C",
    "voltage": "5.12 V",
    "fps": "30.0 FPS"
}

def speak_phrase(phrase):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] AAC Output: {phrase}")
    
    # Contextual Clinical Triage Rule (matches phrase + live automated EAR state)
    current_state = app_state["fatigue_state"]
    if phrase in ["Pain", "Help Me"] and "HIGH" in current_state:
        logged_state = "CRITICAL ALERT: Pain + Severe Fatigue"
    elif phrase == "Water" and "MODERATE" in current_state:
        logged_state = "Advisory: Hydration Request under Strain"
    else:
        logged_state = current_state

    # Update Dashboard History with automated clinical state
    app_state["history"].insert(0, (timestamp, phrase, logged_state))
    if len(app_state["history"]) > 20:
        app_state["history"].pop()
    
    # Trigger Speech
    if tts_process and tts_process.stdin:
        try:
            tts_process.stdin.write(phrase + "\n")
            tts_process.stdin.flush()
        except Exception:
            pass

# ==================== WINDOW 1: PATIENT AAC BOARD ====================
root = tk.Tk()
root.title("SAGE - Patient AAC Communication Board")
root.geometry("600x650+50+50")
root.configure(bg="#f0f2f5")

patient_main_frame = tk.Frame(root, bg="#f0f2f5")
patient_main_frame.pack(fill="both", expand=True, padx=15, pady=15)

header_frame = tk.Frame(patient_main_frame, bg="#ffffff", bd=1, relief="solid")
header_frame.pack(fill="x", pady=(0, 10))

title_label = tk.Label(header_frame, text="SAGE Patient Interface", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#1a1a1a")
title_label.pack(side="left", padx=15, pady=12)

status_label = tk.Label(header_frame, text="Status: Gaze Active", font=("Helvetica", 12, "italic"), bg="#ffffff", fg="#27ae60")
status_label.pack(side="right", padx=15, pady=12)

grid_frame = tk.Frame(patient_main_frame, bg="#f0f2f5")
grid_frame.pack(expand=True, fill="both")

phrases = [
    ("Water", "#2980b9"), ("Food", "#27ae60"), ("Pain", "#e74c3c"),
    ("Medicine", "#d35400"), ("Help Me", "#8e44ad"), ("Yes", "#2ecc71"),
    ("No", "#c0392b"), ("Adjust Bed", "#16a085"), ("Call Nurse", "#f39c12"),
    ("Thank You", "#34495e"),
]

for index, (text, color) in enumerate(phrases):
    btn = tk.Button(
        grid_frame, text=text, font=("Helvetica", 14, "bold"),
        bg=color, fg="white", activebackground=color, activeforeground="white",
        relief="flat", cursor="hand2",
        command=lambda p=text: speak_phrase(p)
    )
    btn.grid(row=index // 3, column=index % 3, sticky="nsew", padx=8, pady=8)

for i in range(4):
    grid_frame.grid_rowconfigure(i, weight=1)
for j in range(3):
    grid_frame.grid_columnconfigure(j, weight=1)


# ==================== WINDOW 2: NURSE DASHBOARD ====================
nurse_win = tk.Toplevel(root)
nurse_win.title("SAGE - Nurse Telemetry & Hardware Control Center")
nurse_win.geometry("720x680+680+50")
nurse_win.configure(bg="#f0f2f5")

nurse_main = tk.Frame(nurse_win, bg="#f0f2f5")
nurse_main.pack(fill="both", expand=True, padx=15, pady=15)

# Top Section: Hardware Simulation & Automated Biometrics Panel
hw_frame = tk.LabelFrame(nurse_main, text=" Edge Hardware Telemetry & Automated Biometrics ", font=("Helvetica", 12, "bold"), bg="#ffffff", fg="#2c3e50", padx=15, pady=15)
hw_frame.pack(fill="x", pady=(0, 15))

# Dynamic Label for Automated Fatigue State
lbl_fatigue_val = tk.Label(hw_frame, text=app_state["fatigue_state"], font=("Helvetica", 10, "bold"), bg="#ffffff", fg=app_state["fatigue_color"])

hw_stats = [
    ("Device Status:", "ONLINE (Active)", 0, 0),
    ("Processor Temp:", "41.2 °C (Optimal)", 0, 2),
    ("Core Voltage:", "5.12 V (Stable)", 1, 0),
    ("Vision Pipeline:", "30.0 FPS (Webcam)", 1, 2),
    ("Fatigue Index:", lbl_fatigue_val, 2, 0)
]

for label_text, val_item, r, c in hw_stats:
    lbl_title = tk.Label(hw_frame, text=label_text, font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#555555")
    lbl_title.grid(row=r, column=c, sticky="w", padx=5, pady=6)
    if isinstance(val_item, str):
        lbl_val = tk.Label(hw_frame, text=val_item, font=("Helvetica", 10), bg="#ffffff", fg="#2980b9")
        lbl_val.grid(row=r, column=c+1, sticky="w", padx=5, pady=6)
    else:
        val_item.grid(row=r, column=c+1, sticky="w", padx=5, pady=6)

# Bottom Section: Live Patient Communication Log
log_frame = tk.LabelFrame(nurse_main, text=" Real-Time Patient Output & Request Audit Log ", font=("Helvetica", 12, "bold"), bg="#ffffff", fg="#2c3e50", padx=15, pady=15)
log_frame.pack(fill="both", expand=True)

columns = ("Time", "Requested Phrase", "Patient State")
tree = ttk.Treeview(log_frame, columns=columns, show="headings", height=11)
tree.heading("Time", text="Timestamp")
tree.heading("Requested Phrase", text="Spoken / Selected Phrase")
tree.heading("Patient State", text="Biometric Fatigue State")
tree.column("Time", width=90, anchor="center")
tree.column("Requested Phrase", width=210, anchor="w")
tree.column("Patient State", width=230, anchor="center")
tree.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)

# Automated Background Reader for Webcam Fatigue Telemetry
def update_automated_telemetry():
    if os.path.exists("fatigue_status.txt"):
        try:
            with open("fatigue_status.txt", "r") as f:
                state = f.read().strip()
                if state:
                    app_state["fatigue_state"] = state
                    if "HIGH" in state:
                        app_state["fatigue_color"] = "#c0392b"  # Red
                    elif "MODERATE" in state:
                        app_state["fatigue_color"] = "#d35400"  # Orange
                    else:
                        app_state["fatigue_color"] = "#27ae60"  # Green
                    
                    lbl_fatigue_val.config(text=app_state["fatigue_state"], fg=app_state["fatigue_color"])
        except Exception:
            pass

    # Refresh treeview log
    tree.delete(*tree.get_children())
    for item in app_state["history"]:
        tree.insert("", "end", values=item)
        
    nurse_win.after(500, update_automated_telemetry)

nurse_win.after(500, update_automated_telemetry)

def on_close():
    if tts_process:
        try:
            tts_process.stdin.close()
            tts_process.terminate()
        except Exception:
            pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
nurse_win.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()