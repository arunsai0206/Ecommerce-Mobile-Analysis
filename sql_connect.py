from sqlalchemy import create_engine
import pandas as pd

# Load updated CSV
df = pd.read_csv("flipkart_mobiles_cleaned.csv")

# Connect to MySQL
engine = create_engine("mysql+pymysql://root:@localhost/ecom")

# Replace the table with the new schema (including your new column)
df.to_sql("flipkart_mobiles_cleaned", con=engine, if_exists="replace", index=False)

print("✅ Table updated with new column.")