import time
import sys,os
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__),os.pardir,"image_finder"))
from img_downloader.img_scraper import search_ddg, search_bing, search_google, search_unsplash

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
    search_unsplash(search, 1, root, ak)
    time.sleep(2)
    _, _, filenames = next(os.walk(path))
    assert os.path.isfile(os.path.join(cwd,root,filenames[0]))

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
    search_ddg(search, 1, root)
    time.sleep(2)
    _, _, filenames = next(os.walk(path))
    print(filenames)
    print(cwd)
    print(root)
    assert os.path.isfile(os.path.join(cwd,root,filenames[0]))
    
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
    search_bing(search, 1, root)
    time.sleep(2)
    _, _, filenames = next(os.walk(path))
    assert os.path.isfile(os.path.join(cwd,root,filenames[0]))
    
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
    search_google(search, 1, root)
    time.sleep(2)
    _, _, filenames = next(os.walk(path))
    assert os.path.isfile(os.path.join(cwd,root,filenames[0]))