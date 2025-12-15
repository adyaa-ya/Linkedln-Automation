import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager


# ------------------ USER DETAILS ------------------
LINKEDIN_EMAIL = "your_email_here"
LINKEDIN_PASSWORD = "your_password_here"

SEARCH_KEYWORD = "Software Engineer"
MAX_CONNECTIONS = 5
# --------------------------------------------------


def human_delay(min_sec=2, max_sec=4):
    """Adds random delay to behave like a human"""
    time.sleep(random.uniform(min_sec, max_sec))


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def login_linkedin(driver):
    driver.get("https://www.linkedin.com/login")
    human_delay()

    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")

    email_input.send_keys(LINKEDIN_EMAIL)
    human_delay(1, 2)
    password_input.send_keys(LINKEDIN_PASSWORD)
    human_delay(1, 2)
    password_input.send_keys(Keys.RETURN)

    human_delay(5, 7)


def search_people(driver):
    search_box = driver.find_element(By.XPATH, "//input[contains(@placeholder,'Search')]")
    search_box.click()
    human_delay(1, 2)

    search_box.send_keys(SEARCH_KEYWORD)
    human_delay(1, 2)
    search_box.send_keys(Keys.RETURN)

    human_delay(4, 6)

    # Click "People" filter
    try:
        people_tab = driver.find_element(By.XPATH, "//button[text()='People']")
        people_tab.click()
        human_delay(3, 5)
    except NoSuchElementException:
        print("People filter not found, continuing...")


def send_connections(driver):
    sent = 0

    while sent < MAX_CONNECTIONS:
        connect_buttons = driver.find_elements(By.XPATH, "//button[.//span[text()='Connect']]")

        if not connect_buttons:
            print("No more connect buttons found.")
            break

        for button in connect_buttons:
            if sent >= MAX_CONNECTIONS:
                break

            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                human_delay(1, 2)
                button.click()
                human_delay(2, 3)

                # Handle popup
                try:
                    send_without_note = driver.find_element(By.XPATH, "//button/span[text()='Send']/..")
                    send_without_note.click()
                except NoSuchElementException:
                    close_btn = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                    close_btn.click()

                sent += 1
                print(f"Connection request sent: {sent}")
                human_delay(4, 6)

            except (ElementClickInterceptedException, NoSuchElementException):
                continue

        # Scroll for more results
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        human_delay(4, 6)


def main():
    driver = setup_driver()

    try:
        login_linkedin(driver)
        search_people(driver)
        send_connections(driver)
        print("Automation completed successfully.")

    except Exception as e:
        print("Error occurred:", e)

    finally:
        human_delay(5, 7)
        driver.quit()


if __name__ == "__main__":
    main()
