import selenium
import getpass
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
import os

missingMessage = "It seems I do not have access to this repository. Please add my username (or resend the invite if it expired) and email me by the Friday night after this grade is posted."
username = input("Please enter your ninernet username: ")
password = getpass.getpass('Please enter your password:')
gitUser = input("Please enter your GitHub username: ")
gitPass = getpass.getpass('Please enter your password:')  

duoPin = input("Please enter your duo push code: ")

s = Service('C:/Users/Michael/Documents/Personal/PY_code/Selenium_Drivers/geckodriver.exe')
driver = webdriver.Firefox(service=s) #replace path with your own geckodriver.exe Path
driver.get('https://github.com/')
time.sleep(1)
driver.find_element(By.XPATH, '/html/body/div[1]/header/div/div[2]/div[2]/div[2]/a').click()
driver.find_element(By.XPATH, '//*[@id="login_field"]').send_keys(gitUser)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(gitPass)
driver.find_element(By.XPATH, '//*[@id="login"]/div[4]/form/div/input[12]').click()

driver.get("https://uncc.instructure.com/courses/168525/assignments/1412123")
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(username)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)

driver.find_element(By.XPATH, '//*[@id="shibboleth-login-button"]').click() #clicks login

time.sleep(2.5)
iframe = driver.find_element(By.XPATH, '//*[@id="duo_iframe"]')
driver.switch_to.frame(iframe)
driver.find_element(By.XPATH, '//*[@id="passcode"]').click()
driver.find_element(By.XPATH, '//*[@id="auth_methods"]/fieldset/div[2]/div/input').send_keys(duoPin)
driver.find_element(By.XPATH, '//*[@id="passcode"]').click()
driver.switch_to.default_content()

# time.sleep(4)
# WebDriverWait(driver,10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="global_nav_courses_link"]')))#wait for page load
# driver.find_element(By.XPATH, '//*[@id="global_nav_courses_link"]').click()

# time.sleep(3)
# WebDriverWait(driver,10).until(ec.presence_of_element_located((By.XPATH,'/html/body/div[3]/span/span/div/div/div/div/div/ul[1]/li[2]/a')))#wait for page load
# driver.find_element(By.XPATH, '/html/body/div[3]/span/span/div/div/div/div/div/ul[1]/li[2]/a').click() # May have to change this XPATH based on where 3155 shows up

# time.sleep(3)
# WebDriverWait(driver,10).until(ec.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/div[2]/div[2]/div/nav/ul/li[7]/a')))#wait for page load
# driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div/nav/ul/li[7]/a').click()

# time.sleep(3)
# ###################################### Change this XPATH per assignment #############################################################
# time.sleep(5)
# # WebDriverWait(driver,10).until(ec.presence_of_element_located((By.CLASS_NAME,'fOyUs_bGBk eHiXd_bGBk eHiXd_brAJ eHiXd_doqw eHiXd_bNlk eHiXd_cuTS'))#wait for page load
# # driver.find_element_by_class_name('fOyUs_bGBk eHiXd_bGBk eHiXd_brAJ eHiXd_doqw eHiXd_bNlk eHiXd_cuTS').click()
# ###################################### Change this XPATH per assignment #############################################################
WebDriverWait(driver,10).until(ec.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/div[2]/div[3]/div[2]/aside/div/ul/li[1]/div[2]/a')))
driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[3]/div[2]/aside/div/ul/li[1]/div[2]/a').click()
time.sleep(2)
driver.switch_to.window(driver.window_handles[1])
for i in range(75):
    didSubmit = False
    time.sleep(3)
    try: 
        driver.switch_to.frame("speedgrader_iframe")
        driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[2]/a').click()
        driver.switch_to.default_content()
        driver.switch_to.window(driver.window_handles[2])
        didSubmit = True
        time.sleep(4)
    except (NoSuchElementException, NoSuchFrameException):
        driver.switch_to.default_content()
        driver.find_element(By.ID, 'speed_grader_comment_textarea').send_keys("missing")
        driver.find_element(By.XPATH, '//*[@id="comment_submit_button"]').click()
        time.sleep(3)
    
    if didSubmit:
        try:
            driver.find_element(By.XPATH, '/html/body/div[6]/main/div[2]/div/div/div[1]/div/form[1]/button').click()
            time.sleep(2)
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
        except NoSuchElementException:
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
            driver.switch_to.default_content()
            driver.find_element(By.ID, 'speed_grader_comment_textarea').send_keys(missingMessage)
            driver.find_element(By.XPATH, '//*[@id="comment_submit_button"]').click()
            time.sleep(3)
    driver.switch_to.default_content()
    driver.find_element(By.XPATH, '//*[@id="next-student-button"]/i').click()
