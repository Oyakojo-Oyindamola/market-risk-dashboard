# Market Risk Dashboard

An interactive dashboard analysing USD/NGN exchange-rate movements, volatility, and the relationship between exchange-rate and Brent crude oil returns.

## Project Overview

This project analyses historical USD/NGN exchange-rate data alongside Brent crude oil prices to examine exchange-rate movements, market volatility, and the relationship between oil-price and exchange-rate returns.

The analysis covers daily market data and uses statistical analysis and visualisation to identify periods of heightened volatility and significant exchange-rate movements. The results are presented through an interactive Streamlit dashboard.

## Business Questions

The project investigates the following questions:

- What has the USD/NGN exchange rate looked like over time?
- When did the exchange rate experience its largest daily increases and decreases?
- How has exchange-rate volatility changed over time?
- Which periods experienced the highest levels of market volatility?
- What is the relationship between Brent crude oil returns and USD/NGN exchange-rate returns?

## Key Insights

- **Weak relationship between Brent crude oil and USD/NGN returns:** The correlation between Brent crude returns and USD/NGN exchange-rate returns was approximately -0.01, indicating almost no linear relationship in the dataset.

- **2024 recorded the highest average volatility:** The highest average 30-day rolling volatility occurred in 2024, at 2.57%.

- **Peak exchange-rate level:** The USD/NGN exchange rate reached a peak of ₦1,696.20 on 25 November 2024.

- **Significant daily movements:** The largest daily increase in the exchange rate was 41.05% on 22 June 2016, while the largest daily decrease was -27.95% on 15 June 2017.

## Tools & Technologies

- **Python** — data cleaning, transformation, and analysis
- **Pandas** — data manipulation and time-series analysis
- **Plotly** — interactive data visualisation
- **Streamlit** — interactive dashboard development
- **Jupyter Notebook** — exploratory analysis and development
- **Git & GitHub** — version control and project documentation

## Data

The analysis uses daily USD/NGN exchange-rate data alongside Brent crude oil price data.

The dataset was prepared for analysis by cleaning the raw market data, handling missing observations, and creating derived variables including:

- Daily exchange-rate returns
- Brent crude oil returns
- 30-day rolling volatility
- Brent return lagged by one period
- Annual and daily market indicators

## Methodology

The analysis was carried out using the following steps:

1. **Data preparation**
   - Loaded historical USD/NGN exchange-rate and Brent crude oil price data.
   - Inspected the datasets for missing values and data-quality issues.
   - Cleaned and prepared the data for analysis.

2. **Feature engineering**
   - Calculated daily exchange-rate returns.
   - Calculated Brent crude oil returns.
   - Calculated 30-day rolling volatility for the USD/NGN exchange rate.
   - Created lagged variables for return analysis.

3. **Exploratory and statistical analysis**
   - Examined exchange-rate movements over time.
   - Identified the largest daily increases and decreases.
   - Compared volatility across years.
   - Calculated the correlation between Brent crude oil returns and USD/NGN exchange-rate returns.

4. **Visualisation**
   - Created interactive charts using Plotly.
   - Presented key market indicators and findings through a Streamlit dashboard.

5. **Dashboard development**
   - Built an interactive Streamlit dashboard to communicate the main findings in a clear and accessible format.

## Dashboard

The Streamlit dashboard presents the analysis through interactive visualisations and key market indicators.

The dashboard includes:

- Key market indicators for the USD/NGN exchange rate and volatility
- USD/NGN exchange-rate movements over time
- Exchange-rate insights, including peak and lowest exchange-rate levels and significant daily movements
- Annual average 30-day rolling volatility
- Brent crude oil and USD/NGN return relationship
- Key analytical insights from the dataset

## How to Run the Project

### 1. Clone the repository

git clone https://github.com/Oyakojo-Oyindamola/market-risk-dashboard.git

cd market-risk-dashboard

### 2. Create and activate a virtual environment

python -m venv .venv

.venv\Scripts\activate

### 3. Install the required packages

pip install -r requirements.txt

### 4. Run the Streamlit dashboard

streamlit run app.py

The dashboard will open in your browser at the local Streamlit address provided in the terminal.


## Project Structure

- `app.py` — Streamlit dashboard application
- `market_price.ipynb` — Data cleaning, analysis, and exploratory work
- `cleaned_market_data.csv` — Cleaned dataset used by the dashboard
- `requirements.txt` — Python dependencies required to run the project
- `.gitignore` — Files and folders excluded from version control


## Limitations & Notes

- The analysis is based on historical market data and therefore describes past market behaviour rather than predicting future movements.
- Correlation measures the strength of a linear relationship between two variables and does not imply causation.
- The analysis uses daily market data, so short-term intraday movements are not captured.
- Exchange-rate and Brent crude oil data may be affected by differences in market timing and data availability.