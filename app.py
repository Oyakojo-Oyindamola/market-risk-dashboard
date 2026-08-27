
import pandas as pd 
import streamlit as st
import plotly.express as px 

st.set_page_config(
    layout="wide"
)

st.title("USD/NGN Market Risk Dashboard")
st.write(
    "An analysis of USD/NGN exchange-rate movements, votality, "
    "and the relationship between exchange-rate and Brent crude oil returns."
    )


data = pd.read_csv("cleaned_market_data.csv")

highest_exchange_rate = data['Exchange_Close'].max()
highest_exchange_date = data.loc[data['Exchange_Close'].idxmax(), 'Date']
lowest_exchange_rate = data['Exchange_Close'].min()
lowest_exchange_date = data.loc[data['Exchange_Close'].idxmin(), 'Date']
highest_volatility_year = data.groupby('Year')['Rolling_Volatility'].mean().idxmax()
lowest_volatility_year = data.groupby('Year')['Rolling_Volatility'].mean().idxmin()
brent_fx_correlation = data['Brent_Return'].corr(data['Exchange_Return'])
annual_exchange_rate = data.groupby('Year')['Exchange_Close'].mean()
annual_exchange_rate_df = annual_exchange_rate.reset_index()


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

st.subheader("Key Market Indicators")

col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    st.markdown(
       f"""
        <div class="metric-card">
            <p>🔺Highest FX</p>
            <h2 class ="fx-high">₦{highest_exchange_rate:,.2f}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <p>🔻Lowest FX</p>
            <h2>₦{lowest_exchange_rate}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <p>⚠️Highest Volatility Year</p>
            <h2>{highest_volatility_year}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <p>🛡️Lowest Volatility year</p>
            <h2>{lowest_volatility_year}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        f"""
        <div class=metric-card>
        <p>🔗Brent Fx Correlation</p>
        <h2>{brent_fx_correlation:,.2f}</h2>
        </div>
        """, 
        unsafe_allow_html=True
    )


st.markdown("""
<style>

.metric-card{
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #E5E7EB;
    color: #1F2937;
}
.metric-card p {
    color: #1F2937;
}
.fx-high{
    color:#1F4E79
    }   

.metric-card h2 {
    color: #1F4E79;
    font-size:15px;
    white-space: nowrap;    

    }

</style>
""",
unsafe_allow_html=True

)

fig_exchange = px.line(
    annual_exchange_rate_df, 
    y= 'Exchange_Close',
    x= 'Year',
    labels={
        'Year':'Year',
        'Exchange_Close': 'Exchange_Rate (₦)',
    }, 
     color_discrete_sequence= ['#1F4E79']
)


fig_exchange.update_yaxes(
    tickprefix = '₦', 
    tickformat = ',.0f'
)

fig_exchange.update_xaxes(
    dtick=2
)

fig_exchange.update_traces(
    hovertemplate = 'Year: %{x}<br>Average Exchange Rate: ₦%{y:,.2f}<extra></extra>'
)



milestones = pd.DataFrame({
    "Metric":[
        "Peak Exchange Rate", 
        "Lowest Exchange Rate",
        "Largest Daily Increase", 
        "Largest Daily Decrease"
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
    f"{highest_exchange_rate:,.2f}",
    f"{lowest_exchange_rate:,.2f}",
    f"{largest_daily_increase:.2%}",
    f"{largest_daily_decrease:.2%}"
]

milestones["Date_Display"] = pd.to_datetime(milestones['Date']).dt.strftime("%d %b %Y")

milestones_display = milestones[
        ['Metric', 'Value_Display', 'Date']].rename(columns={
            'Value_Display': 'Value',
            'Date_Display': 'Date'
    })

st.subheader("Exchange rate analysis")


col1, col2 = st.columns(2)


with col1:
    st.markdown("**USD/NGN Exchange Rate Over Time**")
    st.plotly_chart(fig_exchange)


with col2:
    st.subheader("Exchange rate insights")
    st.dataframe(milestones_display, hide_index=True, use_container_width= True)

st.subheader("Annual Average 30-Day Rolling Volatility")  

col1, col2 = st.columns(2)

annual_volatility = data.groupby('Year')['Rolling_Volatility'].mean()
annual_volatility_df = annual_volatility.reset_index()

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
   

fig_volatility.update_yaxes(
    tickformat= '.2%'
)

fig_volatility.update_xaxes(
    dtick=2 
)

fig_volatility.update_traces(
    hovertemplate='Year: %{x}<br>Average 30-Day Rolling Volatility: %{y:.2%}<extra></extra>'
)

highest_annual_volatility = annual_volatility.max() 
highest_rolling_volatility = annual_volatility.idxmax()
 
lowest_annual_volatility = annual_volatility.min()
lowest_rolling_volatility = annual_volatility.idxmin()

with col1:
    st.write("30-Day Rolling Volatility")
    st.plotly_chart(fig_volatility, use_container_width=True)


with col2:
    st.subheader('Volatility Highlights')

    st.write("Highest Volatility Year") 
    st.write(highest_rolling_volatility)

    st.write("Highest Average Volatility")
    st.write(f'{highest_annual_volatility:.2%}')

    st.write("Lowest Volatility Year")
    st.write(lowest_rolling_volatility)

    st.write("Lowest Average Volatility")
    st.write(f'{lowest_annual_volatility:.2%}')

st.subheader("Brent Crude Oil & Exchange Rate Relationship")

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
    hovertemplate=
    'USD/NGN Exchange Rate Return: %{x:.2%}<br>'
    'Brent Crude Oil Rerurn: %{y:.2%}'
    '<extra></extra>'
)

with col1:
    st.write('Brent Crude oil vs USD/NGN')
    col1.plotly_chart(fig_correlation)
    

with col2:
    st.subheader('Key Insights')
    st.write(
        f'Brent crude returns and USD/NGN exchange-rate returns '
        f'show almost no linear relationship in this dataset,  ' 
        f'of {brent_fx_correlation:.2f}.'
    )
    st.write(
        f'The highest average 30-day rolling volatility occurred in '
        f'{highest_rolling_volatility}, at '
        f'{highest_annual_volatility:.2%}.'
    )
    st.write(
        f'The USD/NGN exchange rate reached its peak of '
        f'₦{highest_exchange_rate:,.2f} on '
        f'{highest_exchange_date}.'
    )
    st.write(
        f'The largest daily increase in the USD/NGN exchange rate was '
        f'{largest_daily_increase:.2%} on {highest_increase_date} '
        f'while the highest decrease was  '
        f'{largest_daily_decrease:.2%} on {lowest_decrease_date}'
        
    )   

