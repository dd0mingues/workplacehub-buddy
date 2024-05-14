import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta

# Choose your seat ex: OPO-6-23
seatNumber = "OPO-6-23"

pageUrl = "https://euronext.sharepoint.com/sites/workplacehub/#"
# pageUrl = "https://euronext.sharepoint.com/sites/WorkplaceHub_QA"

options = webdriver.EdgeOptions()
options.page_load_strategy = 'normal'

with webdriver.Edge(options=options) as driver:
    wait = WebDriverWait(driver, 3)
    driver.get(pageUrl)

    try:
        wait.until(EC.element_to_be_clickable((By.ID, "btnCheckIn"))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "btnConfirmCheckIn"))).click()
    except:
        print("Too late to check in")

    currDate = datetime.now()
    futureDate = currDate + timedelta(days=13)
    
    if datetime.now().weekday() == 0:
        driver.quit()
        raise Exception("Today is Monday, Garfield HATES Mondays...")

    wait.until(EC.element_to_be_clickable((By.ID, "btnReservation"))).click()

    if currDate.month != futureDate.month:
        btnNextList = driver.find_elements(By.CLASS_NAME, "ui-datepicker-next")
        for nextButton in btnNextList:
            nextButton.click()

    calendarList = driver.find_elements(By.TAG_NAME, "table")

    try:
        for calendar in calendarList:
            dayList = calendar.find_elements(By.TAG_NAME, "a")
            lastAvailableDay = dayList[-1]
            lastAvailableDay.click()
    except:
        pass

    driver.find_element(By.ID, "btnSearchFreeLocations").click()
    

    # Location Page
    # Select Country
    buildingElement = wait.until(EC.element_to_be_clickable((By.ID, "ddlBuildings")))
    buildingElement.click()
    portoBuilding = wait.until(EC.element_to_be_clickable((By.ID, "12")))
    portoBuilding.click()

    # Select Floor
    floorElement = wait.until(EC.element_to_be_clickable((By.ID, "ddlFloors")))
    floorElement.click()
    sixthFloor = wait.until(EC.element_to_be_clickable((By.ID, "17")))
    sixthFloor.click()
    

    try:
        mySeatElement = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@title='{seatNumber}']")))
        mySeatElement.click()
        addReservationButton = wait.until(EC.element_to_be_clickable((By.ID, "btnAddReservation")))
        addReservationButton.click()
        submitReservationButton = wait.until(EC.element_to_be_clickable((By.ID, "btnSubmitReservation")))
        submitReservationButton.click()
        print("Completed")
    except:
        print("Seat taken")

time.sleep(2.5)