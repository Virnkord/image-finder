import time
import sys,os
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__),os.pardir,"image_finder"))
print(sys.path)
from img_downloader.img_scraper import search_ddg, search_bing, search_google, search_unsplash
from image_finder.image_finder import search_images

def test_download():
    ak = "Kha6jgNu2s09zWWSw0UK6eA3OhlkmYU2V-D4Fs-MSiA"
    search = "nature"
    root = os.path.join("test_download", "unsplash")
    cwd = os.getcwd()
    path = os.path.join(cwd,root)
    if os.path.exists(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path)
    _, _ = search_unsplash(search, 1, root, ak)
    time.sleep(2)
    _, _, filenames = next(os.walk(path))
    assert os.path.isfile(os.path.join(cwd,root,filenames[0]))

def test_search_unsplash():
    ak = "Kha6jgNu2s09zWWSw0UK6eA3OhlkmYU2V-D4Fs-MSiA"
    search = "nature"
    root = os.path.join("test_download", "unsplash")
    cwd = os.getcwd()
    path = os.path.join(cwd,root)
    if os.path.exists(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path)
    _, url = search_unsplash(search, 1, root, ak)
    time.sleep(2)
    print (url)
    assert len(url) != 0
    # _, _, filenames = next(os.walk(path))
    # assert os.path.isfile(os.path.join(cwd,root,filenames[0]))

def test_search_ddg():
    search = "duck"
    root = os.path.join("test_download", "ddg")
    cwd = os.getcwd()
    path = os.path.join(cwd,root)
    if os.path.exists(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path)
    _, url = search_ddg(search, 1, root)
    time.sleep(2)
    _, _, filenames = next(os.walk(path))
    print (url)
    assert len(url) != 0
    # _, _, filenames = next(os.walk(path))
    # assert os.path.isfile(os.path.join(cwd,root,filenames[0]))
    
def test_search_bing():
    search = "microsoft"
    root = os.path.join("test_download", "bing")
    cwd = os.getcwd()
    path = os.path.join(cwd,root)
    if os.path.exists(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path)
    _, url = search_bing(search, 1, root)
    time.sleep(2)
    _, _, filenames = next(os.walk(path))
    print (url)
    assert len(url) != 0
    # _, _, filenames = next(os.walk(path))
    # assert os.path.isfile(os.path.join(cwd,root,filenames[0]))
    
def test_search_google():
    search = "penguin"
    root = os.path.join("test_download", "google")
    cwd = os.getcwd()
    path = os.path.join(cwd,root)
    if os.path.exists(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path)
    _, url = search_google(search, 1, root)
    time.sleep(2)
    _, _, filenames = next(os.walk(path))
    print (url)
    assert len(url) != 0
    # _, _, filenames = next(os.walk(path))
    # assert os.path.isfile(os.path.join(cwd,root,filenames[0]))
    
def test_path_collector():
    root = os.path.join("test_download", "google")
    cwd = os.getcwd()
    path = os.path.join(cwd,root)
    if os.path.exists(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path)
    images = search_images(["nature"], 1, root, None, ["google"])
    time.sleep(2)
    path = list(images.values())[0][0]
    print(path)
    assert os.path.isabs(path)