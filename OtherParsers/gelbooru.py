import asyncio
import os

import aiohttp
from pygelbooru import Gelbooru
from pygelbooru.gelbooru import GelbooruImage

api_key = 'ENTER YOUR API KEY YOU CAN GET THEM HERE https://gelbooru.com/index.php?page=account&s=options'
user_id = 'ENTER YOUR USER KEY YOU CAN GET THEM HERE https://gelbooru.com/index.php?page=account&s=options'
gelbooru = Gelbooru(api_key, user_id)


async def get_images(amount: int) -> list:
    results = []
    for _ in range(amount):
        image = await gelbooru.random_post(tags=['marcille'])
        print(_)
        results.append(image)
    return results


async def download_image(image: GelbooruImage, folder: str):
    url = image.file_url
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                filename = os.path.join(folder, os.path.basename(url))
                with open(filename, 'wb') as f:
                    f.write(await response.read())
                    print(f"Downloaded: {filename}")


async def save_images(images: list, folder: str):
    if not os.path.exists(folder):
        os.makedirs(folder)
    for image in images:
        await download_image(image, folder)


if __name__ == '__main__':
    image_store_location = '.\images'
    count = int(input('How many cute marcille faces do you need: '))

    loop = asyncio.get_event_loop()
    images = loop.run_until_complete(get_images(count))
    loop.run_until_complete(save_images(images, image_store_location))
