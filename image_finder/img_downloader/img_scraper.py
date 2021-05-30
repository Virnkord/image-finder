import requests
import re
import json
import time
import uuid
import os
import sys
from PIL import Image, UnidentifiedImageError
from io import BytesIO

def download(link, root_folder, class_name):
    while True:
        try:
            response = requests.get(link, timeout=3.000)
            # requests.post(url, headers, timeout=10)
            break
        except requests.exceptions.Timeout:
            time.sleep(1)
            continue

    # Split last part of url to get image name and its extension
    img_name = link.rsplit('/', 1)[1]
    img_type = img_name.split('.')[-1]
    
    if img_type.lower().isdigit(): img_type = "jpg"
    
    if img_type.lower() != "jpg":
        raise Exception("Cannot download this type of file")
    file = BytesIO(response.content)
    try:
        img = Image.open(file)
    except UnidentifiedImageError:
        raise Exception("Corrupted file")
    #Check if another file of the same name already exists
    uid = uuid.uuid4()
    if class_name:
        return_image_name = os.path.join(root_folder, class_name, f"{uid.hex}.jpg")
        img.save(return_image_name, "JPEG")
    else:
        return_image_name = os.path.join(root_folder,f"{uid.hex}.jpg")
        img.save(return_image_name, "JPEG")
    return return_image_name
        

def search_google(keywords, max_results, output_directory, class_name=None):
    from image_finder.img_downloader.google_images_download import googleimagesdownload
    
    root_folder = os.path.join(os.getcwd(),output_directory)
    folder = keywords if class_name else ""
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)
    target_folder = os.path.join(root_folder, folder)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    response = googleimagesdownload()
    folder = keywords if class_name else ""
    arguments = {"keywords":keywords,"limit":max_results,"print_urls":False, "silent_mode":True,
                 "output_directory":root_folder, "image_directory":folder}   #creating list of arguments
    (paths, _, urls) = response.download(arguments)   #passing the arguments to the function
    
    return paths[keywords], urls

def search_bing(keywords, max_results, output_directory, class_name=None):
    BING_IMAGE = 'https://bing.com/images/async?q='

    USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

    downloaded_images = 0
    n_images = max_results
    page = 0
    root_folder = output_directory
    folder = keywords if class_name else ""
    
    root_folder = os.path.join(os.getcwd(),output_directory)
    folder = keywords if class_name else ""
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)
    target_folder = os.path.join(root_folder, folder)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        
    paths = []
    while downloaded_images < n_images:
        searchurl = BING_IMAGE + keywords + '&first=' + str(page) + '&count=20&mmasync=1'

        # request url, without usr_agent the permission gets denied
        response = requests.get(searchurl, headers=USER_AGENT)
        html = response.text

        page += 20
        results = re.findall('murl&quot;:&quot;(.*?)&quot;', html)

        for link in results:
            try:
                if downloaded_images >= n_images:
                    break;
                paths.append(download(link, root_folder,folder))
                downloaded_images += 1
                print("Total images from downloaded Bing: ", downloaded_images, end='\r')
                sys.stdout.flush()
            except:
                continue
    print('\nDone')
    return paths, results
    
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
    
    root_folder = os.path.join(os.getcwd(),output_directory)
    folder = keywords if class_name else ""
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)
    target_folder = os.path.join(root_folder, folder)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    paths, urls = [], []
    while downloaded_images < n_images:
        while True:
            try:
                res = requests.get(request_url, headers=HEADERS, params=PARAMS, timeout=3.000)
                data = json.loads(res.text)
                break
            except ValueError as e:
                time.sleep(5)
                continue


        # Cut the extra result by the amount that still need to be downloaded
        if len(data["results"]) > n_images - downloaded_images:
            data["results"] = data["results"][:n_images - downloaded_images]

        for results in data["results"]:
            try:

                paths.append(download(results["image"], root_folder, folder))
                urls.append(results["image"])
                downloaded_images+= 1
                print("Total images downloaded from DuckDuckGo: ", downloaded_images, end='\r')
                sys.stdout.flush()
            except Exception as e:
                continue

        if "next" not in data:
            return paths
        request_url = URL + data["next"]
    print('\nDone')
    return paths, urls

def search_unsplash(keywords, max_results, output_directory, ak, class_name=None):    
    url = "https://api.unsplash.com/search/photos/?client_id=" + ak
    params = {"query" : keywords, "per_page": max_results}
    while True:
        try:
            response = requests.get(url, params=params, timeout=3.000)
            # requests.post(url, headers, timeout=10)
            break
        except requests.exceptions.Timeout:
            time.sleep(1)
            continue
    if ("errors" in response.json() and response.json()["errors"][0] == "OAuth error: The access token is invalid"):
        raise Exception("OAuth error: The access token is invalid")
    results = response.json()["results"]
    img_urls = [item["urls"]["raw"] for item in results]
    
    
    root_folder = os.path.join(os.getcwd(),output_directory)
    folder = keywords if class_name else ""
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)
    target_folder = os.path.join(root_folder, folder)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    paths = []
    for i, link in enumerate(img_urls):
        paths.append(download(link, root_folder,folder))
        print("Total images downloaded from Unsplash: ", i+1, end='\r')
        sys.stdout.flush()
    print('\nDone')
    return paths, img_urls
