import names
import random
import string
import time
from random import randint
from selenium import webdriver

chromedrive_location = "./chromedriver"
website = "ENTER WEBSITE URL HERE"

def random_email(userName):
    # Can extend this using various email addresses instead of only one
    return userName + "@email.com"

""" Returns a list containing a full name and a user name"""
def random_person():
    fullName = names.get_full_name()
    # Lower case it
    firstName, lastName = fullName.split(" ")
    firstName = firstName.lower()
    lastName = lastName.lower()
    # Create purdue style username
    userName = lastName + firstName[:1]
    return [fullName, userName]
    
def random_password(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))

if __name__ == "__main__":

    driver = webdriver.Chrome(chromedrive_location)

    # Change these according to the form
    login_xpath = '//*[@id="5273081c-d644-447c-bf3f-72182a7ab2f9-bootstrap-container"]/span/div/div/div/form/div[5]/div/div/button'
    fullname_id = 'input6'
    email_id = 'input7'
    password_id = 'input8'
    success_message_xpath = '//*[@id="5273081c-d644-447c-bf3f-72182a7ab2f9-bootstrap-container"]/span/div/div/div/div/div/div[2]'

    counter = 1

    driver.get(website)

    while (True):
        # Create a person
        person = random_person()
        fullName = person[0]
        email = random_email(person[1])
        password = random_password(randint(8, 12))

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(2)
        # Fill in information
        lg = driver.find_element_by_xpath(login_xpath)
        dp = driver.find_element_by_id(password_id)
        de = driver.find_element_by_id(email_id)
        df = driver.find_element_by_id(fullname_id)
        dp.send_keys(password)
        de.send_keys(email)
        df.send_keys(fullName)

        time.sleep(2)

        # Submit
        lg.click()

        driver.implicitly_wait(5)

        if (driver.find_element_by_xpath(success_message_xpath)):
            print(str(counter) + " Sent: " + fullName)

        counter += 1

        driver.refresh()

