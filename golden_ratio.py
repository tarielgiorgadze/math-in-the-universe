import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle, Arc

# =========================
# SETTINGS
# =========================
BG = "#020412"
PANEL = "#08101f"
BORDER = "#1e293b"
TEXT = "#e2e8f0"
SUBTEXT = "#94a3b8"
GOLD = "#facc15"
GOLD2 = "#f59e0b"
CYAN = "#22d3ee"
GREEN = "#4ade80"
WHITE = "#ffffff"
PURPLE = "#a855f7"

FRAMES = 320
PHI = (1 + np.sqrt(5)) / 2

paused = False

# =========================
# FULLSCREEN + KEYS
# =========================
def on_key(event):
    global paused
    if event.key == "escape":
        plt.close(fig)
    elif event.key == "f11":
        try:
            plt.get_current_fig_manager().full_screen_toggle()
        except Exception:
            pass
    elif event.key == " ":
        paused = not paused

# =========================
# FIBONACCI
# =========================
def fibonacci(n):
    seq = [1, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq

fib = fibonacci(10)

# =========================
# FIGURE LAYOUT
# =========================
fig = plt.figure(figsize=(16, 9), facecolor=BG)
gs = fig.add_gridspec(
    2, 2,
    width_ratios=[1.05, 1.0],
    height_ratios=[1, 1],
    left=0.03, right=0.98, top=0.92, bottom=0.08,
    wspace=0.12, hspace=0.18
)

ax_spiral = fig.add_subplot(gs[:, 0])
ax_ratio = fig.add_subplot(gs[0, 1])
ax_phyllo = fig.add_subplot(gs[1, 1])

for ax in [ax_spiral, ax_ratio, ax_phyllo]:
    ax.set_facecolor(BG)

fig.canvas.mpl_connect("key_press_event", on_key)

try:
    plt.get_current_fig_manager().full_screen_toggle()
except Exception:
    pass

# =========================
# TITLES
# =========================
fig.text(
    0.5, 0.965,
    "GOLDEN RATIO AND NATURE",
    ha="center",
    color="white",
    fontsize=24,
    fontweight="bold"
)

fig.text(
    0.5, 0.935,
    "How mathematics appears as beauty, growth, proportion, and natural order",
    ha="center",
    color="#cbd5e1",
    fontsize=12
)

fig.text(
    0.03, 0.973,
    "Esc = close   |   F11 = fullscreen   |   Space = pause/resume",
    ha="left",
    color=SUBTEXT,
    fontsize=9
)

# =========================
# LEFT PANEL: GOLDEN RECTANGLES + SPIRAL
# =========================
ax_spiral.set_aspect("equal")
ax_spiral.set_xticks([])
ax_spiral.set_yticks([])
for spine in ax_spiral.spines.values():
    spine.set_visible(False)

ax_spiral.set_xlim(-1, 22)
ax_spiral.set_ylim(-1, 14)

ax_spiral.text(
    10.5, 13.2,
    "Golden rectangles and Fibonacci spiral",
    color="white",
    fontsize=15,
    ha="center",
    fontweight="bold"
)

# Precomputed rectangles based on Fibonacci tiling
# (x, y, width, height, arc center x, arc center y, theta1, theta2)
rects = [
    (0, 0, 1, 1, 1, 0, 90, 180),
    (1, 0, 1, 1, 1, 1, 0, 90),
    (0, 1, 2, 2, 2, 1, 180, 270),
    (-3, 0, 3, 3, 0, 0, 270, 360),
    (-3, -5, 5, 5, -3, 0, 0, 90),
    (2, -5, 8, 8, 2, -5, 90, 180),
    (2, 3, 13, 13, 2, 3, 180, 270),
]

# shift everything right/up a bit for better framing
shift_x = 6
shift_y = 5

rectangle_patches = []
arc_patches = []

rect_colors = [
    "#1e293b", "#0f172a", "#1d4ed8", "#065f46",
    "#7c2d12", "#4c1d95", "#92400e"
]

for i, (x, y, w, h, cx, cy, t1, t2) in enumerate(rects):
    rect = Rectangle(
        (x + shift_x, y + shift_y),
        w, h,
        fill=True,
        facecolor=rect_colors[i % len(rect_colors)],
        edgecolor="#cbd5e1",
        linewidth=1.5,
        alpha=0.55
    )
    rectangle_patches.append(rect)
    ax_spiral.add_patch(rect)
    rect.set_visible(False)

    arc = Arc(
        (cx + shift_x, cy + shift_y),
        2 * max(w, h),
        2 * max(w, h),
        theta1=t1,
        theta2=t2,
        color=GOLD,
        linewidth=2.3
    )
    arc_patches.append(arc)
    ax_spiral.add_patch(arc)
    arc.set_visible(False)

spiral_info = ax_spiral.text(
    10.5, -0.4,
    "",
    color=TEXT,
    fontsize=11,
    ha="center"
)

# =========================
# TOP RIGHT: FIBONACCI RATIOS
# =========================
for spine in ax_ratio.spines.values():
    spine.set_color(BORDER)

ax_ratio.tick_params(colors="#cbd5e1")
ax_ratio.set_title("Fibonacci Ratios Approaching φ", color="white", fontsize=15, pad=12, fontweight="bold")
ax_ratio.set_xlabel("n", color="#cbd5e1")
ax_ratio.set_ylabel("F(n+1) / F(n)", color="#cbd5e1")

ratios_x = np.arange(2, len(fib))
ratios_y = np.array([fib[i] / fib[i - 1] for i in range(1, len(fib))])

ax_ratio.set_xlim(1, len(fib))
ax_ratio.set_ylim(1.4, 1.75)
ax_ratio.axhline(PHI, color=GOLD, linestyle="--", linewidth=1.8, label="Golden ratio φ")

ratio_line, = ax_ratio.plot([], [], color=CYAN, linewidth=2.5, marker="o")
ratio_text = ax_ratio.text(
    0.03, 0.92,
    "",
    transform=ax_ratio.transAxes,
    color="#dbeafe",
    fontsize=11,
    va="top"
)

leg = ax_ratio.legend(facecolor=PANEL, edgecolor=BORDER, framealpha=0.95, fontsize=10)
for t in leg.get_texts():
    t.set_color("white")

# =========================
# BOTTOM RIGHT: PHYLLOTAXIS
# =========================
for spine in ax_phyllo.spines.values():
    spine.set_visible(False)

ax_phyllo.set_xticks([])
ax_phyllo.set_yticks([])
ax_phyllo.set_aspect("equal")
ax_phyllo.set_title("Phyllotaxis: Sunflower-like Pattern", color="white", fontsize=15, pad=12, fontweight="bold")

ax_phyllo.set_xlim(-18, 18)
ax_phyllo.set_ylim(-18, 18)

# generate sunflower pattern with golden angle
golden_angle = np.deg2rad(137.5)
n_seeds = 700
seed_x = []
seed_y = []
seed_sizes = []

for n in range(n_seeds):
    r = 0.68 * np.sqrt(n)
    theta = n * golden_angle
    seed_x.append(r * np.cos(theta))
    seed_y.append(r * np.sin(theta))
    seed_sizes.append(12 + (n / n_seeds) * 18)

seed_x = np.array(seed_x)
seed_y = np.array(seed_y)
seed_sizes = np.array(seed_sizes)

phyllo_scatter = ax_phyllo.scatter([], [], s=[], c=[], alpha=0.9)

phyllo_text = ax_phyllo.text(
    0.5, 0.03,
    "",
    transform=ax_phyllo.transAxes,
    color=TEXT,
    fontsize=11,
    ha="center"
)

# =========================
# PANELS
# =========================
left_panel = Rectangle(
    (0.035, 0.03), 0.25, 0.13,
    transform=fig.transFigure,
    color=PANEL,
    ec=BORDER,
    lw=1.2,
    alpha=0.92
)
fig.patches.append(left_panel)

right_panel = Rectangle(
    (0.72, 0.03), 0.24, 0.13,
    transform=fig.transFigure,
    color=PANEL,
    ec=BORDER,
    lw=1.2,
    alpha=0.92
)
fig.patches.append(right_panel)

left_info = fig.text(
    0.045, 0.145,
    "",
    color="#dbeafe",
    fontsize=10.5,
    va="top"
)

right_info = fig.text(
    0.73, 0.145,
    "",
    color="#dbeafe",
    fontsize=10.5,
    va="top"
)

bottom_message = fig.text(
    0.5, 0.02,
    "",
    ha="center",
    color=TEXT,
    fontsize=12
)

# =========================
# UPDATE
# =========================
def update(frame):
    global paused

    if paused:
        return

    # ---------------------
    # spiral reveal
    # ---------------------
    rect_count = min(len(rectangle_patches), frame // 18 + 1)
    arc_count = min(len(arc_patches), max(0, (frame - 15) // 18 + 1))

    for i, rect in enumerate(rectangle_patches):
        rect.set_visible(i < rect_count)

    for i, arc in enumerate(arc_patches):
        arc.set_visible(i < arc_count)

    shown_fib = fib[:min(rect_count + 1, len(fib))]
    spiral_info.set_text(
        "Fibonacci numbers: " + ", ".join(str(x) for x in shown_fib)
    )

    # ---------------------
    # ratio graph reveal
    # ---------------------
    ratio_count = min(len(ratios_y), frame // 22 + 1)
    ratio_line.set_data(np.arange(2, 2 + ratio_count), ratios_y[:ratio_count])

    if ratio_count > 0:
        current_ratio = ratios_y[ratio_count - 1]
        ratio_text.set_text(
            f"Golden ratio φ = {PHI:.10f}\n"
            f"Current ratio = {current_ratio:.10f}\n"
            f"Difference = {abs(PHI - current_ratio):.10f}"
        )

    # ---------------------
    # phyllotaxis reveal
    # ---------------------
    seed_count = min(n_seeds, frame * 4 + 10)
    colors = np.linspace(0.2, 1.0, seed_count)
    phyllo_scatter.set_offsets(np.column_stack((seed_x[:seed_count], seed_y[:seed_count])))
    phyllo_scatter.set_sizes(seed_sizes[:seed_count])
    phyllo_scatter.set_array(colors)
    phyllo_scatter.set_cmap("plasma")

    phyllo_text.set_text(
        f"Visible seeds: {seed_count}   |   Golden angle ≈ 137.5°"
    )

    # ---------------------
    # info panels
    # ---------------------
    left_info.set_text(
        "MATHEMATICAL IDEA\n\n"
        f"Golden ratio:\nφ = (1 + √5) / 2\n≈ {PHI:.10f}\n\n"
        "Fibonacci ratios approach φ."
    )

    right_info.set_text(
        "WHY IT MATTERS\n\n"
        "Mathematics appears not only\n"
        "in accuracy and physics,\n"
        "but also in beauty, growth,\n"
        "structure, and natural design."
    )

    # ---------------------
    # bottom story
    # ---------------------
    if frame < 70:
        bottom_message.set_text("The Fibonacci sequence builds shapes that lead toward the golden ratio.")
        bottom_message.set_color(TEXT)
    elif frame < 170:
        bottom_message.set_text("As the sequence grows, ratios stabilize near φ.")
        bottom_message.set_color(TEXT)
    elif frame < 260:
        bottom_message.set_text("The same mathematics can model patterns similar to those seen in flowers and seeds.")
        bottom_message.set_color(TEXT)
    else:
        bottom_message.set_text("FINAL MESSAGE: Mathematics is not only useful — it is also beautiful.")
        bottom_message.set_color(GOLD if frame % 20 < 10 else TEXT)

    return (
        *rectangle_patches,
        *arc_patches,
        ratio_line,
        ratio_text,
        phyllo_scatter,
        phyllo_text,
        spiral_info,
        left_info,
        right_info,
        bottom_message
    )

# =========================
# RUN
# =========================
ani = FuncAnimation(
    fig,
    update,
    frames=FRAMES,
    interval=40,
    blit=False,
    repeat=True
)

plt.show()