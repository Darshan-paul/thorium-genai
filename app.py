# app.py
import streamlit as st
import openai
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# Load OpenAI API key
# -------------------------------
openai.api_key = st.secrets["OPENAI_API_KEY"]

# -------------------------------
# Knowledge Assistant Tab
# -------------------------------
def knowledge_assistant():
    st.header("🔬 Thorium Knowledge Assistant")

    user_question = st.text_input("Ask me anything about thorium or clean energy:")

    if user_question:
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions about thorium, nuclear reactors, clean energy, and India's energy future."},
                    {"role": "user", "content": user_question},
                ],
            )
            st.success(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error: {e}")

# -------------------------------
# Reactor Simulator Tab (Simple demo)
# -------------------------------
def reactor_simulator():
    st.header("⚛️ Thorium Reactor Simulator (Demo)")

    # Reactor parameters
    fuel_input = st.slider("Thorium Fuel Load (tons)", 1, 100, 20)
    efficiency = st.slider("Reactor Efficiency (%)", 30, 60, 45)
    run_time = st.slider("Operational Years", 1, 40, 20)

    # Simple calculation
    energy_output = fuel_input * efficiency * run_time * 10  # arbitrary formula for demo

    st.subheader("🔋 Estimated Energy Output")
    st.write(f"**{energy_output:,} GWh** over {run_time} years")

    # Simple chart
    years = np.arange(1, run_time + 1)
    yearly_output = fuel_input * efficiency * 10
    plt.plot(years, yearly_output * np.ones_like(years))
    plt.title("Yearly Energy Output (GWh)")
    plt.xlabel("Year")
    plt.ylabel("Energy (GWh)")
    st.pyplot(plt)

# -------------------------------
# Policy & Impact Simulator Tab
# -------------------------------
def policy_simulator():
    st.header("🌍 Policy & Impact Simulator")

    adoption_rate = st.slider("EV Adoption by 2035 (%)", 0, 100, 50)
    thorium_share = st.slider("Thorium Share in Energy Mix (%)", 0, 100, 30)

    # Simple CO₂ savings model
    baseline_co2 = 1000  # MtCO2/year (dummy baseline)
    savings = (adoption_rate * 0.5 + thorium_share * 0.8)  # arbitrary weights
    co2_reduction = baseline_co2 * (savings / 100)

    st.subheader("🌱 Estimated CO₂ Reduction")
    st.write(f"By 2035, projected savings: **{co2_reduction:.1f} MtCO₂/year**")

    # Pie chart of energy mix
    labels = ["Thorium", "Other Clean", "Fossil"]
    sizes = [thorium_share, 40, 100 - thorium_share - 40]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%")
    st.pyplot(fig)

# -------------------------------
# Main App
# -------------------------------
st.set_page_config(page_title="Thorium GenAI", layout="wide")

st.title("⚡ Thorium GenAI – India's Clean Energy Future")

tab1, tab2, tab3 = st.tabs([
    "🔬 Knowledge Assistant",
    "⚛️ Reactor Simulator",
    "🌍 Policy Simulator"
])

with tab1:
    knowledge_assistant()

with tab2:
    reactor_simulator()

with tab3:
    policy_simulator()
