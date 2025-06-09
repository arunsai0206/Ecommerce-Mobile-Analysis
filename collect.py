from bs4 import BeautifulSoup
import os
import pandas as pd
import re
d={'title':[],'RAM':[],'storage':[],'color':[],'model_no':[],'deal_price':[],'org_price':[],'discount':[],'rating':[],'no_of_ratings':[],'battery':[],'processor_brand':[],'os':[],'processor_core':[],'camera':[],'warranty':[]}
for fi in os.listdir("mobiles_html"):
    try:
        with open(f"mobiles_html/{fi}", encoding='utf-8') as f:
            htm= f.read()
        soup=BeautifulSoup(htm,'html.parser')
        ram = storage = color = model_no = battery = Processor_Brand = Processor_Core = Operating_System = "N/A"
        #title
        t=soup.find("h1").text
        #print(t)
        #deal_price
        deal_p=soup.find('div',attrs={'class':"Nx9bqj CxhGGd"}).text
        deal_price = re.sub(r"[^\d]", "", deal_p)
        #print(deal_price)
        #orginal_price
        org_price=soup.find('div',attrs={'class':"yRaY8j A6+E6v"}).text
        orginal_price=re.sub(r"[^\d]","",org_price)
        #print(orginal_price)
        #discount
        discount=soup.find('div',attrs={'class':"UkUFwK WW8yVX"}).text
        #print(discount)
        #rating
        rating=soup.find('div',attrs={'class':"XQDdHH"}).text
        #print(rating)
        #no of ratings and reviews
        no_ratings_reviwes=soup.find('span',attrs={'class':"Wphh3N"}).text
        #print(no_ratings_reviwes)
        # ram
        rows=soup.find_all('tr',attrs={'class':"WJdYP6 row"})

        if not rows:
            print("No rows found!")

        # Loop through each row to find the one containing "RAM"
        for row in rows:
            columns = row.find_all("td")
            if columns and "RAM" in columns[0].text.strip():
                ram = columns[1].find("li").text.strip()
                #print(ram)
        #storage
        for row in rows:
            columns = row.find_all("td") 
            if columns and "Internal Storage" in columns[0].text.strip():
                storage = columns[1].find("li").text.strip()
                #print(storage)
        #color
        for row in rows:
            columns = row.find_all("td")
            if columns and "Color" in columns[0].text.strip():
                color_list = columns[1].find_all("li")
                if color_list:
                    color = color_list[0].text.strip()  # Take only the first color (actual product color)
                break  
                #print(color)
        #model number
        for row in rows:
            columns = row.find_all("td")
            if columns and "Model Number" in columns[0].text.strip():
                model_no = columns[1].find("li").text.strip()
                #print("model_no:",model_no)
        #battery
        for row in rows:
            columns = row.find_all("td")
            if columns and "Battery Capacity" in columns[0].text.strip():
                battery = columns[1].find("li").text.strip()
                #print("battery:",battery)

        #processor brand
        for row in rows:
            columns = row.find_all("td")
            if columns and "Processor Brand" in columns[0].text.strip():
                Processor_Brand = columns[1].find("li").text.strip()
                #print("Processor Brand:",Processor_Brand)
        #processor core
        for row in rows:
            columns = row.find_all("td")
            if columns and "Processor Core" in columns[0].text.strip():
                Processor_Core = columns[1].find("li").text.strip()
                #print("Processor Core:",Processor_Core)
        #os
        for row in rows:
            columns = row.find_all("td")
            if columns and "Operating System" in columns[0].text.strip():
                os_list = columns[1].find_all("li")  # Get all <li> elements under "Operating System"
                if os_list:
                    Operating_System = os_list[0].text.strip()  # Take only the first OS name
                break 
        #camara
        Primary_Camera = None

        for row in rows:
            columns = row.find_all("td")
            if columns and "Primary Camera" in columns[0].text.strip():
                li_tags = columns[1].find_all("li")
                for li in li_tags:
                    text = li.text.strip()
                    if "MP" in text:
                        Primary_Camera = text
                        break  # stop at the first proper camera info
                if Primary_Camera:  # if already found, exit outer loop
                    break
        #warrenty
        for row in rows:
            columns = row.find_all("td")
            if columns and "Domestic Warranty" in columns[0].text.strip():
                Warranty = columns[1].find("li").text.strip()
        d['title'].append(t)
        d['RAM'].append(ram)
        d["battery"].append(battery)
        d["color"].append(color)
        d["deal_price"].append(deal_price)
        d["discount"].append(discount)
        d["model_no"].append(model_no)
        d["no_of_ratings"].append(no_ratings_reviwes)
        d["org_price"].append(orginal_price)
        d["os"].append(Operating_System)
        d["processor_brand"].append(Processor_Brand)
        d["processor_core"].append(Processor_Core)
        d["rating"].append(rating)
        d["storage"].append(storage)
        d['camera'].append(Primary_Camera)
        d['warranty'].append(Warranty)

    except Exception as e:
        print(e)
max_length = max(len(lst) for lst in d.values())
for key in d.keys():
    while len(d[key]) < max_length:
        d[key].append("N/A")
pd.set_option('display.max_columns', None)
df=pd.DataFrame(data=d)
print(df.head())
df.to_csv("data.csv",index=False)   