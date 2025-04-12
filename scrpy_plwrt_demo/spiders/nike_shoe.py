import json
from scrapy import Spider, Request
from scrapy_playwright.page import PageMethod

class NikeShoeSpider(Spider):
    name = "nike_shoe"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.captured_ajax_data = []  # List to store captured AJAX data

    def start_requests(self):
        # Initial request to load the target page
        yield Request(
            url="https://www.nike.com/w/mens-dunk-shoes-90aohznik1zy7ok",
            meta={
                "playwright": True,
                "playwright_include_page": True,  # Include Playwright page object
                "playwright_page_methods": [
                    PageMethod(
                        "wait_for_load_state", "networkidle"
                    ),  # Wait for AJAX requests to finish
                ],
            },
            callback=self.parse,
        )

    async def parse(self, response):
        # Retrieve Playwright page object from the response metadata
        page = response.meta["playwright_page"]

        # Function to intercept and capture AJAX requests
        async def intercept_request(route):
            request = route.request
            # Intercept AJAX requests to Nike's API
            if "api.nike.com" in request.url and request.method == "GET":
                # Fetch the intercepted request's response
                response = await route.fetch()
                body = await response.text()  # Get response body as text
                try:
                    # Parse response body as JSON
                    ajax_data = json.loads(body)
                    self.captured_ajax_data.append(ajax_data)  # Store the JSON data
                    self.logger.info(f"Captured data from: {request.url}")
                except json.JSONDecodeError:
                    self.logger.warning(f"Failed to parse JSON from: {request.url}")
            # Continue processing the request
            await route.continue_()

        # Intercept network requests to capture AJAX data
        await page.route("**/*", intercept_request)

        # Function to scroll the page to load more data via AJAX
        async def scroll_page():
            previous_height = await page.evaluate("document.body.scrollHeight")
            # Scroll to the bottom of the page
            while True:
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2000)
                new_height = await page.evaluate("document.body.scrollHeight")
                if new_height == previous_height:
                    break
                previous_height = new_height

        # Scroll to load more products via AJAX
        await scroll_page()

        # Wait for network activity to settle after scrolling
        await page.wait_for_load_state("networkidle")

        # Close the Playwright page
        await page.close()

        # Save captured AJAX data to JSON
        self.save_data_to_json()

    def save_data_to_json(self):
        # Save captured AJAX data into a local JSON file
        file_path = "captured_nike_data.json"
        with open(file_path, "w") as f:
            json.dump(self.captured_ajax_data, f, indent=4)
        self.log(f"Saved AJAX data to {file_path}")