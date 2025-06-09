from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
import time
import os
#import shutil
'''
folder_path = "mobiles_html"  # or whatever your folder is called

# Delete the folder if it exists
if os.path.exists(folder_path):
    shutil.rmtree(folder_path)
'''
driver=webdriver.Chrome()

#base_url = "https://www.amazon.in/s?k=xiaomi+mobiles&crid=20JASM64IW1JH&sprefix=%2Caps%2C317&ref=nb_sb_ss_recent_1_0_recent"
output_folder = "mobiles_html"
os.makedirs(output_folder, exist_ok=True)  # Create folder if not exists

mobile_count =697

for page in range(28,201):  # Loop from page 1 to 20
    print(f"Scraping page {page}...")
    driver.get(f"https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&as-pos=1&as-type=HISTORY&page={page}")
    time.sleep(3)  # Wait for page to load
    
    # Get all product links
    product_links = driver.find_elements(By.CLASS_NAME, "CGtC98")
    links = [link.get_attribute("href") for link in product_links if link.get_attribute("href")]
    
    if not links:
        print("No more pages to scrape.")
        break
    
    for link in links:
        driver.get(link)
        time.sleep(2)  # Wait for product page to load
        
        # Extract outerHTML of a specific div (modify as per requirement)
        try:
            product_div = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]')  # Modify the ID/class as needed
            outer_html = product_div.get_attribute("outerHTML")
            
            # Save each mobile's outerHTML in a separate file
            file_path = os.path.join(output_folder, f"mobile_{mobile_count}.html")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"<!-- {link} -->\n" + outer_html + "\n")
            
            print(f"Saved: {file_path}")
            mobile_count += 1
        except Exception as e:
            print(f"Error extracting data from {link}: {e}")

print("Scraping complete. Data saved in individual files.")
driver.quit()
#//*[@id="container"]/div/div[3]/div[1]/div[2]