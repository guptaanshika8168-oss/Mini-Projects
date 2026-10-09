
import tkinter as tk

FOCUS_TIME = 25 * 60
BREAK_TIME = 5 * 60

time_left = FOCUS_TIME
is_running = False
is_break = False
sessions = 0
timer_id = None

def update_display():
    minutes = time_left // 60
    seconds = time_left % 60
    timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

def countdown():
    global time_left, is_running, is_break, sessions, timer_id

    update_display()

    if time_left > 0:
        time_left -= 1
        timer_id = root.after(1000, countdown)
    else:
        is_running = False
        timer_id = None

        if not is_break:
            sessions += 1
            session_label.config(text=f"Sessions completed: {sessions}")
            is_break = True
            time_left = BREAK_TIME
            status_label.config(text="Break time! ☕")
        else:
            is_break = False
            time_left = FOCUS_TIME
            status_label.config(text="Time to focus! 📚")

        update_display()

def start_timer():
    global is_running

    if not is_running:
        is_running = True
        countdown()

def pause_timer():
    global is_running, timer_id

    is_running = False

    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None

def reset_timer():
    global time_left, is_running, is_break, timer_id

    pause_timer()
    time_left = BREAK_TIME if is_break else FOCUS_TIME
    status_label.config(
        text="Break time! ☕" if is_break else "Time to focus! 📚"
    )
    update_display()

root = tk.Tk()
root.title("Pomodoro Timer")
root.geometry("350x350")
root.configure(bg="#FCE7EF")

title_label = tk.Label(
    root, text="Pomodoro Timer 🍅",
    font=("Arial", 20, "bold"),
    bg="#FCE7EF", fg="#8E4A68"
)
title_label.pack(pady=15)

status_label = tk.Label(
    root, text="Time to focus! 📚",
    font=("Arial", 13),
    bg="#FCE7EF", fg="#8E4A68"
)
status_label.pack(pady=5)

timer_label = tk.Label(
    root, text="25:00",
    font=("Arial", 42, "bold"),
    bg="#FCE7EF", fg="#8E4A68"
)
timer_label.pack(pady=15)

button_frame = tk.Frame(root, bg="#FCE7EF")
button_frame.pack(pady=10)

tk.Button(
    button_frame, text="Start",
    command=start_timer, width=8
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame, text="Pause",
    command=pause_timer, width=8
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame, text="Reset",
    command=reset_timer, width=8
).grid(row=0, column=2, padx=5)

session_label = tk.Label(
    root, text="Sessions completed: 0",
    font=("Arial", 12),
    bg="#FCE7EF", fg="#8E4A68"
)
session_label.pack(pady=15)

root.mainloop()
