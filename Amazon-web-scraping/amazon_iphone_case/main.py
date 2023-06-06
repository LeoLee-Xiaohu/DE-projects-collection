from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time 


# Function to extract Product Title
def get_title(soup):

    try:

        title = soup.find("span", attrs={"id":'productTitle'})
        

        title_value = title.text


        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Price
def get_price(soup):

    try:
        price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()

    except AttributeError:

        try:

            price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

        except:
            price = ""

    return price

# Function to extract Product Rating
def get_rating(soup):

    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	

    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""	

    return review_count

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"	

    return available

def scraping(URL, HEADERS):

    webpage = requests.get(URL, headers = HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    s = soup.find_all("a", attrs={'class':"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal" })

    n = 1
    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}

    for i in s:

        link_n = "https://www.amazon.com.au" + i.get('href')
        new_webpage = requests.get(link_n, headers = HEADERS )
        print(n," -> ", new_webpage)
        n += 1
        new_soup = BeautifulSoup(new_webpage.content,"html.parser")
        



        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))
        d['availability'].append(get_availability(new_soup))
        time.sleep(0.35)
        

    
    return d

def transform(diction):
    dataframe = pd.DataFrame.from_dict(diction)
    dataframe['title'].replace("",np.nan, inplace= True)
    dataframe = dataframe.dropna(subset='title')
    dataframe.to_csv('iphone14_pro_cases3.csv', header= True, index= False)


if __name__ == "__main__":
    URL = "https://www.amazon.com.au/s?k=iphone+14+pro+case&crid=393IQZJ88FNQS&sprefix=%2Caps%2C238&ref=nb_sb_ss_recent_1_0_recent"
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36', 'Accept-Language':'en-US, en;q=0.5'})

    data = scraping(URL, HEADERS)
    transform(data)
