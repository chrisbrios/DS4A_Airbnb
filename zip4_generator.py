from grabZip4_function import grabAndMergeZip4

#Original file 
clean_airbnb = '/Users/chrisrios/Desktop/Data_science/Airbnb_Project/airbnb_data/cleanedlistings.csv'
clean_zillow_sales = '/Users/chrisrios/Desktop/Data_science/Airbnb_Project/zillow_data/cleaned_zillow_sales.csv'
clean_zillow_rental = '/Users/chrisrios/Desktop/Data_science/Airbnb_Project/zillow_data/cleaned_zillow_sales.csv'



if __name__ == '__main__':
    if 'zip4' not in clean_zillow_sales:
        grabAndMergeZip4(clean_zillow_sales)
    
    if 'zip4' not in clean_zillow_rental:
        grabAndMergeZip4(clean_zillow_rental)
    
    if 'zip4' not in clean_airbnb:
        grabAndMergeZip4(clean_airbnb)