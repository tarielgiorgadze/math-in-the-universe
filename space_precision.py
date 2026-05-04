import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# =========================
# DATA / MODEL SETTINGS
# =========================
PI_TRUE = np.pi
PI_APPROX = 3.14

# Educational scale based on average Earth-Moon distance
R_KM = 384400  # km

# Simplified correction model:
# assumed extra correction fuel per km of path error
FUEL_PER_KM = 0.8  # kg/km (educational assumption)

# Visual scene setup
FRAMES = 280
EARTH_X, EARTH_Y = -8.8, 0.0
MOON_X, MOON_Y = 8.8, 0.0
CURVE_HEIGHT = 4.8
DEVIATION_SCALE = 2.6

# =========================
# CALCULATIONS
# =========================
pi_difference = abs(PI_TRUE - PI_APPROX)
percent_error = (pi_difference / PI_TRUE) * 100

# Full-circle educational path-length difference
distance_error_km = 2 * R_KM * pi_difference

# Simplified extra fuel estimate
extra_fuel_kg = distance_error_km * FUEL_PER_KM

# Real-life comparison
water_equivalent_liters = extra_fuel_kg
adult_equivalent = extra_fuel_kg / 75

# =========================
# TRAJECTORY FUNCTION
# =========================
def transfer_trajectory(t, pi_value):
    """
    Simplified Earth-to-Moon transfer-like path.
    t in [0, 1]
    The inaccurate pi slightly changes the path shape so deviation grows over distance.
    """
    x = EARTH_X + (MOON_X - EARTH_X) * t
    base_arc = CURVE_HEIGHT * np.sin(np.pi * t)

    pi_error_factor = (pi_value - PI_TRUE) / PI_TRUE
    drift = DEVIATION_SCALE * pi_error_factor * (t ** 1.85) * 18

    y = base_arc + drift
    return x, y


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
# FIGURE SETUP
# =========================
fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor("#020412")
ax.set_facecolor("#020412")

ax.set_xlim(-12, 12)
ax.set_ylim(-7.3, 7.3)
ax.set_aspect("equal")
ax.set_xticks([])
ax.set_yticks([])

for spine in ax.spines.values():
    spine.set_visible(False)

# Key bindings
def on_key(event):
    if event.key == "escape":
        close_figure()
    elif event.key == "f11":
        toggle_fullscreen()

fig.canvas.mpl_connect("key_press_event", on_key)

# Try fullscreen on start
try:
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
except Exception:
    pass

# =========================
# STAR BACKGROUND
# =========================
np.random.seed(42)
star_x = np.random.uniform(-12, 12, 260)
star_y = np.random.uniform(-7.3, 7.3, 260)
star_sizes = np.random.uniform(2, 14, 260)
star_alpha = np.random.uniform(0.2, 0.95, 260)

for sx, sy, ss, sa in zip(star_x, star_y, star_sizes, star_alpha):
    ax.scatter(sx, sy, s=ss, color="white", alpha=sa, linewidths=0)

# Decorative glow clouds
glow1 = plt.Circle((-7.5, 4.8), 1.9, color="#1e3a8a", alpha=0.08)
glow2 = plt.Circle((6.0, -4.6), 2.2, color="#7c3aed", alpha=0.07)
ax.add_patch(glow1)
ax.add_patch(glow2)

# =========================
# EARTH AND MOON
# =========================
earth_glow_outer = plt.Circle((EARTH_X, EARTH_Y), 1.65, color="#38bdf8", alpha=0.08)
earth_glow = plt.Circle((EARTH_X, EARTH_Y), 1.28, color="#38bdf8", alpha=0.17)
earth = plt.Circle((EARTH_X, EARTH_Y), 0.84, color="#2563eb", ec="#bfdbfe", linewidth=1.5)

moon_glow_outer = plt.Circle((MOON_X, MOON_Y), 1.18, color="#f8fafc", alpha=0.05)
moon_glow = plt.Circle((MOON_X, MOON_Y), 0.92, color="#e5e7eb", alpha=0.12)
moon = plt.Circle((MOON_X, MOON_Y), 0.58, color="#cbd5e1", ec="#f8fafc", linewidth=1.1)

ax.add_patch(earth_glow_outer)
ax.add_patch(earth_glow)
ax.add_patch(earth)

ax.add_patch(moon_glow_outer)
ax.add_patch(moon_glow)
ax.add_patch(moon)

ax.text(EARTH_X, -1.38, "Earth", color="#cbd5e1", fontsize=11, ha="center")
ax.text(MOON_X, -1.03, "Moon", color="#cbd5e1", fontsize=11, ha="center")

# =========================
# PREVIEW PATHS
# =========================
t_preview = np.linspace(0, 1, 500)
x_true_preview, y_true_preview = transfer_trajectory(t_preview, PI_TRUE)
x_bad_preview, y_bad_preview = transfer_trajectory(t_preview, PI_APPROX)

ax.plot(x_true_preview, y_true_preview, color="#22d3ee", alpha=0.08, linewidth=1.5)
ax.plot(x_bad_preview, y_bad_preview, color="#f87171", alpha=0.08, linewidth=1.5, linestyle="--")

# =========================
# TRAIL LINES / MARKERS
# =========================
line_true_glow, = ax.plot([], [], color="#22d3ee", linewidth=8.0, alpha=0.08)
line_bad_glow, = ax.plot([], [], color="#f87171", linewidth=8.0, alpha=0.06, linestyle="--")

line_true, = ax.plot([], [], color="#22d3ee", linewidth=2.8, label="Accurate π")
line_bad, = ax.plot([], [], color="#f87171", linewidth=2.5, linestyle="--", label="π = 3.14")

craft_true, = ax.plot([], [], marker="o", markersize=7, color="#67e8f9",
                      markeredgecolor="white", linestyle="None")
craft_bad, = ax.plot([], [], marker="o", markersize=7, color="#fca5a5",
                     markeredgecolor="white", linestyle="None")

legend = ax.legend(
    loc="upper right",
    facecolor="#0b1020",
    edgecolor="#334155",
    framealpha=0.92,
    fontsize=11
)
for text in legend.get_texts():
    text.set_color("white")

# =========================
# TITLES / PANELS
# =========================
ax.text(
    0, 6.45,
    "PI AND SPACE PRECISION",
    color="white",
    fontsize=24,
    ha="center",
    fontweight="bold"
)

ax.text(
    0, 5.8,
    "Why small mathematical approximations can matter at large distances",
    color="#cbd5e1",
    fontsize=12,
    ha="center"
)

# Left info panel
panel_left = plt.Rectangle(
    (-11.5, -6.8), 5.0, 4.75,
    color="#08101f", alpha=0.82, ec="#1e293b", lw=1.2
)
ax.add_patch(panel_left)

ax.text(
    -9.0, -2.45,
    "MODEL DATA",
    color="white",
    fontsize=14,
    ha="center",
    fontweight="bold"
)

panel_text = ax.text(
    -11.1, -3.05,
    (
        f"Real π = {PI_TRUE:.10f}\n"
        f"Approx π = {PI_APPROX}\n"
        f"π difference = {pi_difference:.10f}\n"
        f"Percent error = {percent_error:.6f}%\n\n"
        f"Radius scale = {R_KM:,} km\n"
        f"Distance error ≈ {distance_error_km:,.2f} km\n"
        f"Fuel factor = {FUEL_PER_KM} kg/km\n"
        f"Estimated extra fuel ≈ {extra_fuel_kg:,.2f} kg\n"
        f"≈ {water_equivalent_liters:,.0f} liters of water\n"
        f"≈ {adult_equivalent:.1f} adults (75 kg each)"
    ),
    color="#dbeafe",
    fontsize=10.2,
    ha="left",
    va="top"
)

# Right panel surprise section
panel_right = plt.Rectangle(
    (6.7, -6.8), 4.8, 4.75,
    color="#08101f", alpha=0.82, ec="#1e293b", lw=1.2
)
ax.add_patch(panel_right)

ax.text(
    9.1, -2.45,
    "WHY IT MATTERS",
    color="white",
    fontsize=14,
    ha="center",
    fontweight="bold"
)

impact_text = ax.text(
    6.95, -3.05,
    (
        "Small errors can become big\n"
        "when distance becomes huge.\n\n"
        "Mathematics is not only theory:\n"
        "it affects navigation,\n"
        "engineering, prediction,\n"
        "and mission safety."
    ),
    color="#dbeafe",
    fontsize=10.4,
    ha="left",
    va="top"
)

# Bottom panel
bottom_panel = plt.Rectangle(
    (-5.9, -6.95), 11.8, 1.15,
    color="#08101f", alpha=0.82, ec="#1e293b", lw=1.0
)
ax.add_patch(bottom_panel)

info_text = ax.text(
    0, -6.43,
    "",
    color="#e2e8f0",
    fontsize=11,
    ha="center"
)

deviation_text = ax.text(
    0, -5.95,
    "",
    color="#f8fafc",
    fontsize=10.5,
    ha="center"
)

ax.text(
    -11.4, 6.7,
    "Esc = close   |   F11 = fullscreen toggle",
    color="#94a3b8",
    fontsize=9,
    ha="left"
)

note_text = ax.text(
    0, 4.95,
    "Note: This is a simplified educational model. Real missions use highly precise calculations.",
    color="#94a3b8",
    fontsize=9.5,
    ha="center"
)

# =========================
# ANIMATION DATA
# =========================
t_vals = np.linspace(0, 1, FRAMES)
x_true_vals, y_true_vals = [], []
x_bad_vals, y_bad_vals = [], []

# =========================
# UPDATE FUNCTION
# =========================
def update(frame):
    t = t_vals[frame]

    x_t, y_t = transfer_trajectory(t, PI_TRUE)
    x_b, y_b = transfer_trajectory(t, PI_APPROX)

    x_true_vals.append(x_t)
    y_true_vals.append(y_t)

    x_bad_vals.append(x_b)
    y_bad_vals.append(y_b)

    line_true.set_data(x_true_vals, y_true_vals)
    line_bad.set_data(x_bad_vals, y_bad_vals)

    line_true_glow.set_data(x_true_vals, y_true_vals)
    line_bad_glow.set_data(x_bad_vals, y_bad_vals)

    craft_true.set_data([x_t], [y_t])
    craft_bad.set_data([x_b], [y_b])

    path_separation = np.sqrt((x_t - x_b) ** 2 + (y_t - y_b) ** 2)

    # Default text color
    info_text.set_color("#e2e8f0")

    if frame < 55:
        info_text.set_text("A spacecraft leaves Earth on a simplified transfer path toward the Moon.")
        deviation_text.set_text(
            f"Current visual path deviation: {path_separation:.4f}"
        )
    elif frame < 145:
        info_text.set_text("Two trajectories are compared: one uses real π, the other uses π = 3.14.")
        deviation_text.set_text(
            f"Current visual path deviation: {path_separation:.4f}"
        )
    elif frame < 230:
        info_text.set_text("Even a small approximation can accumulate into a visible navigation difference.")
        deviation_text.set_text(
            f"Current visual path deviation: {path_separation:.4f}   |   Educational distance error estimate: {distance_error_km:,.2f} km"
        )
    else:
        info_text.set_text(
            "MISSION RESULT: Small mathematical approximation → Large-scale deviation. Precision is critical."
        )
        deviation_text.set_text(
            f"≈ {distance_error_km:,.0f} km path error   |   ≈ {extra_fuel_kg:,.0f} kg correction   |   ≈ {water_equivalent_liters:,.0f} L water"
        )

        # Blink effect
        if frame % 20 < 10:
            info_text.set_color("#f87171")
        else:
            info_text.set_color("#e2e8f0")

    return (
        line_true_glow, line_bad_glow,
        line_true, line_bad,
        craft_true, craft_bad,
        info_text, deviation_text
    )

# =========================
# RUN
# =========================
ani = FuncAnimation(
    fig,
    update,
    frames=FRAMES,
    interval=28,
    blit=True,
    repeat=True
)

plt.show()