
import tkinter as tk
from tkinter import messagebox
import math

try:
    import winsound
except ImportError:
    winsound = None

BG = "#F8F3FA"
PINK = "#F5C6D8"
PINK_DARK = "#B85F85"
BLUE = "#D9ECFA"
BLUE_DARK = "#588DB5"
WHITE = "#FFFFFF"
TEXT = "#51445A"
MUTED = "#978A9F"
GREEN = "#BFE3D0"
BORDER = "#EAE0EE"

root = tk.Tk()
root.title("Pomodoro - My Cozy Study Space")
root.geometry("850x760")
root.minsize(720, 700)
root.configure(bg=BG)

focus_minutes = tk.IntVar(value=25)
short_break_minutes = tk.IntVar(value=5)
long_break_minutes = tk.IntVar(value=15)
daily_goal = tk.IntVar(value=4)

mode = "Focus Time"
remaining = 25 * 60
running = False
after_id = None
completed_sessions = 0
total_focus_seconds = 0
current_focus_seconds = 0
long_break_next = False

def format_time(seconds):
    return f"{seconds // 60:02d}:{seconds % 60:02d}"

def current_duration():
    if mode == "Focus Time":
        return max(1, focus_minutes.get()) * 60
    if mode == "Short Break":
        return max(1, short_break_minutes.get()) * 60
    return max(1, long_break_minutes.get()) * 60

def play_sound():
    try:
        if winsound:
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        else:
            root.bell()
    except Exception:
        pass

def notify(title, text):
    play_sound()
    try:
        root.attributes("-topmost", True)
        root.after(700, lambda: root.attributes("-topmost", False))
    except Exception:
        pass
    messagebox.showinfo(title, text, parent=root)

def update_ring():
    duration = current_duration()
    progress = max(0, min(1, remaining / duration))

    timer_canvas.delete("all")

    timer_canvas.create_oval(
        28, 28, 252, 252,
        outline=BLUE, width=15
    )

    ring_color = PINK_DARK if mode == "Focus Time" else BLUE_DARK

    timer_canvas.create_arc(
        28, 28, 252, 252,
        start=90,
        extent=-360 * progress,
        style="arc",
        outline=ring_color,
        width=15
    )

    timer_canvas.create_text(
        140, 102,
        text=mode,
        fill=TEXT,
        font=("Arial", 14, "bold")
    )

    timer_canvas.create_text(
        140, 145,
        text=format_time(remaining),
        fill=TEXT,
        font=("Arial", 32, "bold")
    )

    timer_canvas.create_text(
        140, 180,
        text="YOU'VE GOT THIS!",
        fill=MUTED,
        font=("Arial", 9, "bold")
    )

def update_dashboard():
    session_label.config(
        text=f"{completed_sessions} / {max(1, daily_goal.get())}"
    )

    goal = max(1, daily_goal.get())
    progress = min(1, completed_sessions / goal)

    goal_canvas.delete("all")
    goal_canvas.create_rectangle(
        0, 0, 300, 12,
        fill=BLUE, outline=""
    )
    if progress > 0:
        goal_canvas.create_rectangle(
            0, 0, 300 * progress, 12,
            fill=PINK_DARK, outline=""
        )

    minutes = total_focus_seconds // 60
    hours = minutes // 60
    mins = minutes % 60

    study_label.config(text=f"{hours}h {mins:02d}m")
    remaining_goal_label.config(
        text="Daily goal completed! Great job!"
        if completed_sessions >= goal
        else f"{goal - completed_sessions} more session(s) to reach your goal"
    )

def set_mode(new_mode):
    global mode, remaining, current_focus_seconds

    mode = new_mode
    remaining = current_duration()
    current_focus_seconds = 0

    if mode == "Focus Time":
        status_label.config(
            text="Time to focus. One step at a time.",
            fg=PINK_DARK
        )
        root.configure(bg=BG)
    elif mode == "Short Break":
        status_label.config(
            text="Take a breath. You earned a little break!",
            fg=BLUE_DARK
        )
    else:
        status_label.config(
            text="Long break time. Rest and recharge!",
            fg=BLUE_DARK
        )

    update_ring()

def finish_session():
    global completed_sessions, total_focus_seconds
    global running, after_id, long_break_next

    running = False
    after_id = None

    if mode == "Focus Time":
        completed_sessions += 1
        total_focus_seconds += current_focus_seconds
        update_dashboard()

        if completed_sessions % 4 == 0:
            next_mode = "Long Break"
        else:
            next_mode = "Short Break"

        set_mode(next_mode)
        notify(
            "Focus session complete!",
            f"Lovely work! You completed {completed_sessions} focus session(s).\n\n"
            f"Time for your {next_mode.lower()}."
        )
    else:
        set_mode("Focus Time")
        notify(
            "Break finished!",
            "Hope you feel refreshed!\n\nLet's get back to focusing."
        )

    start_button.config(text="Start Focus" if mode == "Focus Time" else "Start Break")

def tick():
    global remaining, after_id, running, current_focus_seconds

    after_id = None

    if not running:
        return

    if remaining <= 0:
        finish_session()
        return

    if mode == "Focus Time":
        current_focus_seconds += 1

    remaining -= 1
    update_ring()

    after_id = root.after(1000, tick)

def start_timer():
    global running, after_id

    if running:
        return

    running = True
    start_button.config(text="Running...")
    tick()

def pause_timer():
    global running, after_id

    running = False

    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None

    start_button.config(text="Resume" if remaining < current_duration() else "Start")
    update_ring()

def reset_timer():
    global running, after_id, remaining, current_focus_seconds

    running = False

    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None

    remaining = current_duration()
    current_focus_seconds = 0

    start_button.config(
        text="Start Focus" if mode == "Focus Time" else "Start Break"
    )
    update_ring()

def skip_session():
    global running, after_id

    pause_timer()

    if mode == "Focus Time":
        next_mode = (
            "Long Break" if (completed_sessions + 1) % 4 == 0
            else "Short Break"
        )
    else:
        next_mode = "Focus Time"

    set_mode(next_mode)
    start_button.config(
        text="Start Focus" if mode == "Focus Time" else "Start Break"
    )

def apply_settings():
    global remaining

    if running:
        messagebox.showwarning(
            "Timer running",
            "Please pause the timer before changing settings.",
            parent=root
        )
        return

    try:
        values = [
            focus_minutes.get(),
            short_break_minutes.get(),
            long_break_minutes.get(),
            daily_goal.get()
        ]

        if any(v < 1 for v in values):
            raise ValueError

        if any(v > 180 for v in values[:3]) or values[3] > 100:
            raise ValueError

    except (ValueError, tk.TclError):
        messagebox.showerror(
            "Invalid settings",
            "Durations must be 1–180 minutes and the daily goal must be 1–100.",
            parent=root
        )
        return

    remaining = current_duration()
    update_ring()
    update_dashboard()
    start_button.config(
        text="Start Focus" if mode == "Focus Time" else "Start Break"
    )

def make_button(parent, text, command, bg, fg=TEXT):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=WHITE,
        activeforeground=TEXT,
        font=("Arial", 10, "bold"),
        relief="flat",
        bd=0,
        padx=15,
        pady=10,
        cursor="hand2"
    )

header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=30, pady=(20, 8))

tk.Label(
    header,
    text="my cozy study space",
    font=("Arial", 24, "bold"),
    bg=BG,
    fg=TEXT
).pack()

tk.Label(
    header,
    text="small steps, lovely progress",
    font=("Arial", 11),
    bg=BG,
    fg=MUTED
).pack(pady=(4, 0))

main = tk.Frame(root, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
main.pack(fill="x", padx=35, pady=12)

timer_canvas = tk.Canvas(
    main,
    width=280,
    height=280,
    bg=WHITE,
    highlightthickness=0
)
timer_canvas.pack(pady=(18, 0))

status_label = tk.Label(
    main,
    text="Time to focus. One step at a time.",
    font=("Arial", 11),
    bg=WHITE,
    fg=PINK_DARK
)
status_label.pack(pady=5)

controls = tk.Frame(main, bg=WHITE)
controls.pack(pady=(8, 20))

start_button = make_button(
    controls, "Start Focus", start_timer, PINK, TEXT
)
start_button.grid(row=0, column=0, padx=5)

make_button(
    controls, "Pause", pause_timer, BLUE, TEXT
).grid(row=0, column=1, padx=5)

make_button(
    controls, "Reset", reset_timer, "#F0E6F5", TEXT
).grid(row=0, column=2, padx=5)

make_button(
    controls, "Skip", skip_session, GREEN, TEXT
).grid(row=0, column=3, padx=5)

dashboard = tk.Frame(root, bg=BG)
dashboard.pack(fill="x", padx=35, pady=8)

stats = tk.Frame(dashboard, bg=BG)
stats.pack(fill="x")

session_card = tk.Frame(
    stats, bg=WHITE, highlightbackground=BORDER, highlightthickness=1
)
session_card.pack(side="left", fill="both", expand=True, padx=(0, 7))

tk.Label(
    session_card, text="FOCUS SESSIONS",
    font=("Arial", 9, "bold"), bg=WHITE, fg=MUTED
).pack(pady=(12, 4))

session_label = tk.Label(
    session_card, text="0 / 4",
    font=("Arial", 22, "bold"), bg=WHITE, fg=PINK_DARK
)
session_label.pack(pady=(0, 12))

study_card = tk.Frame(
    stats, bg=WHITE, highlightbackground=BORDER, highlightthickness=1
)
study_card.pack(side="left", fill="both", expand=True, padx=(7, 0))

tk.Label(
    study_card, text="FOCUS TIME",
    font=("Arial", 9, "bold"), bg=WHITE, fg=MUTED
).pack(pady=(12, 4))

study_label = tk.Label(
    study_card, text="0h 00m",
    font=("Arial", 22, "bold"), bg=WHITE, fg=BLUE_DARK
)
study_label.pack(pady=(0, 12))

goal_frame = tk.Frame(
    dashboard, bg=WHITE, highlightbackground=BORDER, highlightthickness=1
)
goal_frame.pack(fill="x", pady=(12, 0))

tk.Label(
    goal_frame, text="YOUR DAILY GOAL",
    font=("Arial", 10, "bold"), bg=WHITE, fg=TEXT
).pack(anchor="w", padx=15, pady=(12, 8))

goal_canvas = tk.Canvas(
    goal_frame, width=300, height=12, bg=WHITE, highlightthickness=0
)
goal_canvas.pack(anchor="w", padx=15)

remaining_goal_label = tk.Label(
    goal_frame, text="4 more sessions to reach your goal",
    font=("Arial", 9), bg=WHITE, fg=MUTED
)
remaining_goal_label.pack(anchor="w", padx=15, pady=(7, 12))

settings = tk.LabelFrame(
    root,
    text="  CUSTOMIZE YOUR TIMER  ",
    font=("Arial", 10, "bold"),
    bg=BG,
    fg=TEXT,
    bd=1,
    relief="groove",
    padx=10,
    pady=8
)
settings.pack(fill="x", padx=35, pady=(5, 18))

def add_setting(label, variable, column):
    frame = tk.Frame(settings, bg=BG)
    frame.grid(row=0, column=column, padx=8, pady=3)

    tk.Label(
        frame, text=label, font=("Arial", 9),
        bg=BG, fg=MUTED
    ).pack(pady=(0, 4))

    tk.Spinbox(
        frame,
        from_=1,
        to=180 if column < 3 else 100,
        textvariable=variable,
        width=6,
        justify="center",
        font=("Arial", 11),
        bg=WHITE,
        fg=TEXT,
        relief="flat"
    ).pack()

add_setting("Focus (min)", focus_minutes, 0)
add_setting("Short break", short_break_minutes, 1)
add_setting("Long break", long_break_minutes, 2)
add_setting("Daily goal", daily_goal, 3)

make_button(
    settings, "Apply Settings", apply_settings, BLUE
).grid(row=0, column=4, padx=8, pady=12)

tk.Label(
    root,
    text="focus gently • rest often • be proud of yourself",
    font=("Arial", 9, "italic"),
    bg=BG,
    fg=MUTED
).pack(pady=(0, 10))

update_ring()
update_dashboard()

root.mainloop()