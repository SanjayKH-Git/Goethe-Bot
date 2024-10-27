import time
import csv
import asyncio
from playwright.async_api import async_playwright

async def open_page_from_row(row_data, url, page, page_number):
    print(f"Opening page {page_number}: {url}")
    await page.goto(url)

    # Send other column data as parameters (for example, printing them)
    print(f"Row Data for Page {page_number}: {row_data}")

    # Check if the button with data-testid exists
    accept_button = await page.query_selector('[data-testid="uc-accept-all-button"]')

    # If the button is found, click it
    if accept_button:
        print("Button found. Clicking the accept button.")
        await accept_button.click()
        await page.wait_for_load_state('load')
        time.sleep(2)

    # Find all elements with the selector //pr-button
    pr_buttons = await page.query_selector_all('//td[@class="pr-buttons"]//button')

    # Click the first clickable button if found
    for button in pr_buttons:
        if await button.is_enabled():
            print("Open Green button found. Clicking it.")
            await button.click()
            await page.wait_for_load_state('load')
            time.sleep(2)            
            break  # Stop after clicking the first one

    interests = [x.lower().strip() for x in row_data["Interests"].split(',')]
    
    all_checkboxes = await page.query_selector_all('//label[@class="cs-checkbox__label cs-checkbox__label--exam"]')

    # Click checkboxes except those related to interests
    for checkbox in all_checkboxes:
        checkbox_id = await checkbox.get_attribute('for')
        
        if checkbox_id.strip().lower() not in interests:
            print(f"Clicking checkbox: {checkbox_id}")
            await page.evaluate('(element) => element.click()', checkbox)

    continue_button = await page.query_selector('//button[@class="cs-button cs-button--arrow_next"]')
    
    if continue_button:
        await continue_button.click() 
        await page.wait_for_load_state('load')
        time.sleep(2)

    book_buttun = await page.query_selector('//button[contains(., "Book for myself")]')
    print("Clicking on Book for myself Button")
    if book_buttun:
        await book_buttun.click() 
        await page.wait_for_load_state('load')
        time.sleep(2)

    email = row_data["Email"]
    username_input = await page.query_selector('//input[@id="username"]')
    await username_input.fill(email)

    password = row_data["Password"]
    password_input = await page.query_selector('//input[@id="password"]')
    await password_input.fill(password)
    print("Entered Credentials")

    await password_input.press("Enter")    
    time.sleep(5)
    print(f"Successfully booked slot for {row_data["Name"]}")

async def main(file_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        tasks = []

        # Read the CSV file using Python's built-in csv module
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            
            # Identify the last column name for URL and other columns for data
            url_column = fieldnames[-1]  # Last column assumed to be the URL
            other_columns = fieldnames[:-1]  # All columns except the last

            # Iterate over each row and open pages
            for index, row in enumerate(reader):
                url = row[url_column]
                row_data = {col: row[col] for col in other_columns}  # Other columns data as params
                
                page = await browser.new_page()
                task = open_page_from_row(row_data, url, page, index + 1)
                tasks.append(task)
                
                if len(tasks) == 10:  # Open 10 pages at a time
                    await asyncio.gather(*tasks)
                    tasks.clear()  # Clear tasks for the next batch of 10

            # Handle any remaining tasks (less than 10)
            if tasks:
                await asyncio.gather(*tasks)

        await browser.close()

# Run the script with the uploaded CSV file path
input_csv = input("Enter Input CSV: ")
if not input_csv:
    input_csv = 'default_example_input.csv'

asyncio.run(main(input_csv))
