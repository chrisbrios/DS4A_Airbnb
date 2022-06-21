


def grabCoordinates(df):
    from geopy.geocoders import Nominatim
    import re

    df['street_address'] = df['street_address'].str.replace("Holw","Hollow")
    df['street_address'] = df['street_address'].str.replace("Roadg","Road")
    df['street_address'] = df['street_address'].str.replace("Bnd","Bend")

    df['street_address'] = df['street_address'].str.replace("Hwy","Highway")
    df['street_address'] = df['street_address'].str.replace("Crk","Creek")
    df['street_address'] = df['street_address'].str.replace("Xing","Crossing")

    geolocator = Nominatim(user_agent="DS4a Group-1 Property Coordinates")

#Iterate through the properties and strip apartments
    for index,row in df.iterrows():
        # Grabbing the address         
        street_address = str(df.loc[index , 'street_address'])
        
        #Strip off apartment numbers for ingestions
        refined_street_address = re.search(r"(.*(?:ST|St|st|Street|Bend|bend|Dr|Ave|Avenue|Jacksdaw|Trl|Trail|Run|run|Sier|Sq|Road|Glade|Glen|Creek|Blvd|blvd|Hl|Hollow|hollow|Lane|Ln|Court|Ct|Cv|Crv|Ter|ter|Way|way|Mdws|Pl|Place|Plz|Pass|Path|Loop|Cir|Circle|Aly|Pkwy|Range|Embassy|Point|pnt|Gln|Oaks|Road|Rd|Drive|Overlook|Ledge|Flds|Row|Creek|Highway|Expy|Crossing|Spg|Hl|Walk|Trce|Tail|Cors)\b)", street_address)
        zipcode = str(df.loc[index , 'zipcode'])
        
        #Try and create an elongated string of jus tthe street address, and if the refined address is not in the regex will be ignored
        try:         
            single_line_address = str(refined_street_address.group()) + ", Austin, TX " + zipcode
        except:
                print("Check suffix of " + street_address)
                #Use geopy to grab full location via address
        else:
                location = geolocator.geocode(single_line_address,timeout=None)

        #Assign the longitude and latitude values and assign to columns
        try:
                latitude = location.latitude
                longitude = location.longitude
        except:
                print("No coordinates found for " + single_line_address)
        else:
                df.loc[index,'latitude'] = latitude
                df.loc[index,'longitude'] = longitude
    return df