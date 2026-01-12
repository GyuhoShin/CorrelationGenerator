import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats

# 1. Load Data
try:
    df = pd.read_csv("dataset.csv")
except FileNotFoundError:
    st.error("dataset.csv not found! Please make sure it is in the same folder.")
    st.stop()

# 2. Page Config (Wide layout is crucial here)
st.set_page_config(page_title="Correlation Explorer", layout="wide")

# Use a smaller header to save vertical space
st.markdown("### US State Data Explorer")

# --- PRE-PROCESSING ---
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
if "State" in numeric_cols: numeric_cols.remove("State")
if "state" in numeric_cols: numeric_cols.remove("state")

# --- SIDEBAR: VARIABLE LIST ---
with st.sidebar:
    st.header("📚 Variable List")
    # 1. Define your Categories manually here
    # Keys are the Category Names, Values are the lists of exact column names
    categories = {
        "👥 Demographics": [
            "Total Population", "Population Under 18 Pct", "Population Over 65 Pct", 
            "Foreign Born Pct", "Non English Home Pct", 
            "Married Couple Household Pct"
        ],
        "💰 Economy & Wealth": [
            "Median Income", "Poverty Rate", "Unemployment Rate", 
            "Food Stamps Pct", "Uninsured Pct", "Income Over 200k Pct"
        ],
        "🎓 Education": [
            "Bachelor Degree Pct", "High School Grad Pct"
        ],
        "🏠 Housing & Lifestyle": [
            "Total Housing Units", "Work From Home Pct", "Mean Commute Time", 
            "Public Transit Pct", "Non Family House Pct"
        ],

    }

    for category_name, variable_list in categories.items():
            st.markdown(f"### {category_name}")
            for var in variable_list:
                if var in numeric_cols:
                    st.markdown(f"• {var}") 
            st.write("")

# --- MAIN LAYOUT: SPLIT SCREEN ---
# Create two columns: 
# Left (1 part) = Controls & Stats
# Right (3 parts) = The Chart
left_col, right_col = st.columns([1, 4])

# --- LEFT COLUMN: CONTROLS & STATS ---
with left_col:
    st.markdown("#### 1. Axis Selection")
    
    # Y-Axis first (Intuitive since Y is vertical)
    # Using index=1 (defaulting to 2nd variable)
    default_x = 1 if len(numeric_cols) > 1 else 0
    y_var = st.selectbox("Vertical Axis (Y):", numeric_cols, index=0)
    
    # X-Axis second
    x_var = st.selectbox("Horizontal Axis (X):", numeric_cols, index=default_x)
    
    st.divider()
    
    # Calculate Stats immediately
    valid_data = df[[x_var, y_var]].dropna()
    r, p_value = stats.pearsonr(valid_data[x_var], valid_data[y_var])
    r_squared = r ** 2

    # Display Stats vertically in the side panel
    st.markdown("#### 2. Statistics")
    st.metric("Correlation (r)", f"{r:.3f}")
    st.metric("R-Squared (r²)", f"{r_squared:.3f}")
    # Shorten p-value logic for cleaner display
    p_text = "< 0.001" if p_value < 0.001 else f"{p_value:.3f}"
    st.metric("P-Value", p_text)

# --- RIGHT COLUMN: THE CHART ---
with right_col:
    # We remove the subheader title to save space, the chart has a title anyway
    fig = px.scatter(
        df, 
        x=x_var, 
        y=y_var, 
        hover_name="State", 
        trendline="ols",
        title=f"Scatterplot: {x_var} vs. {y_var}", # Title inside the chart
        height=600 # You can keep it tall now because it has the whole column!
    )

    fig.update_layout(
        template="plotly_white",
        margin=dict(t=50, b=50, l=50, r=50) # Tweak margins to fit better
    )

    st.plotly_chart(fig, use_container_width=True)

# --- FOOTER ---
# This stays at the bottom for those who want to scroll down
with st.expander("🔎 View Raw Data"):
    selected_cols = ["State", x_var, y_var]
    selected_cols = list(dict.fromkeys(selected_cols))
    st.dataframe(df[selected_cols], height=1823)

st.divider()
st.markdown("### 📝 Data Source")
st.caption("""
**Source:** U.S. Census Bureau, 2024 American Community Survey (ACS) 1-Year Estimates.  
""")