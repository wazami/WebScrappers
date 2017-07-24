##This program scraps Dice.com for cybersecurity jobs that they have and stores
#it in a csv file 
import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as soup

def indeed(): 
	driver = webdriver.Chrome("/Users/HNizami/Downloads/chromedriver")
	driver.get("https://www.dice.com/jobs?q=Cybersecurity&l=New+York%2C+NY&searchid=4666161751595&stst=")

	filename = "people_dice.csv"
	f = open(filename,"w") 
	headers = "Job Title, Information, Company, Location\n"
	f.write(headers) 

	page_html = driver.page_source.encode('ascii', 'ignore')
	page_soup = soup(page_html, "html.parser")
	containers = page_soup.findAll("div",{"class":"complete-serp-result-div"})

	for container in containers: 
		title = container.findAll("span", {"itemprop":"title"})
		job_title = title[0].text 

		description = container.findAll("span", {"itemprop":"description"})
		information = description[0].text 

		compname  = container.findAll("span", {"class":"compName"})
		company = compname[0].text 

		jobloc = container.findAll("span", {"class":"jobLoc"})
		location = jobloc[0].text

		f.write(job_title.replace(",", "|") + "," + information.replace(",", "|") + "," + company.replace(",", "|") + "," + location.replace(",", "|") + "\n")

	driver.get("https://www.dice.com/jobs/q-cybersecurity-l-New_York%2C_NY-radius-30-startPage-2-jobs?searchid=8196623467888&stst=") 
	page_html2 = driver.page_source.encode('ascii', 'ignore')
	page_soup2 = soup(page_html2, "html.parser")
	containers = page_soup2.findAll("div",{"class":"complete-serp-result-div"})
	
	for container in containers: 
		title = container.findAll("span", {"itemprop":"title"})
		job_title = title[0].text 

		description = container.findAll("span", {"itemprop":"description"})
		information = description[0].text 

		compname  = container.findAll("span", {"class":"compName"})
		company = compname[0].text 

		jobloc = container.findAll("span", {"class":"jobLoc"})
		location = jobloc[0].text

		f.write(job_title.replace(",", "|") + "," + information.replace(",", "|") + "," + company.replace(",", "|") + "," + location.replace(",", "|") + "\n")
	
indeed()
print("Scraping complete. Check people_dice.csv for results.")