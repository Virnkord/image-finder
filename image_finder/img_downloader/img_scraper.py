
def search_google(keywords, max_results, output_directory, class_name=None):
    from img_downloader.google_images_download import googleimagesdownload
    response = googleimagesdownload()
    arguments = {"keywords":keywords,"limit":max_results,"print_urls":False}   #creating list of arguments
    response.download(arguments)   #passing the arguments to the function

import requests
import re
import json
import time
import uuid
import os
from PIL import Image
from io import BytesIO

def download(link, root_folder, class_name):
    response = requests.get(link, timeout=3.000)
    file = BytesIO(response.content)
    img = Image.open(file)

    # Split last part of url to get image name and its extension
    img_name = link.rsplit('/', 1)[1]
    img_type = img_name.split('.')[-1]
    
    if img_type.lower().isdigit(): img_type = "jpg"
    
    if img_type.lower() != "jpg":
        raise Exception("Cannot download this type of file")
    #Check if another file of the same name already exists
    uid = uuid.uuid1()
    if class_name:
        img.save(f"./{root_folder}/{class_name}/{class_name}-{uid.hex}.jpg", "JPEG")
    else:
        img.save(f"./{root_folder}/{class_name}-{uid.hex}.jpg", "JPEG")
        

def search_bing(keywords, max_results, output_directory, class_name=None):
    BING_IMAGE = 'https://www.bing.com/images/async?q='

    USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}

    downloaded_images = 0
    n_images = max_results
    page = 0
    root_folder = output_directory
    folder = keywords if class_name else ""
    while downloaded_images < n_images:
        searchurl = BING_IMAGE + keywords + '&first=' + str(page) + '&count=100'

        # request url, without usr_agent the permission gets denied
        response = requests.get(searchurl, headers=USER_AGENT)
        html = response.text
        page += 100
        results = re.findall('murl&quot;:&quot;(.*?)&quot;', html)

        if not os.path.exists(root_folder):
            os.mkdir(root_folder)

        target_folder = os.path.join(root_folder, folder)
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)

        for link in results:
            try:
                if downloaded_images >= n_images:
                    break;
                download(link, root_folder,folder)
                downloaded_images += 1
            except:
                continue
    print('Done')
    
def search_ddg(keywords, max_results, output_directory, class_name=None):
    URL = 'https://duckduckgo.com/'
    PARAMS = {'q': keywords}
    HEADERS = {
    'authority': 'duckduckgo.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'sec-fetch-dest': 'empty',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'referer': 'https://duckduckgo.com/',
    'accept-language': 'en-US,en;q=0.9'}

    res = requests.post(URL, data=PARAMS, timeout=3.000)
    search_object = re.search(r'vqd=([\d-]+)\&', res.text, re.M|re.I)

    if not search_object:
        return -1

    PARAMS = (
    ('l', 'us-en'),
    ('o', 'json'),
    ('q', keywords),
    ('vqd', search_object.group(1)),
    ('f', ',,,'),
    ('p', '1'),
    ('v7exp', 'a'))

    page_counter = 0
    downloaded_images = 0
    n_images = max_results
    page = 0
    root_folder = output_directory
    folder = keywords if class_name else ""
    request_url = URL + "i.js"
    while downloaded_images < n_images:
        while True:
            try:
                res = requests.get(request_url, headers=HEADERS, params=PARAMS, timeout=3.000)
                data = json.loads(res.text)
                break
            except ValueError as e:
                time.sleep(5)
                continue

        if not os.path.exists(root_folder):
            os.mkdir(root_folder)

        target_folder = os.path.join(root_folder, folder)
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)

        # Cut the extra result by the amount that still need to be downloaded
        if len(data["results"]) > n_images - downloaded_images:
            data["results"] = data["results"][:n_images - downloaded_images]

        for results in data["results"]:
            try:
                download(results["image"], root_folder, folder)
                downloaded_images+= 1
            except Exception as e:
                continue

        if "next" not in data:
            return 0
        request_url = URL + data["next"]
    print('Done')

# search_google("rain", 10)
# search_bing("galaxy", 10)
# search_ddg("firefly", 1, "downloads")

def search_unsplash(keywords, max_results, output_directory, class_name=None):       
    ak = input("Paste your access key here")

    url = "https://api.unsplash.com/search/photos/?client_id=" + ak
    params = {"query" : keywords, "per_page": max_results}
    response = requests.get(url, params=params)
    results = response.json()["results"]
    img_urls = [item["urls"]["raw"] for item in results]
    root_folder = output_directory
    folder = keywords if class_name else ""
    
    if not os.path.exists(root_folder):
            os.mkdir(root_folder)

    target_folder = os.path.join(root_folder, folder)
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
    
    for link in img_urls:
        download(link, root_folder,folder)
