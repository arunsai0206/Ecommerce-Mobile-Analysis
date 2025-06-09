import pandas as pd
import re
import pymysql
#import mysql.connector
#from sqlalchemy import create_engine

# Load scraped CSV file
df = pd.read_csv("data.csv")  # Change filename if needed

# ----- Step 1: Clean Price Columns -----
df['deal_price'] = df['deal_price'].astype(str).str.replace('₹', '').str.replace(',', '').astype(float)
df['org_price'] = df['org_price'].astype(str).str.replace('₹', '').str.replace(',', '').astype(float)

# ----- Step 2: Handle Missing Values -----
df['rating'] = df['rating'].fillna(df['rating'].median())  # Fill missing ratings with median
df['number_of_ratings'] = df['no_of_ratings'].str.extract(r'(\d[\d,]*)').replace(',', '', regex=True).astype(float).fillna(0).astype(int)
df['number_of_reviews'] = df['no_of_ratings'].str.extract(r'&\s*(\d[\d,]*)').replace(',', '', regex=True).astype(float).fillna(0).astype(int)

# You can now drop the original messy column
df.drop(columns=['no_of_ratings'], inplace=True)
#putting brand
df['brand'] = df['title'].str.split().str[0]
df['os_version'] = df['os'].str.extract(r'(\d+)').astype(float)
df['os_version'] = df['os_version'].fillna(df['os_version'].median()).astype(int)
# ----- Step 3: Extract Numeric Features -----
df['battery_capacity'] = df['battery'].str.extract(r'(\d+)').astype(float)  # Extract battery mAh
df['battery_capacity']=df['battery_capacity'].fillna(round(df['battery_capacity'].mean())).astype(int)
df.drop(columns=['battery'],inplace=True)
df['Camera'] = df['camera'].str.extract(r'(\d+)').astype(float)  # Extract MP from camera column
df['Camera'] = df['Camera'].fillna(0).astype(int)
df.drop(columns=['camera'],inplace=True)
df['discount'] = df['discount'].str.extract(r'(\d+)').astype(int)
#extract gb from ram
df['RAM']=df['RAM'].str.extract(r'(\d+)').astype(float)
df["RAM"]=df["RAM"].fillna(round(df["RAM"].mean())).astype(int)
#extract GB from storage
df['storage']=df['storage'].str.extract(r'(\d+)').astype(float)
df["storage"]=df["storage"].fillna(round(df["storage"].mean())).astype(int)
df["operating_system"]=df['os']
df.drop(columns=['os'],inplace=True)
df['waranty']=df['warranty'].fillna("1 Year")
df.drop(columns=['waranty'],inplace=True)
# ----- Step 4: Save Cleaned Data to CSV -----
pd.set_option('display.max_columns', None)
print(df.head())
df.to_csv("flipkart_mobiles_cleaned.csv", index=False)
print("Preprocessing complete! Cleaned data saved as 'flipkart_mobiles_cleaned.csv'")
