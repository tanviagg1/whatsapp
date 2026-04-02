from fetch_images import fetch_lily_images
from edit_image import edit_all_images
from send_whatsapp import send_images_to_contact


def main():
    print("Step 1: Fetching 3 lily images from Unsplash...")
    image_paths = fetch_lily_images(count=3)

    print("\nStep 2: Adding 'Hello' text to each image...")
    edited_paths = edit_all_images(image_paths)

    print("\nStep 3: Sending images to Apar on WhatsApp...")
    send_images_to_contact(edited_paths)

    print("\nDone!")


if __name__ == "__main__":
    main()
