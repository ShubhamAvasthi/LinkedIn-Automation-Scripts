from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException        
from progress.bar import IncrementalBar
import time, csv, getpass

SCROLL_PAUSE_TIME = 2.0

options = Options()
options.set_headless(headless = False)

#Workaround since latest geckodriver and Firefox versions do not completely support Selenium
capabilities = webdriver.DesiredCapabilities().FIREFOX
capabilities["marionette"] = True

firefox_profile = FirefoxProfile()
## Disable images
firefox_profile.set_preference('permissions.default.image', 2)

driver = webdriver.Firefox(firefox_options=options, firefox_profile=firefox_profile, capabilities=capabilities)

#Change the following strings using a text editor
username = "insert username here"
password = "insert password here"
custom_message = """insert custom message here"""

#Logging in
driver.get("https://www.linkedin.com")
driver.find_element_by_id('login-email').send_keys(username)
driver.find_element_by_id('login-password').send_keys(password)
driver.find_element_by_id('login-submit').click()

while True:
    educationStartYear = 1900
    educationEndYear = 1960
    driver.get("https://www.linkedin.com/school/iit-bhu/alumni/?educationStartYear=%d&educationEndYear=%d"%(educationStartYear,educationEndYear))

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    links = driver.find_elements_by_class_name('org-alumni-profile-card__connect-button-expanded')
    links[0].click()
    try:
        driver.find_element_by_class_name('send-invite__cancel-btn').click()
    except NoSuchElementException:
        pass
    else:
        break

bar = IncrementalBar('Sending Connections', max=len(links))

for link in links:
    
    while(True):
        try:
            link.click()
        except ElementClickInterceptedException:
            # Scroll into view with middle alignment
            driver.execute_script("window.scrollBy(0, 10);")            
            continue
        else:
            break
    actions = driver.find_element_by_class_name('send-invite__actions')
    
    #Click "Add a Note"
    actions.find_element_by_class_name('button-secondary-large').click()

    driver.find_element_by_id('custom-message').send_keys(custom_message)

    #Click "Send Now"
    actions.find_element_by_class_name('button-primary-large').click()

    bar.next()
    time.sleep(1.5)

bar.finish()
#driver.close()
