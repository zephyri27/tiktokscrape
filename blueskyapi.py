from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

data = []

service = Service(r"_______edge driver________")
driver = webdriver.Edge(service=service)
driver.get("https://bsky.app")
time.sleep(5)

username = "finaltester"
password = "firefly!!"

driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div/nav/div/div[2]/button[2]').click()
time.sleep(2)

#login
driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div/div/div/div/div/div/div/div[3]/div[2]/div[1]/input').send_keys(username)
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div/div/div/div/div/div/div/div[3]/div[2]/div[2]/input').send_keys(password)
time.sleep(2)
driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div/div/div/div/div/div/div/div/div[4]/button[2]').click()
time.sleep(3)

bskydf = pd.DataFrame(columns=["posts", "likes", "comments"])
x = 2
countno = 1000
def processbskytweet():
    global bskydf
    global x
    global countno
    print(f"Processing post {x}")

    #postfinding
    try:
        post = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div/div/div/div/main/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div[{x}]/div/div/div/div[3]/div[2]/div[2]/div[1]/div')
        posttext = post.text
        print(posttext)
    except NoSuchElementException:
        print("No post found")
        x += 1
        countno += 1
        return

    #commentfinding
    try:
        comment = driver.find_element(By.XPATH,f'//*[@id="root"]/div/div/div/div/div/main/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div[{x}]/div/div/div/div[3]/div[2]/div[3]/div[1]/button/div')
        commenttext = comment.text
        print(commenttext)
    except NoSuchElementException:
        print("no comment")
        x += 1
        countno += 1
        return

    #likefinding
    try:
        likes = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div/div/div/div/main/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/div[{x}]/div/div/div/div[3]/div[2]/div[3]/div[3]/button/div[2]/div/div')
        likestext = likes.text
        print(likestext)
    except NoSuchElementException:
        print("no like")
        x += 1
        countno += 1
        return

    bskydf.loc[x] = [posttext, likestext, commenttext]
    x += 1
    driver.execute_script("window.scrollBy(0, 750);")  # Scroll down 100 pixels

counter = 0
for counter in range(countno):
    processbskytweet()
    time.sleep(2)

print(bskydf)


df = pd.DataFrame(bskydf)
print(df)
df.index += 1 
excel_file_path = r"____________________________________"
df.to_excel(excel_file_path, index=False)
print(f"Data saved to {excel_file_path}")
