from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as soup


def linkedin(title,maxPages):  


    #if auto login doesn't work, manual login with this code
    """driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/")
    time.sleep(20)"""

    #auto login
    driver = webdriver.Chrome("/Users/HNizami/Downloads/chromedriver")
    driver.get("https://www.linkedin.com/")
    username = driver.find_element_by_id("login-email")
    password = driver.find_element_by_id("login-password")
    username.send_keys("hamzahanizami@gmail.com")
    password.send_keys("Dr5g0nxHndd")
    login_attempt = driver.find_element_by_xpath("//*[@type='submit']")
    login_attempt.submit()

    filename = "people.csv" 
    f = open(filename,"w")
    headers = "Name, Location, Position, Company\n"
    f.write(headers)

    numberVisited = 0
    
    while numberVisited < maxPages:
        numberVisited = numberVisited +1
        url = "https://www.linkedin.com/search/results/people/?origin=FACETED_SEARCH&page="+str(numberVisited)+"&title="+title
        driver.get(url)
        
        #selenium has to scroll down and wait in order all entires to appear
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)

        names = driver.find_elements_by_class_name("actor-name")
        locations = driver.find_elements_by_class_name("subline-level-2")
        page_html = driver.page_source.encode('ascii', 'ignore')
        html = soup(page_html, "html.parser")
        containers = html.findAll("div",{"class":"search-result__info"})

        positions = []
        companies = []


        #can't use find_elements_by_class_name because not all entries list position and company
        for container in containers:
            step1 = container.findAll("p",{"class":"search-result__snippets"})

            if step1 and "Current:" in step1[0].text and "at" in step1[0].text:
                step2 = step1[0].text 
                step3 = step2[step2.find(":")+1: ] 
                step4 = step3.split(" at ")
                position = step4[0].strip()
                company = step4[1].strip()
                positions.append(position)
                companies.append(company)

            else:
                positions.append("Position Not Found")
                companies.append("Company Not Found") 


        
        
        for i in range(0,len(names)):
            try: 
                f.write(names[i].text.replace(",","|")  + "," + locations[i].text.replace(",","|") + "," + positions[i].replace(",","|") + "," + companies[i].replace(",","|") + "\n")
            except UnicodeEncodeError:
                pass
                      

    f.close()
    driver.quit()


title = input("Enter the title to search for: ")
maxPages = int(input("Enter the maximum number of pages to be scraped (1 page = 10 entries): "))
print("Scraping linkedIn...")
linkedin(title,maxPages)
print("Information scraped to file labeled \"people.csv\"")
