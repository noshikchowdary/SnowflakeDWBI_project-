#import python libraries 
import pandas as pd
import random
import csv
from faker import Faker


#Initialize 

fake= Faker()

#input the number of rows that the csv file should have 

num_rows = int(input( " Enter the number of rows that you want to generate in the csv file : "))


#input the name of the csv file (e.g data.csv)

csv_file = input ( " Enter the name of the csv file : ")

# details of the excel file that has the lookup data , File Path and Name , Sheet Name and column names where the data is present 

excel_file_path_name = "C:/Users/anshu/Desktop/Personal/End to End Project/Lookup Data/LookupFile.xlsx"
excel_sheet_name = "Store Name Data"
adjective_column_name  = "Adjectives"
noun_column_name = "Nouns"


#fetch this sheet data in a dataframe 

df = pd.read_excel(excel_file_path_name,sheet_name=excel_sheet_name)



#open the csv file 

with open(csv_file,mode='w',newline='') as file:
    writer=csv.writer(file)


#create the header 
    header=['StoreName','StoreType','StoreOpeningDate','Address','City','State','Country','Region','Manager Name']


#write the header to the csv file 
    writer.writerow(header)


#loop and generate multiple rows 
    for _ in range(num_rows):

#Select a random Adjective and Noun and we are going to concatenate it with the word "The" and finally use that as our store name 
        random_adjective=df[adjective_column_name].sample(n=1).values[0]
        random_noun=df[noun_column_name].sample(n=1).values[0]
        store_name= f"The {random_adjective} {random_noun}"
        

#Generate a Single row 
        row = [
        store_name,
        random.choice(['Exclusive','MBO','SMB','Outlet Stores']),
        fake.date(),
        fake.address().replace("\n"," ").replace(","," "),
        fake.city(),
        fake.state(),
        fake.country(),
        random.choice(['North','South','East','West']),
        fake.first_name()
        ]


# write the row to the csv file 

        writer.writerow(row)


#print success statement 

print(" the process completed Successfully")
