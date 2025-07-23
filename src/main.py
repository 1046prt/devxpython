import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Luxury Car Explorer", layout="wide", page_icon="🚘")

with st.sidebar:
    st.title("🛠️ Settings")
    dark_mode = st.toggle("🌙 Dark Mode", value=False)

if dark_mode:
    st.markdown("""
    <style>
        body { background-color: #0e1117; color: white; }
        .stDataFrame { background-color: #1e1e1e; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("components/data/car_dataset.csv", encoding="cp1252")

df = load_data()
df.columns = [col.strip() for col in df.columns]

def parse_price(price):
    try:
        return float(str(price).replace("$", "").replace(",", "").split("-")[0])
    except:
        return None

def parse_hp(hp):
    try:
        return float(str(hp).replace(" hp", "").split("-")[0])
    except:
        return None

df['Parsed Price'] = df['Cars Prices'].apply(parse_price)
df['Parsed HP'] = df['HorsePower'].apply(parse_hp)

st.title("🚗 Luxury Car Explorer")
st.markdown("""
Welcome to the **interactive luxury car dashboard** 🚀  
Explore car specs, filter brands, and visualize performance data in real-time!
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Cars", value=len(df))
with col2:
    st.metric("Max HP", value=f"{int(df['Parsed HP'].max())} hp")
with col3:
    st.metric("Most Expensive", value=f"${int(df['Parsed Price'].max()):,}")

with st.expander("🎛️ Show Filters"):
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_brand = st.selectbox("Brand", ['All'] + sorted(df['Company Names'].unique()))
    with col2:
        selected_fuel = st.selectbox("Fuel Type", ['All'] + sorted(df['Fuel Types'].unique()))
    with col3:
        selected_engine = st.selectbox("Engine", ['All'] + sorted(df['Engines'].unique()))

    filtered_df = df.copy()
    if selected_brand != 'All':
        filtered_df = filtered_df[filtered_df['Company Names'] == selected_brand]
    if selected_fuel != 'All':
        filtered_df = filtered_df[filtered_df['Fuel Types'] == selected_fuel]
    if selected_engine != 'All':
        filtered_df = filtered_df[filtered_df['Engines'] == selected_engine]

st.subheader("📊 Horsepower vs Price Comparison")
st.caption("Explore how engine power affects pricing.")
st.scatter_chart(filtered_df.dropna(subset=['Parsed Price', 'Parsed HP'])[['Parsed Price', 'Parsed HP']])

st.subheader("🏷️ Car Brands by Count")
brand_counts = filtered_df['Company Names'].value_counts().reset_index()
brand_counts.columns = ['Brand', 'Number of Cars']
st.bar_chart(brand_counts.set_index('Brand'))

st.subheader("🔍 Filtered Car Details")
st.dataframe(filtered_df, use_container_width=True)

csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download Filtered Cars as CSV",
    data=csv,
    file_name='filtered_car_data.csv',
    mime='text/csv'
)

st.subheader("💡 Feature Highlights")
st.markdown("""
- **Max Speed**: Up to `356 km/h` 🏎️  
- **Horsepower**: Ranges from 70 hp to 963 hp ⚡  
- **Price Spectrum**: From `$12,000` to `$4.5M` 💰  
- **Fuel**: Mostly Petrol, some Plug-in Hybrids  
""")

st.subheader("🤖 Coming Soon: Model Training")
st.info("You’ll soon be able to train regression models to predict price or performance from car specs.")

st.markdown("---")
st.markdown("<center>Made with Streamlit • 2025</center>", unsafe_allow_html=True)
