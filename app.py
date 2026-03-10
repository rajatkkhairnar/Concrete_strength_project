import streamlit as st
import pandas as pd
import pickle

# Load the model you just created locally
model = pickle.load(open('concrete_model.pkl', 'rb'))

st.set_page_config(page_title="Wonder Cement AI Advisor", layout="wide")

st.title("🏗️ Smart Concrete AI Advisor")
st.markdown("### Predicting strength and providing real-time mix adjustments.")

# Sidebar for user inputs
st.sidebar.header("Input Concrete Mix Design")
cement = st.sidebar.number_input("Cement (kg/m³)", value=300.0)
slag = st.sidebar.number_input("Blast Furnace Slag (kg/m³)", value=0.0)
fly_ash = st.sidebar.number_input("Fly Ash (kg/m³)", value=0.0)
water = st.sidebar.number_input("Water (kg/m³)", value=150.0)
superplast = st.sidebar.number_input("Superplasticizer (kg/m³)", value=0.0)
coarse_agg = st.sidebar.number_input("Coarse Aggregate (kg/m³)", value=1000.0)
fine_agg = st.sidebar.number_input("Fine Aggregate (kg/m³)", value=800.0)
age = st.sidebar.slider("Age (Days)", 1, 365, 28)

# FIX: Wrap inputs in a DataFrame with EXACT column names from your CSV
input_df = pd.DataFrame([[cement, slag, fly_ash, water, superplast, coarse_agg, fine_agg, age]],
                        columns=['Cement_1', 'Blast_Furnace_Slag_2', 'Fly_ash_3', 'Water_4', 
                                 'Superplasticizer_5', 'Coarse_Aggregate_6', 'Fine_Aggregate_7', 'Age'])

# Make Prediction
prediction = model.predict(input_df)[0]

# Display Results
st.metric("Predicted Compressive Strength", f"{prediction:.2f} MPa")

# Smart Advisor Logic
st.subheader("💡 AI Advisor Recommendations")
target_strength = 30.0 # Example Target for M30 grade

if prediction < target_strength:
    st.error(f"Predicted strength ({prediction:.2f} MPa) is below target ({target_strength} MPa).")
    st.write("### Recommended Actions:")
    if (water/cement) > 0.45:
        st.warning("👉 **Reduce Water-Cement Ratio:** Your W/C ratio is currently high. Try reducing water content.")
    if superplast == 0:
        st.info("👉 **Use Admixtures:** Consider adding a Superplasticizer to improve strength without adding water.")
else:
    st.success(f"✅ Predicted strength ({prediction:.2f} MPa) meets your target!")