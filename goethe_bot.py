from playwright.sync_api import sync_playwright

def scrape_goethe_b2():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)  # Set headless=True to hide browser
        page = browser.new_page()

        # Go to the Goethe B2 exam page
        page.goto("https://www.goethe.de/ins/in/en/sta/new/prf/gzb2.cfm")

        # Extract the page title
        title = page.title()
        print(f"Page Title: {title}")
        
        # Check if the button with data-testid exists
        accept_button = page.query_selector('[data-testid="uc-accept-all-button"]')

        # If the button is found, click it
        if accept_button:
            print("Button found. Clicking the accept button.")
            accept_button.click()
        else:
            print("Accept button not found.")

        page.wait_for_timeout(5000) 

        # Close the browser
        browser.close()

if __name__ == "__main__":
    scrape_goethe_b2()
