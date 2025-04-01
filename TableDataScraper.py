from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
from io import StringIO






options = webdriver.ChromeOptions()
options.add_argument("--headless")  
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


url = "url" #url of the project. (it keeps changing)
driver.get(url)


time.sleep(6)


html = driver.page_source
driver.quit()

glolist=[]


soup = BeautifulSoup(html, "html.parser")

building_details_section = soup.find("h2", string="Building Details")

if building_details_section:
   
    outer_table = building_details_section.find_next("table")

    if outer_table:
       
        nested_tables = outer_table.find_all("table", recursive=True)

        print(f"Total nested tables found: {len(nested_tables)}\n")

       
        for table in nested_tables:
            
            rows = table.find_all("tr")
            
            
            headers_row = table.find("tr") 
            headers=[]
            for th in headers_row.find_all("th"):
                headers.append(th.text.strip())
            

            for row in rows:
                cols = row.find_all("td")
                rowdata={}
               
                for col, header in zip(cols, headers):
                    if header == "Floor ID" or header == "Apartment Type" or header == "Saleable Area (in Sqmts)" or header == "Number of Apartment":
                        # print(header,":", col.text.strip())
                        rowdata[header]=col.text.strip()

                if(rowdata):
                    glolist.append(rowdata)
                 
                

               

    else:
        print("no outer tables")

else:
    print("no data.")

# print(glolist)

data={}

for row in glolist:
    key=(row["Saleable Area (in Sqmts)"],row["Apartment Type"].lower())
    if row["Apartment Type"]=="AMENITIES":
        continue

    if key in data:
        data[key]+=int(row["Number of Apartment"])
    else:
        data[key]=int(row["Number of Apartment"])
    
print("\n")
print("asdsdasdsd","\n",data)


#boilerplate code to print a dictionary in csv format


# Create a StringIO buffer to store CSV
with open('output.csv', 'w', newline='') as file:  # 'newline=""' avoids extra blank lines
    writer = csv.writer(file)
    writer.writerow(['Area', 'Type', 'Count'])  # Header
    for (area, type_), count in data.items():
        writer.writerow([area, type_, count])  # Rows

print("CSV file saved as 'output.csv'")
