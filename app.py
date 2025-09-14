# app.py - Advanced Thorium GenAI Platform (debugged + resilient)
import streamlit as st
import openai
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
import os
import json
from datetime import datetime



# Page config - MUST be before any Streamlit UI calls
# ========================
st.set_page_config(
    page_title="Thorium GenAI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================
# Optional custom modules (safe fallbacks)
# ========================
try:
    from auth import check_auth, show_logout_button, get_current_user, auth_manager
except Exception as e:
    # Fallback stub implementations so the app won't crash
    st.error(f"Authentication module failed to load: {e}")
    def check_auth():
        st.error("Authentication system not available. Please check the auth.py file.")
        return False

    def show_logout_button():
        return None

    def get_current_user():
        return None

    class auth_manager:
        @staticmethod
        def save_simulation(user_id, sim_type, params, results):
            pass

        @staticmethod
        def get_user_simulations(user_id):
            return []

try:
    from database import db_manager
except Exception:
    class db_manager:
        @staticmethod
        def log_analytics(user_id, event, source, session_id, payload=None):
            pass

        @staticmethod
        def save_user_preference(user_id, key, value):
            pass

        @staticmethod
        def get_export_history(user_id):
            return []

        @staticmethod
        def get_user_stats(user_id):
            return {"simulation_count": 0, "export_count": 0, "favorite_simulation": "None"}

        @staticmethod
        def get_user_stats_display(user_id):
            st.write("User stats placeholder")

try:
    from export_utils import show_export_options, prepare_simulation_data, export_manager
except Exception:
    def show_export_options(user_id, data, tag):
        st.info("Export options placeholder")

    def prepare_simulation_data(tag, params, results):
        return {"params": params, "results": results}

    class export_manager:
        pass

try:
    from realtime_data import show_realtime_dashboard, show_realtime_insights
except Exception:
    def show_realtime_dashboard():
        st.info("Realtime dashboard placeholder")

    def show_realtime_insights():
        st.info("Realtime insights placeholder")

try:
    from mobile_styles import optimize_for_mobile, show_mobile_navigation, create_mobile_friendly_metrics
except Exception:
    def optimize_for_mobile():
        pass

    def show_mobile_navigation():
        pass

    def create_mobile_friendly_metrics():
        pass

# ========================
# Load OpenAI API key (non-fatal)
# ========================
api_key = os.getenv("OPENAI_API_KEY") or (st.secrets.get("OPENAI_API_KEY") if hasattr(st, "secrets") else None)
if api_key:
    try:
        openai.api_key = api_key
    except Exception:
        # don't crash; API might be set differently
        pass
else:
    # Non-fatal warning: features depending on OpenAI will show an error on use
    if not st.session_state.get("openai_missing_warning_shown", False):
        st.warning("⚠️ OPENAI_API_KEY not found. Knowledge Assistant will be disabled until you add a key to Streamlit Secrets or set OPENAI_API_KEY as an environment variable.")
        st.session_state["openai_missing_warning_shown"] = True

# ========================
# Custom CSS for professional styling (kept from your original)
# ========================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main theme colors */
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #ff7f0e;
        --success-color: #2ca02c;
        --warning-color: #d62728;
        --background-color: #f8f9fa;
        --card-background: #ffffff;
        --text-primary: #2c3e50;
        --text-secondary: #6c757d;
        --border-color: #e9ecef;
        --shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Global styles */
    .main {
        font-family: 'Inter', sans-serif;
        background-color: var(--background-color);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: var(--shadow);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Card styling */
    .metric-card {
        background: var(--card-background);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: var(--shadow);
        border-left: 4px solid var(--primary-color);
        margin: 1rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: var(--background-color);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        padding: 0.75rem 1.25rem;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        min-width: 200px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        white-space: nowrap;
        border: 2px solid transparent;
        position: relative;
        overflow: hidden;
    }
    
    /* Ensure tab text is visible */
    .stTabs [data-baseweb="tab"] span {
        display: inline-block;
        margin-left: 0.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1f77b4 0%, #ff7f0e 100%);
        color: white;
        box-shadow: 0 6px 20px rgba(31, 119, 180, 0.4);
        border-color: #1f77b4;
        transform: translateY(-1px);
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [aria-selected="true"]:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(255,255,255,0.1) 100%);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(31, 119, 180, 0.15);
        transform: translateY(-2px);
        border-color: rgba(31, 119, 180, 0.3);
        box-shadow: 0 4px 15px rgba(31, 119, 180, 0.2);
        transform: translateY(-1px);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: var(--primary-color);
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stError {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Loading spinner */
    .spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid var(--primary-color);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Ensure all text is visible */
    .stButton > button {
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    
    /* Make sure sidebar text is visible with enhanced highlighting */
    .sidebar .stButton > button {
        width: 100%;
        margin: 0.25rem 0;
        text-align: left;
        padding: 0.75rem 1rem;
        border: 2px solid transparent;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .sidebar .stButton > button:hover {
        transform: translateX(5px);
        border-color: rgba(31, 119, 180, 0.3);
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.2);
    }
    
    .sidebar .stButton > button:active {
        background: linear-gradient(135deg, #1f77b4 0%, #ff7f0e 100%);
        transform: translateX(3px);
    }
    
    /* Ensure metric labels are visible */
    .metric-label {
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
    }
    
    /* Make sure all headings have proper spacing */
    h1, h2, h3, h4, h5, h6 {
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ========================
# Helper: safe OpenAI chat call
# ========================
def call_openai_chat(messages, model="gpt-3.5-turbo", max_tokens=700, temperature=0.2):
    if not (openai and getattr(openai, "api_key", None)):
        raise RuntimeError("OpenAI API key not configured.")
    client = openai.OpenAI(api_key=openai.api_key)
    resp = client.chat.completions.create(model=model, messages=messages, max_tokens=max_tokens, temperature=temperature)
    return resp

# ========================
# Knowledge Assistant Tab
# ========================
def knowledge_assistant(user_id=None):
    st.markdown('<div class="main-header"><h1>🔬 Thorium Knowledge Assistant</h1><p>Ask intelligent questions about thorium, nuclear energy, and India\'s clean energy future</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Ask Your Question")
        user_question = st.text_area(
            "What would you like to know about thorium or clean energy?",
            placeholder="e.g., How does thorium-based nuclear energy work? What are the benefits for India's energy security?",
            height=100
        )
        
        if st.button("🚀 Get Expert Answer"):
            if not user_question:
                st.warning("⚠️ Please enter a question first!")
            else:
                if not (openai and getattr(openai, "api_key", None)):
                    st.error("OpenAI API key missing — Knowledge Assistant disabled. Add OPENAI_API_KEY in Streamlit Secrets or environment.")
                else:
                    with st.spinner("🧠 Analyzing your question and generating expert response..."):
                        try:
                            messages = [
                                {"role": "system", "content": "You are a nuclear energy expert and thorium specialist. Provide detailed, accurate, and accessible answers about thorium-based reactors and India's energy future."},
                                {"role": "user", "content": user_question},
                            ]
                            resp = call_openai_chat(messages, model="gpt-3.5-turbo")
                            answer = resp.choices[0].message.content

                            st.markdown("### 📋 Expert Response")
                            st.markdown(f"""
                            <div class="metric-card">
                                <div style="font-size: 1.1rem; line-height: 1.6; color: var(--text-primary);">
                                    {answer}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                            # Save conversation if user is logged in
                            try:
                                if user_id:
                                    conversation_data = {
                                        "question": user_question,
                                        "answer": answer,
                                        "timestamp": datetime.now().isoformat()
                                    }
                                    auth_manager.save_simulation(user_id, "knowledge_assistant", {"question": user_question}, conversation_data)
                                    db_manager.log_analytics(user_id, "ai_question_asked", "knowledge_assistant", st.session_state.get('session_id', 'unknown'), {"question_length": len(user_question)})
                            except Exception:
                                pass

                        except Exception as e:
                            st.error(f"❌ Error calling OpenAI: {e}")
    
    with col2:
        st.markdown("### 📊 Quick Facts")
        
        # Sample metrics cards
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">4x</div>
            <div class="metric-label">More Abundant</div>
            <p style="font-size: 0.8rem; margin: 0.5rem 0 0 0; color: var(--text-secondary);">Thorium vs Uranium reserves</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">70%</div>
            <div class="metric-label">Less Waste</div>
            <p style="font-size: 0.8rem; margin: 0.5rem 0 0 0; color: var(--text-secondary);">Compared to traditional reactors</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">3-4</div>
            <div class="metric-label">Years</div>
            <p style="font-size: 0.8rem; margin: 0.5rem 0 0 0; color: var(--text-secondary);">Average construction time</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sample questions
        st.markdown("### 💡 Sample Questions")
        st.markdown("*Click on any question below to use it:*")
        
        sample_questions = [
            "How do thorium reactors differ from uranium reactors?",
            "What is India's thorium program timeline?",
            "How safe are thorium-based nuclear plants?",
            "What are the economic benefits of thorium energy?"
        ]
        
        for i, question in enumerate(sample_questions, 1):
            if st.button(f"❓ {question}", key=f"sample_{i}", help=f"Click to use this question"):
                st.session_state.sample_question = question
                st.rerun()
        
        if 'sample_question' in st.session_state:
            st.text_area("Selected question:", value=st.session_state.sample_question, key="sample_input")
            if st.button("Ask This Question"):
                # copy sample question to main input and trigger run
                st.session_state['sample_to_ask'] = st.session_state['sample_question']
                st.rerun()

# ========================
# Reactor Simulator Tab
# ========================
def reactor_simulator(user_id=None):
    st.markdown('<div class="main-header"><h1>⚛️ Thorium Reactor Simulator</h1><p>Interactive simulation of thorium-based nuclear reactor performance and energy output</p></div>', unsafe_allow_html=True)
    
    # Create columns for better layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### ⚙️ Reactor Parameters")
        
        # Reactor parameters with better styling
        fuel_input = st.slider("Thorium Fuel Load (tons)", 1, 100, 20, help="Amount of thorium fuel loaded into the reactor")
        efficiency = st.slider("Reactor Efficiency (%)", 30, 60, 45, help="Thermal efficiency of the reactor system")
        run_time = st.slider("Operational Years", 1, 40, 20, help="Expected operational lifetime")
        capacity_factor = st.slider("Capacity Factor (%)", 70, 95, 85, help="Percentage of time reactor operates at full power")
        
        # Additional parameters
        st.markdown("### 🔧 Advanced Settings")
        cooling_system = st.selectbox("Cooling System", ["Liquid Sodium", "Molten Salt", "Helium Gas"], index=1)
        reactor_type = st.selectbox("Reactor Type", ["Fast Breeder", "Molten Salt", "Heavy Water"], index=1)
        
        # Calculate outputs
        # Convert percents into fractions correctly
        yearly_output = fuel_input * (efficiency/100.0) * (capacity_factor/100.0) * 1000  # demo scale (GWh-ish)
        total_output = yearly_output * run_time
        co2_saved = total_output * 0.4  # placeholder metric
        
        # Prepare simulation data for saving
        simulation_parameters = {
            "fuel_input": fuel_input,
            "efficiency": efficiency,
            "run_time": run_time,
            "capacity_factor": capacity_factor,
            "cooling_system": cooling_system,
            "reactor_type": reactor_type
        }
        
        simulation_results = {
            "yearly_output": yearly_output,
            "total_output": total_output,
            "co2_saved": co2_saved,
            "fuel_utilization": (efficiency * capacity_factor / 10000.0),
            "cost_per_mwh": 45 + (100-fuel_input)*0.5
        }
        
        # Display key metrics
        st.markdown("### 📊 Key Metrics")
        
        metric_col1, metric_col2 = st.columns(2)
        
        with metric_col1:
            st.metric("Total Energy Output (approx)", f"{total_output:,.0f}", delta=f"{yearly_output:,.0f}/yr")
            st.metric("CO₂ Emissions Saved (approx)", f"{co2_saved:,.0f}", delta="Estimated")
        
        with metric_col2:
            st.metric("Fuel Utilization", f"{simulation_results['fuel_utilization']:.2%}", delta="Utilization")
            st.metric("Cost per MWh", f"₹{simulation_results['cost_per_mwh']:.0f}", delta="Estimate")
    
    with col2:
        st.markdown("### 📈 Performance Analytics")
        
        # Create interactive Plotly charts (correctly indented)
        years = np.arange(1, run_time + 1)
        cumulative_output = np.cumsum([yearly_output] * run_time)
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Yearly Energy Output', 'Cumulative Energy Output', 'Efficiency Trends', 'Cost Analysis'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Yearly output chart
        fig.add_trace(
            go.Scatter(x=years, y=[yearly_output] * run_time, 
                      mode='lines+markers', name='Yearly Output',
                      line=dict(color='#1f77b4', width=3),
                      marker=dict(size=8)),
            row=1, col=1
        )
        
        # Cumulative output chart
        fig.add_trace(
            go.Scatter(x=years, y=cumulative_output,
                      mode='lines+markers', name='Cumulative Output',
                      line=dict(color='#ff7f0e', width=3),
                      marker=dict(size=8)),
            row=1, col=2
        )
        
        # Efficiency trends (simulated)
        efficiency_trend = [efficiency + float(np.random.normal(0, 2)) for _ in years]
        fig.add_trace(
            go.Scatter(x=years, y=efficiency_trend,
                      mode='lines+markers', name='Efficiency',
                      line=dict(color='#2ca02c', width=3),
                      marker=dict(size=8)),
            row=2, col=1
        )
        
        # Cost analysis
        cost_per_mwh = [simulation_results['cost_per_mwh'] + float(np.random.normal(0, 1)) for _ in years]
        fig.add_trace(
            go.Scatter(x=years, y=cost_per_mwh,
                      mode='lines+markers', name='Cost/MWh',
                      line=dict(color='#d62728', width=3),
                      marker=dict(size=8)),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=600,
            showlegend=False,
            title_text="Thorium Reactor Performance Dashboard",
            title_x=0.5,
            font=dict(family="Inter", size=12)
        )
        
        # Update x and y axis labels
        fig.update_xaxes(title_text="Years", row=2, col=1)
        fig.update_xaxes(title_text="Years", row=2, col=2)
        fig.update_yaxes(title_text="Efficiency (%)", row=2, col=1)
        fig.update_yaxes(title_text="Cost (₹/MWh)", row=2, col=2)
        fig.update_yaxes(title_text="Energy (GWh)", row=1, col=1)
        fig.update_yaxes(title_text="Energy (GWh)", row=1, col=2)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional insights
        st.markdown("### 💡 Insights & Recommendations")
        
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            if efficiency > 50:
                st.success("✅ High Efficiency: Excellent thermal efficiency for clean energy production")
            else:
                st.warning("⚠️ Moderate Efficiency: Consider optimizing reactor design")
                
            if fuel_input > 50:
                st.info("🔋 High Fuel Load: Optimal for long-term energy security")
            else:
                st.info("🔋 Standard Fuel Load: Adequate for current requirements")
        
        with insight_col2:
            if capacity_factor > 85:
                st.success("⚡ High Availability: Excellent operational reliability")
            else:
                st.warning("⚡ Standard Availability: Room for operational improvements")
                
            if cooling_system == "Molten Salt":
                st.success("🧪 Advanced Cooling: Best safety and efficiency profile")
            else:
                st.info("🧪 Standard Cooling: Reliable and proven technology")
        
        # Save simulation and export options
        st.markdown("---")
        
        save_col, export_col = st.columns(2)
        
        with save_col:
            if st.button("💾 Save Reactor Simulation", help="Save your reactor simulation parameters and results"):
                if user_id:
                    try:
                        auth_manager.save_simulation(user_id, "reactor", simulation_parameters, simulation_results)
                        st.success("Reactor simulation saved successfully!")
                        db_manager.log_analytics(user_id, "simulation_saved", "reactor", st.session_state.get('session_id', 'unknown'), simulation_parameters)
                    except Exception:
                        st.error("Save failed (placeholder).")
                else:
                    st.error("Please login to save simulations")
        
        with export_col:
            if st.button("📊 Export Simulation Results", help="Export your simulation data as PDF, Excel, or JSON"):
                if user_id:
                    export_data = prepare_simulation_data("reactor", simulation_parameters, simulation_results)
                    show_export_options(user_id, export_data, "reactor")
                else:
                    st.error("Please login to export data")

# ========================
# Policy & Impact Simulator Tab
# ========================
def policy_simulator(user_id=None):
    st.markdown('<div class="main-header"><h1>🌍 Policy & Impact Simulator</h1><p>Analyze the environmental and economic impact of thorium energy adoption in India</p></div>', unsafe_allow_html=True)
    
    # Create columns for layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🎛️ Policy Parameters")
        
        # Policy sliders with better organization
        st.markdown("#### 🚗 Transportation Sector")
        ev_adoption = st.slider("EV Adoption by 2035 (%)", 0, 100, 50, help="Percentage of vehicles that will be electric by 2035")
        public_transport = st.slider("Public Transport Enhancement (%)", 0, 100, 30, help="Improvement in public transportation infrastructure")
        
        st.markdown("#### ⚡ Energy Sector")
        thorium_share = st.slider("Thorium Share in Energy Mix (%)", 0, 100, 30, help="Percentage of energy from thorium-based nuclear")
        renewable_share = st.slider("Renewable Energy Share (%)", 0, 100, 25, help="Percentage from solar, wind, hydro")
        
        st.markdown("#### 🏭 Industrial Sector")
        industrial_efficiency = st.slider("Industrial Efficiency Gains (%)", 0, 50, 20, help="Energy efficiency improvements in industry")
        carbon_capture = st.slider("Carbon Capture Technology (%)", 0, 30, 10, help="Percentage of emissions captured")
        
        # Calculate comprehensive impact
        baseline_co2 = 3500  # MtCO2/year (India's current baseline)
        
        # More sophisticated calculation
        transport_savings = ev_adoption * 0.4 + public_transport * 0.3
        energy_savings = thorium_share * 0.6 + renewable_share * 0.4
        industrial_savings = industrial_efficiency * 0.5 + carbon_capture * 0.8
        
        total_savings = (transport_savings + energy_savings + industrial_savings) / 3
        co2_reduction = baseline_co2 * (total_savings / 100)
        
        # Economic benefits
        energy_cost_savings = thorium_share * 2.5  # Billion USD per year
        job_creation = (thorium_share + renewable_share) * 0.8  # Million jobs
        
        # Prepare simulation data for saving
        policy_parameters = {
            "ev_adoption": ev_adoption,
            "public_transport": public_transport,
            "thorium_share": thorium_share,
            "renewable_share": renewable_share,
            "industrial_efficiency": industrial_efficiency,
            "carbon_capture": carbon_capture
        }
        
        policy_results = {
            "co2_reduction": co2_reduction,
            "energy_cost_savings": energy_cost_savings,
            "job_creation": job_creation,
            "total_savings": total_savings,
            "transport_savings": transport_savings,
            "energy_savings": energy_savings,
            "industrial_savings": industrial_savings
        }
        
        # Display key metrics
        st.markdown("### 📊 Impact Metrics")
        
        st.metric("CO₂ Reduction", f"{co2_reduction:,.0f} MtCO₂/year", delta=f"{total_savings:.1f}% reduction")
        st.metric("Energy Cost Savings", f"${energy_cost_savings:,.1f}B/year", delta="Economic Benefit")
        st.metric("Jobs Created", f"{job_creation:.1f}M", delta="Employment Impact")
        
        # Policy recommendations
        st.markdown("### 💡 Policy Recommendations")
        
        if thorium_share < 20:
            st.warning("⚠️ Low Thorium Adoption: Consider increasing thorium energy investment")
        elif thorium_share > 40:
            st.success("✅ High Thorium Adoption: Excellent for energy security and emissions reduction")
        else:
            st.info("📈 Moderate Thorium Adoption: Good progress, room for expansion")
            
        if ev_adoption < 30:
            st.warning("🚗 Low EV Adoption: Need stronger EV incentives and infrastructure")
        else:
            st.success("🚗 Good EV Adoption: Strong progress in transportation electrification")
    
    with col2:
        st.markdown("### 📈 Impact Visualization")
        
        # Create comprehensive dashboard
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Energy Mix 2035', 'CO₂ Emissions Trend', 'Economic Benefits', 'Sectoral Impact'),
            specs=[[{"type": "pie"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Energy mix pie chart
        energy_labels = ["Thorium", "Renewables", "Fossil Fuels", "Other Nuclear"]
        energy_values = [thorium_share, renewable_share, 
                        max(0, 100 - thorium_share - renewable_share - 10), 10]
        colors = ['#1f77b4', '#2ca02c', '#d62728', '#ff7f0e']
        
        fig.add_trace(
            go.Pie(labels=energy_labels, values=energy_values, 
                  marker_colors=colors, textinfo='label+percent'),
            row=1, col=1
        )
        
        # CO₂ emissions trend
        years_plot = [2024, 2025, 2030, 2035]
        current_emissions = [baseline_co2, baseline_co2 * 1.05, baseline_co2 * 1.1, baseline_co2 * 1.15]
        projected_emissions = [baseline_co2, baseline_co2 * 0.98, baseline_co2 * 0.85, baseline_co2 * (1 - total_savings/100)]
        
        fig.add_trace(
            go.Scatter(x=years_plot, y=current_emissions, mode='lines+markers', 
                      name='Business as Usual', line=dict(color='#d62728', width=3)),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=years_plot, y=projected_emissions, mode='lines+markers', 
                      name='With Thorium Policy', line=dict(color='#2ca02c', width=3)),
            row=1, col=2
        )
        
        # Economic benefits
        benefit_categories = ['Energy Savings', 'Job Creation', 'Health Benefits', 'Technology Export']
        benefit_values = [energy_cost_savings, job_creation * 2, thorium_share * 1.5, renewable_share * 0.8]
        
        fig.add_trace(
            go.Bar(x=benefit_categories, y=benefit_values, 
                  marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd']),
            row=2, col=1
        )
        
        # Sectoral impact
        sectors = ['Transport', 'Energy', 'Industry', 'Buildings']
        sector_impact = [transport_savings, energy_savings, industrial_savings, (transport_savings + energy_savings) / 2]
        
        fig.add_trace(
            go.Bar(x=sectors, y=sector_impact, 
                  marker_color=['#17becf', '#bcbd22', '#e377c2', '#8c564b']),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=700,
            showlegend=True,
            title_text="India's Clean Energy Transition Dashboard",
            title_x=0.5,
            font=dict(family="Inter", size=12)
        )
        
        # Update axis labels
        fig.update_xaxes(title_text="Year", row=1, col=2)
        fig.update_yaxes(title_text="CO₂ Emissions (MtCO₂)", row=1, col=2)
        fig.update_yaxes(title_text="Economic Value (Billion USD)", row=2, col=1)
        fig.update_yaxes(title_text="Impact Score", row=2, col=2)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional insights
        st.markdown("### 🎯 Strategic Insights")
        
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            if total_savings > 30:
                st.success("🎉 Excellent Impact: Strong environmental and economic benefits projected")
            elif total_savings > 15:
                st.info("📈 Good Impact: Solid progress towards clean energy goals")
            else:
                st.warning("⚠️ Limited Impact: Consider more aggressive policy measures")
        
        with insight_col2:
            if thorium_share + renewable_share > 60:
                st.success("🌱 Clean Energy Leader: India positioned as clean energy leader")
            else:
                st.info("🌱 Clean Energy Progress: Good foundation, potential for more")
        
        # Policy timeline
        st.markdown("### 📅 Recommended Policy Timeline")
        
        timeline_data = {
            "Phase": ["2024-2026", "2026-2030", "2030-2035"],
            "Focus": ["Foundation", "Scale-up", "Optimization"],
            "Key Actions": [
                "Establish thorium research facilities, EV charging infrastructure",
                "Deploy thorium reactors, expand renewable capacity",
                "Achieve energy independence, export clean tech"
            ]
        }
        
        timeline_df = pd.DataFrame(timeline_data)
        st.dataframe(timeline_df, use_container_width=True, hide_index=True)
        
        # Save simulation and export options
        st.markdown("---")
        
        c1, c2 = st.columns(2)
        
        with c1:
            if st.button("💾 Save Policy Analysis", help="Save your policy simulation parameters and results"):
                if user_id:
                    try:
                        auth_manager.save_simulation(user_id, "policy", policy_parameters, policy_results)
                        st.success("Policy analysis saved successfully!")
                        db_manager.log_analytics(user_id, "simulation_saved", "policy", st.session_state.get('session_id', 'unknown'), policy_parameters)
                    except Exception:
                        st.error("Save failed (placeholder).")
                else:
                    st.error("Please login to save analyses")
        
        with c2:
            if st.button("📊 Export Policy Analysis", help="Export your policy analysis data as PDF, Excel, or JSON"):
                if user_id:
                    export_data = prepare_simulation_data("policy", policy_parameters, policy_results)
                    show_export_options(user_id, export_data, "policy")
                else:
                    st.error("Please login to export data")

# ========================
# Main App with Authentication
# ========================

# Apply mobile optimization (safe stub)
optimize_for_mobile()

# Check authentication - if not authenticated, show login page and stop
if not check_auth():
    st.stop()  # This will stop the app execution and only show the login page

# Get current user (only reached if authentication is successful)
current_user = get_current_user()
user_id = current_user.get('id') if isinstance(current_user, dict) else None

# Sidebar with user info and features
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h2 style="color: white; margin: 0;">⚡ Thorium GenAI</h2>
        <p style="color: white; opacity: 0.8; margin: 0.5rem 0;">India's Clean Energy Future</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User info
    if current_user:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <p style="color: white; margin: 0;"><strong>👤 {current_user.get('username','User')}</strong></p>
            <p style="color: white; opacity: 0.8; margin: 0; font-size: 0.9rem;">Role: {current_user.get('role','guest')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # User stats display if available
        try:
            from database import get_user_stats_display
            get_user_stats_display(user_id)
        except Exception:
            pass
    
    st.markdown("---")
    
    # App info
    st.markdown("### 📖 About This App")
    st.info("""
    **Thorium GenAI** is an interactive platform for exploring thorium-based nuclear energy solutions for India's clean energy transition.
    
    - 🔬 Knowledge Assistant
    - ⚛️ Reactor Simulator
    - 🌍 Policy Simulator
    - 🌐 Real-time Data
    """)
    
    st.markdown("### 🎯 Key Benefits")
    st.markdown("""
    - Energy Security: 4x more thorium than uranium reserves
    - Clean Energy: 70% less nuclear waste
    - Economic Growth: Job creation and technology export
    - Climate Action: Significant CO₂ emissions reduction
    """)
    
    st.markdown("---")
    
    # Settings
    st.markdown("### ⚙️ Settings")
    theme = st.selectbox("Theme", ["Default", "Dark Mode", "High Contrast"], index=0)
    language = st.selectbox("Language", ["English", "Hindi", "Tamil", "Telugu"], index=0)
    if st.button("💾 Save Preferences"):
        try:
            db_manager.save_user_preference(user_id, "app_preferences", {"theme": theme, "language": language})
            st.success("Preferences saved!")
        except Exception:
            st.info("Preferences saved (demo)")
    
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    if st.button("📊 View Analytics Dashboard"):
        st.session_state.show_analytics = True

    if st.button("📈 View Export History"):
        exports = db_manager.get_export_history(user_id)
        if exports:
            st.write("Recent exports:")
            for export in exports[:5]:
                st.write(f"• {export[0]} - {export[1]} ({export[2][:10]})")
        else:
            st.info("No exports yet")

    if st.button("🧠 View Simulation History"):
        try:
            simulations = auth_manager.get_user_simulations(user_id)
        except Exception:
            simulations = []
        if simulations:
            for sim in simulations[:5]:
                st.write(f"• {sim[0]} ({sim[3][:10]})")
        else:
            st.info("No simulations yet")
    
    st.markdown("---")
    st.markdown("### 📞 Contact")
    st.markdown("""
    **Developed by:** Thorium Research Team  
    **Email:** info@thoriumgenai.com  
    **Website:** www.thoriumgenai.com
    """)
    show_logout_button()

# Main content - Welcome Dashboard
st.markdown("""
<div class="main-header">
    <h1>⚡ Thorium GenAI Dashboard</h1>
    <p>Welcome back, {username}! Explore India's Clean Energy Future through Advanced Thorium Technology</p>
</div>
""".format(username=current_user.get('username', 'User')), unsafe_allow_html=True)

# Intro block
st.markdown("""
<div style="background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 2rem;">
    <h3 style="color: #1f77b4; margin-top: 0;">🌱 Welcome to India's Thorium Energy Revolution</h3>
    <p style="font-size: 1.1rem; line-height: 1.6; color: #2c3e50;">
        India holds one of the world's largest thorium reserves, positioning us to become a global leader in clean, 
        safe, and abundant nuclear energy. This interactive platform helps you explore the potential of thorium-based 
        nuclear reactors for India's energy security and climate goals.
    </p>
    <div style="display: flex; gap: 2rem; margin-top: 1.5rem;">
        <div style="text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #1f77b4;">360,000</div>
            <div style="font-size: 0.9rem; color: #6c757d;">Tons of Thorium Reserves</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #2ca02c;">70%</div>
            <div style="font-size: 0.9rem; color: #6c757d;">Less Nuclear Waste</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #ff7f0e;">2035</div>
            <div style="font-size: 0.9rem; color: #6c757d;">Target Deployment</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Mobile navigation (stub safe)
show_mobile_navigation()

# Navigation tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔬 Knowledge Assistant",
    "⚛️ Reactor Simulator",
    "🌍 Policy Simulator",
    "🌐 Real-time Data"
])

with tab1:
    st.markdown("### 🔬 Knowledge Assistant")
    st.markdown("Ask questions about thorium-based nuclear energy and get expert AI-powered answers.")
    knowledge_assistant(user_id=user_id)

with tab2:
    st.markdown("### ⚛️ Reactor Simulator")
    st.markdown("Model and simulate thorium-based nuclear reactor performance with interactive parameters.")
    reactor_simulator(user_id=user_id)

with tab3:
    st.markdown("### 🌍 Policy Simulator")
    st.markdown("Analyze the impact of clean energy policies on India's energy landscape.")
    policy_simulator(user_id=user_id)

with tab4:
    st.markdown("### 🌐 Real-time Data Dashboard")
    st.markdown("Monitor live energy data, weather impacts, and economic indicators.")
    try:
        show_realtime_dashboard()
        st.markdown("---")
        show_realtime_insights()
    except Exception:
        st.info("Realtime data module not available (placeholder).")

# Analytics section (if requested)
if st.session_state.get('show_analytics', False):
    st.markdown("---")
    st.markdown("### 📊 User Analytics")
    try:
        db_manager.log_analytics(user_id, "analytics_view", "main_page", st.session_state.get('session_id', 'unknown'))
    except Exception:
        pass
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Usage Statistics")
        stats = db_manager.get_user_stats(user_id)
        
        # Create usage chart
        usage_data = {
            'Simulations': stats.get('simulation_count', 0),
            'Exports': stats.get('export_count', 0),
            'Days Active': 7  # placeholder
        }
        
        fig = px.bar(x=list(usage_data.keys()), y=list(usage_data.values()),
                    title="Your Activity Summary",
                    color=list(usage_data.keys()),
                    color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Recommendations")
        if stats.get('simulation_count', 0) == 0:
            st.info("🚀 Get Started: Try running your first reactor simulation!")
        elif stats.get('simulation_count', 0) < 5:
            st.success("📈 Keep Exploring")
        else:
            st.success("🏆 Expert User")
        
        if stats.get('export_count', 0) == 0:
            st.info("📊 Export Data: Try exporting your simulation results for analysis!")
        
        if stats.get('favorite_simulation', 'None') == 'None':
            st.info("🔬 Explore All Tools: Try different simulation types to find your favorite!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #6c757d;">
    <p>© 2025 Thorium GenAI. Empowering India's Clean Energy Future.</p>
    <p>Built with ❤️ for India's sustainable development</p>
    <p style="font-size: 0.8rem;">Version 2.0 - Advanced Enterprise Platform</p>
</div>
""", unsafe_allow_html=True)

