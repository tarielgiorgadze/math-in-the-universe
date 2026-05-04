import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os


# =========================
# WINDOW SETUP
# =========================
root = tk.Tk()
root.title("Math in the Universe")
root.geometry("1000x650")
root.configure(bg="#020412")
root.resizable(False, False)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# =========================
# HELPER FUNCTIONS
# =========================
def run_script(filename):
    script_path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(script_path):
        messagebox.showwarning(
            "File not found",
            f"'{filename}' ვერ მოიძებნა.\nჯერ ეს მოდული არ შეგვიქმნია."
        )
        return

    try:
        subprocess.Popen([sys.executable, script_path])
    except Exception as e:
        messagebox.showerror("Error", f"ფაილი ვერ გაეშვა:\n{e}")


def open_space_precision():
    run_script("space_precision.py")


def open_monte_carlo():
    run_script("monte_carlo_pi.py")


def open_golden_ratio():
    run_script("golden_ratio.py")


def open_about():
    about_window = tk.Toplevel(root)
    about_window.title("About Project")
    about_window.geometry("760x480")
    about_window.configure(bg="#071120")
    about_window.resizable(False, False)

    title = tk.Label(
        about_window,
        text="About This Project",
        font=("Helvetica", 22, "bold"),
        fg="white",
        bg="#071120"
    )
    title.pack(pady=(25, 15))

    about_text = (
        "This project explores how mathematics appears in reality and in the universe.\n\n"
        "Sections included:\n"
        "• Pi and Space Precision\n"
        "• Monte Carlo Simulation for Pi\n"
        "• Golden Ratio in Nature\n\n"
        "Main idea:\n"
        "Mathematics is not only abstract theory. It shapes motion, design,\n"
        "patterns in nature, engineering accuracy, and our understanding of the world.\n\n"
        "Built with Python using Tkinter, Matplotlib, and NumPy."
    )

    content = tk.Label(
        about_window,
        text=about_text,
        font=("Helvetica", 13),
        fg="#dbeafe",
        bg="#071120",
        justify="left",
        wraplength=650
    )
    content.pack(pady=10)

    close_btn = tk.Button(
        about_window,
        text="Close",
        font=("Helvetica", 12, "bold"),
        bg="#1d4ed8",
        fg="white",
        activebackground="#2563eb",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        padx=18,
        pady=8,
        command=about_window.destroy
    )
    close_btn.pack(pady=25)


# =========================
# BACKGROUND DECOR
# =========================
canvas = tk.Canvas(root, width=1000, height=650, bg="#020412", highlightthickness=0)
canvas.place(x=0, y=0)

# Stars
import random
random.seed(42)
for _ in range(180):
    x = random.randint(0, 1000)
    y = random.randint(0, 650)
    r = random.randint(1, 2)
    color = random.choice(["#ffffff", "#cbd5e1", "#dbeafe", "#e2e8f0"])
    canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="")

# Decorative glowing circles
canvas.create_oval(60, 70, 220, 230, fill="#0f172a", outline="")
canvas.create_oval(70, 80, 210, 220, fill="#1e3a8a", outline="")
canvas.create_oval(760, 430, 930, 600, fill="#180a3a", outline="")
canvas.create_oval(785, 455, 905, 575, fill="#3b0764", outline="")

# Planet-like shapes
canvas.create_oval(830, 70, 930, 170, fill="#2563eb", outline="#93c5fd", width=2)
canvas.create_oval(120, 500, 185, 565, fill="#cbd5e1", outline="#f8fafc", width=1)


# =========================
# MAIN CONTENT FRAME
# =========================
main_frame = tk.Frame(root, bg="#08101f", bd=0, highlightthickness=1, highlightbackground="#1e293b")
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=540, height=470)

title_label = tk.Label(
    main_frame,
    text="MATH IN THE UNIVERSE",
    font=("Helvetica", 24, "bold"),
    fg="white",
    bg="#08101f"
)
title_label.pack(pady=(30, 10))

subtitle_label = tk.Label(
    main_frame,
    text="Interactive Python Project on Mathematics in Reality",
    font=("Helvetica", 12),
    fg="#cbd5e1",
    bg="#08101f"
)
subtitle_label.pack(pady=(0, 25))


# =========================
# BUTTON STYLE
# =========================
def create_menu_button(parent, text, command):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Helvetica", 13, "bold"),
        bg="#0f172a",
        fg="white",
        activebackground="#1d4ed8",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        width=28,
        height=2,
        bd=0
    )
    return btn


btn1 = create_menu_button(main_frame, "1. Pi and Space Precision", open_space_precision)
btn1.pack(pady=8)

btn2 = create_menu_button(main_frame, "2. Monte Carlo Pi Simulation", open_monte_carlo)
btn2.pack(pady=8)

btn3 = create_menu_button(main_frame, "3. Golden Ratio and Nature", open_golden_ratio)
btn3.pack(pady=8)

btn4 = create_menu_button(main_frame, "4. About Project", open_about)
btn4.pack(pady=8)

btn5 = tk.Button(
    main_frame,
    text="5. Exit",
    command=root.destroy,
    font=("Helvetica", 13, "bold"),
    bg="#7f1d1d",
    fg="white",
    activebackground="#b91c1c",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    width=28,
    height=2,
    bd=0
)
btn5.pack(pady=(12, 8))


footer_label = tk.Label(
    main_frame,
    text="Created in Python • Mathematics, Simulation, and Beauty",
    font=("Helvetica", 10),
    fg="#94a3b8",
    bg="#08101f"
)
footer_label.pack(side="bottom", pady=20)


# =========================
# RUN APP
# =========================
root.mainloop()