### Exec Streamlit
# cd path/to/dir
# streamlit run app.py

### Install Library for WebScraping and Import
# !pip3 install beautifulsoup4
# "requests" is to retrieve HTML data
import requests
# "BeautifulSoup" is to arrange the retrieved HTML data
from bs4 import BeautifulSoup
import pandas as pd

### Get web data 1
def get_data_udemy():
    # html resource by using reques.get()
    url = "https://scraping-for-beginner.herokuapp.com/udemy"
    res=requests.get(url)
    html_raw=res.text

    # Arrange the html following the defined rule: html.parser
    soup = BeautifulSoup(html_raw, "html.parser")

    # Check the count of class: subscribers
    test = len(soup.find_all("p", {"class": "subscribers"}))
    if test==1:
        # Retrieve the necessary html text
        n_subscriber = soup.find("p", {"class": "subscribers"}).text
        n_review = soup.find("p", {"class": "reviews"}).text

        # Retrieve subscribers/reviewers data only
        n_subscriber = int(n_subscriber.split("：")[1])
        n_review = int(n_review.split("：")[1])

        result = {
            "n_subscriber":n_subscriber,
            "n_review":n_review
        }
        return result   # {'n_subscriber': 11639, 'n_review': 2026}

    else:
        err = "Multiple html class: subscribers are detected"
        print(err)


### Get web data 2
def get_data_ec():
    # html resource by using reques.get()
    url = "https://scraping.official.ec/"
    res=requests.get(url)
    html_raw=res.text

    # Arrange the html following the defined rule: html.parser
    soup = BeautifulSoup(html_raw, "html.parser")

    # Retrieve the contents in the ul tag with the id: itemlist
    item_list=soup.find("ul", {"id": "itemList"})

    # Retrieve the contents in all the li tag within above
    items = item_list.find_all("li")

    # Filter the necessary data in each li tag and Store them
    data_ec = []
    for item in items:
        # Prepare {} to store necessary data in each list tag
        datum_ec ={}

        # Retrieve the necessary html text, convert it and store
        datum_ec["title"]=item.find("p",{"class":"items-grid_itemTitleText_b58666da"}).text

        datum_ec["link"] = item.find("a")["href"]

        price = item.find("p",{"class":"items-grid_price_b58666da"}).text
        datum_ec["price"] = price.replace("¥ ", "").replace(",","")

        is_stock = item.find("p",{"class":"items-grid_soldOut_b58666da"}) == None
        datum_ec["is_stock"] = "在庫在り" if is_stock == True else "在庫なし"

        # Necessary data in each li tag are stored
        data_ec.append(datum_ec)
        # [{'title': 'YouTubeコンサルティング',
        #   'link': 'https://scraping.official.ec/items/40792454',
        #   'price': '15000',
        #   'is_stock': '在庫なし'}...]

    # Form into table
    df_ec = pd.DataFrame(data_ec)
    return df_ec


### Install Library for Google Drive & SpreadSheet
# Library for Google Drive and Sheets API
# !pip3 install gspread
# !pip3 install google


### Authenticate & Instantiate & Get Worksheet - "db"
def get_worksheet():
    ### Authenticate & Instantiate the client (old method)
    # Note: To follow the latest auth method, need to set the credential as designated way
    # Ref. https://docs.gspread.org/en/latest/oauth2.html
    from google.oauth2.service_account import Credentials
    import gspread
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = Credentials.from_service_account_file(
        'secret-gcp-srv-gss.json',
        scopes=scopes
    )
    gc = gspread.authorize(credentials)
    # <gspread.client.Client at 0x7f0f7956ae50>

    ### Opens a spreadsheet specified by key
    # Note1: Configure to share it with a client_email issued from GCP client
    # Npte2: Key is in spreadsheet url:         ↓here↓
    # https://docs.google.com/spreadsheets/d/1933N62keeW9XUMsV7TkAXL0BLSTEsEB-9CYRDCSyjKA/edit#gid=0
    SP_SHEET_KEY ="1933N62keeW9XUMsV7TkAXL0BLSTEsEB-9CYRDCSyjKA"
    sh = gc.open_by_key(SP_SHEET_KEY) # <Spreadsheet 'スクレ―ピング用DB' id:1933N62keeW9XUMsV7TkAXL0BLSTEsEB-9CYRDCSyjKA>

    # Get worksheet "db"
    SP_SHEET = "db"
    worksheet = sh.worksheet(SP_SHEET)
    return worksheet


### Build graph for df_udemy with two axis
def get_chart():
    # Import Altair
    import altair as alt

    # Get the latest data in the spreadsheet
    worksheet = get_worksheet()
    data = worksheet.get_all_values()   # [['date', 'n_subscriber', 'n_review'],['2021/03/09', '11032', '1882'], ...
    df_udemy = pd.DataFrame(data[1:], columns=data[0])

    # Check & Custom data type in each column
    # df_udemy.dtypes
    df_udemy = df_udemy.astype({
        "n_subscriber": int,
        "n_review": int
    })

    # Pick max | min for each column (to scale the axis range)
    ymin1=df_udemy["n_subscriber"].min() - 10
    ymax1=df_udemy["n_subscriber"].max() + 10
    ymin2=df_udemy["n_review"].min() - 10
    ymax2=df_udemy["n_review"].max() + 10

    # Baseform with x axis detail
    base = alt.Chart(df_udemy).encode(
        alt.X('date:T',
            axis=alt.Axis(title=None)
        )
    )

    # Add Y-axis 1 with detail on the baseform
    line1 = base.mark_line(opacity=0.3, color='#57A44C').encode(
        alt.Y('n_subscriber',
            axis=alt.Axis(title='Subscribers', titleColor='#57A44C'),
            scale=alt.Scale(domain=[ymin1,ymax1])
        )
    )

    # Add Y-axis 2 with detail on the baseform
    line2 = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(
        alt.Y('n_review',
            axis=alt.Axis(title='Reviewers', titleColor='#5276A7'),
            scale=alt.Scale(domain=[ymin2,ymax2])
        )
    )

    # Overwrite (Resolve) layers
    chart = alt.layer(line1, line2).resolve_scale(
        y = 'independent'
    )
    return chart

### Build app with Steramlit
import streamlit as st
st.title("WebScraping")

st.write("## Web Scraping 活用アプリ")
chart = get_chart()
st.altair_chart(chart, use_container_width=True)

ec = get_data_ec()
st.write("## EC在庫情報", ec)
