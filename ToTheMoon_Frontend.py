import streamlit as st
import requests
import time
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, date
from streamlit_plotly_events import plotly_events




# Create tabs for navigation
tab1, tab2, tab3, tab4 = st.tabs(["📊 Portfolio Projection", "📊 Portfolio Snapshot", "💡 Portfolio Suggestions", "📈 Historical Performance"])

### ------------------- TAB 1: PORTFOLIO TRACKER ------------------- ###
with tab1:
    data = {
        "Date": pd.date_range(start="2025-03-01", end="2025-03-31"),
        "Total_Portfolio_Value": [
            9980, 9980, 9975, 9960, 9960, 9985, 9985, 10070, 10070, 10070,
            10060, 10060, 10060, 9970, 9970, 9970, 9970, 10390, 10400, 10420,
            10500, 10550, 10550, 10550, 10220, 10270, 10270, 10150, 10150, 10150, 10150
        ],
        "Blue_Chip_Value": [
            3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500,
            3400, 3400, 3400, 3400, 3400, 3400, 3400, 3500, 3500, 3500,
            3500, 3500, 3500, 3500, 3500, 3500, 3500, 3400, 3400, 3400, 3400
        ],
        "Gold_Cash_Value": [
            3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500,
            3500, 3500, 3500, 3500, 3500, 3500, 3500, 4600, 4600, 4600,
            4600, 4600, 4600, 4600, 4700, 4700, 4700, 4700, 4700, 4700, 4700
        ],
        "Growth_Crypto_Value": [
            2980, 2980, 2975, 2960, 2960, 2985, 2985, 4070, 4070, 4070,
            4160, 4160, 4160, 3170, 3170, 3170, 3170, 2290, 2300, 2320,
            2400, 2550, 2550, 2550, 920, 970, 970, 1350, 1350, 1350, 1350
        ]
    }

    df = pd.DataFrame(data)

    # Page title
    st.markdown("## 📊Portfolio Value Growth")
    st.markdown("Visualize portfolio performance using fixed model results. Adjust the capital and date range to see scaled outcomes.")

    # User inputs
    capital = st.number_input("💰 Enter initial capital ($)", value=10000, step=100)
    start_date = st.date_input("Start Date", value=date(2025, 3, 1), min_value=date(2025, 3, 1), max_value=date(2025, 3, 31))
    end_date = st.date_input("End Date", value=date(2025, 3, 31), min_value=date(2025, 3, 1), max_value=date(2025, 3, 31))

    if st.button("▶️ Run Simulation"):
        # Proportional scaling
        default_capital = 10000
        scale = capital / default_capital
        scaled_df = df.copy()
        for col in ["Total_Portfolio_Value", "Blue_Chip_Value", "Gold_Cash_Value", "Growth_Crypto_Value"]:
            scaled_df[col] *= scale

        # Filter by date
        mask = (scaled_df["Date"] >= pd.to_datetime(start_date)) & (scaled_df["Date"] <= pd.to_datetime(end_date))
        df_selected = scaled_df.loc[mask]

        # --- Plot 1 ---
        fig1 = px.line(
            df_selected,
            x="Date",
            y="Total_Portfolio_Value",
            title="📈 Total Portfolio Value vs Initial Capital",
            labels={"Total_Portfolio_Value": "Portfolio Value ($)"}
        )
        fig1.add_hline(
            y=capital,
            line_dash="solid",
            line_color="red",
            annotation_text=f"Initial Capital (${capital:,.0f})",
            annotation_position="top right"
        )
        fig1.update_traces(line_color="#00BFFF", name="Total Portfolio Value")
        st.plotly_chart(fig1, use_container_width=True)

        # --- Plot 2 ---
        fig2 = px.line(
            df_selected,
            x="Date",
            y=["Blue_Chip_Value", "Gold_Cash_Value", "Growth_Crypto_Value", "Total_Portfolio_Value"],
            labels={"value": "Value ($)", "variable": "Allocation"},
            title="📊 Portfolio Allocation Breakdown (March 2025)",
            line_dash_sequence=["dot", "dot", "dot", "solid"]
        )
        fig2.add_hline(
            y=capital,
            line_dash="solid",
            line_color="red",
            annotation_text=f"Initial Capital (${capital:,.0f})",
            annotation_position="top right"
        )
        st.plotly_chart(fig2, use_container_width=True)

        # --- Table ---
        st.markdown("### 📋 March Portfolio Snapshot")
        st.dataframe(
            df_selected[["Date", "Total_Portfolio_Value", "Blue_Chip_Value", "Gold_Cash_Value", "Growth_Crypto_Value"]],
            use_container_width=True
        )
### ------------------- TAB 3: PORTFOLIO SUGGESTIONS ------------------- ###
with tab3:
    st.title("💡 Portfolio Suggestions")

    # -- 1) Blue-bordered text block above the pie chart
    st.markdown(
        """
        <div style="border: 2px solid #3498DB; border-radius: 5px; padding: 10px;">
            <strong style="font-size:1.4em;">🚀 ToTheMoon Trading Model 🌝</strong><br><br>
            This model helps investors grow their money through smart, low-risk investing. Each week, money is automatically split across different 
            assets like blue chip stocks, growth stocks, cryptocurrency, gold and liquid USD — based on market signals. The model tracks portfolios 
            daily, reinvests profits, and adjusts to changing conditions so that investments stay balanced, on track and low risk.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Initialize session state for toggling the Growth breakdown
    if "growth_chart" not in st.session_state:
        st.session_state.growth_chart = False

    # --- 2) Base portfolio data & pie chart
    base_portfolio = {
        "Growth": 40,
        "Blue Chip": 30,
        "Gold": 20,
        "Cash": 10
    }
    df = pd.DataFrame({
        "Category": list(base_portfolio.keys()),
        "Allocation": list(base_portfolio.values())
    })

    # Base chart with fixed width & height
    base_colors = ["#7FB3D5", "#7DCEA0", "#F7DC6F", "#B3B6B7"]
    base_fig = px.pie(
        df,
        names="Category",
        values="Allocation",
        hole=0.4,
        color_discrete_sequence=base_colors
    )
    base_fig.update_layout(
        template="plotly_dark",
        width=600,
        height=500,
        margin=dict(l=50, r=50, t=30, b=150),  # increased bottom margin
        legend=dict(
            orientation="h",
            x=0.5,
            y=-0.3,      # moved legend further down
            xanchor="center"
        )
    )

    # --- 3) Centered header + chart for Base Portfolio
    st.markdown(
        """
        <div style="width:600px; margin:50 auto; text-align:left;">
            <h3>Base Portfolio Allocation</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div style='width:600px; margin:50 auto; text-align:center;'>", unsafe_allow_html=True)
    clicked_events = plotly_events(
        base_fig,
        click_event=True,
        hover_event=False,
        select_event=False,
        override_width=600,
        override_height=500
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # --- 4) Toggle second chart by clicking the "Growth" slice
    if clicked_events:
        point_index = clicked_events[0]["pointNumber"]
        clicked_label = df["Category"].iloc[point_index]
        if clicked_label == "Growth":
            st.session_state.growth_chart = not st.session_state.growth_chart

    # --- 5) Conditionally show/hide the Growth breakdown chart
    if st.session_state.growth_chart:
        # Growth breakdown data
        growth_breakdown = {
            "Growth Stocks": 70,
            "Crypto": 30
        }
        growth_df = pd.DataFrame({
            "SubCategory": list(growth_breakdown.keys()),
            "Allocation": list(growth_breakdown.values())
        })

        growth_colors = ["#B39DDB", "#F0B27A"]
        growth_fig = px.pie(
            growth_df,
            names="SubCategory",
            values="Allocation",
            hole=0.4,
            color_discrete_sequence=growth_colors
        )
        growth_fig.update_layout(
            template="plotly_dark",
            width=600,
            height=500,
            margin=dict(l=50, r=50, t=30, b=150),
            legend=dict(
                orientation="h",
                x=0.5,
                y=-0.3,
                xanchor="center"
            )
        )

        # Centered heading for the second chart
        st.markdown(
            """
            <div style="width:600px; margin:50 auto; text-align:left;">
                <h3>Breakdown of Growth Category</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<div style='width:600px; margin:50 auto; text-align:center;'>", unsafe_allow_html=True)
        st.plotly_chart(growth_fig, use_container_width=False)
        st.markdown("</div>", unsafe_allow_html=True)

### ------------------- TAB 4: HISTORICAL PERFORMANCE ------------------- ###
with tab4:
    st.title("📈 Historical Performance")

# Load your CSV file with historical trading data
    data_file = "Master Sheet.csv"
    try:
        # Parse the "Date" column as datetime
        df = pd.read_csv(data_file, parse_dates=["Date"])
    except Exception as e:
        st.error(f"Error loading data from {data_file}: {e}")
        st.stop()

    # Ensure the expected columns exist
    required_columns = ["Name", "Date", "Close"]
    for col in required_columns:
        if col not in df.columns:
            st.error(f"Missing required column '{col}' in CSV.")
            st.stop()

    # Convert "Date" to datetime if not already and "Close" to numeric
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    # Build a list of unique assets from the "Name" column
    assets_list = sorted(df["Name"].unique().tolist())

    # Drop-down for asset selection; this will update the title dynamically
    selected_asset = st.selectbox("Select an Asset", assets_list)

    # Filter DataFrame to rows for that asset
    asset_data = df[df["Name"] == selected_asset].copy()

    if asset_data.empty:
        st.warning(f"No data found for the asset: {selected_asset}")
    else:
        # Sort dates for this asset
        asset_data.sort_values("Date", inplace=True)
        min_date = asset_data["Date"].iloc[0].date()
        max_date = asset_data["Date"].iloc[-1].date()

        # Separate date pickers for start and end dates
        start_date = st.date_input(
            "Select Start Date",
            value=min_date,
            min_value=min_date,
            max_value=max_date
        )
        end_date = st.date_input(
            "Select End Date",
            value=max_date,
            min_value=min_date,
            max_value=max_date
        )

        if start_date > end_date:
            st.warning("⚠️ Start date must be on or before the end date.")
        else:
            # Filter data based on the chosen date range
            mask = (asset_data["Date"].dt.date >= start_date) & (asset_data["Date"].dt.date <= end_date)
            filtered_data = asset_data.loc[mask]

            if filtered_data.empty:
                st.warning("No data available for the selected date range.")
            else:
                st.write(f"**Displaying data for {selected_asset} from {start_date} to {end_date}.**")
                # Plot historical closing prices with a dynamic title based on the asset
                fig = px.line(
                    filtered_data,
                    x="Date",
                    y="Close",
                    title=f"{selected_asset} Historical Closing Prices",
                    labels={"Close": "Closing Price (USD)"}
                )
                st.plotly_chart(fig)

### ------------------- TAB 2: PORTFOLIO SNAPSHOT------------------- ###

with tab2:
    st.title("📊 Portfolio Snapshot")

    st.markdown("""
    <div style="border: 1px solid #00cc99; border-radius: 6px; padding: 15px; background-color: #0e1117;">
        <h4 style="color:#3ecf8e;">📘 Portfolio Allocation Viewer</h4>
        <ul style="line-height: 1.7;">
            <li><strong>Best For:</strong> Reviewing daily allocations during your simulation.</li>
            <li>Select a date to see <strong>which assets</strong> you were holding and their weights.</li>
            <li>Understand how your capital was allocated and shifted across days.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ---- Portfolio snapshot ---- #
    data = {
        "Date": pd.date_range(start="2025-03-01", end="2025-03-31"),
        "Total Portfolio": [
            9980, 9980, 9975, 9960, 9960, 9985, 9985, 10070, 10070, 10070, 10060, 10060, 10060, 9970, 9970, 9970,
            9970, 10390, 10400, 10420, 10500, 10550, 10550, 10550, 10220, 10270, 10270, 10150, 10150, 10150, 10150
        ],
        "Blue Chip": [
            3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3400, 3400, 3400, 3400, 3400, 3400,
            3400, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3400, 3400, 3400, 3400
        ],
        "Gold & Cash": [
            3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500, 3500,
            3500, 4600, 4600, 4600, 4600, 4600, 4600, 4600, 4700, 4700, 4700, 4700, 4700, 4700, 4700
        ],
        "Growth & Crypto": [
            2980, 2980, 2975, 2960, 2960, 2985, 2985, 4070, 4070, 4070, 4160, 4160, 4160, 3170, 3170, 3170,
            3170, 2290, 2300, 2320, 2400, 2550, 2550, 2550, 920, 970, 970, 1350, 1350, 1350, 1350
        ]
    }

    df = pd.DataFrame(data)

    # ---- Pie chart generator ---- #
    def get_allocation_pie_chart(selected_date_str: str):
        capital = 10000.0
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        row = df[df["Date"] == pd.Timestamp(selected_date)]

        if row.empty:
            return None

        proportions = row[["Blue Chip", "Gold & Cash", "Growth & Crypto"]].iloc[0] / 10000
        allocations_scaled = proportions * capital

        pie_df = pd.DataFrame({
            "Asset Class": allocations_scaled.index,
            "Value ($)": allocations_scaled.values
        })

        fig = px.pie(
            pie_df,
            names="Asset Class",
            values="Value ($)",
            title=f"📊 Portfolio Allocation on {selected_date}",
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig

    # ---- User Inputs ---- #
    selected_date = st.date_input(
        "📅 Select a Date", 
        min_value=datetime(2025, 3, 1), 
        max_value=datetime(2025, 3, 31), 
        value=datetime(2025, 3, 15)
    )

    if st.button("📊 Show Allocation Pie Chart"):
        fig = get_allocation_pie_chart(str(selected_date))
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for the selected date.")


  