# ToTheMoon: Machine Learning-Driven Portfolio Simulation

**ToTheMoon** is a transparent, low-risk, machine learning-based portfolio simulation platform designed to dynamically allocate capital across various asset classes based on weekly market signals. The project bridges the gap in traditional models by integrating cross-asset strategies with macroeconomic-driven rebalancing.

---

## 🚀 Key Features

- **Three-Tiered Framework**: Strategies are categorized into **Growth** (Cryptocurrency/Growth stocks), **Stability** (Blue Chip stocks), and **Safety** (Gold/Cash).

- **Dynamic Capital Allocation**: Weekly rebalancing is guided by a market condition assessment model using the Volatility Index (VIX) and S&P 500 trend analysis to classify the market as Bullish, Neutral, or Bearish.

- **Predictive ML Models**: Employs Gradient Boosting and technical indicators such as RSI and MACD to generate asset-level price predictions and trading signals.

- **Risk Management**: Features inverse volatility weighting, confidence-scaled capital deployment, and automated take-profit/stop-loss thresholds.

- **Interactive Dashboard**: A multi-tab Streamlit frontend for visualizing portfolio value growth, snapshots, and historical asset performance.

---

## 📊 Methodology

### 1. Capital Allocation Model

The allocation strategy shifts based on a composite scoring system:

- **Bullish**: High Growth (45%), Blue Chip (35%), Gold (10%), Cash (10%)
- **Neutral**: High Growth (30%), Blue Chip (35%), Gold (20%), Cash (15%)
- **Bearish**: High Growth (20%), Blue Chip (35%), Gold (25%), Cash (20%)

---

### 2. Machine Learning Pipeline

- **Data**: Standardized OHLCV data from Jan-2020 to early 2025 across crypto (BTC, ETH, XRP), growth stocks, and blue chips.

- **Feature Engineering**: Technical indicators including Bollinger Bands, momentum, and moving averages.

- **Model Selection**: Random Forest for feature selection and Gradient Boosting for return prediction and classification.

---

## 📈 Performance Summary

The integrated portfolio demonstrates enhanced diversification and consistency across market conditions.

| Metric | Value |
|--------|-------|
| **Annual Return** | 7.33% |
| **Sharpe Ratio** | 0.75 |
| **Max Drawdown** | -1.19% |
| **Win Rate** | 59.20% |

---

## 🛠️ Tech Stack

- **Language**: Python  
- **Data Processing**: yfinance, technical indicator engineering  
- **Machine Learning**: Gradient Boosting, Random Forest  
- **Frontend**: Streamlit  

---

## 👥 Contributors

- **Sew Xuan Le**: Developed the Growth portfolio and trading models; evaluated overall performance.
- **Yeo Hiong Wu Darryl**: Developed the Stability portfolio, trading model, and the integrated Capital Allocation model.
- **Shayn Ang**: Developed the Safety portfolio and trading models.
- **Leow Yu Sheng**: Developed frontend dashboard tabs 1-2 and integrated backend models.
- **Terence Lai**: Developed frontend dashboard tabs 3-4 and UI improvements.
