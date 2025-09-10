# app.py
import streamlit as st
import openai
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="GenAI for Thorium", layout="wide")

st.title("⚡ GenAI for Thorium: India’s Clean Energy Future")

# Sidebar for API key
openai.api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

# Tabs
tab1, tab2, tab3 = st.tabs([
    "📘 Knowledge Assistant",
    "⚛️ Reactor Simulator",
    "🌍 Policy Simulator"
])

# ---------------------------
# Tab 1: Knowledge Assistant
# ---------------------------
with tab1:
    st.header("📘 Thorium Knowledge Assistant")
    st.write("Ask any question about thorium, reactors, or clean energy.")

    query = st.text_input("Your question:")
    if st.button("Ask AI"):
        if not openai.api_key:
            st.warning("Please enter your OpenAI API key in the sidebar.")
        else:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": query}],
                    temperature=0.2
                )
                st.success(response.choices[0].message["content"])
            except Exception as e:
                st.error(f"Error: {e}")

# ---------------------------
# Tab 2: Reactor Simulator
# ---------------------------
with tab2:
    st.header("⚛️ Reactor Digital Twin Simulator (Prototype)")

    fuel_type = st.selectbox("Select Fuel Type:", ["Thorium (Th-232)", "Uranium (U-235)"])
    temperature = st.slider("Core Temperature (°C)", 300, 1200, 600)
    burnup = st.slider("Burnup (GWd/t)", 10, 120, 40)

    # Simple placeholder formulas
    if fuel_type == "Thorium (Th-232)":
        efficiency = 30 + (temperature - 300) / 100
        waste = 5 + (burnup / 50)
    else:
        efficiency = 25 + (temperature - 300) / 120
        waste = 10 + (burnup / 40)

    st.metric("Estimated Efficiency (%)", round(efficiency, 2))
    st.metric("Waste Intensity (kg/TWh)", round(waste, 2))

    # Chart
    fig, ax = plt.subplots()
    temps = list(range(300, 1201, 100))
    effs = [30 + (t - 300) / 100 if fuel_type.startswith("Thorium") else 25 + (t - 300) / 120 for t in temps]
    ax.plot(temps, effs, marker="o")
    ax.set_xlabel("Core Temperature (°C)")
    ax.set_ylabel("Efficiency (%)")
    ax.set_title(f"Efficiency vs Temperature ({fuel_type})")
    st.pyplot(fig)

# ---------------------------
# Tab 3: Policy Simulator
# ---------------------------
with tab3:
    st.header("🌍 Policy & Energy Impact Simulator")

    adoption = st.slider("Thorium Adoption by 2035 (%)", 0, 100, 10)
    capacity = st.number_input("Reactor Capacity (MW)", 100, 5000, 300)
    units = st.number_input("Number of Units", 1, 100, 5)

    annual_gen = capacity * units * 0.85 * 8760 / 1e6  # TWh
    co2_saved = annual_gen * adoption * 0.8  # Mt CO₂ avoided
    ev_supported = annual_gen * adoption * 20000  # Approx EVs

    st.metric("Annual Generation (TWh)", round(annual_gen, 2))
    st.metric("CO₂ Avoided (Mt)", round(co2_saved, 2))
    st.metric("EVs Supported", int(ev_supported))

    st.write("👉 Future: Use OpenAI to generate plain-English policy impact summaries.")

