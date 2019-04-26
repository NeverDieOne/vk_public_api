import requests


def get_picture_data(picture_id):
    url = f'http://xkcd.com/{picture_id}/info.0.json'
    return requests.get(url).json()


def download_picture(picture_id):
    picture_link = get_picture_data(picture_id)['img']

    picture_response = requests.get(picture_link)
    filename = f'{picture_id}.png'
    with open(filename, 'wb') as image:
        image.write(picture_response.content)


if __name__ == '__main__':
    print(get_picture_data(312)['alt'])
