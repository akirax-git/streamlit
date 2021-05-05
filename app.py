### Install YFinance Library and import :
# pip3 install yfinance

### For JupyterLab's diagram drwaing: Ref.https://www.yutaka-note.com/entry/matplotlib_inline
# import matplotlib.pyplot as plt
# %matplotlib inline

### Import Packages
import yfinance as yf
import pandas as pd
import altair as alt
import streamlit as st

### Title
st.title("GAFA 株価可視化ツール")

### Configure Days
st.sidebar.write(
  """
  ## 表示日数を指定
  """
)
days = st.sidebar.slider(
  "days",
  1,
  50,
  20
)
st.write(
  f"""
  ### 過去{days}日間のGAFA株価
  """
)

### Configure Max/Min Price
st.sidebar.write(
  f"""
  ### 株価の表示範囲
  """
)
ymin, ymax = st.sidebar.slider(
  "範囲を指定して下さい",
  0.0,
  3500.0,
  (0.0, 3500.0) # Select the placeholder value (Max/Min can be set)
)

### Set Companies with their tickers
tickers = {
    "apple": "AAPL",
    "facebook": "FB",
    "google": "GOOGL",
    "microsoft": "MSFT",
    "amazon": "AMZN"
}

### Retrieve Data from YFinance package(yf)
# Cache returned value from the function if params are not changed.
# Ref.https://docs.streamlit.io/en/stable/caching.html
@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])     # Retrieve data obj from yf
        hist = tkr.history(period=f"{days}d") # Designate period for retrieved data obj
        hist.reset_index()                    # Normarize Index of data obj
        hist.index.strftime("%d %B %Y")       # Change Index time format
        hist = hist[["Close"]]                # Extract Closed-Price only
        hist.columns =[company]               # Select only company
        hist = hist.T                         # Transpose the data obj
        hist.index.name ="Name"               # Change Index's title of data obj
        df = pd.concat([df, hist])            # Concat data of each data obj
    return df

### Extract data for tickers within days
df = get_data(days, tickers)

try:
### Select companies
  companies = st.multiselect(
    "会社名を選択して下さい",
    list(df.index),                                     # list of company from df
    ["google","amazon","facebook","apple","microsoft"]  # display value for each list
  )

  if not companies:
    st.error("少なくとも一社は選んでください")

### Display the selected companies
  else:
    ### Show the data table of selected companies
    data = df.loc[companies]    # loc: location, select the liseted companies from Index in df
    st.write(
      "株価 (USD)",
      data.sort_index()         # Display data with sorting by alphabetical order
    )

    ### RE-Prepare the data source
    # Transpose and Normilize Index
    data = data.T.reset_index()

    # Pivoting the data structure based on the "Date" Column
    # Rename the column "value"
    data =  pd.melt(
      data, id_vars=["Date"]
      ).rename(
        columns={"value": "Stock Prices(USD)"}
        )

    ### data source to chart
    chart = (
      alt.Chart(data)
        .mark_line(opacity=0.8, clip=True) # Set Overview. clip=true will remote the graph line out of table
        .encode(
          x="Date:T",     # :T is a format
          # alt.Y() is a function of Y axis graph formating.  :Q is a forat of Y axis title
          y=alt.Y("Stock Prices(USD):Q", stack=None,scale=alt.Scale(domain=[ymin, ymax])),
          color="Name:N"  # for Legend
        )
    )
    st.altair_chart(chart, use_container_width=True)

except:
  st.error(
    "Loading Error..."
  )