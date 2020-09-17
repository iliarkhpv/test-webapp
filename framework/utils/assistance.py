import json
from string import ascii_uppercase, ascii_lowercase, digits
from random import choice
import datetime
from PIL import Image, ImageChops
import re
import requests
import base64


def get_config_data():
    with open("../config.json", encoding='utf-8') as config_data:
        data = json.load(config_data)
    return data


def get_testrail_data():
    with open("../testrail.json", encoding='utf-8') as config_data:
        data = json.load(config_data)
    return data


def get_test_data():
    with open("../test_data.json", encoding='utf-8') as config_data:
        data = json.load(config_data)
    return data


def generate_string(length=16):
    return ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for i in range(length))


def generate_integer(length=4):
    return ''.join(choice(digits) for i in range(length))


def get_current_date():
    return datetime.datetime.now().strftime("%a %b %d %Y")


def get_random_number(row_length):
    return choice(range(row_length))


def compare_images(image_1, image_2):
    img_1=Image.open(image_1)
    img_2=Image.open(image_2)
    result = ImageChops.difference(img_1, img_2).getbbox()
    return result


def match_url(attribute):
    pic = re.search('(?P<picture>http\S*.\w.(?:png|jpg|jpeg|gif))', attribute)
    return pic['picture'].replace('\\', '')


def get_script_content(url, login, password):
    response = requests.get(url.replace('http://', f'http://{login}:{password}@'))
    return response.text


def strip_span_content(string):
    return int(string.lstrip("Version: "))


def encode_file_to_base64(file):
    file = base64.b64encode(open(file, "rb").read())
    return file.decode('utf-8')


def open_logfile(logfile):
    with open(logfile, 'r') as log:
        content = log.read()
    return content

