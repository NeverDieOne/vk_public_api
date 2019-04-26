import requests
from dotenv import load_dotenv
import os
import random


def get_picture_data(picture_id):
    url = f'http://xkcd.com/{picture_id}/info.0.json'
    return requests.get(url).json()


def download_picture(picture_id):
    picture_link = get_picture_data(picture_id)['img']

    picture_response = requests.get(picture_link)
    filename = f'{picture_id}.png'
    with open(filename, 'wb') as image:
        image.write(picture_response.content)


def get_info_for_upload(*args):
    params = f'group_id=181636090'
    url = f'https://api.vk.com/method/photos.getWallUploadServer?{params}&access_token={ACCESS_TOKEN}&v=5.95'
    response = requests.get(url).json()
    return response['response'][args[0]]


# TODO new name for this function
def upload_picture(pic_num):
    upload_url = get_info_for_upload('upload_url')
    pic_file = open(f'{pic_num}.png', 'rb')
    files = {'photo': pic_file}
    response = requests.post(upload_url, files=files).json()
    pic_file.close()
    return response['server'], response['photo'], response['hash']


# TODO new name for this function
def get_media_id(pic_num):
    server, photo, _hash = upload_picture(pic_num)
    params = f'server={server}&photo={photo}&hash={_hash}&group_id=181636090'

    url = f'https://api.vk.com/method/photos.saveWallPhoto?{params}&access_token={ACCESS_TOKEN}&v=5.95'
    response = requests.post(url).json()
    return response['response'][0]['id'], response['response'][0]['owner_id']


def post_picture(pic_num):
    media_id, owner_id = get_media_id(pic_num)
    attachments = f'photo{owner_id}_{media_id}'
    message = get_picture_data(pic_num)['alt']
    params = f'owner_id=-181636090&from_group=1&attachments={attachments}&message={message}'

    url = f'https://api.vk.com/method/wall.post?{params}&access_token={ACCESS_TOKEN}&v=5.95'
    response = requests.get(url)
    print(response.json())


def get_last_picture_num():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url).json()
    return response['num']


def main():
    pass


if __name__ == '__main__':
    load_dotenv()
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

    random_number = random.randint(1, get_last_picture_num())
    print(random_number)


