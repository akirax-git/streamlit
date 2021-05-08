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


### Install Library for Google Drive & SpreadSheet
# Library for Google Drive and Sheets API
# !pip3 install gspread
# !pip3 install google


### Update Google Spreadsheet
def main():
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


  ### Prepare data
  # Set Sheet name
  SP_SHEET = "db"
  worksheet = sh.worksheet(SP_SHEET)

  # Get data in sheet
  data = worksheet.get_all_values()   # [['date', 'n_subscriber', 'n_review'],['2021/03/09', '11032', '1882'], ...

  # Form the list data into table
  df = pd.DataFrame(data[1:], columns=data[0])        # df[:5]

  # Make the latesst data
  import datetime
  today = datetime.date.today().strftime("%Y/%m/%d")  # '2021/05/08'
  data_udemy = get_data_udemy() # {'n_subscriber': 11637, 'n_review': 2020}
  data_udemy["date"]=today      # {'n_subscriber': 11637, 'n_review': 2020, 'date': '2021/05/08'}

  # Add data in the bottom of df
  # Note: pandas can recognize columns from the dict type
  df=df.append(data_udemy, ignore_index=True)
  df.tail()


  ### Transfer the prepared data in python to spreadsheet
  # Install library to transfer data
  # !pip3 install gspread-dataframe
  from gspread_dataframe import set_with_dataframe

  # Load data into spreadsheet to update
  set_with_dataframe(worksheet, df, row=1, col=1)


### When this module is called, execute main()
if __name__ == "__main__":
  main()