from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()

driver.get("https://hprera.nic.in/PublicDashboard")

time.sleep(60)

soup = BeautifulSoup(driver.page_source, "html.parser")

projects_section = soup.find_all("div", class_="shadow py-3 px-3 font-sm radius-3 mb-2")
project_links = []

for project in projects_section[:6]:
    link = project.find("a")
    if link:
        project_links.append(link["data-qs"])

for project_data in project_links:
    driver.execute_script(f"tab_project_main_ApplicationPreview($(\"[data-qs='{project_data}']\"))")

    time.sleep(10)

    new_soup = BeautifulSoup(driver.page_source, "html.parser")

    gstin_span = new_soup.find("td", string="GSTIN No.").find_next("span") if new_soup.find("td", string="GSTIN No.") else None          
    pan_span = new_soup.find("td", string="PAN No.").find_next("span") if new_soup.find("td", string="PAN No.") else None
    name_span = new_soup.find("td", string="Name").find_next("td", class_="fw-600") if new_soup.find("td", string="Name") else None
    address_span = new_soup.find("td", string="Permanent Address").find_next("span") if new_soup.find("td", string="Permanent Address") else None

    gstin = gstin_span.get_text(strip=True) if gstin_span else "GSTIN Not Found"
    pan = pan_span.get_text(strip=True) if pan_span else "PAN Not Found"
    name = name_span.get_text(strip=True) if name_span else "Name Not Found"
    address = address_span.get_text(strip=True) if address_span else "Address Not Found"

    print(f"GSTIN No: {gstin}")
    print(f"PAN No: {pan}")
    print(f"Name: {name}")
    print(f"Permanent Address: {address}")
    print("\n")

driver.quit()
