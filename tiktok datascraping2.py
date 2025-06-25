
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

data = []

service = Service(r"C:\Users\dsvan\Downloads\edgedriver_win64\msedgedriver.exe")
driver = webdriver.Edge(service=service)
driver.get("https://www.tiktok.com")
time.sleep(5)
gotofy = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div/div[3]/div[1]/div[1]/a/button/div/div[2]')
gotofy.click()
time.sleep(5)
x = 2
def processvideo():
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_DOWN)
    global x
    time.sleep(1)
    print(f"Processing video {x}")
    time.sleep(1)
    try:
        descriptionfind = driver.find_element(By.XPATH, f'//*[@id="one-column-item-{x-1}"]/div/div[1]/div[1]/span/picture/img')
        caption_element = descriptionfind.get_attribute("alt")
        print(caption_element)
    except NoSuchElementException:
        print("nothing")
        x += 1
        return
    try:
        likecount = driver.find_element(By.XPATH, f'//*[@id="column-list-container"]/article[{x}]/div/section[2]/button[1]/strong')
        likeelement = likecount.text
        print(likeelement)
    except NoSuchElementException:
        likeelement = "n/a"
        print("no like")
        x += 1
        return
    try:
        savecount = driver.find_element(By.XPATH, f'//*[@id="column-list-container"]/article[{x}]/div/section[2]/div[2]/button/strong')
        saveelement = savecount.text
        print(saveelement)
    except NoSuchElementException:
        saveelement = "n/a"
        print("no save")
        x += 1
        return
    try:
        commentcount = driver.find_element(By.XPATH, f'//*[@id="column-list-container"]/article[{x}]/div/section[2]/button[2]/strong')
        commentelement = commentcount.text
        print(commentelement)
    except NoSuchElementException:
        commentelement = "n/a"
        print("no comment")
        x += 1
        return
    data.append({
        "Description": caption_element,
        "Comments": commentelement,
        "Likes": likeelement,
        "Saves": saveelement

    })

    x += 1
counter = 0
while counter<1000:
    processvideo()
    time.sleep(1)
    counter += 1

driver.quit()


df = pd.DataFrame(data)
print(df)
df.index += 1
excel_file_path = r"C:\Users\dsvan\OneDrive\Desktop\Anish\School\1st year\yv databases\tiktokdata3.xlsx"
df.to_excel(excel_file_path, index=False)
print(f"Data saved to {excel_file_path}")