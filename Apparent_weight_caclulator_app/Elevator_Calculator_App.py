import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

st.set_page_config(layout="wide")

BASE_DIR = Path(__file__).parent

def svg_to_uri(path):
    svg_path = BASE_DIR / path
    svg = svg_path.read_text(encoding="utf-8")
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{b64}"


st.markdown(
    "<h1 style='text-align: center;'>Apparent Weight in an Elevator</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: grey;'>An interactive physics simulator by Sidh Raval :3</p>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1, 2, 1])

#====================================================
# Right side inputs
with col1:
    st.header("Options")

    input_mode = st.radio('Input type?', ['Slider','Manual'], horizontal= True)

    gravity = st.selectbox(
        "Gravity Preset",
        ['Earth', 'Moon', 'Mars', 'Custom']
    )
    if gravity == 'Earth':
        g = 9.8
    elif gravity == "Moon":
        g = 1.62
    elif gravity == "Mars":
        g = 3.71
    else:
        g = st.number_input("Custom gravity (m/s²)", min_value=0.0, value=9.8, step=0.1)

    if input_mode == 'Slider':
        mass = st.slider("Mass (kg)", 1.0, 200.0, 100.0, 1.0)
        a = st.slider("Acceleration (m/s²)", -10.0, 10.0, 0.0, 0.1)
    elif input_mode == "Manual":
        mass = st.number_input("Mass (kg)", min_value = 0.1, max_value= 200.0, value= 60.0, step = 1.0)
        a = st.number_input("Acceleration (m/s²)", min_value=-10.0, max_value= 10.0, value= 0.0, step = 0.5)
    
#=======================================================================
#Calculations:
normal_weight = mass*g
normal_mass = mass
apparent_weight = mass * (g + a)
apparent_mass = (mass * (g + a) ) / g

elevator = svg_to_uri("Elevator sprite.svg")

if g + a <= 0:
    person = svg_to_uri("dummy_free-fall.svg")
elif a > 1.5:
    person = svg_to_uri("dummy_crouched.svg")
else:
    person = svg_to_uri("dummy_normal.svg")

if apparent_weight < 0:
    displayed_weight = 0.0
else:
    displayed_weight = apparent_weight

if apparent_mass < 0:
    displayed_mass = 0.0
else:
    displayed_mass = apparent_mass

line_height = max(24, abs(a) * 16)
line_duration = max(0.25, 1.0 - abs(a) * 0.06)
line_opacity = 0 if abs(a) < 0.05 else 0.7
line_animation = "none" if abs(a) < 0.05 else ("scrollUp" if a < 0 else "scrollDown")

#=======================================================================
#Column 2 Animation
html = f"""
<div style="
    position: relative;
    width: 300px;
    height: 360px;
    margin: auto;
">
<div class="line lineA line1"></div>
<div class="line lineA line2"></div>
<div class="line lineA line3"></div>

<div class="line lineB line4"></div>
<div class="line lineB line5"></div>
<div class="line lineB line6"></div>

    <!-- Elevator -->
    <img src="{elevator}" style="
    position: absolute;
    width: 600px;
    left: 50%;
    top: 50px;
    transform: translateX(-50%);
    z-index: 1;
">
    <!-- Person -->
<img src="{person}" style="
    position: absolute;
    left: 50%;
    top: 30px;
    transform: translateX(-50%);
    height: 450px;
    z-index: 2;
    transition: all 0.3s ease;
">


    <style>
    .line {{
        position: absolute;
        width: 4px;
        height: {line_height}px;
        border-radius: 999px;
        background: rgba(100, 116, 139, {line_opacity});
        animation: {line_animation} {line_duration}s linear infinite;
    }}

    .line1 {{ left: 0px;  top: 0px;   animation-delay: 0s; }}
    .line2 {{ left: 75px;  top: 35px;  animation-delay: 0.12s; }}
    .line3 {{ left: 150px;  top: 75px;  animation-delay: 0.24s; }}
    .line4 {{ left: 240px; top: 20px;  animation-delay: 0.36s; }}
    .line5 {{ left: 300px; top: 100px; animation-delay: 0.48s; }}
    .line6 {{ left: 40px;  top: 400px; animation-delay: 0.60s; }}

    @keyframes scrollDown {{
        from {{ transform: translateY(-260px); }}
        to   {{ transform: translateY(260px); }}
    }}

    @keyframes scrollUp {{
        from {{ transform: translateY(260px); }}
        to   {{ transform: translateY(-260px); }}
    }}
    </style>
</div>
"""

with col2:
    components.html(html, height=520)
#=======================================================================
#Left side outputs
with col3:
    st.header("Results")

    st.metric("Gravity (m/s²):", f"{g:.2f}")
    st.metric("Normal Weight (N):", f"{normal_weight:.2f}")
    st.metric("Apparent Weight (N):", f"{displayed_weight:.2f}")
    st.metric("Normal Mass (kg):", f"{normal_mass:.2f}")
    st.metric("Apparent Mass (kg):", f"{apparent_mass:.2f}")

    if apparent_weight < 0:
        st.error("No contact with the floor(Free-fall).")
    elif a > 0:
        st.success("Apparent weight is greater than normal weight.")
    elif a == 0:
        st.info("Apparent weight is equal to normal weight.")
    elif a < 0:
        st.warning("Apparent weight is less than normal weight.")

    st.subheader("Formula")
    st.latex(r"F_\text{apparent} = m(g + a)")

    if gravity != "Custom":
        st.write(f"Selected planet/body: **{gravity}**")
