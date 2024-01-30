from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

def get_title(soup):
  try:
    title = soup.find("span", attrs={"id":'productTitle'})

    title_value = title.text

    title_string = title_value.strip()
  
  except AttributeError:
    title_string = ""

  return title_string

def get_price(soup):
  try:
    price = soup.find("span", attrs={"class":'a-offscreen'}).string.strip()

  except AttributeError:
    try:
      price = soup.find("span", attrs={"class":'a-price-whole'}).string.strip()
    
    except:
      price = ""

  return price

def get_rating(soup):
  try:
    rating = soup.find("i", attrs={"class":'a-icon a-icon-star-medium a-star-medium-4-5'}).string.strip()
    
  except AttributeError:
    try:
      rating = soup.find("span", attrs={"class":'a-icon-alt'}).string.strip()

    except:
      rating = ""	

    return rating

def get_review_count(soup):
  try:
    review_count = soup.find("span", attrs={"id":'acrCustomerReviewText'}).string.strip()
  
  except AttributeError:
    review_count = ""

  return review_count

if __name__ == '__main__':

  #Adding user agent 
  HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

  #URL
  url = "https://www.amazon.com/s?k=laptop&crid=2YET9S5DFS70M&sprefix=laptop%2Caps%2C408&ref=nb_sb_noss_1"

  #HTTP Request
  webpage = requests.get(url, headers=HEADERS)

  #Soup Object containing all the data
  soup = BeautifulSoup(webpage.content, "html.parser")

  Links = soup.find_all("a", attrs={'class': "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})

  # Store the links
  Links_list = []

  for link in Links:
    Links_list.append(link.get('href'))

  d = {"title":[], "price":[], "rating":[], "reviews":[]}
    
  for link in Links_list:
    new_webpage = requests.get("https://www.amazon.com/" + link, headers=HEADERS)

    new_soup = BeautifulSoup(new_webpage.content, "html.parser")

    # Function calls
    d['title'].append(get_title(new_soup))
    d['price'].append(get_price(new_soup))
    d['rating'].append(get_rating(new_soup))
    d['reviews'].append(get_review_count(new_soup))
    
  amazon_data = pd.DataFrame.from_dict(d)
  amazon_data['title'].replace('', np.nan, inplace=True)
  amazon_data = amazon_data.dropna(subset=['title'])
  amazon_data.to_csv("amazon_data.csv", header=True, index=False)
  
  print(amazon_data)