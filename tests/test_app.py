import time
import sys,os
# sys.path.append(os.path.join(os.path.dirname(__file__),os.pardir,"image_finder"))
from img_downloader.img_scraper import search_ddg, search_bing, search_google, search_unsplash

search = "dog"
root = "test_download"
class_name = "test"

# def test_search_unsplash():
#     cwd = os.getcwd()
#     path = os.path.join(cwd,root)
#     for root, dirs, files in os.walk(path, topdown=False):
#         for name in files:
#             os.remove(os.path.join(root, name))
#         for name in dirs:
#             os.rmdir(os.path.join(root, name))
#     search_unsplash(search, 1, root)
#     time.sleep(2)
#     _, _, filenames = next(os.walk(path))
#     assert os.path.isfile(os.path.join(cwd,root,filenames[0]))

def test_search_ddg():
    cwd = os.getcwd()
    path = os.path.join(cwd,root)
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    search_ddg(search, 1, root)
    time.sleep(2)
    _, _, filenames = next(os.walk(path))
    assert os.path.isfile(os.path.join(cwd,root,filenames[0]))
    
def test_search_bing():
    cwd = os.getcwd()
    path = os.path.join(cwd,root)
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    search_bing(search, 1, root)
    time.sleep(2)
    _, _, filenames = next(os.walk(path))
    assert os.path.isfile(os.path.join(cwd,root,filenames[0]))
    
def test_search_google():
    cwd = os.getcwd()
    path = os.path.join(cwd,root)
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    search_google(search, 1, root)
    time.sleep(2)
    _, _, filenames = next(os.walk(path))
    assert os.path.isfile(os.path.join(cwd,root,filenames[0]))