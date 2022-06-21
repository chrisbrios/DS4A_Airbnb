#%%
from click import open_file
import pandas as pd
import requests
import json
import time

pd.set_option('display.max_columns', None)

city = 'dallas'
state = 'tx'
search_str = city + ', ' + state
print('Search string:', search_str)

#%%
rapid_api_key = 'ed27ca8449msh0a3a4bd8378e03ap1c6f9ajsn0f61bb3f747a'

# %%
# get data
url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"

querystring = {"location":search_str,
               "home_type":"Houses"}

headers = {
    'x-rapidapi-host': "zillow-com1.p.rapidapi.com",
    'x-rapidapi-key': rapid_api_key
    }

z_for_sale_resp = requests.request("GET", url, headers=headers, params=querystring)

# transform to json
z_for_sale_resp_json = z_for_sale_resp.json()
z_for_sale_resp_json

# %%
# view data
df_z_for_sale = pd.json_normalize(data=z_for_sale_resp_json['props'])
print('Num of rows:', len(df_z_for_sale))
print('Num of cols:', len(df_z_for_sale.columns))
df_z_for_sale.head()

# %%
# get zpids to a list
zpid_list = df_z_for_sale['zpid'].tolist()
zpid_list

# %%
# get property detail

# create empty list
prop_detail_list = []

# iterate through list of properties
for zpid in zpid_list:

  # end point
  url = "https://zillow-com1.p.rapidapi.com/property"

  querystring = {"zpid":zpid}

  # header
  headers = {
      'x-rapidapi-host': "zillow-com1.p.rapidapi.com",
      'x-rapidapi-key': rapid_api_key
      }

  # get property detail
  z_prop_detail_resp = requests.request("GET", url, headers=headers, params=querystring)
  z_prop_detail_resp_json = z_prop_detail_resp.json()

  # wait 15 sec based on limit
  time.sleep(15)

  prop_detail_list.append(z_prop_detail_resp_json)

# %%
df_z_prop_detail = pd.json_normalize(prop_detail_list)
print('Num of rows:', len(df_z_prop_detail))
print('Num of cols:', len(df_z_prop_detail.columns))
df_z_prop_detail.head(2)

# %%
# columns of interest
detail_cols = ['streetAddress', 
 'city',
 'county',
 'zipcode',
 'state',
 'price',
 'homeType',
 'timeOnZillow', 
 'zestimate',
 'rentZestimate',
 'livingArea',
 'bedrooms',
 'bathrooms',
 'yearBuilt',
 'description',
 'priceHistory',
 'taxHistory',
 'zpid'
 ]

# retain limited columns for output
df_z_prop_detail_output = df_z_prop_detail[detail_cols]
df_z_prop_detail_output.head()

# %%
# download file
df_z_prop_detail_output.to_csv('df_z_prop_detail_output.csv')
#files.download('df_z_prop_detail_output.csv')

# %%
open('df_z_prop_detail_output.csv')
# %%
