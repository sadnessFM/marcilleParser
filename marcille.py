import os
import time
import urllib
import requests


access_token = "PUT YOUR VK TOKEN HERE YOU CAN GET IT HERE https://vkhost.github.io/"
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/91.0.4472.124 Safari/537.36'}
image_output_folder = 'images'


def get_group_id(access_token):
    base_url = 'https://api.vk.com/method/groups.getById'
    params = {
        'group_id': 'marcille',
        'access_token': access_token,
        'v': '5.131'
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    group_id = data['response'][0]['id']
    return group_id


def get_image_urls_from_posts(group_id, access_token, count=100):
    base_url = 'https://api.vk.com/method/wall.get'
    image_urls = []
    offset = 0
    while count > 0:
        params = {
            'owner_id': -group_id,
            'count': min(count, 100),
            'offset': offset,
            'access_token': access_token,
            'v': '5.131'
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if 'response' in data and 'items' in data['response']:
            items = data['response']['items']
            for post in items:
                if 'attachments' in post:
                    for attachment in post['attachments']:
                        if attachment['type'] == 'photo':
                            sizes = attachment['photo']['sizes']
                            image_url = sizes[-1]['url']
                            image_urls.append(image_url)
            count -= len(items)
            offset += len(items)
        else:
            print('Error occurred while getting posts')
            break

        time.sleep(0)

    print(f"{len(image_urls)} are indexed successfully")
    return image_urls


def save_images_from_verified_urls(image_urls, output_folder):
    saved_posts = 0
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, image_url in enumerate(image_urls):
        response = requests.get(image_url)

        if response.status_code == 200:
            filename = urllib.parse.unquote(os.path.basename(urllib.parse.urlparse(image_url).path))
            image_name = f"image_{i}_{filename}"
            image_path = os.path.join(output_folder, image_name)
            with open(image_path, 'wb') as f:
                f.write(response.content)
            saved_posts += 1
            print(f"Saved: {image_name}")
        else:
            print(f"Failed to download image: {image_url}")

        time.sleep(0.35)

    print(f"Amount of saved pictures: {saved_posts}")


def check_image_urls(image_urls):
    verified_urls = []
    for image_url in image_urls:
        response = requests.get(image_url)
        if response.status_code == 200:
            print(f"Valid URL: {image_url}")
            verified_urls.append(image_url)
        else:
            print(f"Invalid URL: {image_url}")
    return verified_urls


count = int(input('Enter the number of posts to process: '))
print(' ')
print('Please wait...\n')

group_id = get_group_id(access_token)
image_urls = get_image_urls_from_posts(group_id, access_token, count)
good_urls = check_image_urls(image_urls)
save_images_from_verified_urls(good_urls, image_output_folder)
total_posts = count

print('Posts saved to file and processed.\n')
print(f'pics are in folder {image_output_folder}')
print('Praise Marcille my friend, goodbye for now')
