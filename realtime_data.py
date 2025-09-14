# realtime_data.py - Real-time data integration and APIs
import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import time
import plotly.express as px
import plotly.graph_objects as go
from database import db_manager

class RealTimeDataManager:
    def __init__(self):
        self.cache_ttl = 3600  # 1 hour cache TTL
        self.api_keys = {
            'energy_api': st.secrets.get("ENERGY_API_KEY", ""),
            'weather_api': st.secrets.get("WEATHER_API_KEY", ""),
            'economic_api': st.secrets.get("ECONOMIC_API_KEY", "")
        }
    
    def get_india_energy_data(self):
        """Get real-time India energy data"""
        cache_key = "india_energy_data"
        cached_data = db_manager.get_cached_energy_data("energy", cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            # Simulate API call to real energy data source
            # In production, replace with actual API calls
            energy_data = {
                "timestamp": datetime.now().isoformat(),
                "total_generation": {
                    "thermal": 180000,  # MW
                    "hydro": 45000,
                    "nuclear": 6780,
                    "renewable": 120000,
                    "total": 351780
                },
                "demand": {
                    "peak_demand": 220000,  # MW
                    "current_demand": 195000,
                    "demand_supply_gap": 156780
                },
                "thorium_potential": {
                    "reserves": 360000,  # tons
                    "current_utilization": 0,
                    "potential_capacity": 500000  # MW
                },
                "emissions": {
                    "co2_emissions": 2500,  # MtCO2/year
                    "reduction_potential": 1800  # MtCO2/year with thorium
                }
            }
            
            # Cache the data
            db_manager.cache_energy_data("energy", cache_key, energy_data, self.cache_ttl)
            
            return energy_data
            
        except Exception as e:
            st.error(f"Error fetching energy data: {str(e)}")
            return None
    
    def get_weather_data(self, city="New Delhi"):
        """Get weather data for solar/wind energy calculations"""
        cache_key = f"weather_{city}"
        cached_data = db_manager.get_cached_energy_data("weather", cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            # Simulate weather API call
            weather_data = {
                "timestamp": datetime.now().isoformat(),
                "city": city,
                "temperature": 28.5,  # Celsius
                "humidity": 65,  # %
                "wind_speed": 12.3,  # km/h
                "solar_irradiance": 850,  # W/m²
                "cloud_cover": 30,  # %
                "renewable_potential": {
                    "solar_efficiency": 0.85,
                    "wind_efficiency": 0.75,
                    "optimal_conditions": True
                }
            }
            
            db_manager.cache_energy_data("weather", cache_key, weather_data, 1800)  # 30 min cache
            
            return weather_data
            
        except Exception as e:
            st.error(f"Error fetching weather data: {str(e)}")
            return None
    
    def get_economic_indicators(self):
        """Get economic indicators relevant to energy sector"""
        cache_key = "economic_indicators"
        cached_data = db_manager.get_cached_energy_data("economic", cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            economic_data = {
                "timestamp": datetime.now().isoformat(),
                "currency": {
                    "usd_to_inr": 83.25,
                    "eur_to_inr": 90.15
                },
                "energy_prices": {
                    "crude_oil_usd_per_barrel": 78.50,
                    "natural_gas_usd_per_mbtu": 3.25,
                    "coal_usd_per_ton": 120.00,
                    "electricity_cost_inr_per_kwh": 6.50
                },
                "economic_indicators": {
                    "gdp_growth_rate": 6.8,  # %
                    "inflation_rate": 4.5,  # %
                    "unemployment_rate": 7.2,  # %
                    "energy_sector_contribution": 8.5  # % of GDP
                },
                "investment_opportunities": {
                    "renewable_energy_investment": 150,  # Billion USD
                    "nuclear_energy_investment": 25,
                    "thorium_research_funding": 2.5
                }
            }
            
            db_manager.cache_energy_data("economic", cache_key, economic_data, 7200)  # 2 hour cache
            
            return economic_data
            
        except Exception as e:
            st.error(f"Error fetching economic data: {str(e)}")
            return None
    
    def get_global_energy_trends(self):
        """Get global energy trends and comparisons"""
        cache_key = "global_energy_trends"
        cached_data = db_manager.get_cached_energy_data("global", cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            global_data = {
                "timestamp": datetime.now().isoformat(),
                "global_generation": {
                    "fossil_fuels": 63.5,  # % of global generation
                    "renewables": 28.2,
                    "nuclear": 8.3,
                    "total_capacity": 7500  # GW
                },
                "country_comparisons": {
                    "india": {
                        "total_capacity": 351.78,  # GW
                        "renewable_share": 34.1,  # %
                        "nuclear_share": 1.9,
                        "thorium_reserves_rank": 1
                    },
                    "china": {
                        "total_capacity": 2200,
                        "renewable_share": 45.2,
                        "nuclear_share": 4.9,
                        "thorium_reserves_rank": 2
                    },
                    "usa": {
                        "total_capacity": 1200,
                        "renewable_share": 22.1,
                        "nuclear_share": 19.7,
                        "thorium_reserves_rank": 3
                    }
                },
                "technology_trends": {
                    "thorium_research_investment": 5.2,  # Billion USD globally
                    "advanced_reactor_projects": 47,  # Number of projects
                    "fusion_energy_progress": 0.75,  # Progress score 0-1
                    "energy_storage_advancement": 0.65
                }
            }
            
            db_manager.cache_energy_data("global", cache_key, global_data, 10800)  # 3 hour cache
            
            return global_data
            
        except Exception as e:
            st.error(f"Error fetching global data: {str(e)}")
            return None
    
    def calculate_real_time_insights(self, energy_data, weather_data, economic_data):
        """Calculate real-time insights from multiple data sources"""
        if not all([energy_data, weather_data, economic_data]):
            return None
        
        insights = {
            "timestamp": datetime.now().isoformat(),
            "energy_security_score": 0,
            "renewable_potential": 0,
            "economic_viability": 0,
            "recommendations": []
        }
        
        # Calculate energy security score
        demand_supply_ratio = energy_data["demand"]["current_demand"] / energy_data["total_generation"]["total"]
        insights["energy_security_score"] = min(100, (1 - demand_supply_ratio) * 100)
        
        # Calculate renewable potential
        renewable_share = energy_data["total_generation"]["renewable"] / energy_data["total_generation"]["total"]
        weather_factor = (weather_data["renewable_potential"]["solar_efficiency"] + 
                         weather_data["renewable_potential"]["wind_efficiency"]) / 2
        insights["renewable_potential"] = (renewable_share * weather_factor) * 100
        
        # Calculate economic viability
        thorium_potential = energy_data["thorium_potential"]["potential_capacity"]
        current_nuclear = energy_data["total_generation"]["nuclear"]
        cost_factor = 1 / (economic_data["energy_prices"]["electricity_cost_inr_per_kwh"] / 10)
        insights["economic_viability"] = min(100, (thorium_potential / current_nuclear) * cost_factor * 10)
        
        # Generate recommendations
        if insights["energy_security_score"] < 70:
            insights["recommendations"].append("Consider increasing thorium reactor deployment for energy security")
        
        if insights["renewable_potential"] > 80:
            insights["recommendations"].append("Excellent conditions for renewable energy expansion")
        
        if insights["economic_viability"] > 75:
            insights["recommendations"].append("Strong economic case for thorium energy investment")
        
        return insights

# Initialize real-time data manager
rt_data_manager = RealTimeDataManager()

def show_realtime_dashboard():
    """Display real-time data dashboard"""
    st.markdown("### 🌐 Real-Time Energy Dashboard")
    
    # Create tabs for different data views
    tab1, tab2, tab3, tab4 = st.tabs([
        "⚡ India Energy", "🌤️ Weather Impact", "💰 Economic Indicators", "🌍 Global Trends"
    ])
    
    with tab1:
        show_india_energy_tab()
    
    with tab2:
        show_weather_impact_tab()
    
    with tab3:
        show_economic_indicators_tab()
    
    with tab4:
        show_global_trends_tab()

def show_india_energy_tab():
    """Show India energy data"""
    energy_data = rt_data_manager.get_india_energy_data()
    
    if energy_data:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Current Generation Mix")
            generation_data = energy_data["total_generation"]
            
            # Create pie chart
            labels = list(generation_data.keys())[:-1]  # Exclude total
            values = [generation_data[key] for key in labels]
            
            fig = px.pie(values=values, names=labels, 
                        title="India's Energy Generation Mix",
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### ⚡ Demand vs Supply")
            demand_data = energy_data["demand"]
            
            metrics_col1, metrics_col2 = st.columns(2)
            with metrics_col1:
                st.metric("Current Demand", f"{demand_data['current_demand']:,} MW")
                st.metric("Peak Demand", f"{demand_data['peak_demand']:,} MW")
            
            with metrics_col2:
                st.metric("Supply", f"{generation_data['total']:,} MW")
                st.metric("Surplus", f"{demand_data['demand_supply_gap']:,} MW")
        
        # Thorium potential
        st.markdown("#### ⚛️ Thorium Energy Potential")
        thorium_data = energy_data["thorium_potential"]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Thorium Reserves", f"{thorium_data['reserves']:,} tons")
        with col2:
            st.metric("Potential Capacity", f"{thorium_data['potential_capacity']:,} MW")
        with col3:
            st.metric("Current Utilization", f"{thorium_data['current_utilization']} MW")
        
        # Emissions data
        st.markdown("#### 🌱 Emissions Impact")
        emissions_data = energy_data["emissions"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Current CO₂ Emissions", f"{emissions_data['co2_emissions']:,} MtCO₂/year")
        with col2:
            st.metric("Reduction Potential", f"{emissions_data['reduction_potential']:,} MtCO₂/year")

def show_weather_impact_tab():
    """Show weather impact on renewable energy"""
    weather_data = rt_data_manager.get_weather_data()
    
    if weather_data:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌤️ Current Weather Conditions")
            
            metrics_col1, metrics_col2 = st.columns(2)
            with metrics_col1:
                st.metric("Temperature", f"{weather_data['temperature']}°C")
                st.metric("Humidity", f"{weather_data['humidity']}%")
            
            with metrics_col2:
                st.metric("Wind Speed", f"{weather_data['wind_speed']} km/h")
                st.metric("Solar Irradiance", f"{weather_data['solar_irradiance']} W/m²")
        
        with col2:
            st.markdown("#### ⚡ Renewable Energy Efficiency")
            renewable_data = weather_data["renewable_potential"]
            
            # Create gauge chart for efficiency
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = (renewable_data["solar_efficiency"] + renewable_data["wind_efficiency"]) / 2 * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Renewable Efficiency (%)"},
                delta = {'reference': 80},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        if weather_data["renewable_potential"]["optimal_conditions"]:
            st.success("✅ **Optimal Conditions**: Excellent weather for renewable energy generation")
        else:
            st.warning("⚠️ **Sub-optimal Conditions**: Weather may impact renewable energy efficiency")

def show_economic_indicators_tab():
    """Show economic indicators"""
    economic_data = rt_data_manager.get_economic_indicators()
    
    if economic_data:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💱 Currency & Energy Prices")
            
            currency_data = economic_data["currency"]
            price_data = economic_data["energy_prices"]
            
            st.metric("USD to INR", f"₹{currency_data['usd_to_inr']}")
            st.metric("EUR to INR", f"₹{currency_data['eur_to_inr']}")
            
            st.markdown("**Energy Prices:**")
            st.write(f"• Crude Oil: ${price_data['crude_oil_usd_per_barrel']}/barrel")
            st.write(f"• Natural Gas: ${price_data['natural_gas_usd_per_mbtu']}/MBTU")
            st.write(f"• Coal: ${price_data['coal_usd_per_ton']}/ton")
            st.write(f"• Electricity: ₹{price_data['electricity_cost_inr_per_kwh']}/kWh")
        
        with col2:
            st.markdown("#### 📈 Economic Indicators")
            
            indicators = economic_data["economic_indicators"]
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("GDP Growth", f"{indicators['gdp_growth_rate']}%")
                st.metric("Inflation Rate", f"{indicators['inflation_rate']}%")
            
            with col2:
                st.metric("Unemployment", f"{indicators['unemployment_rate']}%")
                st.metric("Energy Sector GDP", f"{indicators['energy_sector_contribution']}%")
        
        # Investment opportunities
        st.markdown("#### 💰 Investment Opportunities")
        investment_data = economic_data["investment_opportunities"]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Renewable Energy", f"${investment_data['renewable_energy_investment']}B")
        with col2:
            st.metric("Nuclear Energy", f"${investment_data['nuclear_energy_investment']}B")
        with col3:
            st.metric("Thorium Research", f"${investment_data['thorium_research_funding']}B")

def show_global_trends_tab():
    """Show global energy trends"""
    global_data = rt_data_manager.get_global_energy_trends()
    
    if global_data:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌍 Global Generation Mix")
            
            global_gen = global_data["global_generation"]
            
            # Bar chart for global generation
            fig = px.bar(
                x=list(global_gen.keys())[:-1],  # Exclude total
                y=[global_gen[key] for key in list(global_gen.keys())[:-1]],
                title="Global Energy Generation Mix (%)",
                color=list(global_gen.keys())[:-1],
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🏆 Country Comparison")
            
            country_data = global_data["country_comparisons"]
            
            comparison_df = pd.DataFrame(country_data).T
            comparison_df = comparison_df[['total_capacity', 'renewable_share', 'nuclear_share', 'thorium_reserves_rank']]
            
            st.dataframe(comparison_df, use_container_width=True)
        
        # Technology trends
        st.markdown("#### 🚀 Technology Trends")
        tech_data = global_data["technology_trends"]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Thorium Research", f"${tech_data['thorium_research_investment']}B")
        with col2:
            st.metric("Advanced Reactors", f"{tech_data['advanced_reactor_projects']}")
        with col3:
            st.metric("Fusion Progress", f"{tech_data['fusion_energy_progress']*100:.1f}%")
        with col4:
            st.metric("Storage Advancement", f"{tech_data['energy_storage_advancement']*100:.1f}%")

def show_realtime_insights():
    """Show real-time insights combining all data sources"""
    st.markdown("### 🧠 Real-Time Insights")
    
    energy_data = rt_data_manager.get_india_energy_data()
    weather_data = rt_data_manager.get_weather_data()
    economic_data = rt_data_manager.get_economic_indicators()
    
    insights = rt_data_manager.calculate_real_time_insights(energy_data, weather_data, economic_data)
    
    if insights:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Energy Security Score", f"{insights['energy_security_score']:.1f}/100")
        with col2:
            st.metric("Renewable Potential", f"{insights['renewable_potential']:.1f}/100")
        with col3:
            st.metric("Economic Viability", f"{insights['economic_viability']:.1f}/100")
        
        if insights["recommendations"]:
            st.markdown("#### 💡 Recommendations")
            for recommendation in insights["recommendations"]:
                st.info(f"• {recommendation}")
    else:
        st.warning("Unable to generate insights - some data sources unavailable")
