import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Luxury Car Explorer", 
    layout="wide", 
    page_icon="🚗",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with vibrant, eye-catching colors
def inject_css(dark_mode=False):
    if dark_mode:
        css = """
        <style>
        /* Dark Mode - Vibrant Gradient Theme */
        .main > div {
            padding: 2rem 1rem;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a0033 25%, #330066 50%, #1a0033 75%, #0a0a0a 100%);
            min-height: 100vh;
            position: relative;
        }
        
        .main > div::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
            pointer-events: none;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a0033 25%, #330066 50%, #1a0033 75%, #0a0a0a 100%);
        }
        
        .metric-card {
            background: linear-gradient(145deg, rgba(30, 30, 60, 0.9), rgba(60, 30, 90, 0.9));
            padding: 2rem;
            border-radius: 20px;
            border: 2px solid rgba(255, 119, 198, 0.3);
            box-shadow: 0 15px 35px rgba(255, 119, 198, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            text-align: center;
            margin: 1rem 0;
            backdrop-filter: blur(20px);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255, 119, 198, 0.1), transparent);
            transform: rotate(-45deg);
            transition: all 0.6s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-10px) scale(1.02);
            border-color: rgba(255, 119, 198, 0.6);
            box-shadow: 0 25px 50px rgba(255, 119, 198, 0.3);
        }
        
        .metric-card:hover::before {
            animation: shimmer 2s infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%) translateY(-100%) rotate(-45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(-45deg); }
        }
        
        .feature-card {
            background: linear-gradient(145deg, rgba(40, 40, 80, 0.9), rgba(70, 40, 100, 0.9));
            padding: 2rem;
            border-radius: 15px;
            border-left: 4px solid #ff77c6;
            border-right: 1px solid rgba(255, 119, 198, 0.3);
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(255, 119, 198, 0.15);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateX(10px);
            border-left-color: #78dbff;
            box-shadow: 0 12px 40px rgba(120, 219, 255, 0.2);
        }
        
        .stats-container {
            background: linear-gradient(145deg, rgba(30, 30, 60, 0.95), rgba(60, 30, 90, 0.95));
            padding: 2.5rem;
            border-radius: 20px;
            margin: 1rem 0;
            border: 1px solid rgba(120, 219, 255, 0.3);
            backdrop-filter: blur(20px);
            box-shadow: 0 10px 40px rgba(120, 219, 255, 0.1);
        }
        
        .prediction-result {
            background: linear-gradient(145deg, rgba(40, 70, 80, 0.95), rgba(60, 100, 120, 0.95));
            padding: 2rem;
            border-radius: 15px;
            border-left: 4px solid #78dbff;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(120, 219, 255, 0.2);
            backdrop-filter: blur(10px);
            animation: glow 3s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { box-shadow: 0 8px 32px rgba(120, 219, 255, 0.2); }
            to { box-shadow: 0 12px 40px rgba(120, 219, 255, 0.4); }
        }
        
        h1, h2, h3 {
            color: #ffffff !important;
            text-shadow: 0 0 20px rgba(255, 119, 198, 0.5);
            font-weight: 700 !important;
        }
        
        h1 {
            background: linear-gradient(45deg, #ff77c6, #78dbff, #ff77c6);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: rainbow 3s ease-in-out infinite;
        }
        
        @keyframes rainbow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .stButton > button {
            background: linear-gradient(45deg, #ff77c6, #ff4081, #ff77c6);
            background-size: 200% 200%;
            border: none;
            color: white;
            border-radius: 15px;
            padding: 0.8rem 2rem;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            animation: buttonGlow 2s ease-in-out infinite alternate;
        }
        
        @keyframes buttonGlow {
            from { background-position: 0% 50%; box-shadow: 0 4px 15px rgba(255, 119, 198, 0.4); }
            to { background-position: 100% 50%; box-shadow: 0 6px 25px rgba(255, 119, 198, 0.6); }
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 10px 30px rgba(255, 119, 198, 0.7);
        }
        
        /* Hide any code blocks that might appear */
        .stCode, pre, code {
            display: none !important;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(45deg, #ff77c6, #78dbff);
            border-radius: 10px;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(180deg, rgba(30, 30, 60, 0.95), rgba(60, 30, 90, 0.95));
            backdrop-filter: blur(20px);
        }
        </style>
        """
    else:
        css = """
        <style>
        /* Light Mode - Vibrant Premium Theme */
        .main > div {
            padding: 2rem 1rem;
            background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 25%, #e0f2fe 50%, #f0f9ff 75%, #ffffff 100%);
            min-height: 100vh;
            position: relative;
        }
        
        .main > div::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(236, 72, 153, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(168, 85, 247, 0.05) 0%, transparent 50%);
            pointer-events: none;
        }
        
        .stApp {
            background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 25%, #e0f2fe 50%, #f0f9ff 75%, #ffffff 100%);
        }
        
        .metric-card {
            background: linear-gradient(145deg, rgba(255, 255, 255, 0.95), rgba(240, 249, 255, 0.95));
            padding: 2rem;
            border-radius: 20px;
            border: 2px solid rgba(59, 130, 246, 0.2);
            box-shadow: 0 15px 35px rgba(59, 130, 246, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.8);
            text-align: center;
            margin: 1rem 0;
            backdrop-filter: blur(20px);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(59, 130, 246, 0.1), transparent);
            transform: rotate(-45deg);
            transition: all 0.6s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-10px) scale(1.02);
            border-color: rgba(59, 130, 246, 0.4);
            box-shadow: 0 25px 50px rgba(59, 130, 246, 0.2);
        }
        
        .metric-card:hover::before {
            animation: shimmer 2s infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%) translateY(-100%) rotate(-45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(-45deg); }
        }
        
        .feature-card {
            background: linear-gradient(145deg, rgba(255, 255, 255, 0.9), rgba(240, 249, 255, 0.9));
            padding: 2rem;
            border-radius: 15px;
            border-left: 4px solid #3b82f6;
            border-right: 1px solid rgba(59, 130, 246, 0.2);
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(59, 130, 246, 0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateX(10px);
            border-left-color: #ec4899;
            box-shadow: 0 12px 40px rgba(236, 72, 153, 0.15);
        }
        
        .stats-container {
            background: linear-gradient(145deg, rgba(255, 255, 255, 0.95), rgba(240, 249, 255, 0.95));
            padding: 2.5rem;
            border-radius: 20px;
            margin: 1rem 0;
            border: 1px solid rgba(59, 130, 246, 0.2);
            backdrop-filter: blur(20px);
            box-shadow: 0 10px 40px rgba(59, 130, 246, 0.08);
        }
        
        .prediction-result {
            background: linear-gradient(145deg, rgba(239, 246, 255, 0.95), rgba(219, 234, 254, 0.95));
            padding: 2rem;
            border-radius: 15px;
            border-left: 4px solid #3b82f6;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15);
            backdrop-filter: blur(10px);
            animation: glow 3s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15); }
            to { box-shadow: 0 12px 40px rgba(59, 130, 246, 0.25); }
        }
        
        h1, h2, h3 {
            color: #1e293b !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            font-weight: 700 !important;
        }
        
        h1 {
            background: linear-gradient(45deg, #3b82f6, #ec4899, #8b5cf6);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: rainbow 3s ease-in-out infinite;
        }
        
        @keyframes rainbow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .stButton > button {
            background: linear-gradient(45deg, #3b82f6, #1d4ed8, #3b82f6);
            background-size: 200% 200%;
            border: none;
            color: white;
            border-radius: 15px;
            padding: 0.8rem 2rem;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            animation: buttonGlow 2s ease-in-out infinite alternate;
        }
        
        @keyframes buttonGlow {
            from { background-position: 0% 50%; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3); }
            to { background-position: 100% 50%; box-shadow: 0 6px 25px rgba(59, 130, 246, 0.5); }
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.6);
        }
        
        /* Hide any code blocks that might appear */
        .stCode, pre, code, .highlight {
            display: none !important;
            visibility: hidden !important;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(59, 130, 246, 0.1);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(45deg, #3b82f6, #ec4899);
            border-radius: 10px;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(240, 249, 255, 0.95));
            backdrop-filter: blur(20px);
        }
        
        /* Enhanced plotly charts */
        .js-plotly-plot {
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

# Sidebar with improved styling
with st.sidebar:
    st.markdown("# 🛠️ Control Panel")
    
    # Dark mode toggle
    dark_mode = st.toggle("🌙 Dark Mode", value=False, key="dark_mode")
    
    st.markdown("---")
    
    # Navigation with emojis
    page = st.selectbox(
        "📍 Navigate to:",
        ["🏠 Dashboard", "📊 Analytics", "🤖 ML Predictions", "📈 Advanced Charts", "🔍 Data Explorer", "🎨 Theme Gallery"]
    )
    
    st.markdown("---")

# Inject CSS based on mode
inject_css(dark_mode)

# Enhanced data loading with error handling
@st.cache_data
def load_data():
    try:
        # Create enhanced sample data with more variety
        np.random.seed(42)
        brands = ['Ferrari', 'Lamborghini', 'McLaren', 'Porsche', 'Bugatti', 'Aston Martin', 
                 'Bentley', 'Rolls-Royce', 'Maserati', 'Lotus', 'Koenigsegg', 'Pagani',
                 'Mercedes-AMG', 'BMW M', 'Audi RS']
        fuel_types = ['Petrol', 'Hybrid', 'Electric', 'Plug-in Hybrid']
        engines = ['V8', 'V12', 'V6', 'Electric', 'V10', 'W16', 'Twin-Turbo V8', 'Quad-Turbo V12']
        models = ['Spider', 'Coupe', 'GT', 'Turbo', 'S', 'RS', 'AMG', 'Competition', 'Track', 'Roadster']
        
        n_cars = 250
        data = {
            'Car Names': [f"{np.random.choice(brands)} {np.random.choice(models)} {np.random.choice(['2024', '2023', 'Limited'])}" for _ in range(n_cars)],
            'Company Names': np.random.choice(brands, n_cars),
            'Cars Prices': [f"${int(np.random.exponential(250000) + 75000):,}" for _ in range(n_cars)],
            'HorsePower': [f"{max(150, int(np.random.normal(600, 200)))} hp" for _ in range(n_cars)],
            'Fuel Types': np.random.choice(fuel_types, n_cars),
            'Engines': np.random.choice(engines, n_cars),
            'Max Speed': [f"{max(220, int(np.random.normal(320, 60)))} km/h" for _ in range(n_cars)],
            'Acceleration': [f"{max(2.0, np.random.normal(3.2, 0.8)):.1f}s" for _ in range(n_cars)]
        }
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Load and process data
df = load_data()

if df.empty:
    st.error("Failed to load data. Please refresh the page.")
    st.stop()

# Clean column names
df.columns = [col.strip() for col in df.columns]

# Enhanced data parsing functions with error handling
def parse_price(price):
    try:
        return float(str(price).replace("$", "").replace(",", ""))
    except:
        return 0

def parse_hp(hp):
    try:
        return float(str(hp).replace(" hp", ""))
    except:
        return 0

def parse_speed(speed):
    try:
        return float(str(speed).replace(" km/h", ""))
    except:
        return 0

def parse_acceleration(acc):
    try:
        return float(str(acc).replace("s", ""))
    except:
        return 0

# Apply parsing
df['Parsed Price'] = df['Cars Prices'].apply(parse_price)
df['Parsed HP'] = df['HorsePower'].apply(parse_hp)
df['Parsed Speed'] = df['Max Speed'].apply(parse_speed)
df['Parsed Acceleration'] = df['Acceleration'].apply(parse_acceleration)

# Filter out invalid data
df = df[(df['Parsed Price'] > 0) & (df['Parsed HP'] > 0) & (df['Parsed Speed'] > 0)]

# Main content based on page selection
if page == "🏠 Dashboard":
    
    # Enhanced header with animation
    st.markdown("""
    <div style='text-align: center; padding: 2rem; margin-bottom: 3rem;'>
        <h1 style='font-size: 3.5em; margin-bottom: 1rem;'>🚗 Luxury Car Explorer</h1>
        <div style='background: linear-gradient(45deg, #3b82f6, #ec4899, #8b5cf6); padding: 2px; border-radius: 25px; display: inline-block; margin-bottom: 1rem;'>
            <div style='background: inherit; padding: 1rem 2rem; border-radius: 23px; backdrop-filter: blur(10px);'>
                <h3 style='color: white; margin: 0; font-size: 1.8em; text-shadow: 0 0 10px rgba(255,255,255,0.3);'>
                    🚀 Discover Excellence in Automotive Engineering
                </h3>
            </div>
        </div>
        <p style='font-size: 1.3em; opacity: 0.9; margin-top: 1rem; font-weight: 500;'>
            Interactive analytics for the world's finest automobiles ✨
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced key metrics with better icons and colors
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3em; margin-bottom: 0.5rem;">🏎️</div>
            <h2 style="margin: 0.5rem 0; font-size: 2.2em; background: linear-gradient(45deg, #ff6b6b, #ff8e8e); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{len(df)}</h2>
            <p style="margin: 0; opacity: 0.8; font-size: 1.2em; font-weight: 600;">Premium Cars</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        max_hp = int(df['Parsed HP'].max()) if df['Parsed HP'].max() else 0
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3em; margin-bottom: 0.5rem;">⚡</div>
            <h2 style="margin: 0.5rem 0; font-size: 2.2em; background: linear-gradient(45deg, #ffd93d, #ffed4e); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{max_hp}</h2>
            <p style="margin: 0; opacity: 0.8; font-size: 1.2em; font-weight: 600;">Max Horsepower</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        max_price = int(df['Parsed Price'].max()) if df['Parsed Price'].max() else 0
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3em; margin-bottom: 0.5rem;">💎</div>
            <h2 style="margin: 0.5rem 0; font-size: 2.2em; background: linear-gradient(45deg, #4ade80, #22d3ee); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">${max_price:,}</h2>
            <p style="margin: 0; opacity: 0.8; font-size: 1.2em; font-weight: 600;">Highest Value</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        max_speed = int(df['Parsed Speed'].max()) if df['Parsed Speed'].max() else 0
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3em; margin-bottom: 0.5rem;">🚀</div>
            <h2 style="margin: 0.5rem 0; font-size: 2.2em; background: linear-gradient(45deg, #a78bfa, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{max_speed}</h2>
            <p style="margin: 0; opacity: 0.8; font-size: 1.2em; font-weight: 600;">Top Speed (km/h)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced filters with better styling
    with st.expander("🎛️ Advanced Filtering System", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            selected_brand = st.selectbox("🏢 Select Brand", ['All'] + sorted(df['Company Names'].unique()))
        with col2:
            selected_fuel = st.selectbox("⛽ Fuel Technology", ['All'] + sorted(df['Fuel Types'].unique()))
        with col3:
            selected_engine = st.selectbox("🔧 Engine Type", ['All'] + sorted(df['Engines'].unique()))
        with col4:
            price_range = st.slider("💰 Price Range ($)", 
                                   min_value=int(df['Parsed Price'].min()), 
                                   max_value=int(df['Parsed Price'].max()), 
                                   value=(int(df['Parsed Price'].min()), int(df['Parsed Price'].max())))
    
    # Apply filters with error handling
    try:
        filtered_df = df.copy()
        if selected_brand != 'All':
            filtered_df = filtered_df[filtered_df['Company Names'] == selected_brand]
        if selected_fuel != 'All':
            filtered_df = filtered_df[filtered_df['Fuel Types'] == selected_fuel]
        if selected_engine != 'All':
            filtered_df = filtered_df[filtered_df['Engines'] == selected_engine]
        
        filtered_df = filtered_df[
            (filtered_df['Parsed Price'] >= price_range[0]) & 
            (filtered_df['Parsed Price'] <= price_range[1])
        ]
    except Exception as e:
        st.error(f"Error applying filters: {e}")
        filtered_df = df.copy()
    
    # Enhanced charts with vibrant colors
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Performance vs Price Analysis")
        try:
            fig_scatter = px.scatter(
                filtered_df.dropna(subset=['Parsed Price', 'Parsed HP']), 
                x='Parsed HP', 
                y='Parsed Price',
                color='Company Names',
                size='Parsed Speed',
                hover_data=['Car Names', 'Max Speed', 'Acceleration'],
                title="🏎️ Power vs Value Matrix",
                color_discrete_sequence=px.colors.qualitative.Vivid
            )
            fig_scatter.update_traces(marker=dict(opacity=0.8, line=dict(width=2, color='white')))
            fig_scatter.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=13, family="Arial Black"),
                title_font_size=18,
                title_font_color='#3b82f6'
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating scatter plot: {e}")
    
    with col2:
        st.subheader("🥧 Brand Market Distribution")
        try:
            brand_counts = filtered_df['Company Names'].value_counts()
            fig_pie = px.pie(
                values=brand_counts.values, 
                names=brand_counts.index,
                title="🏆 Market Share by Excellence",
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
            fig_pie.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                textfont_size=12,
                marker=dict(line=dict(color='white', width=3))
            )
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=13, family="Arial Black"),
                title_font_size=18,
                title_font_color='#ec4899'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating pie chart: {e}")
    
    # Enhanced data table with search
    st.subheader("🔍 Premium Car Showcase")
    
    # Add search functionality
    search_term = st.text_input("🔎 Search for specific models:", placeholder="Enter car name, brand, or feature...")
    
    if search_term:
        filtered_df = filtered_df[filtered_df['Car Names'].str.contains(search_term, case=False, na=False)]
    
    if not filtered_df.empty:
        # Show count
        st.info(f"📊 Displaying {len(filtered_df)} premium vehicles")
        
        display_df = filtered_df[['Car Names', 'Company Names', 'Cars Prices', 'HorsePower', 'Max Speed', 'Fuel Types', 'Engines', 'Acceleration']]
        st.dataframe(
            display_df, 
            use_container_width=True, 
            height=400,
            column_config={
                "Car Names": st.column_config.TextColumn("🚗 Model", width="large"),
                "Company Names": st.column_config.TextColumn("🏢 Brand", width="medium"),
                "Cars Prices": st.column_config.TextColumn("💰 Price", width="medium"),
                "HorsePower": st.column_config.TextColumn("⚡ Power", width="small"),
                "Max Speed": st.column_config.TextColumn("🏎️ Top Speed", width="small"),
                "Fuel Types": st.column_config.TextColumn("⛽ Fuel", width="small"),
                "Engines": st.column_config.TextColumn("🔧 Engine", width="medium"),
                "Acceleration": st.column_config.TextColumn("🚀 0-100km/h", width="small")
            }
        )
        
        # Enhanced download options
        col1, col2, col3 = st.columns(3)
        with col1:
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📊 Download CSV",
                data=csv,
                file_name=f'luxury_cars_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mime='text/csv'
            )
        with col2:
            json_data = filtered_df.to_json(orient='records', indent=2).encode('utf-8')
            st.download_button(
                label="🔧 Download JSON",
                data=json_data,
                file_name=f'luxury_cars_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
                mime='application/json'
            )
        with col3:
            if st.button("🎊 Celebrate Find!", type="secondary"):
                st.balloons()
                st.success("🏆 Excellent choice in automotive excellence!")
    else:
        st.warning("🔍 No vehicles match your search criteria. Try adjusting filters or search terms.")

elif page == "📊 Analytics":
    st.markdown("# 📊 Advanced Analytics Dashboard")
    st.markdown("### Dive deep into performance metrics and market trends 🚀")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Performance Analysis", "💰 Market Intelligence", "🔧 Engineering Insights", "🏆 Brand Comparison"])
    
    with tab1:
        st.subheader("🚀 Performance Metrics Deep Dive")
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                fig_hp = px.histogram(
                    df.dropna(subset=['Parsed HP']), 
                    x='Parsed HP', 
                    color='Company Names',
                    title="🔥 Horsepower Distribution Spectrum",
                    nbins=30,
                    color_discrete_sequence=px.colors.qualitative.Dark24
                )
                fig_hp.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    title_font_color='#ec4899',
                    showlegend=True
                )
                st.plotly_chart(fig_hp, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating histogram: {e}")
        
        with col2:
            try:
                fig_speed_acc = px.scatter(
                    df.dropna(subset=['Parsed Speed', 'Parsed Acceleration']), 
                    x='Parsed Speed', 
                    y='Parsed Acceleration',
                    color='Fuel Types',
                    size='Parsed HP',
                    title="🏁 Speed vs Acceleration Matrix",
                    labels={'Parsed Acceleration': '🚀 Acceleration (0-100 km/h)', 'Parsed Speed': '🏎️ Top Speed (km/h)'},
                    color_discrete_sequence=px.colors.qualitative.Set1
                )
                fig_speed_acc.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color='white')))
                fig_speed_acc.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    title_font_color='#3b82f6'
                )
                st.plotly_chart(fig_speed_acc, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating speed vs acceleration plot: {e}")
    
    with tab2:
        st.subheader("💎 Market Value Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                fig_price_brand = px.box(
                    df.dropna(subset=['Parsed Price']), 
                    x='Company Names', 
                    y='Parsed Price',
                    title="💰 Price Distribution by Premium Brands",
                    color='Company Names',
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_price_brand.update_xaxes(tickangle=45)
                fig_price_brand.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    title_font_color='#8b5cf6',
                    showlegend=False
                )
                st.plotly_chart(fig_price_brand, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating box plot: {e}")
        
        with col2:
            try:
                avg_stats = df.groupby('Company Names').agg({
                    'Parsed Price': 'mean',
                    'Parsed HP': 'mean',
                    'Parsed Speed': 'mean'
                }).reset_index().dropna()
                
                fig_brand_perf = px.scatter(
                    avg_stats, 
                    x='Parsed HP', 
                    y='Parsed Price',
                    size='Parsed Speed',
                    text='Company Names',
                    title="🏆 Brand Excellence Matrix",
                    color='Parsed Speed',
                    color_continuous_scale='viridis'
                )
                fig_brand_perf.update_traces(textposition="top center", marker=dict(opacity=0.8))
                fig_brand_perf.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    title_font_color='#10b981'
                )
                st.plotly_chart(fig_brand_perf, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating brand performance plot: {e}")
    
    with tab3:
        st.subheader("⚙️ Engineering Excellence Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                engine_stats = df.groupby('Engines').agg({
                    'Parsed HP': 'mean',
                    'Parsed Speed': 'mean',
                    'Car Names': 'count'
                }).reset_index()
                engine_stats = engine_stats.rename(columns={'Car Names': 'Count'})
                
                fig_engine = px.bar(
                    engine_stats, 
                    x='Engines', 
                    y='Count',
                    color='Parsed HP',
                    title="🔧 Engine Technology Distribution",
                    color_continuous_scale='plasma'
                )
                fig_engine.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    title_font_color='#f59e0b',
                    xaxis_tickangle=45
                )
                st.plotly_chart(fig_engine, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating engine distribution: {e}")
        
        with col2:
            try:
                fuel_stats = df.groupby('Fuel Types').agg({
                    'Parsed HP': 'mean',
                    'Parsed Price': 'mean',
                    'Parsed Speed': 'mean'
                }).reset_index().dropna()
                
                fig_fuel = px.scatter(
                    fuel_stats, 
                    x='Parsed HP', 
                    y='Parsed Price',
                    color='Fuel Types',
                    size='Parsed Speed',
                    title="⛽ Fuel Technology Performance",
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_fuel.update_traces(marker=dict(opacity=0.8, line=dict(width=2, color='white')))
                fig_fuel.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    title_font_color='#06b6d4'
                )
                st.plotly_chart(fig_fuel, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating fuel type comparison: {e}")
    
    with tab4:
        st.subheader("🏆 Elite Brand Showdown")
        
        # Brand comparison selector
        available_brands = sorted(df['Company Names'].unique())
        selected_brands = st.multiselect(
            "🎯 Select brands to compare (max 5):",
            available_brands,
            default=available_brands[:3] if len(available_brands) >= 3 else available_brands,
            max_selections=5
        )
        
        if selected_brands:
            comparison_df = df[df['Company Names'].isin(selected_brands)]
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Performance comparison
                perf_comparison = comparison_df.groupby('Company Names').agg({
                    'Parsed HP': ['mean', 'max'],
                    'Parsed Speed': ['mean', 'max'],
                    'Parsed Price': ['mean', 'max']
                }).round(0)
                
                perf_comparison.columns = ['Avg HP', 'Max HP', 'Avg Speed', 'Max Speed', 'Avg Price', 'Max Price']
                st.dataframe(perf_comparison, use_container_width=True)
            
            with col2:
                # Radar chart comparison
                try:
                    fig_radar = go.Figure()
                    
                    metrics = ['Parsed HP', 'Parsed Speed', 'Parsed Price']
                    colors = px.colors.qualitative.Set1
                    
                    for i, brand in enumerate(selected_brands):
                        brand_data = comparison_df[comparison_df['Company Names'] == brand][metrics].mean()
                        # Normalize data for radar chart
                        normalized_data = []
                        for metric in metrics:
                            max_val = df[metric].max()
                            min_val = df[metric].min()
                            normalized = (brand_data[metric] - min_val) / (max_val - min_val) * 100
                            normalized_data.append(normalized)
                        
                        fig_radar.add_trace(go.Scatterpolar(
                            r=normalized_data,
                            theta=['Horsepower', 'Top Speed', 'Price'],
                            fill='toself',
                            name=brand,
                            line_color=colors[i % len(colors)]
                        ))
                    
                    fig_radar.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 100]
                            )),
                        title="🎯 Multi-Dimensional Brand Comparison",
                        title_font_color='#7c3aed',
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig_radar, use_container_width=True)
                except Exception as e:
                    st.error(f"Error creating radar chart: {e}")

elif page == "🤖 ML Predictions":
    st.markdown("# 🤖 AI-Powered Automotive Intelligence")
    st.markdown("### Harness machine learning to predict automotive excellence 🚀")
    
    # Model selection with enhanced UI
    col1, col2, col3 = st.columns(3)
    
    with col1:
        prediction_target = st.selectbox(
            "🎯 Prediction Target",
            ["💰 Car Price", "⚡ Horsepower", "🏎️ Top Speed"],
            help="Choose what you want to predict"
        )
    
    with col2:
        model_type = st.selectbox(
            "🧠 AI Model",
            ["🌳 Random Forest", "📈 Linear Regression"],
            help="Select the machine learning algorithm"
        )
    
    with col3:
        test_size = st.slider("🔬 Test Data %", 10, 40, 20, help="Percentage of data for testing")
    
    # Enhanced training section
    st.markdown("### 🚀 Model Training Center")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🚀 Launch AI Training", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is learning automotive patterns..."):
                # Enhanced progress bar
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)
                
                try:
                    # Prepare data
                    model_df = df.dropna(subset=['Parsed Price', 'Parsed HP', 'Parsed Speed'])
                    
                    if model_df.empty:
                        st.error("⚠️ Insufficient data for training. Please check your dataset.")
                        st.stop()
                    
                    # Feature encoding
                    model_df_encoded = pd.get_dummies(model_df, columns=['Company Names', 'Fuel Types', 'Engines'])
                    
                    # Define features and target
                    if prediction_target == "💰 Car Price":
                        target_col = 'Parsed Price'
                        feature_cols = ['Parsed HP', 'Parsed Speed', 'Parsed Acceleration'] + [col for col in model_df_encoded.columns if col.startswith(('Company Names_', 'Fuel Types_', 'Engines_'))]
                        target_name = "Price ($)"
                    elif prediction_target == "⚡ Horsepower":
                        target_col = 'Parsed HP'
                        feature_cols = ['Parsed Price', 'Parsed Speed', 'Parsed Acceleration'] + [col for col in model_df_encoded.columns if col.startswith(('Company Names_', 'Fuel Types_', 'Engines_'))]
                        target_name = "Horsepower"
                    else:  # Top Speed
                        target_col = 'Parsed Speed'
                        feature_cols = ['Parsed Price', 'Parsed HP', 'Parsed Acceleration'] + [col for col in model_df_encoded.columns if col.startswith(('Company Names_', 'Fuel Types_', 'Engines_'))]
                        target_name = "Top Speed (km/h)"
                    
                    X = model_df_encoded[feature_cols]
                    y = model_df_encoded[target_col]
                    
                    # Train-test split
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size/100, random_state=42)
                    
                    # Train model
                    if "Random Forest" in model_type:
                        model = RandomForestRegressor(n_estimators=150, random_state=42, max_depth=10)
                        model_emoji = "🌳"
                    else:
                        model = LinearRegression()
                        model_emoji = "📈"
                    
                    model.fit(X_train, y_train)
                    
                    # Predictions
                    y_pred = model.predict(X_test)
                    
                    # Metrics
                    r2 = r2_score(y_test, y_pred)
                    mae = mean_absolute_error(y_test, y_pred)
                    
                    # Display enhanced results
                    st.markdown(f"""
                    <div class="prediction-result">
                        <div style="text-align: center; margin-bottom: 1.5rem;">
                            <div style="font-size: 4em; margin-bottom: 0.5rem;">{model_emoji}</div>
                            <h2>🎉 AI Training Complete!</h2>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                            <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
                                <h4>🎯 Target</h4>
                                <p style="font-size: 1.2em; font-weight: bold;">{prediction_target}</p>
                            </div>
                            <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
                                <h4>🧠 Model</h4>
                                <p style="font-size: 1.2em; font-weight: bold;">{model_type}</p>
                            </div>
                            <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
                                <h4>📊 R² Score</h4>
                                <p style="font-size: 1.2em; font-weight: bold; color: {'#4ade80' if r2 > 0.8 else '#fbbf24' if r2 > 0.6 else '#f87171'};">{r2:.3f}</p>
                            </div>
                            <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
                                <h4>📏 MAE</h4>
                                <p style="font-size: 1.2em; font-weight: bold;">{mae:,.0f}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Enhanced prediction vs actual plot
                    fig_pred = px.scatter(
                        x=y_test, 
                        y=y_pred,
                        title=f"🎯 AI Predictions vs Reality: {target_name}",
                        labels={'x': f'Actual {target_name}', 'y': f'Predicted {target_name}'},
                        color_discrete_sequence=['#8b5cf6']
                    )
                    
                    # Add perfect prediction line
                    min_val = min(y_test.min(), y_pred.min())
                    max_val = max(y_test.max(), y_pred.max())
                    fig_pred.add_trace(
                        go.Scatter(
                            x=[min_val, max_val], 
                            y=[min_val, max_val],
                            mode='lines',
                            name='Perfect Prediction',
                            line=dict(dash='dash', color='#ef4444', width=3)
                        )
                    )
                    
                    fig_pred.update_traces(marker=dict(size=8, opacity=0.7, line=dict(width=1, color='white')))
                    fig_pred.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        title_font_color='#8b5cf6',
                        title_font_size=18
                    )
                    st.plotly_chart(fig_pred, use_container_width=True)
                    
                    # Feature importance (for Random Forest)
                    if "Random Forest" in model_type:
                        importance_df = pd.DataFrame({
                            'Feature': feature_cols,
                            'Importance': model.feature_importances_
                        }).sort_values('Importance', ascending=False).head(10)
                        
                        # Clean feature names for display
                        importance_df['Clean_Feature'] = importance_df['Feature'].str.replace('Company Names_', '🏢 ').str.replace('Fuel Types_', '⛽ ').str.replace('Engines_', '🔧 ').str.replace('Parsed_', '')
                        
                        fig_importance = px.bar(
                            importance_df, 
                            x='Importance', 
                            y='Clean_Feature',
                            orientation='h',
                            title="🎯 Top 10 Most Important Features",
                            color='Importance',
                            color_continuous_scale='viridis'
                        )
                        fig_importance.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            title_font_color='#06b6d4',
                            title_font_size=18
                        )
                        st.plotly_chart(fig_importance, use_container_width=True)
                        
                        # Store model for predictions
                        st.session_state['trained_model'] = model
                        st.session_state['feature_cols'] = feature_cols
                        st.session_state['model_df_encoded'] = model_df_encoded
                
                except Exception as e:
                    st.error(f"❌ Training failed: {e}")
                    
                progress_bar.empty()
    
    with col2:
        st.info("💡 **AI Training Tips**\n\n✅ Higher R² score = better predictions\n\n📊 MAE shows average error\n\n🎯 More data = better accuracy")
    
    st.markdown("---")
    
    # Enhanced interactive prediction section
    st.markdown("### 🔮 Interactive Prediction Studio")
    
    with st.expander("🎛️ Configure Your Dream Car", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            pred_brand = st.selectbox("🏢 Premium Brand", sorted(df['Company Names'].unique()), key="pred_brand")
            pred_fuel = st.selectbox("⛽ Fuel Technology", sorted(df['Fuel Types'].unique()), key="pred_fuel")
        
        with col2:
            pred_engine = st.selectbox("🔧 Engine Type", sorted(df['Engines'].unique()), key="pred_engine")
            pred_hp = st.number_input("⚡ Horsepower", min_value=100, max_value=1500, value=650, step=50)
        
        with col3:
            pred_speed = st.number_input("🏎️ Top Speed (km/h)", min_value=200, max_value=500, value=350, step=10)
            pred_acceleration = st.number_input("🚀 0-100km/h (seconds)", min_value=1.5, max_value=8.0, value=3.0, step=0.1)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🔮 Generate AI Prediction", type="primary", use_container_width=True):
            try:
                # Enhanced prediction with multiple methods
                method1_price = 0
                method2_price = 0
                
                # Method 1: Brand-based estimation
                brand_data = df[df['Company Names'] == pred_brand]
                if not brand_data.empty:
                    brand_avg_price = brand_data['Parsed Price'].mean()
                    brand_avg_hp = brand_data['Parsed HP'].mean()
                    brand_avg_speed = brand_data['Parsed Speed'].mean()
                    
                    hp_factor = pred_hp / brand_avg_hp if brand_avg_hp > 0 else 1
                    speed_factor = pred_speed / brand_avg_speed if brand_avg_speed > 0 else 1
                    
                    method1_price = brand_avg_price * hp_factor * speed_factor * 0.85
                else:
                    method1_price = df['Parsed Price'].mean()
                
                # Method 2: Overall market estimation
                avg_price_per_hp = df['Parsed Price'].sum() / df['Parsed HP'].sum()
                avg_price_per_speed = df['Parsed Price'].sum() / df['Parsed Speed'].sum()
                
                method2_price = (pred_hp * avg_price_per_hp + pred_speed * avg_price_per_speed) / 2
                
                # Combine methods
                final_prediction = (method1_price * 0.6 + method2_price * 0.4)
                
                # Add some intelligent adjustments
                fuel_multiplier = {'Electric': 1.2, 'Hybrid': 1.1, 'Plug-in Hybrid': 1.15, 'Petrol': 1.0}
                engine_multiplier = {'W16': 1.5, 'V12': 1.3, 'V10': 1.2, 'V8': 1.1, 'V6': 1.0, 'Electric': 1.1}
                
                final_prediction *= fuel_multiplier.get(pred_fuel, 1.0)
                final_prediction *= engine_multiplier.get(pred_engine, 1.0)
                
                # Confidence calculation
                brand_count = len(df[df['Company Names'] == pred_brand])
                confidence = min(95, max(60, brand_count * 10))
                
                # Display enhanced result
                st.markdown(f"""
                <div class="prediction-result" style="text-align: center;">
                    <div style="font-size: 4em; margin-bottom: 1rem;">🎯</div>
                    <h2 style="background: linear-gradient(45deg, #3b82f6, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5em;">
                        ${final_prediction:,.0f}
                    </h2>
                    <p style="font-size: 1.3em; margin: 1rem 0; opacity: 0.9;">
                        Predicted value for your <strong>{pred_brand}</strong> configuration
                    </p>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-top: 2rem;">
                        <div style="padding: 0.8rem; background: rgba(59,130,246,0.1); border-radius: 10px;">
                            <div style="font-size: 1.5em;">🏢</div>
                            <div><strong>{pred_brand}</strong></div>
                        </div>
                        <div style="padding: 0.8rem; background: rgba(236,72,153,0.1); border-radius: 10px;">
                            <div style="font-size: 1.5em;">⚡</div>
                            <div><strong>{pred_hp} HP</strong></div>
                        </div>
                        <div style="padding: 0.8rem; background: rgba(139,92,246,0.1); border-radius: 10px;">
                            <div style="font-size: 1.5em;">🏎️</div>
                            <div><strong>{pred_speed} km/h</strong></div>
                        </div>
                        <div style="padding: 0.8rem; background: rgba(16,185,129,0.1); border-radius: 10px;">
                            <div style="font-size: 1.5em;">📊</div>
                            <div><strong>{confidence}% Confidence</strong></div>
                        </div>
                    </div>
                    <p style="margin-top: 1.5rem; opacity: 0.7; font-size: 0.9em;">
                        🔬 Prediction based on advanced market analysis and brand performance metrics
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show similar cars
                similar_cars = df[
                    (abs(df['Parsed HP'] - pred_hp) <= 100) & 
                    (abs(df['Parsed Speed'] - pred_speed) <= 50)
                ].head(3)
                
                if not similar_cars.empty:
                    st.subheader("🔍 Similar Performance Vehicles")
                    for _, car in similar_cars.iterrows():
                        st.info(f"🚗 **{car['Car Names']}** - ${car['Parsed Price']:,.0f} | {car['HorsePower']} | {car['Max Speed']}")
                        
            except Exception as e:
                st.error(f"🚫 Prediction error: {e}")

elif page == "📈 Advanced Charts":
    st.markdown("# 📈 Premium Visualization Suite")
    st.markdown("### Experience data like never before with cutting-edge visualizations 🎨")
    
    chart_type = st.selectbox(
        "🎯 Select Visualization Experience",
        ["🔥 Correlation Heatmap", "🌌 3D Performance Space", "🎭 Brand Radar", "☀️ Market Sunburst", "🗺️ Value Treemap", "📊 Interactive Bubble Chart"]
    )
    
    if chart_type == "🔥 Correlation Heatmap":
        st.subheader("🔥 Performance Correlation Matrix")
        try:
            numeric_cols = ['Parsed Price', 'Parsed HP', 'Parsed Speed', 'Parsed Acceleration']
            corr_data = df[numeric_cols].corr()
            
            fig_heatmap = px.imshow(
                corr_data,
                title="🧬 DNA of Automotive Performance",
                color_continuous_scale="RdBu_r",
                aspect="auto",
                text_auto=True,
                labels=dict(color="Correlation Strength")
            )
            fig_heatmap.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                title_font_color='#ef4444',
                title_font_size=20,
                font=dict(size=12)
            )
            fig_heatmap.update_traces(textfont_size=14, textfont_color="white")
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Correlation insights
            st.markdown("""
            <div class="feature-card">
                <h4>🧠 Correlation Insights</h4>
                <p>• <strong>Strong correlations (>0.7)</strong>: Highly related metrics</p>
                <p>• <strong>Moderate correlations (0.3-0.7)</strong>: Some relationship</p>
                <p>• <strong>Weak correlations (<0.3)</strong>: Little to no relationship</p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error creating heatmap: {e}")
    
    elif chart_type == "🌌 3D Performance Space":
        st.subheader("🌌 3D Automotive Universe")
        try:
            fig_3d = px.scatter_3d(
                df.dropna(subset=['Parsed Price', 'Parsed HP', 'Parsed Speed']), 
                x='Parsed HP', 
                y='Parsed Speed', 
                z='Parsed Price',
                color='Company Names',
                size='Parsed Acceleration',
                hover_data=['Car Names'],
                title="🚀 Navigate the 3D Performance Galaxy",
                color_discrete_sequence=px.colors.qualitative.Light24
            )
            fig_3d.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color='white')))
            fig_3d.update_layout(
                scene=dict(
                    bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(backgroundcolor='rgba(0,0,0,0)', title="⚡ Horsepower"),
                    yaxis=dict(backgroundcolor='rgba(0,0,0,0)', title="🏎️ Top Speed (km/h)"),
                    zaxis=dict(backgroundcolor='rgba(0,0,0,0)', title="💰 Price ($)")
                ),
                title_font_color='#8b5cf6',
                title_font_size=20
            )
            st.plotly_chart(fig_3d, use_container_width=True)
            
            st.info("🎮 **Pro Tip**: Click and drag to rotate the 3D space! Use mouse wheel to zoom in/out.")
            
        except Exception as e:
            st.error(f"Error creating 3D plot: {e}")
    
    elif chart_type == "🎭 Brand Radar":
        st.subheader("🎭 Multi-Dimensional Brand Performance")
        try:
            # Brand selector with enhanced UI
            available_brands = sorted(df['Company Names'].unique())
            
            col1, col2 = st.columns([2, 1])
            with col1:
                selected_brands = st.multiselect(
                    "🎯 Select brands for epic comparison (max 6):",
                    available_brands,
                    default=available_brands[:4] if len(available_brands) >= 4 else available_brands,
                    max_selections=6
                )
            
            with col2:
                radar_metrics = st.multiselect(
                    "📊 Performance Metrics:",
                    ['Parsed HP', 'Parsed Speed', 'Parsed Price'],
                    default=['Parsed HP', 'Parsed Speed', 'Parsed Price']
                )
            
            if selected_brands and radar_metrics:
                # Calculate brand averages
                radar_data = df.groupby('Company Names')[radar_metrics].mean().fillna(0)
                
                # Normalize data (0-100 scale)
                radar_data_norm = pd.DataFrame()
                for col in radar_metrics:
                    max_val = df[col].max()
                    min_val = df[col].min()
                    radar_data_norm[col] = ((radar_data[col] - min_val) / (max_val - min_val)) * 100
                
                fig_radar = go.Figure()
                colors = px.colors.qualitative.Set1
                
                metric_names = {
                    'Parsed HP': 'Horsepower',
                    'Parsed Speed': 'Top Speed',
                    'Parsed Price': 'Price Range'
                }
                
                for i, brand in enumerate(selected_brands):
                    if brand in radar_data_norm.index:
                        fig_radar.add_trace(go.Scatterpolar(
                            r=radar_data_norm.loc[brand].values.tolist(),
                            theta=[metric_names.get(col, col) for col in radar_metrics],
                            fill='toself',
                            name=brand,
                            line_color=colors[i % len(colors)],
                            marker=dict(size=8)
                        ))
                
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True, 
                            range=[0, 100],
                            tickfont=dict(size=12),
                            gridcolor='rgba(255,255,255,0.2)'
                        ),
                        angularaxis=dict(
                            tickfont=dict(size=14, color='white'),
                            gridcolor='rgba(255,255,255,0.2)'
                        )
                    ),
                    title="🎭 Brand Performance Arena",
                    title_font_size=20,
                    title_font_color='#ec4899',
                    showlegend=True,
                    legend=dict(font=dict(size=12)),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig_radar, use_container_width=True)
                
                # Performance summary
                st.markdown("### 🏆 Performance Summary")
                summary_df = radar_data.loc[selected_brands].round(0)
                summary_df.columns = [metric_names.get(col, col) for col in summary_df.columns]
                st.dataframe(summary_df, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error creating radar chart: {e}")
    
    elif chart_type == "☀️ Market Sunburst":
        st.subheader("☀️ Hierarchical Market Structure")
        try:
            # Create hierarchical data
            sunburst_data = df.groupby(['Company Names', 'Fuel Types', 'Engines']).agg({
                'Parsed Price': 'mean',
                'Car Names': 'count'
            }).reset_index()
            sunburst_data = sunburst_data.rename(columns={'Car Names': 'count'})
            
            fig_sunburst = px.sunburst(
                sunburst_data,
                path=['Company Names', 'Fuel Types', 'Engines'],
                values='count',
                color='Parsed Price',
                title="☀️ Automotive Ecosystem: Brand → Fuel → Engine",
                color_continuous_scale='plasma'
            )
            fig_sunburst.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                title_font_color='#f59e0b',
                title_font_size=20,
                font=dict(size=12)
            )
            st.plotly_chart(fig_sunburst, use_container_width=True)
            
            st.markdown("""
            <div class="feature-card">
                <h4>🧭 Navigation Guide</h4>
                <p>• <strong>Center</strong>: Click to zoom out to root level</p>
                <p>• <strong>Segments</strong>: Click to drill down into categories</p>
                <p>• <strong>Colors</strong>: Represent average price ranges</p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error creating sunburst chart: {e}")
    
    elif chart_type == "🗺️ Value Treemap":
        st.subheader("🗺️ Market Value Landscape")
        try:
            treemap_data = df.groupby(['Company Names', 'Fuel Types']).agg({
                'Parsed Price': 'mean',
                'Car Names': 'count'
            }).reset_index()
            treemap_data = treemap_data.rename(columns={'Car Names': 'count'})
            
            fig_treemap = px.treemap(
                treemap_data,
                path=[px.Constant("Luxury Car Market"), 'Company Names', 'Fuel Types'],
                values='count',
                color='Parsed Price',
                title="🗺️ Navigate the Value Territory",
                color_continuous_scale='viridis',
                hover_data={'Parsed Price': ':,.0f'}
            )
            fig_treemap.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                title_font_color='#10b981',
                title_font_size=20
            )
            fig_treemap.update_traces(textfont_size=12)
            st.plotly_chart(fig_treemap, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error creating treemap: {e}")
    
    elif chart_type == "📊 Interactive Bubble Chart":
        st.subheader("📊 Dynamic Performance Bubble Universe")
        
        # Interactive controls
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            x_axis = st.selectbox("🔸 X-Axis", ['Parsed HP', 'Parsed Speed', 'Parsed Price', 'Parsed Acceleration'], key="bubble_x")
        with col2:
            y_axis = st.selectbox("🔹 Y-Axis", ['Parsed Price', 'Parsed HP', 'Parsed Speed', 'Parsed Acceleration'], key="bubble_y")
        with col3:
            size_by = st.selectbox("⭕ Bubble Size", ['Parsed HP', 'Parsed Speed', 'Parsed Price', 'Parsed Acceleration'], key="bubble_size")
        with col4:
            color_by = st.selectbox("🎨 Color By", ['Company Names', 'Fuel Types', 'Engines'], key="bubble_color")
        
        try:
            fig_bubble = px.scatter(
                df.dropna(subset=[x_axis, y_axis, size_by]), 
                x=x_axis, 
                y=y_axis,
                size=size_by,
                color=color_by,
                hover_data=['Car Names'],
                title=f"🌟 Interactive Bubble Analysis: {x_axis.replace('Parsed ', '')} vs {y_axis.replace('Parsed ', '')}",
                size_max=30,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_bubble.update_traces(marker=dict(opacity=0.7, line=dict(width=2, color='white')))
            fig_bubble.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                title_font_color='#3b82f6',
                title_font_size=18,
                font=dict(size=12)
            )
            st.plotly_chart(fig_bubble, use_container_width=True)
            
            # Show statistics
            col1, col2 = st.columns(2)
            
            with col1:
                correlation = df[[x_axis, y_axis]].corr().iloc[0, 1]
                st.metric("📈 Correlation Strength", f"{correlation:.3f}")
            
            with col2:
                total_bubbles = len(df.dropna(subset=[x_axis, y_axis, size_by]))
                st.metric("🫧 Total Bubbles", total_bubbles)
                
        except Exception as e:
            st.error(f"Error creating bubble chart: {e}")

elif page == "🔍 Data Explorer":
    st.markdown("# 🔍 Data Intelligence Center")
    st.markdown("### Deep dive into the automotive dataset with advanced analytics 🧠")
    
    # Enhanced data overview
    try:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="stats-container">
                <div style="text-align: center;">
                    <div style="font-size: 3em; margin-bottom: 0.5rem;">📊</div>
                    <h3>Dataset Overview</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                        <div>
                            <p><strong>Records:</strong></p>
                            <p style="font-size: 1.5em; color: #3b82f6;">{len(df)}</p>
                        </div>
                        <div>
                            <p><strong>Features:</strong></p>
                            <p style="font-size: 1.5em; color: #ec4899;">{len(df.columns)}</p>
                        </div>
                        <div>
                            <p><strong>Brands:</strong></p>
                            <p style="font-size: 1.5em; color: #10b981;">{df['Company Names'].nunique()}</p>
                        </div>
                        <div>
                            <p><strong>Fuel Types:</strong></p>
                            <p style="font-size: 1.5em; color: #f59e0b;">{df['Fuel Types'].nunique()}</p>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_price = df['Parsed Price'].mean()
            median_price = df['Parsed Price'].median()
            std_price = df['Parsed Price'].std()
            min_price = df['Parsed Price'].min()
            max_price = df['Parsed Price'].max()
            
            st.markdown(f"""
            <div class="stats-container">
                <div style="text-align: center;">
                    <div style="font-size: 3em; margin-bottom: 0.5rem;">💰</div>
                    <h3>Price Analytics</h3>
                    <div style="margin-top: 1rem;">
                        <p><strong>Average:</strong> <span style="color: #3b82f6;">${avg_price:,.0f}</span></p>
                        <p><strong>Median:</strong> <span style="color: #ec4899;">${median_price:,.0f}</span></p>
                        <p><strong>Range:</strong> <span style="color: #10b981;">${min_price:,.0f} - ${max_price:,.0f}</span></p>
                        <p><strong>Std Dev:</strong> <span style="color: #f59e0b;">${std_price:,.0f}</span></p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_hp = df['Parsed HP'].mean()
            max_hp = df['Parsed HP'].max()
            avg_speed = df['Parsed Speed'].mean()
            max_speed = df['Parsed Speed'].max()
            
            st.markdown(f"""
            <div class="stats-container">
                <div style="text-align: center;">
                    <div style="font-size: 3em; margin-bottom: 0.5rem;">⚡</div>
                    <h3>Performance Stats</h3>
                    <div style="margin-top: 1rem;">
                        <p><strong>Avg Power:</strong> <span style="color: #3b82f6;">{avg_hp:.0f} HP</span></p>
                        <p><strong>Max Power:</strong> <span style="color: #ec4899;">{max_hp:.0f} HP</span></p>
                        <p><strong>Avg Speed:</strong> <span style="color: #10b981;">{avg_speed:.0f} km/h</span></p>
                        <p><strong>Top Speed:</strong> <span style="color: #f59e0b;">{max_speed:.0f} km/h</span></p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error displaying statistics: {e}")
    
    # Enhanced search and filter
    st.markdown("### 🔍 Advanced Search & Discovery")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_term = st.text_input(
            "🔎 Search the automotive universe:", 
            placeholder="Enter car model, brand, or any feature...",
            help="Search across all text fields in the dataset"
        )
    
    with col2:
        search_scope = st.selectbox(
            "🎯 Search Scope",
            ["All Fields", "Car Names", "Company Names", "Fuel Types", "Engines"]
        )
    
    # Advanced filtering
    with st.expander("🎛️ Advanced Filtering Engine", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            hp_range = st.slider(
                "⚡ Horsepower Range",
                min_value=int(df['Parsed HP'].min()),
                max_value=int(df['Parsed HP'].max()),
                value=(int(df['Parsed HP'].min()), int(df['Parsed HP'].max()))
            )
        
        with col2:
            speed_range = st.slider(
                "🏎️ Speed Range (km/h)",
                min_value=int(df['Parsed Speed'].min()),
                max_value=int(df['Parsed Speed'].max()),
                value=(int(df['Parsed Speed'].min()), int(df['Parsed Speed'].max()))
            )
        
        with col3:
            price_filter = st.slider(
                "💰 Price Filter ($)",
                min_value=int(df['Parsed Price'].min()),
                max_value=int(df['Parsed Price'].max()),
                value=(int(df['Parsed Price'].min()), int(df['Parsed Price'].max()))
            )
    
    # Apply search and filters
    try:
        filtered_data = df.copy()
        
        # Apply search
        if search_term:
            if search_scope == "All Fields":
                mask = df.apply(lambda x: x.astype(str).str.contains(search_term, case=False, na=False).any(), axis=1)
            else:
                column_map = {
                    "Car Names": "Car Names",
                    "Company Names": "Company Names", 
                    "Fuel Types": "Fuel Types",
                    "Engines": "Engines"
                }
                if search_scope in column_map:
                    mask = df[column_map[search_scope]].str.contains(search_term, case=False, na=False)
                else:
                    mask = df.apply(lambda x: x.astype(str).str.contains(search_term, case=False, na=False).any(), axis=1)
            
            filtered_data = filtered_data[mask]
        
        # Apply range filters
        filtered_data = filtered_data[
            (filtered_data['Parsed HP'] >= hp_range[0]) & (filtered_data['Parsed HP'] <= hp_range[1]) &
            (filtered_data['Parsed Speed'] >= speed_range[0]) & (filtered_data['Parsed Speed'] <= speed_range[1]) &
            (filtered_data['Parsed Price'] >= price_filter[0]) & (filtered_data['Parsed Price'] <= price_filter[1])
        ]
        
        # Display results
        st.markdown(f"### 🎯 Discovery Results ({len(filtered_data)} vehicles found)")
        
        if not filtered_data.empty:
            # Quick stats
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🚗 Found", len(filtered_data))
            with col2:
                st.metric("💰 Avg Price", f"${filtered_data['Parsed Price'].mean():,.0f}")
            with col3:
                st.metric("⚡ Avg HP", f"{filtered_data['Parsed HP'].mean():.0f}")
            with col4:
                st.metric("🏎️ Avg Speed", f"{filtered_data['Parsed Speed'].mean():.0f} km/h")
            
            # Enhanced data display
            display_columns = ['Car Names', 'Company Names', 'Cars Prices', 'HorsePower', 'Max Speed', 'Acceleration', 'Fuel Types', 'Engines']
            
            st.dataframe(
                filtered_data[display_columns],
                use_container_width=True,
                height=400,
                column_config={
                    "Car Names": st.column_config.TextColumn("🚗 Vehicle", width="large"),
                    "Company Names": st.column_config.TextColumn("🏢 Manufacturer", width="medium"),
                    "Cars Prices": st.column_config.TextColumn("💰 MSRP", width="medium"),
                    "HorsePower": st.column_config.TextColumn("⚡ Power", width="small"),
                    "Max Speed": st.column_config.TextColumn("🏎️ V-Max", width="small"),
                    "Acceleration": st.column_config.TextColumn("🚀 0-100", width="small"),
                    "Fuel Types": st.column_config.TextColumn("⛽ Fuel", width="small"),
                    "Engines": st.column_config.TextColumn("🔧 Engine", width="medium")
                }
            )
            
        else:
            st.warning("🔍 No vehicles match your criteria. Try broadening your search or adjusting filters.")
            
    except Exception as e:
        st.error(f"Error in search/filter: {e}")
    
    # Data quality and insights
    st.markdown("### 🧠 Data Intelligence Insights")
    
    tab1, tab2, tab3 = st.tabs(["📊 Statistical Analysis", "🔬 Data Quality", "🎯 Market Insights"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Distribution Analysis")
            analysis_column = st.selectbox(
                "Choose metric to analyze:",
                ['Parsed Price', 'Parsed HP', 'Parsed Speed', 'Parsed Acceleration']
            )
            
            if analysis_column:
                try:
                    fig_dist = px.histogram(
                        df.dropna(subset=[analysis_column]),
                        x=analysis_column,
                        title=f"📊 {analysis_column.replace('Parsed ', '')} Distribution",
                        nbins=25,
                        color_discrete_sequence=['#8b5cf6']
                    )
                    
                    mean_val = df[analysis_column].mean()
                    median_val = df[analysis_column].median()
                    
                    fig_dist.add_vline(x=mean_val, line_dash="dash", line_color="#ef4444", annotation_text="Mean")
                    fig_dist.add_vline(x=median_val, line_dash="dash", line_color="#10b981", annotation_text="Median")
                    
                    fig_dist.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        title_font_color='#8b5cf6'
                    )
                    st.plotly_chart(fig_dist, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Error creating distribution plot: {e}")
        
        with col2:
            st.subheader("🎭 Brand Performance")
            try:
                fig_violin = px.violin(
                    df.dropna(subset=[analysis_column]),
                    x='Company Names',
                    y=analysis_column,
                    title=f"🎭 {analysis_column.replace('Parsed ', '')} by Brand",
                    color='Company Names',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_violin.update_xaxes(tickangle=45)
                fig_violin.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    title_font_color='#ec4899',
                    showlegend=False
                )
                st.plotly_chart(fig_violin, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error creating violin plot: {e}")
    
    with tab2:
        st.subheader("🔬 Data Quality Assessment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Missing values analysis
            missing_data = df.isnull().sum()
            if missing_data.sum() > 0:
                fig_missing = px.bar(
                    x=missing_data.index,
                    y=missing_data.values,
                    title="🔍 Missing Data Analysis",
                    color=missing_data.values,
                    color_continuous_scale='Reds'
                )
                fig_missing.update_xaxes(tickangle=45)
                fig_missing.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    title_font_color='#ef4444'
                )
                st.plotly_chart(fig_missing, use_container_width=True)
            else:
                st.success("✅ Perfect Data Quality - No Missing Values!")
        
        with col2:
            # Data completeness
            completeness_df = pd.DataFrame({
                'Column': df.columns,
                'Data Type': df.dtypes.astype(str),
                'Non-Null %': (df.count() / len(df) * 100).round(1),
                'Unique Values': df.nunique(),
                'Memory Usage': df.memory_usage(deep=True).values
            })
            
            st.dataframe(
                completeness_df,
                use_container_width=True,
                column_config={
                    "Column": st.column_config.TextColumn("📋 Column", width="medium"),
                    "Data Type": st.column_config.TextColumn("🔤 Type", width="small"),
                    "Non-Null %": st.column_config.ProgressColumn("✅ Completeness", min_value=0, max_value=100, width="medium"),
                    "Unique Values": st.column_config.NumberColumn("🎯 Unique", width="small"),
                    "Memory Usage": st.column_config.NumberColumn("💾 Memory (bytes)", width="small")
                }
            )
    
        with col2:
            # Top performing brands
            brand_performance = df.groupby('Company Names').agg({
                'Parsed Price': 'mean',  # Average price
                'Parsed HP': 'mean',     # Average horsepower
                'Car Names': 'count'     # Number of models
            }).round(0)

            # Rename columns for better readability
            brand_performance = brand_performance.rename(columns={
                'Parsed Price': 'Avg Price (₹)',
                'Parsed HP': 'Avg HP',
                'Car Names': 'Model Count'
            }).sort_values(by='Model Count', ascending=False).head(10)

            # Create bar chart for brand performance
            fig_brand_bar = px.bar(
                brand_performance.reset_index(),
                x='Company Names',
                y='Model Count',
                title="🏆 Top Performing Brands by Model Count",
                text='Model Count',
                color='Model Count',
                color_continuous_scale=px.colors.sequential.Tealgrn
            )

            fig_brand_bar.update_traces(textposition='outside')
            fig_brand_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                title_font_color='#06b6d4',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False)
            )

            st.plotly_chart(fig_brand_bar, use_container_width=True)
