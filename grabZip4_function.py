from unicodedata import name
import urllib 
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET 
import pandas as pd
import time


#Original file 

def grabAndMergeZip4(csv_path: str):
    """
    Input: CSV file path 
    Requirements: contains address + zipcode column 
    Takes in a file that contains [street address] 
    column and [zipcode] and appends the Zip9 value to the sheet
    """
    #Making the Dataframe
    re_dataframe = pd.read_csv(csv_path)

    for index,row in re_dataframe.iterrows():
        address = row['street_address']
        print(address)
        zip5 = row['zipcode']
    
        requestXML = f"""
        <ZipCodeLookupRequest USERID="612CARDO0017">
        <Address ID="1">
            <Address1></Address1>
            <Address2>{address}</Address2>
            <City>Austin</City>
            <State>TX</State>
            <Zip5>{zip5}</Zip5>
            <Zip4></Zip4>
            </Address>
        </ZipCodeLookupRequest>
        """
        #prepare xml string doc for query string
        docString = requestXML
        docString = docString.replace('\n', '').replace('\t', '')
        docString = urllib.parse.quote_plus(docString)
    
        url = 'https://secure.shippingapis.com/ShippingAPI.dll?API=ZipCodeLookup&XML=' + docString
        print(url + "\n\n")
        response = urllib.request.urlopen(url)

        #Check for errors
        if response.getcode() != 200:
            print('Error making HTTP call: ')
            print(response.infp())
            exit()

        contents = response.read()
        print(contents)
        root = ET.fromstring(contents)
    
        #print("this is the root")
        #print(root.findall('Address').find("Address")    )

        #Get the Zip 4 and append it to the dataframe
        for address in root.findall('Address'):
            try:
                print()
                print(address)
                print("Zip5: " + address.find("Zip5").text)

                print("Zip4: " + address.find("Zip4").text)
                zip4 = address.find("Zip4").text
            except: 
                print("index" + str(index) + "did not complete successfully")
            else: 
                re_dataframe.loc[index, 'zip4'] = zip4
                print("column added")
                print("Working on row: " + str(index))

    target_df = pd.merge(
        left= pd.read_csv(csv_path), 
        right=re_dataframe,
        how="left",
        on='street_address')
    
    #zillow_df['zip4'] = zillow_df['zip4'].astype('int64')
    target_df.dropna(subset='zip4',inplace=True)
    
    #Drop Invalid Zip4s    
    target_df = target_df.drop(target_df.index[target_df['zip4'] < 1000])

    #Convert Zip4 into a int type after changing empty to NaN
    target_df['zip4'] = target_df['zip4'].astype('int64')
   
    target_df.to_csv(csv_path)




















    



   
