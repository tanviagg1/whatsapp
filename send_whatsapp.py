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

        print("Waiting for WhatsApp Web to load (you have 2 minutes to scan QR)...")
        page.wait_for_function(
            """() => {
                return document.querySelector('#pane-side') !== null ||
                       document.querySelector('#side') !== null ||
                       document.querySelector('div[data-testid="chat-list"]') !== null;
            }""",
            timeout=120000
        )
        # Extra wait for full render
        page.wait_for_timeout(3000)
        print("WhatsApp Web loaded.")

        # Try to click the contact directly from the chat list (fastest approach)
        contact = page.locator(f'span[title="{CONTACT_NAME}"]').first
        try:
            contact.wait_for(timeout=5000)
            contact.click()
            print(f"Opened chat with {CONTACT_NAME} directly from list.")
        except Exception:
            # Fall back to search if contact not visible in list
            print(f"{CONTACT_NAME} not visible in list, searching...")
            search_input = page.locator('input[type="text"], input[placeholder]').first
            search_input.wait_for(timeout=10000)
            search_input.click()
            search_input.type(CONTACT_NAME)
            page.wait_for_timeout(2000)
            contact = page.locator(f'span[title="{CONTACT_NAME}"]').first
            contact.wait_for(timeout=10000)
            contact.click()
            print(f"Opened chat with {CONTACT_NAME} via search.")

        page.wait_for_timeout(1000)

        for i, image_path in enumerate(image_paths):
            abs_path = os.path.abspath(image_path)

            # Click the attachment button
            attach_btn = page.locator(
                'div[data-testid="attach-menu-plus"], '
                '[aria-label="Attach"], '
                'span[data-icon="plus"]'
            ).first
            attach_btn.wait_for(timeout=10000)
            attach_btn.click()
            page.wait_for_timeout(1000)

            # Upload image via file input
            file_input = page.locator('input[type="file"]').first
            file_input.set_input_files(abs_path)
            page.wait_for_timeout(2000)

            # Click send
            send_btn = page.locator(
                'div[data-testid="send-or-record-icon"], '
                '[aria-label="Send"], '
                'span[data-icon="send"]'
            ).first
            send_btn.wait_for(timeout=10000)
            send_btn.click()
            print(f"Sent image {i + 1}: {image_path}")

            if i < len(image_paths) - 1:
                print("Waiting 5 minutes before sending next image...")
                time.sleep(INTERVAL_SECONDS)

        print("All images sent!")
        browser.close()


if __name__ == "__main__":
    paths = [f"images/edited_{i}.jpg" for i in range(1, 4)]
    send_images_to_contact(paths)
