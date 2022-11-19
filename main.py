import requests
import json
from config import tok
from tqdm import tqdm
import time


class VK:

    def __init__(self, access_token, id_of_user, version='5.131'):
        self.token = access_token
        self.id = id_of_user
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_photo(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id, 'album_id': 'wall', 'photo_sizes': 0, 'extended': 1, 'rev': 1}
        response = requests.get(url, params={**self.params, **params})
        return response.json()


class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def get_upload_link(self, disk_file_path, file_url):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, 'url': file_url, "overwrite": "true"}
        response = requests.post(upload_url, headers=headers, params=params)
        return response.json()

    def create_folder(self, file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/"
        headers = self.get_headers()
        params = {'path': file_path}
        responce = requests.put(upload_url, headers=headers, params=params)
        for i in tqdm(photos_json, desc="Загрузка фотографий на диск: "):
            time.sleep(1)
        return responce


likes = 0
date = 0
photo_info = {}
photos_json = []
user_id = input('Введите айди страницы вконтакте - ')
token_of_yd = input('Введите токен своего яндекс диска - ')
folder_yd = input('Введите название папки в которую будут сохранены ваши фотографии - ')
vk = VK(tok, user_id)
photos_info = vk.users_photo()

for items in photos_info.values():
    for keys, values in items.items():
        if keys == 'items':
            for each_photo_info in values:
                for key, value in each_photo_info.items():
                    if key == 'likes':
                        likes = value.get('count')
                    if key == 'date':
                        date = value
                    if key == 'sizes':
                        sorted_pic = (sorted(value, key=lambda d: d['height']))[-5:]
                        photo_info['sizes'] = sorted_pic[-1].get('type')
                        photo_info['url'] = sorted_pic[-1].get('url')
                photo_info['file_name'] = f'{likes}_{date}'
                photos_json.append(photo_info)
                photo_info = {}

uploader = YandexDisk(token_of_yd)
uploader.create_folder(folder_yd)

for link in photos_json:
    photo_link = link.get('url')
    name = link.get('file_name')
    uploader.get_upload_link(f'{folder_yd}/{name}', photo_link)
    link.pop('url')


with open('list_photos.json', 'w') as f:
    json.dump(photos_json, f, sort_keys=True, ensure_ascii=False, indent=2)
