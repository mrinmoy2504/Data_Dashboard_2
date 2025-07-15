
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.title(body = "Microsoft vs Google - Stock Price Analysis(2015-2024)")
col = st.columns(( 4 , 4) , gap = 'medium')
st.set_page_config(page_title='Stock Market Analysis' , page_icon='📶',layout="wide" , initial_sidebar_state='auto' )


ms_df = pd.read_csv("Microsoft_stock_data.csv")
g_df = pd.read_csv("GoogleStockPrices.csv")

#datetime
ms_df['Date'] = pd.to_datetime(ms_df['Date'])
ms_df = ms_df[(ms_df['Date'] >= '2015-01-02 00:00:00') & (ms_df['Date'] <= '2024-12-31 00:00:00')]
g_df['Date'] = pd.to_datetime(g_df['Date'])
g_df['Date'] = g_df['Date'].dt.normalize() + pd.Timedelta(hours=0)

ms_df.sort_values('Date' , inplace= True)
g_df.sort_values('Date' , inplace= True)



#renaming columns 
ms_df = ms_df.rename (columns= {
    'Date' : 'date',
    'Open' : 'Open MSFT' ,
    'High' : 'High MSFT' ,
    'Low' : 'Low MSFT' ,
    'Close' : 'Close MSFT' ,
    'Volume' : 'Volume MSFT'
})

g_df= g_df.rename (columns= {
    'Date' : 'date',
    'Open' : 'Open GOOGL' ,
    'High' : 'High GOOGL' ,
    'Low' : 'Low GOOGL' ,
    'Close' : 'Close GOOGL' ,
    'Volume' : 'Volume GOOGL'
})



#st.dataframe(ms_df , hide_index= True )
#st.dataframe(g_df , hide_index= True)
merged_df = pd.merge(ms_df, g_df, on='date', how='outer')

 #daily return percentage
merged_df['Daily Return MSFT'] = merged_df['Close MSFT'].pct_change() * 100
merged_df['Daily Return Google'] = merged_df['Close GOOGL'].pct_change() * 100

#moving avg
for window in [20, 50, 100]:
    merged_df[f'Avg {window} MSFT'] = merged_df['Close MSFT'].rolling(window).mean()
    merged_df[f'Avg {window} GOOGL'] = merged_df['Close GOOGL'].rolling(window).mean()



#sidebar filters
with st.sidebar:
    st.markdown('***Filter for Time-Series and Volume Comparison***')
    company = st.selectbox("Choose Company", ["Microsoft", "Google", "Both"])
    metric_select = st.multiselect("Metrics", ["Open", "Close", "High", "Low", "Volume"], default=["Close"])
    agg = st.radio("Aggregation", ["Daily", "Monthly", "Yearly"])

#time series chart
st.subheader("📉 Time Series Chart")
if company == "Microsoft":
    fig = px.line(ms_df, x="date", y=[f"{m} MSFT" for m in metric_select] , labels={'date' : 'Date'})
elif company == "Google":
    fig = px.line(g_df, x="date", y=[f"{m} GOOGL" for m in metric_select] , labels={'date' : 'Date'})
else:
    fig = px.line(merged_df, x="date", y=[f"{m} MSFT" for m in metric_select] + [f"{m} GOOGL" for m in metric_select] , labels={'date' : 'Date'})

st.plotly_chart(fig)
st.caption(' ➤ Compares the closing price trends of Microsoft and the Google stock over time.')

# Volume Chart
st.subheader("📊 Volume Comparison")
fig_vol = px.bar(merged_df, x="date", y=["Volume MSFT", "Volume GOOGL"] , labels={'date' : 'Date'})
st.plotly_chart(fig_vol)
st.caption(' ➤ Displays and compares total monthly trading volume for both stocks.')

st.subheader(' ✍️ ***Raw Dataframe Preview***')
st.dataframe(merged_df , hide_index=True , column_config= {'date' : 'Date'})


with col[0]:
    #candelstick chart 
    fig = go.Figure(data=[go.Candlestick(
    x=merged_df['date'],
    open=merged_df['Open MSFT'],
    high=merged_df['High MSFT'],
    low=merged_df['Low MSFT'],
    close=merged_df['Close MSFT']
    )])
    fig.update_layout(title=' 🕯️ Microsoft OHLC Candlestick Chart', xaxis_title='Date', yaxis_title='Price (USD)')
    st.plotly_chart(fig) 
    st.caption(' ➤ Shows detailed daily price movements (open, high, low, close) for Microsoft stock.')
    #line chart
    fig = px.line(merged_df, x='date', y=['Close MSFT', 'Avg 20 MSFT', 'Avg 50 MSFT', 'Avg 100 MSFT'],
              labels={"value": "Price (USD)", "date": "Date", "variable": "Metric"},
              title=" 📈 Microsoft Stock Price with Moving Averages")
    st.plotly_chart(fig)
    st.caption(' ➤ Illustrates Microsoft’s price trend with 20-, 50-, and 100-day moving averages.')

    #histogram
    fig = px.histogram(
    merged_df,
    x="Daily Return MSFT",
    nbins=100,
    title=" 📊 Histogram of Microsoft Daily Returns (%)",
    labels={"Daily Return MSFT": "Daily % Change"}
    )
    st.plotly_chart(fig)
    st.caption(' ➤ Visualizes the distribution of Microsoft’s daily percentage price changes.')

    #box-plot
    box_df = pd.melt(
    merged_df,
    id_vars=["date"],
    value_vars=["Open MSFT", "High MSFT", "Low MSFT", "Close MSFT"],
    var_name="Metric",
    value_name="Price"
    )

    fig = px.box(box_df, x="Metric", y="Price", title=" ⬜ Distribution of Microsoft Stock Prices")
    st.plotly_chart(fig)
    st.caption(' ➤ Highlights the spread, central tendency, and outliers in Microsoft’s daily prices.')


with col[1]:
    #candelstick chart
    fig = go.Figure(data=[go.Candlestick(
    x=merged_df['date'],
    open=merged_df['Open GOOGL'],
    high=merged_df['High GOOGL'],
    low=merged_df['Low GOOGL'],
    close=merged_df['Close GOOGL']
    )])
    fig.update_layout(title=' 🕯️ Google OHLC Candlestick Chart', xaxis_title='Date', yaxis_title='Price (USD)')
    st.plotly_chart(fig)
    st.caption(' ➤ Shows detailed daily price movements (open, high, low, close) for Google stock.')
    
    #line chart
    fig = px.line(merged_df, x='date', y=['Close GOOGL', 'Avg 20 GOOGL', 'Avg 50 GOOGL', 'Avg 100 GOOGL'],
              labels={"value": "Price (USD)", "date": "Date", "variable": "Metric"},
              title=" 📈 Google Stock Price with Moving Averages")
    st.plotly_chart(fig)
    st.caption(' ➤ Illustrates Google’s price trend with 20-, 50-, and 100-day moving averages.')

    #histogram
    fig = px.histogram(
    merged_df,
    x="Daily Return Google",
    nbins=100,
    title=" 📊 Histogram of Google Daily Returns (%)",
    labels={"Daily Return GOOGL": "Daily % Change"}
    )
    st.plotly_chart(fig)
    st.caption(' ➤ Visualizes the distribution of Google’s daily percentage price changes.')

    #box plot 
    box_df = pd.melt(
    merged_df,
    id_vars=["date"],
    value_vars=["Open GOOGL", "High GOOGL", "Low GOOGL", "Close GOOGL"],
    var_name="Metric",
    value_name="Price" 
    )

    fig = px.box(box_df, x="Metric", y="Price", title=" ⬜ Distribution of Google Stock Prices")
    st.plotly_chart(fig)
    st.caption(' ➤ Highlights the spread, central tendency, and outliers in Google’s daily prices.')

