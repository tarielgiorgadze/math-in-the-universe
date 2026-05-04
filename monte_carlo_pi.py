import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, Rectangle

# =========================
# SETTINGS
# =========================
FRAMES = 350
POINTS_PER_FRAME = 25
MAX_POINTS = FRAMES * POINTS_PER_FRAME

BG = "#020412"
PANEL = "#08101f"
BORDER = "#1e293b"
TEXT = "#e2e8f0"
SUBTEXT = "#94a3b8"
CYAN = "#22d3ee"
RED = "#f87171"
GREEN = "#4ade80"
WHITE = "#ffffff"

# =========================
# FULLSCREEN HELPERS
# =========================
def toggle_fullscreen(event=None):
    try:
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
    except Exception:
        pass

def close_figure(event=None):
    plt.close(fig)

# =========================
# PRE-GENERATE RANDOM POINTS
# =========================
np.random.seed(42)
x_all = np.random.uniform(-1, 1, MAX_POINTS)
y_all = np.random.uniform(-1, 1, MAX_POINTS)
inside_mask = x_all**2 + y_all**2 <= 1

pi_estimates = []
errors = []

inside_count_running = 0
for i in range(MAX_POINTS):
    if inside_mask[i]:
        inside_count_running += 1
    estimate = 4 * inside_count_running / (i + 1)
    pi_estimates.append(estimate)
    errors.append(abs(np.pi - estimate))

pi_estimates = np.array(pi_estimates)
errors = np.array(errors)
sample_sizes = np.arange(1, MAX_POINTS + 1)

# =========================
# FIGURE + LAYOUT
# =========================
fig = plt.figure(figsize=(16, 9), facecolor=BG)
gs = fig.add_gridspec(
    2, 2,
    width_ratios=[1.05, 1.15],
    height_ratios=[1, 1],
    left=0.03, right=0.98, top=0.93, bottom=0.06,
    wspace=0.12, hspace=0.17
)

ax_sim = fig.add_subplot(gs[:, 0])
ax_est = fig.add_subplot(gs[0, 1])
ax_err = fig.add_subplot(gs[1, 1])

for ax in [ax_sim, ax_est, ax_err]:
    ax.set_facecolor(BG)

# Key bindings
def on_key(event):
    if event.key == "escape":
        close_figure()
    elif event.key == "f11":
        toggle_fullscreen()

fig.canvas.mpl_connect("key_press_event", on_key)

try:
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
except Exception:
    pass

# =========================
# STAR BACKGROUND FOR SIM PANEL
# =========================
np.random.seed(7)
star_x = np.random.uniform(-1.45, 1.45, 120)
star_y = np.random.uniform(-1.45, 1.45, 120)
star_s = np.random.uniform(3, 15, 120)
star_a = np.random.uniform(0.15, 0.7, 120)

for sx, sy, ss, sa in zip(star_x, star_y, star_s, star_a):
    ax_sim.scatter(sx, sy, s=ss, color="white", alpha=sa, linewidths=0, zorder=0)

# =========================
# SIMULATION PANEL
# =========================
ax_sim.set_xlim(-1.35, 1.35)
ax_sim.set_ylim(-1.35, 1.35)
ax_sim.set_aspect("equal")
ax_sim.set_xticks([])
ax_sim.set_yticks([])
for spine in ax_sim.spines.values():
    spine.set_visible(False)

square = Rectangle((-1, -1), 2, 2, fill=False, edgecolor=WHITE, linewidth=1.8, alpha=0.9)
circle_glow = Circle((0, 0), 1.02, color=CYAN, alpha=0.05)
circle = Circle((0, 0), 1, fill=False, edgecolor=CYAN, linewidth=2.2)

ax_sim.add_patch(circle_glow)
ax_sim.add_patch(square)
ax_sim.add_patch(circle)

inside_scatter = ax_sim.scatter([], [], s=10, c=GREEN, alpha=0.75, label="Inside circle")
outside_scatter = ax_sim.scatter([], [], s=10, c=RED, alpha=0.65, label="Outside circle")

legend = ax_sim.legend(
    loc="upper right",
    facecolor=PANEL,
    edgecolor=BORDER,
    framealpha=0.95,
    fontsize=11
)
for t in legend.get_texts():
    t.set_color("white")

# Titles
fig.text(0.5, 0.965, "MONTE CARLO π SIMULATION", ha="center", color="white", fontsize=24, fontweight="bold")
fig.text(0.5, 0.935, "Estimating pi using random points, geometry, and statistical convergence",
         ha="center", color="#cbd5e1", fontsize=12)

fig.text(0.03, 0.975, "Esc = close   |   F11 = fullscreen toggle", ha="left", color=SUBTEXT, fontsize=9)

# Simulation labels
sim_title = ax_sim.text(0, 1.18, "Random points in a square and a circle", color="white",
                        fontsize=15, ha="center", fontweight="bold")
sim_subtitle = ax_sim.text(0, 1.08, "π ≈ 4 × (points inside circle / total points)",
                           color="#cbd5e1", fontsize=11, ha="center")

live_text = ax_sim.text(-1.28, -1.22, "", color=TEXT, fontsize=11, ha="left", va="bottom")
formula_text = ax_sim.text(0, -1.24, "", color=CYAN, fontsize=12, ha="center", va="bottom", fontweight="bold")

# =========================
# ESTIMATE GRAPH
# =========================
for spine in ax_est.spines.values():
    spine.set_color(BORDER)

ax_est.tick_params(colors="#cbd5e1")
ax_est.set_title("π Estimate Convergence", color="white", fontsize=15, pad=12, fontweight="bold")
ax_est.set_xlabel("Number of Random Points", color="#cbd5e1")
ax_est.set_ylabel("Estimated π", color="#cbd5e1")

ax_est.set_xlim(1, MAX_POINTS)
margin = 0.35
ax_est.set_ylim(np.pi - margin, np.pi + margin)

ax_est.axhline(np.pi, color=WHITE, linestyle="--", linewidth=1.5, alpha=0.8)
ax_est.text(MAX_POINTS * 0.82, np.pi + 0.02, "True π", color=WHITE, fontsize=10)

estimate_line, = ax_est.plot([], [], color=CYAN, linewidth=2.2)
estimate_dot, = ax_est.plot([], [], marker="o", markersize=6, color=CYAN)

# =========================
# ERROR GRAPH
# =========================
for spine in ax_err.spines.values():
    spine.set_color(BORDER)

ax_err.tick_params(colors="#cbd5e1")
ax_err.set_title("Absolute Error", color="white", fontsize=15, pad=12, fontweight="bold")
ax_err.set_xlabel("Number of Random Points", color="#cbd5e1")
ax_err.set_ylabel("|π - estimate|", color="#cbd5e1")

ax_err.set_xlim(1, MAX_POINTS)
ax_err.set_ylim(0, max(errors[:800]) * 1.15 if max(errors[:800]) > 0 else 1)

error_line, = ax_err.plot([], [], color=RED, linewidth=2.2)
error_fill = None
error_dot, = ax_err.plot([], [], marker="o", markersize=6, color=RED)

# =========================
# SIDE PANELS / INFO BOXES
# =========================
info_box = Rectangle((0.055, 0.08), 0.22, 0.12, transform=fig.transFigure,
                     color=PANEL, ec=BORDER, lw=1.2, alpha=0.92)
fig.patches.append(info_box)

summary_box = Rectangle((0.72, 0.08), 0.23, 0.12, transform=fig.transFigure,
                        color=PANEL, ec=BORDER, lw=1.2, alpha=0.92)
fig.patches.append(summary_box)

info_panel = fig.text(0.065, 0.175, "", color="#dbeafe", fontsize=11, va="top")
summary_panel = fig.text(0.73, 0.175, "", color="#dbeafe", fontsize=11, va="top")

bottom_message = fig.text(0.5, 0.025, "", ha="center", color=TEXT, fontsize=12)

# =========================
# UPDATE FUNCTION
# =========================
def update(frame):
    global error_fill

    total_points = min((frame + 1) * POINTS_PER_FRAME, MAX_POINTS)

    x_current = x_all[:total_points]
    y_current = y_all[:total_points]
    inside_current = inside_mask[:total_points]
    outside_current = ~inside_current

    inside_x = x_current[inside_current]
    inside_y = y_current[inside_current]
    outside_x = x_current[outside_current]
    outside_y = y_current[outside_current]

    inside_scatter.set_offsets(np.column_stack((inside_x, inside_y)) if len(inside_x) else np.empty((0, 2)))
    outside_scatter.set_offsets(np.column_stack((outside_x, outside_y)) if len(outside_x) else np.empty((0, 2)))

    inside_count = int(np.sum(inside_current))
    outside_count = total_points - inside_count
    current_estimate = pi_estimates[total_points - 1]
    current_error = errors[total_points - 1]

    # Live texts
    live_text.set_text(
        f"Total points: {total_points:,}\n"
        f"Inside circle: {inside_count:,}\n"
        f"Outside circle: {outside_count:,}\n"
        f"Current estimate: {current_estimate:.8f}\n"
        f"Absolute error: {current_error:.8f}"
    )

    formula_text.set_text(
        f"π ≈ 4 × ({inside_count:,} / {total_points:,}) = {current_estimate:.8f}"
    )

    # Estimate graph
    estimate_line.set_data(sample_sizes[:total_points], pi_estimates[:total_points])
    estimate_dot.set_data([sample_sizes[total_points - 1]], [current_estimate])

    # Error graph
    error_line.set_data(sample_sizes[:total_points], errors[:total_points])
    error_dot.set_data([sample_sizes[total_points - 1]], [current_error])

    if error_fill is not None:
        error_fill.remove()
    error_fill = ax_err.fill_between(
        sample_sizes[:total_points], errors[:total_points],
        color=RED, alpha=0.15
    )

    # Info panels
    info_panel.set_text(
        "MODEL DATA\n\n"
        f"True π = {np.pi:.10f}\n"
        f"Estimate = {current_estimate:.10f}\n"
        f"Error = {current_error:.10f}\n"
        f"Points/frame = {POINTS_PER_FRAME}"
    )

    water_like = current_error * 1_000_000
    summary_panel.set_text(
        "INTERPRETATION\n\n"
        "More random points\n"
        "→ better approximation\n"
        "→ smaller error\n\n"
        f"Scaled error index: {water_like:,.0f}"
    )

    # Bottom messages
    if frame < 70:
        bottom_message.set_text("Monte Carlo uses randomness to estimate a geometric constant.")
        bottom_message.set_color(TEXT)
    elif frame < 180:
        bottom_message.set_text("As the number of points increases, the estimate tends to get closer to π.")
        bottom_message.set_color(TEXT)
    elif frame < 300:
        bottom_message.set_text("The convergence is not perfectly smooth, but the overall trend improves.")
        bottom_message.set_color(TEXT)
    else:
        bottom_message.set_text("FINAL RESULT: Randomness + mathematics + large samples can reveal hidden order.")
        bottom_message.set_color("#facc15" if frame % 20 < 10 else TEXT)

    return (
        inside_scatter, outside_scatter,
        estimate_line, estimate_dot,
        error_line, error_dot,
        live_text, formula_text,
        info_panel, summary_panel,
        bottom_message
    )

# =========================
# RUN
# =========================
ani = FuncAnimation(
    fig,
    update,
    frames=FRAMES,
    interval=35,
    blit=False,
    repeat=True
)

plt.show()