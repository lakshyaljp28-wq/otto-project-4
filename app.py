import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Air Standard Otto Cycle Simulator",
    page_icon="⚙️",
    layout="wide"
)

GAMMA = 1.4
R = 287.0
CV = R / (GAMMA - 1.0)

st.title("⚙️ Air Standard Otto Cycle")
st.subheader("Efficiency Calculator & P–V Diagram Plotter")

st.markdown("""
**Mechanical Engineering Project**

This interactive simulator calculates the thermal efficiency,
state-point properties, net work and mean effective pressure
of an ideal Air-Standard Otto Cycle.
""")

with st.expander("👥 Team Details", expanded=True):
    st.write("**Group Number:** XX")
    st.write("**Member 1:** Name - Enrollment Number")
    st.write("**Member 2:** Name - Enrollment Number")
    st.write("**Member 3:** Name - Enrollment Number")
    st.write("**Member 4:** Name - Enrollment Number")

st.divider()

st.sidebar.title("⚙️ Cycle Inputs")
st.sidebar.subheader("Cylinder Geometry")

bore_mm = st.sidebar.number_input(
    "Cylinder Bore (mm)", min_value=1.0, max_value=1000.0,
    value=100.0, step=1.0
)

stroke_mm = st.sidebar.number_input(
    "Stroke Length (mm)", min_value=1.0, max_value=1000.0,
    value=100.0, step=1.0
)

compression_ratio = st.sidebar.slider(
    "Compression Ratio (r)", min_value=2.0, max_value=20.0,
    value=8.0, step=0.1
)

st.sidebar.subheader("Initial Conditions")

T1 = st.sidebar.number_input(
    "Initial Temperature T₁ (K)", min_value=100.0, max_value=1000.0,
    value=300.0, step=10.0
)

P1_kPa = st.sidebar.number_input(
    "Initial Pressure P₁ (kPa)", min_value=1.0, max_value=1000.0,
    value=100.0, step=5.0
)

st.sidebar.subheader("Heat Addition")

T3 = st.sidebar.number_input(
    "Maximum Temperature T₃ (K)", min_value=301.0, max_value=5000.0,
    value=2000.0, step=50.0
)

P1 = P1_kPa * 1000.0
valid = True

if bore_mm <= 0:
    st.error("❌ Bore must be greater than zero.")
    valid = False

if stroke_mm <= 0:
    st.error("❌ Stroke length must be greater than zero.")
    valid = False

if compression_ratio <= 1:
    st.error("❌ Compression ratio must be greater than 1.")
    valid = False

if T1 <= 0:
    st.error("❌ Initial temperature must be greater than zero.")
    valid = False

if P1 <= 0:
    st.error("❌ Initial pressure must be greater than zero.")
    valid = False

if T3 <= T1:
    st.error("❌ T₃ must be greater than T₁.")
    valid = False

if valid:
    bore = bore_mm / 1000.0
    stroke = stroke_mm / 1000.0

    Vd = (np.pi / 4.0) * bore**2 * stroke
    Vc = Vd / (compression_ratio - 1.0)
    V1 = Vd + Vc
    V2 = Vc

    T2 = T1 * compression_ratio**(GAMMA - 1.0)
    P2 = P1 * compression_ratio**GAMMA

    T3_state = T3
    P3 = P2 * (T3 / T2)

    T4 = T3 / compression_ratio**(GAMMA - 1.0)
    P4 = P3 / compression_ratio**GAMMA

    efficiency = 1.0 - (1.0 / compression_ratio**(GAMMA - 1.0))

    Qin = CV * (T3 - T2)
    Qout = CV * (T4 - T1)
    Wnet = Qin - Qout

    MEP_Pa = Wnet / Vd
    MEP_kPa = MEP_Pa / 1000.0

    st.header("📊 Cycle Results")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Thermal Efficiency", f"{efficiency * 100:.2f}%")
    with col2:
        st.metric("MEP", f"{MEP_kPa:.2f} kPa")
    with col3:
        st.metric("Net Work", f"{Wnet:.2f} J/kg")
    with col4:
        st.metric("Compression Ratio", f"{compression_ratio:.2f}")

    st.subheader("📐 Cylinder Volume")

    v1, v2, v3 = st.columns(3)

    with v1:
        st.metric("Displacement Volume", f"{Vd * 1e6:.2f} cm³")
    with v2:
        st.metric("Clearance Volume", f"{Vc * 1e6:.2f} cm³")
    with v3:
        st.metric("Maximum Volume V₁", f"{V1 * 1e6:.2f} cm³")

    st.subheader("🔢 Otto Cycle State Points")

    state_table = {
        "State": [
            "1 - Start of Compression",
            "2 - End of Compression",
            "3 - End of Heat Addition",
            "4 - End of Expansion"
        ],
        "Temperature (K)": [
            f"{T1:.2f}", f"{T2:.2f}", f"{T3:.2f}", f"{T4:.2f}"
        ],
        "Pressure (kPa)": [
            f"{P1 / 1000:.2f}", f"{P2 / 1000:.2f}",
            f"{P3 / 1000:.2f}", f"{P4 / 1000:.2f}"
        ],
        "Volume (cm³)": [
            f"{V1 * 1e6:.2f}", f"{V2 * 1e6:.2f}",
            f"{V2 * 1e6:.2f}", f"{V1 * 1e6:.2f}"
        ]
    }

    st.table(state_table)

    st.subheader("📈 Air Standard Otto Cycle P–V Diagram")

    V_compression = np.linspace(V1, V2, 150)
    P_compression = P1 * (V1 / V_compression)**GAMMA

    V_heat_addition = np.full(40, V2)
    P_heat_addition = np.linspace(P2, P3, 40)

    V_expansion = np.linspace(V2, V1, 150)
    P_expansion = P3 * (V2 / V_expansion)**GAMMA

    V_heat_rejection = np.full(40, V1)
    P_heat_rejection = np.linspace(P4, P1, 40)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        V_compression * 1e6, P_compression / 1000,
        linewidth=2, label="1 → 2 Isentropic Compression"
    )
    ax.plot(
        V_heat_addition * 1e6, P_heat_addition / 1000,
        linewidth=2, label="2 → 3 Constant Volume Heat Addition"
    )
    ax.plot(
        V_expansion * 1e6, P_expansion / 1000,
        linewidth=2, label="3 → 4 Isentropic Expansion"
    )
    ax.plot(
        V_heat_rejection * 1e6, P_heat_rejection / 1000,
        linewidth=2, label="4 → 1 Constant Volume Heat Rejection"
    )

    state_volumes = np.array([V1, V2, V2, V1]) * 1e6
    state_pressures = np.array([P1, P2, P3, P4]) / 1000

    ax.scatter(
        state_volumes, state_pressures,
        s=70, zorder=5, label="State Points"
    )

    for x, y, label in zip(
        state_volumes, state_pressures, ["1", "2", "3", "4"]
    ):
        ax.annotate(
            label, (x, y), xytext=(8, 8),
            textcoords="offset points",
            fontsize=12, fontweight="bold"
        )

    ax.set_xlabel("Volume (cm³)", fontsize=12)
    ax.set_ylabel("Pressure (kPa)", fontsize=12)
    ax.set_title(
        "Air Standard Otto Cycle P–V Diagram",
        fontsize=14, fontweight="bold"
    )
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend()
    fig.tight_layout()

    st.pyplot(fig)

    with st.expander("📚 Engineering Formulas Used"):
        st.markdown(r"""
### Displacement Volume
\[
V_d = \frac{\pi}{4}D^2L
\]

### Clearance Volume
\[
V_c = \frac{V_d}{r-1}
\]

### Compression Ratio
\[
r = \frac{V_1}{V_2}
\]

### Isentropic Compression
\[
T_2 = T_1r^{\gamma-1}
\]
\[
P_2 = P_1r^\gamma
\]

### Constant Volume Heat Addition
\[
\frac{P_3}{P_2}=\frac{T_3}{T_2}
\]

### Isentropic Expansion
\[
T_4 = \frac{T_3}{r^{\gamma-1}}
\]
\[
P_4 = \frac{P_3}{r^\gamma}
\]

### Otto Cycle Thermal Efficiency
\[
\eta = 1-\frac{1}{r^{\gamma-1}}
\]

### Heat Supplied
\[
Q_{in}=C_v(T_3-T_2)
\]

### Heat Rejected
\[
Q_{out}=C_v(T_4-T_1)
\]

### Net Work
\[
W_{net}=Q_{in}-Q_{out}
\]

### Mean Effective Pressure
\[
MEP=\frac{W_{net}}{V_d}
\]

### Assumptions
- Air-standard Otto cycle
- Ideal gas
- Constant specific heats
- \(\gamma=1.4\)
- \(R=287\ J/(kg\cdot K)\)
- \(C_v=717.5\ J/(kg\cdot K)\)
""")

    st.subheader("💡 Engineering Interpretation")
    st.write(
        f"For the selected compression ratio of **{compression_ratio:.2f}**, "
        f"the calculated air-standard Otto cycle thermal efficiency is "
        f"**{efficiency * 100:.2f}%**. The calculated mean effective pressure "
        f"is **{MEP_kPa:.2f} kPa**, and the net work is **{Wnet:.2f} J/kg**."
    )

    st.info(
        "For the ideal air-standard Otto cycle, increasing compression ratio "
        "increases thermal efficiency."
    )

    st.divider()
    st.caption(
        "Mechanical Engineering Project | "
        "Air Standard Otto Cycle Efficiency & P–V Diagram Plotter"
    )
else:
    st.warning("Please correct the input values to perform the calculation.")
