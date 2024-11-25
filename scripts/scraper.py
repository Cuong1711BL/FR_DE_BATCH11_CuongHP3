from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
import logging
import time
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def scrape_jobs():
    print("Starting the scrape_jobs function...")
    # Configure Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)
    service = Service('/usr/bin/chromedriver')  # Ensure this path is correct
    print("Setting up Chrome WebDriver...")
    driver = webdriver.Chrome(service=service, options=options)

    print("Opening the Indeed website...")
    driver.get("https://vn.indeed.com/jobs?q=developer&l=Th%C3%A0nh+ph%E1%BB%91+H%E1%BB%93+Ch%C3%AD+Minh&fromage=1&start=10&vjk=b3ebaf4de86513c6")

    data = []

    time.sleep(10)

    print(driver.page_source)

    # wait = WebDriverWait(driver, 10)

    # try:
    #     job_elements = wait.until(
    #     EC.presence_of_all_elements_located((By.XPATH, "//*[@class='job_seen_beacon']"))
    #     )
    #     print(f"Found {len(job_elements)} job listings.")
    # except Exception as e:
    #     print(f"Error waiting for elements: {e}")



    try:
        print("Scraping job data ......")
        jobs = driver.find_elements(By.XPATH, ".//*[@class='job_seen_beacon']")
        
        if len(jobs) == 0:
            print("There are no jobs to scrape")
        
        print(len(jobs))
        print(type(jobs))
        print(list(jobs))

        data = []
        page_number = 1

        while True:
            for job in driver.find_elements(By.XPATH, ".//*[@class='job_seen_beacon']"):
                print("Processing a job listing...")
                title = job.find_element(By.XPATH, ".//*[contains(@class,'JobTitle')]").get_attribute("aria-label").replace("full details of ", "")
                company = job.find_element(By.XPATH, ".//*[@data-testid='company-name']").text
                logger.info(f"Title: {title}, Company: {company}")
                data.append({"title": title, "company": company})
                logger.info(f"data: {data}")

            # Check for the next page
            next_page_button_xpath = f".//*[@aria-label='pagination']/ul/li/a[text()='{page_number + 1}']"
            next_page_elements = driver.find_elements(By.XPATH, next_page_button_xpath)

            if len(next_page_elements) == 0:
                print("No more pages to scrape.")
                break  # Exit loop if no next page exists
            else:
                print(f"Navigating to page {page_number + 1}")
                next_page_elements[0].click()
                page_number += 1

    except Exception as e:
        print(f"Error while scraping: {e}")
    finally:
        driver.quit()


    # Save scraped data to jobs.csv
    print("Saving data to jobs.csv...")
    output_path = '/opt/airflow/datasets/jobs.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["title", "company"])
        writer.writeheader()
        writer.writerows(data)

    print(f"Job listings scraped successfully! File saved at {output_path}")




