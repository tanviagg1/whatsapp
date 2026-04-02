import os
import time
from playwright.sync_api import sync_playwright

CONTACT_NAME = "Apar"
WHATSAPP_WEB_URL = "https://web.whatsapp.com"
INTERVAL_SECONDS = 5 * 60  # 5 minutes


def send_images_to_contact(image_paths):
    """Open WhatsApp Web, find contact, and send each image 5 mins apart."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("Opening WhatsApp Web — please scan the QR code if prompted...")
        page.goto(WHATSAPP_WEB_URL)

        # Wait for WhatsApp to load (scan QR if needed — up to 60 seconds)
        page.wait_for_selector('div[data-testid="chat-list"]', timeout=60000)
        print("WhatsApp Web loaded.")

        # Search for contact
        search_box = page.locator('div[data-testid="chat-list-search"]')
        search_box.click()
        search_box.type(CONTACT_NAME)
        page.wait_for_timeout(2000)

        # Click on the contact
        contact = page.locator(f'span[title="{CONTACT_NAME}"]').first
        contact.click()
        page.wait_for_timeout(1000)
        print(f"Opened chat with {CONTACT_NAME}.")

        for i, image_path in enumerate(image_paths):
            abs_path = os.path.abspath(image_path)

            # Click the attachment button
            attach_btn = page.locator('div[data-testid="attach-menu-plus"]')
            attach_btn.click()
            page.wait_for_timeout(1000)

            # Upload image via file input
            file_input = page.locator('input[accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
            file_input.set_input_files(abs_path)
            page.wait_for_timeout(2000)

            # Click send
            send_btn = page.locator('div[data-testid="send-or-record-icon"]')
            send_btn.click()
            print(f"Sent image {i + 1}: {image_path}")

            if i < len(image_paths) - 1:
                print(f"Waiting 5 minutes before sending next image...")
                time.sleep(INTERVAL_SECONDS)

        print("All images sent!")
        browser.close()


if __name__ == "__main__":
    paths = [f"images/edited_{i}.jpg" for i in range(1, 4)]
    send_images_to_contact(paths)
