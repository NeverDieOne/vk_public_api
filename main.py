import requests
from dotenv import load_dotenv
import os
import random


def get_picture_data(picture_id):
    url = f'http://xkcd.com/{picture_id}/info.0.json'
    response = requests.get(url)
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        print('Picture not found')
        exit()


def download_picture(picture_id):
    picture_link = get_picture_data(picture_id)['img']

    picture_response = requests.get(picture_link)
    try:
        picture_response.raise_for_status()
        filename = f'{picture_id}.png'
        with open(filename, 'wb') as image:
            image.write(picture_response.content)
    except requests.exceptions.HTTPError:
        print('Picture not found')
        exit()


def get_info_for_upload(group_id, *args):
    params = {
        'group_id': group_id,
        'access_token': ACCESS_TOKEN,
        'v': '5.95'
    }
    url = f'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, params=params).json()
    try:
        print(response['error']['error_msg'])
        exit()
    except KeyError:
        return response['response'][args[0]]


def upload_picture(pic_num, group_id):
    upload_url = get_info_for_upload(group_id, 'upload_url')
    download_picture(pic_num)
    pic_file = open(f'{pic_num}.png', 'rb')
    files = {'photo': pic_file}
    response = requests.post(upload_url, files=files).json()
    pic_file.close()
    try:
        print(response['error']['error_msg'])
        exit()
    except KeyError:
        return response['server'], response['photo'], response['hash']


def get_data_for_post(pic_num, group_id):
    server, photo, _hash = upload_picture(pic_num, group_id)
    params = {
        'server': server,
        'photo': photo,
        'hash': _hash,
        'group_id': group_id,
        'access_token': ACCESS_TOKEN,
        'v': '5.95'
    }
    url = f'https://api.vk.com/method/photos.saveWallPhoto'
    response = requests.post(url, params=params).json()
    try:
        print(response['error']['error_msg'])
        exit()
    except KeyError:
        return response['response'][0]['id'], response['response'][0]['owner_id']


def post_picture(pic_num, group_id):
    media_id, owner_id = get_data_for_post(pic_num, group_id)
    params = {
        'owner_id': f'-{group_id}',
        'message': get_picture_data(pic_num)['alt'],
        'attachments': f'photo{owner_id}_{media_id}',
        'from_group': 1,
        'access_token': ACCESS_TOKEN,
        'v': '5.95'
    }
    url = f'https://api.vk.com/method/wall.post'
    response = requests.get(url, params=params).json()
    try:
        print(response['error']['error_msg'])
        exit()
    except KeyError:
        os.remove(f'{pic_num}.png')


def get_last_picture_num():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    try:
        response.raise_for_status()
        return response.json()['num']
    except requests.exceptions.HTTPError:
        exit()


if __name__ == '__main__':
    load_dotenv()
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    GROUP_ID = os.getenv('GROUP_ID')

    random_number = random.randint(1, get_last_picture_num())
    post_picture(random_number, GROUP_ID)
