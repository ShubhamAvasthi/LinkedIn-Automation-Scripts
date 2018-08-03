from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.common.exceptions import NoSuchElementException        
from progress.bar import IncrementalBar
import time, csv, getpass

SCROLL_PAUSE_TIME = 1.0

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
username = ""
password = ""

driver.get("https://www.linkedin.com")
driver.find_element_by_id('login-email').send_keys(username)
driver.find_element_by_id('login-password').send_keys(password)
driver.find_element_by_id('login-submit').click()

driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections")

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

cards = driver.find_elements_by_class_name('mn-connection-card__link')

links =[]

for card in cards:
	links.append(card.get_attribute('href'))

with open("connections.csv","w", newline='') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames = ['Name', 'Headline', 'Location', 'Link', 'Website', 'Phone', 'Address', 'E-mail', 'Twitter'])
	writer.writeheader()

	bar = IncrementalBar('Fetching Connections', max=len(links))

	for link in links:

		driver.get(link + 'detail/contact-info')

		#Currently single website
		try:
			website = driver.find_element_by_class_name('ci-websites').find_element_by_class_name('pv-contact-info__contact-link').text
		except NoSuchElementException:
			website = ""

		try:
			phone = driver.find_element_by_class_name('ci-phone').find_element_by_class_name('pv-contact-info__ci-container').find_element_by_tag_name('span').text
		except NoSuchElementException:
			phone = ""

		try:
			address = driver.find_element_by_class_name('ci-address').find_element_by_class_name('pv-contact-info__contact-link').text
		except NoSuchElementException:
			address = ""

		try:
			email = driver.find_element_by_class_name('ci-email').find_element_by_class_name('pv-contact-info__contact-link').text
		except NoSuchElementException:
			email = ""

		try:
			twitter = driver.find_element_by_class_name('ci-twitter').find_element_by_class_name('pv-contact-info__contact-link').text
		except NoSuchElementException:
			twitter = ""

		#IM

		driver.find_element_by_class_name('artdeco-dismiss').click()

		name = driver.find_element_by_class_name('pv-top-card-section__name').text
		
		try:
			headline = driver.find_element_by_class_name('pv-top-card-section__headline').text
		except NoSuchElementException:
			headline = ""

		try:
			location = driver.find_element_by_class_name('pv-top-card-section__location').text
		except NoSuchElementException:
			location = ""

		writer.writerow({'Name': name, 'Headline': headline, 'Location': location, 'Link': link, 'Website': website, 'Phone': phone, 'Address': address, 'E-mail': email, 'Twitter': twitter})
		bar.next()
		time.sleep(0.2)
	
	bar.finish()
	driver.close()
