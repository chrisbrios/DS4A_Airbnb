from bs4 import BeautifulSoup
import requests
import re
import csv
#url = "https://www.trulia.com/TX/Dallas/"#'https://www.redfin.com/city/30794/TX/Dallas'
#page = requests.get(url)
#print(page)

#soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify)
#tag = soup.url
#print(tag)
#lists = soup.find_all('div', id:"main-content")
#items = soup.select('div[data-testid$="property-address"]')
#items=soup.find_all("div", {"id": "main-content"})
#print(items)

# Parse the MANUALLY downloaded html files
with open('/Users/bhava/Desktop/DS4A/Trulia.csv', 'w') as csv_file:
    fieldnames = ['ID', 'Address', 'SFT', 'Beds', 'Baths', 'Price']
    
    # Create fields
    csv_writer = csv.writer(csv_file, delimiter =',')
    csv_writer.writerow(fieldnames)
    
    line_count=0
   
    x=16;
    while x != 0 :        
        with open('/Users/bhava/downloads/pag'+str(x)+'.html', 'r') as f:        
            
            # Read the contents
            contents = f.read()

            soup = BeautifulSoup(contents, 'lxml')
            
            pdetails = soup.find_all('ul', attrs={ 'data-testid' : 'search-result-list-container'}) 
            # print(pdetails)
            
            hc="srp-home-card"
            i=0;
            row=[]
            while i<40 :
                li = soup.find('li', attrs={ 'data-testid' : hc+'-'+str(i)})
                address = li.find('div', attrs={ 'data-testid' : 'property-address'})
                # print(address)
                price = li.find('div', attrs={ 'data-testid' : 'property-price'})
                beds = li.find('div', attrs={ 'data-testid' : 'property-beds'})
                baths = li.find('div', attrs={ 'data-testid' : 'property-baths'})
                sft = li.find('div', attrs={'data-testid' : 'property-floorSpace'})
                row = [str(i), address.get('title'), sft.get('title') if sft is not None else "NA", beds.text if beds is not None else "NA", baths.text if baths is not None else "NA", price.get('title')]
                #print(row)
                
                csv_writer.writerow(row)
                    
                i=i+1    
        x=x-1

        
