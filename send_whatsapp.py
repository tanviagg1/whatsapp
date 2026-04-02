import os
import time
from playwright.sync_api import sync_playwright

CONTACT_NAME = "Apar"
WHATSAPP_WEB_URL = "https://web.whatsapp.com"
INTERVAL_SECONDS = 5 * 60  # 5 minutes


def find_search_box(page):
    """Find the WhatsApp search box using JavaScript to inspect actual DOM."""
    # Dump all contenteditable elements so we can debug if needed
    elements = page.evaluate("""() => {
        const els = document.querySelectorAll('[contenteditable="true"]');
        return Array.from(els).map(el => ({
            id: el.id,
            ariaLabel: el.getAttribute('aria-label'),
            dataTab: el.getAttribute('data-tab'),
            placeholder: el.getAttribute('data-lexical-editor') || el.getAttribute('placeholder') || '',
            parentId: el.parentElement ? el.parentElement.id : ''
        }));
    }""")
    print(f"DEBUG — contenteditable elements found: {elements}")

    # Try to click search using JavaScript directly on the first one in #side or #pane-side
    clicked = page.evaluate("""() => {
        const side = document.querySelector('#side') || document.querySelector('#pane-side');
        if (!side) return 'no side panel found';
        const box = side.querySelector('[contenteditable="true"]');
        if (!box) return 'no contenteditable in side panel';
        box.click();
        box.focus();
        return 'clicked';
    }""")
    print(f"DEBUG — search box click result: {clicked}")

    if clicked == 'clicked':
        return True
    return False


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

        # Take a screenshot to help debug selector issues
        page.screenshot(path="images/debug_screenshot.png")
        print("DEBUG — screenshot saved to images/debug_screenshot.png")

        # Find and click the search box via JS
        found = find_search_box(page)
        if not found:
            raise Exception("Could not find the search box. Check images/debug_screenshot.png")

        # Type the contact name
        page.keyboard.type(CONTACT_NAME)
        page.wait_for_timeout(2000)

        # Click on the contact
        contact = page.locator(f'span[title="{CONTACT_NAME}"]').first
        contact.wait_for(timeout=10000)
        contact.click()
        page.wait_for_timeout(1000)
        print(f"Opened chat with {CONTACT_NAME}.")

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
