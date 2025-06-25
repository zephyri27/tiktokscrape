import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

options = Options()
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("window_size=1280,800")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-save-password-bubble")

driver = webdriver.Chrome(options=options)
driver.get("https://accounts.google.com/v3/signin/identifier?hl=en_GB&ifkv=AXo7B7VGP4Y_gNfwPri72zV40Ii9kmgYbvLRXoOhOeBNkeBYcMPcPOX_Aolo1vK16FetaA4URMIfUA&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-1140670556%3A1692882589574310")
#email:
email = 'email'
#password:
password = 'password'

#LOGIN
driver.find_element(By.XPATH,'//*[@id="identifierId"]').send_keys(email)
time.sleep(3)
driver.find_element(By.XPATH,'//*[@id="identifierNext"]/div/button/span').click()
time.sleep(5)
driver.find_element(By.XPATH,'//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
driver.find_element(By.XPATH,'//*[@id="passwordNext"]/div/button/span').click()
time.sleep(5)

#GO TO TWITTER
driver.get("https://twitter.com/")
time.sleep(30)

tweets_df = pd.DataFrame(columns=["posts", "views", "likes", "reposts", "comments"])

def processtweet():
    global tweets_df
    #posttext
    try:
        post = driver.find_element(By.XPATH, '//*[starts-with(@id, "id__")]/span[1]')
        posttext = post.text
        print(posttext)
        if posttext in tweets_df['posts'].values:
            print("Post already there")
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
            return
    except StaleElementReferenceException:
        print("cant find tweet")
        return
    except NoSuchElementException:
        print("posts, nosuchelement")
        return

    #viewtext
    try:
        views = driver.find_element(By.XPATH, '//*[starts-with(@id, "id__")]/div[4]/a/div/div[2]/span/span/span')
        viewtxt = views.text
        print(viewtxt)
    except StaleElementReferenceException:
        print("cant find views")
        return
    except NoSuchElementException:
        print("views, nosuchelement")
        return

    #liketext
    try:
        likes = driver.find_element(By.XPATH,'//*[starts-with(@id, "id__")]/div[3]/button/div/div[2]/span/span/span')
        likestxt = likes.text
        print(likestxt)
    except StaleElementReferenceException:
        print("cant find likes")
        return
    except NoSuchElementException:
        print("likes, nosuchelement")
        return

    #reposttext
    try:
        reposts = driver.find_element(By.XPATH, '//*[starts-with(@id, "id__")]/div[2]/button/div/div[2]/span/span/span')
        repoststxt = reposts.text
        print(repoststxt)
    except StaleElementReferenceException:
        print("cant find reposts")
        return
    except NoSuchElementException:
        print("repost, nosuchelement")
        return

    #commenttext
    try:
        comments = driver.find_element(By.XPATH, '//*[starts-with(@id, "id__")]//div[1]/button/div/div[2]/span/span/span')
        commentstxt = comments.text
        print(commentstxt)
    except StaleElementReferenceException:
        print("cant find comments")
        return
    except NoSuchElementException:
        print("comment, nosuchelement")
        return


    #compiling all data
    new_data = {
        "posts": [posttext],
        "views": [viewtxt],
        "likes": [likestxt],
        "reposts": [repoststxt],
        "comments": [commentstxt]
    }

    #dfstuff
    postall_df = pd.DataFrame(new_data)
    tweets_df = pd.concat([tweets_df, postall_df], ignore_index=True)
    print(tweets_df)
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)

counter = 0
while counter<1100:
    processtweet()
    time.sleep(2)
    counter+=1

print(tweets_df)


df = pd.DataFrame(tweets_df)
print(df)
df.index += 1
excel_file_path = r"_______________"
df.to_excel(excel_file_path, index=False)
print(f"Data saved to {excel_file_path}")

