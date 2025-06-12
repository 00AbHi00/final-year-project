import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# === FILE PATHS ===
FILE1_PATH = r"clean data\data\clean_data_v1.csv"
FILE2_PATH = r"clean data\data\recent_data_v2.csv"
DIVIDEND_PATH = r"clean data\data\dividend_history_v1.csv"  # update if needed

# === CHECK FILES EXIST ===
missing_files = []
for path in [FILE1_PATH, FILE2_PATH, DIVIDEND_PATH]:
    if not os.path.exists(path):
        missing_files.append(path)
if missing_files:
    st.error(f"CSV files missing! Please add these:\n" + "\n".join(missing_files))
    st.stop()

# === LOAD DATA ===
df1 = pd.read_csv(FILE1_PATH, parse_dates=["Date"])
df2 = pd.read_csv(FILE2_PATH, parse_dates=["Oldest Date", "Recent Date"])
df_div = pd.read_csv(DIVIDEND_PATH)

# Replace Sector with NaN as requested
if "Sector" in df1.columns:
    df1["Sector"] = np.nan

# === STREAMLIT PAGE SETUP ===
st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("Interactive Stock Market Dashboard with Dividends")

# Show summary table (file2)
st.subheader("Stock Summary (recent_data_v2.csv)")
st.dataframe(df2, use_container_width=True)

# Sidebar: select stock symbol
st.sidebar.header("Select Stock Symbol")
symbols = df1["Symbol"].dropna().unique()
selected_symbol = st.sidebar.selectbox("Choose Symbol", sorted(symbols))

# Filter detailed data for the selected symbol
filtered_df = df1[df1["Symbol"] == selected_symbol].sort_values("Date")

# Show detailed filtered data (file1)
st.subheader(f"Historical Data for `{selected_symbol}`")
st.dataframe(filtered_df, use_container_width=True)

# === Candlestick Chart filtered by Symbol ===
st.subheader("Candlestick Chart")
fig = go.Figure(data=[go.Candlestick(
    x=filtered_df['Date'],
    open=filtered_df['Open'],
    high=filtered_df['High'],
    low=filtered_df['Low'],
    close=filtered_df['Close'],
    increasing_line_color='green',
    decreasing_line_color='red',
    name='Price'
)])
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Price',
    xaxis_rangeslider_visible=True,
    template='plotly_white',
    height=600
)
st.plotly_chart(fig, use_container_width=True)

# === Volume Bar Chart ===
st.subheader("Volume Over Time")
fig_vol = px.bar(filtered_df, x='Date', y='Volume', title=f"Volume for {selected_symbol}",
                 labels={'Volume': 'Volume', 'Date': 'Date'}, template='plotly_white')
st.plotly_chart(fig_vol, use_container_width=True)

# === Percent Change Line Chart ===
st.subheader("Percent Change Over Time")
fig_pct = px.line(filtered_df, x='Date', y='Percent Change', title=f"Percent Change for {selected_symbol}",
                  labels={'Percent Change': 'Percent Change (%)', 'Date': 'Date'}, template='plotly_white')
fig_pct.add_hline(y=0, line_dash="dash", line_color="gray")
st.plotly_chart(fig_pct, use_container_width=True)

# === Dividend History for selected symbol ===
# === Dividend History for selected symbol ===
# === Dividend History for selected symbol ===
st.subheader(f"Dividend History for `{selected_symbol}`")

dividend_filtered = df_div[df_div["Symbol"] == selected_symbol]

if dividend_filtered.empty:
    st.info("No dividend history found for this symbol.")
else:
    # Define percentage columns
    pct_cols = ["Bonus %", "Cash %", "Total %"]
    
    # Format each column
    for col in pct_cols:
        if col in dividend_filtered.columns:
            def format_percent(x):
                try:
                    x = str(x).replace("%", "").strip()
                    num = float(x)
                    return f"{num:.2f}%"
                except:
                    return ""
            dividend_filtered[col] = dividend_filtered[col].apply(format_percent)

    st.dataframe(dividend_filtered.reset_index(drop=True), use_container_width=True)
