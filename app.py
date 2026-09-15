
import pandas as pd 
import streamlit as st
import plotly.express as px 

st.set_page_config(
    layout="wide"
)

data = pd.read_csv("cleaned_market_data.csv")
data['Date'] = pd.to_datetime(data["Date"])

col1, col2 = st.columns([3, 1])

with col1:
    st.title("USD/NGN Market Risk Dashboard")
    st.write(
        "AN ANALYSIS OF USD/NGN EXCHANGE-RATE MOVEMENTS, VOLATILITY, "
        "AND THE RELATIONSHIP BETWEEN EXCHANGE-RATE AND BRENT CRUDE OIL RETURNS."
    )


with col2:
    st.write("Date Range")

    date_range = st.date_input(
        "Data Range",
        value = (data["Date"].min().date(), data['Date'].max().date()),
        format="YYYY-MM-DD",
        label_visibility="collapsed"
    )

if len(date_range) == 2:
    start_date, end_date = date_range

    data = data[
        (data["Date"] >= pd.Timestamp(start_date)) &
        (data["Date"] <= pd.Timestamp(end_date))
    ]

highest_exchange_rate = data['Exchange_Close'].max()
highest_exchange_date = data.loc[data['Exchange_Close'].idxmax(), 'Date']
lowest_exchange_rate = data['Exchange_Close'].min()
lowest_exchange_date = data.loc[data['Exchange_Close'].idxmin(), 'Date']
highest_volatility_year = data.groupby('Year')['Rolling_Volatility'].mean().idxmax()
lowest_volatility_year = data.groupby('Year')['Rolling_Volatility'].mean().idxmin()
brent_fx_correlation = data['Brent_Return'].corr(data['Exchange_Return'])
annual_exchange_rate = data.groupby('Year')['Exchange_Close'].mean()
annual_exchange_rate_df = annual_exchange_rate.reset_index()
annual_volatility = data.groupby('Year')['Rolling_Volatility'].mean()
annual_volatility_df = annual_volatility.reset_index()

highest_annual_volatility = annual_volatility.max() 
highest_rolling_volatility = annual_volatility.idxmax()
lowest_annual_volatility = annual_volatility.min()
lowest_rolling_volatility = annual_volatility.idxmin()

volatility_points = pd.DataFrame({
    "Year": [
        highest_rolling_volatility,
        lowest_rolling_volatility
    ],
    "Rolling_Volatility": [
        highest_annual_volatility,
        lowest_annual_volatility
    ]
})

largest_daily_increase = data['Exchange_Return'].max()
highest_increase_date= data.loc[
    data['Exchange_Return'].idxmax(),
    'Date'
]

largest_daily_decrease = data['Exchange_Return'].min()
lowest_decrease_date = data.loc[
    data ['Exchange_Return'].idxmin(),
    'Date'
    ]

st.subheader("KEY MARKET INDICATORS")

col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    st.markdown(
       f"""
        <div class="metric-card">
            <p>🔺HIGHEST EXCHANGE RATE</p>
            <h2 class ="fx-high">₦{highest_exchange_rate:,.2f}</h2>
            <p class="metric-date">{highest_exchange_date.strftime("%d %b %Y")}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <p>🔻LOWEST EXCHANGE RATE</p>
            <h2>₦{lowest_exchange_rate:,.2f}</h2>
            <p class="metric-date">{lowest_exchange_date.strftime("%d %b %Y")}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <p>⚠️HIGHEST VOLATILITY YEAR</p>
            <h2>{highest_volatility_year}</h2>
            <p class="metric-date">Avg Volatility: {highest_annual_volatility:.2%}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <p>🛡️LOWEST VOLATILITY YEAR</p>
            <h2>{lowest_volatility_year}</h2>
            <p class= "metric-date">Avg Volatility: {lowest_annual_volatility:.2%}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        f"""
        <div class=metric-card>
        <p>🔗BRENT FX CORRELATION</p>
        <h2>{brent_fx_correlation:,.2f}</h2>
        <p class="metric-date">(Almost no linear relationship)</p>
     </div>
     """, 
    unsafe_allow_html=True
    )


st.markdown("""
<style>

.metric-card {
    background-color: #111827;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #334155;
    color: white;
}
.metric-card p {
    color: #E5E7EB;
}
.metric-date {
    font-size: 13px;
    color: #94A3B8;
    margin-top: 5px;
}
.fx-high{
    color:#1F4E79
    }   

.metric-card h2 {
    color: white;
    font-size:24px;
    white-space: nowrap;    

    }
.vol-high {
    background-color: #0B3D2E;
    color: #22C55E;
    padding: 4px 8px;
    border-radius: 5px;
    font-weight: bold;
}

.vol-low {
    background-color: #172554;
    color: #60A5FA;
    padding: 4px 8px;
    border-radius: 5px;
    font-weight: bold;
}

.vol-row {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: center;
    column-gap: 16px;
    margin-bottom: 12px;
}
</style>
""",
unsafe_allow_html=True

)


fig_exchange = px.area(
    annual_exchange_rate_df, 
    y= 'Exchange_Close',
    x= 'Year',
    labels={
        'Year':'Year',
        'Exchange_Close': 'Exchange_Rate (₦)',
    }, 
     color_discrete_sequence= ["#1F3779"]
)


fig_exchange.update_yaxes(
    tickprefix = '₦', 
    tickformat = ',.0f'
)

fig_exchange.update_layout(
    margin=dict(l=10, r=10, t=30, b=10),
    height=250,
    hovermode="x unified"
)

fig_exchange.update_xaxes(
    dtick=2
)

fig_exchange.update_traces(
    hovertemplate = 'Year: %{x}<br>Average Exchange Rate: ₦%{y:,.2f}<extra></extra>'
)



milestones = pd.DataFrame({
    "Metric":[
        "PEAK EXCHANGE RATE", 
        "LOWEST EXCHANGE RATE",
        "LARGEST DAILY INCREASE", 
        "LARGEST DAILY DECREASE"
        ], 
    "Value":[
        highest_exchange_rate,
        lowest_exchange_rate,
        largest_daily_increase,
        largest_daily_decrease
        ],
    "Date": [
        highest_exchange_date,
        lowest_exchange_date,
        highest_increase_date,
        lowest_decrease_date
    ]
})

milestones['Value_Display'] = [
    f"₦{highest_exchange_rate:,.2f}",
    f"₦{lowest_exchange_rate:,.2f}",
    f"{largest_daily_increase:.2%}",
    f"{largest_daily_decrease:.2%}"
]

milestones["Date_Display"] = pd.to_datetime(milestones['Date']).dt.strftime("%d %b %Y")

milestones_display = milestones[
        ['Metric', 'Value_Display', 'Date_Display']].rename(columns={
            'Value_Display': 'Value',
            'Date_Display': 'Date'
    })

st.subheader("1. EXCHANGE RATE ANALYSIS")

col1, col2 = st.columns(2)


with col1:
    st.markdown("**USD/NGN Exchange Rate Over Time**")
    st.plotly_chart(fig_exchange)


with col2:
    st.subheader("Exchange rate insights")

    styled_milestones = milestones_display.style

    styled_milestones = styled_milestones.apply(
    lambda row: [
        "color: #F59E0B; font-weight: bold;" if row["Metric"] == "PEAK EXCHANGE RATE" and col == "Value"
        else "color: #3B82F6; font-weight: bold;" if row["Metric"] == "LOWEST EXCHANGE RATE" and col == "Value"
        else "color: #22C55E; font-weight: bold;" if row["Metric"] == "LARGEST DAILY INCREASE" and col == "Value"
        else "color: #EF4444; font-weight: bold;" if row["Metric"] == "LARGEST DAILY DECREASE" and col == "Value"
        else ""
        for col in row.index
    ],
    axis=1
)

    st.dataframe(
        styled_milestones,
        hide_index=True,
        use_container_width=True
    )


st.subheader("2. VOLATILITY ANALYSIS")  

col1, col2 = st.columns(2)


fig_volatility = px.line(
    annual_volatility_df,
    x= 'Year',
    y= 'Rolling_Volatility',
    labels= {
        'Year':'Year',
        'Rolling_Volatility':'30-Day Rolling Volatility (%)'
    }, 

    color_discrete_sequence=['#1F4E79']
    )
    
fig_volatility.add_scatter(
    x=[highest_rolling_volatility],
    y=[highest_annual_volatility],
    mode="markers",
    marker=dict(size=10, color="#F59E0B"),
    name="Highest Volatility"
)

fig_volatility.add_scatter(
    x=[lowest_rolling_volatility],
    y=[lowest_annual_volatility],
    mode="markers",
    marker=dict(size=10, color="#3B82F6"),
    name="Lowest Volatility"
)

fig_volatility.update_yaxes(
    tickformat= '.2%'
)

fig_volatility.update_xaxes(
    dtick=2 
)

fig_volatility.update_layout(
    margin=dict(l=10, r=10, t=30, b=10),
    height=270,
    hovermode="x unified"
)

fig_volatility.update_traces(
    hovertemplate='Year: %{x}<br>Average 30-Day Rolling Volatility: %{y:.2%}<extra></extra>'
)


with col1:
    st.write("30-Day Rolling Volatility")
    st.plotly_chart(fig_volatility, use_container_width=True)


with col2:
    st.subheader('Volatility Highlights')

    st.markdown(
    f"""
    <div class="vol-row">
        <span>Highest Volatility Year</span>
        <span class="vol-high">{highest_rolling_volatility}</span>
    </div>

    <div class="vol-row">
        <span>Highest Average Volatility</span>
        <span class="vol-high">{highest_annual_volatility:.2%}</span>
    </div>

    <div class="vol-row">
        <span>Lowest Volatility Year</span>
        <span class="vol-low">{lowest_rolling_volatility}</span>
    </div>

    <div class="vol-row">
        <span>Lowest Average Volatility</span>
        <span class="vol-low">{lowest_annual_volatility:.2%}</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("3. BRENT CRUDE OIL & EXCHANGE RATE RELATIONSHIP")

col1, col2 = st.columns(2)

fig_correlation = px.scatter(
    data, 
    x='Exchange_Return',
    y='Brent_Return',
    labels={
        'Exchange_Return': 'USD/NGN Exchange Rate Return',
        'Brent_Return': 'Brent Crude Oil Return'
    },
    trendline='ols',
    color_discrete_sequence= ['#1F4E79']
)

fig_correlation.update_traces(
    marker=dict(
        size=6,
        opacity=0.6
    )
)

fig_correlation.update_traces(
    selector=dict(mode="lines"),
    line=dict(width=3)
)

fig_correlation.update_layout(
    margin=dict(l=10, r=10, t=30, b=10),
    height=300,
    hovermode="closest"
)

fig_correlation.update_traces(
    hovertemplate=
    'USD/NGN Exchange Rate Return: %{x:.2%}<br>'
    'Brent Crude Oil Rerurn: %{y:.2%}'
    '<extra></extra>'
)

formatted_highest_exchange_date = highest_exchange_date.strftime("%d %b %Y")
formatted_highest_increase_date = highest_increase_date.strftime("%d %b %Y")
formatted_lowest_decrease_date = lowest_decrease_date.strftime("%d %b %Y")

with col1:
    st.write('Brent Crude oil vs USD/NGN')
    col1.plotly_chart(fig_correlation)
    

with col2:
    st.write('Key Insights')
    st.write(
        f'✅  Brent crude returns and USD/NGN exchange-rate returns '
        f'show almost no linear relationship in this dataset, with a correlation  ' 
        f'of {brent_fx_correlation:.2f}.'
    )
    st.write(
        f'✅  The highest average 30-day rolling volatility occurred in '
        f'{highest_rolling_volatility}, at '
        f'{highest_annual_volatility:.2%}.'
    )
    st.write(
        f'✅  The USD/NGN exchange rate reached its peak of '
        f'₦{highest_exchange_rate:,.2f} on '
        f'{formatted_highest_exchange_date}.'
    )
    st.write(
        f'✅  The largest daily increase in the USD/NGN exchange rate was '
        f'{largest_daily_increase:.2%} on {formatted_highest_increase_date} '
        f'while the highest decrease was  '
        f'{largest_daily_decrease:.2%} on {formatted_lowest_decrease_date}'
        
    )   

