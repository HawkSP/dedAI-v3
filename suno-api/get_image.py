import requests
import os

base_url = 'http://localhost:3000'

def get_image_information(image_ids):
    url = f"{base_url}/api/get?ids={image_ids}"
    response = requests.get(url)
    return response.json()

def download_image(image_url, save_dir='images', filename=None):
    if not filename:
        filename = image_url.split('/')[-1]  # Extracts the file name from URL
    os.makedirs(save_dir, exist_ok=True)  # Ensure the directory exists
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(os.path.join(save_dir, filename), 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded successfully: {filename}")
    else:
        print(f"Failed to download the image: {response.status_code}")

def main(image_ids):
    image_information = get_image_information(image_ids)
    if image_information and 'image_url' in image_information[0]:
        image_url = image_information[0]['image_url']
        print(f"Image URL: {image_url}")
        download_image(image_url)
    else:
        print("No image URL found in the response.")

if __name__ == '__main__':
    image_ids = "35438699-2088-4dc3-a6af-9e71abaea2a7"
    main(image_ids)
