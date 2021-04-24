import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from image_finder.NN.pyimagesearch import config
from image_finder.NN.predict import nn_filter
from tensorflow.keras.models import load_model
import pickle

def search_images(search_keywords, limit, output_directory, class_directory, search_engines):
    from image_finder.img_downloader.img_scraper import search_google, search_bing, search_ddg, search_unsplash
    images = {}
    for keyword in search_keywords:
        images[keyword] = []
        if "unsplash" in search_engines:
            ak = input("Paste your access key here\n")
            images[keyword].extend(search_unsplash(keyword, limit, output_directory, ak, class_directory))
        if "google" in search_engines:
            images[keyword].extend(search_google(keyword, limit, output_directory, class_directory))
        if "bing" in search_engines:
            images[keyword].extend(search_bing(keyword, limit, output_directory, class_directory))
        if "duckduckgo" in search_engines:
            images[keyword].extend(search_ddg(keyword, limit, output_directory, class_directory))
    return images

def filter_images(images):
    model_path = os.path.abspath(os.path.join("image_finder", "NN", config.MODEL_PATH))
    lb_path = os.path.abspath(os.path.join("image_finder", "NN", config.LB_PATH))
    model = load_model(model_path)
    lb = pickle.loads(open(lb_path, "rb").read())
    for keyword, imagePaths in images.items():
        nn_filter(imagePaths, model, lb, keyword)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keywords',
                        help='delimited list input', type=str, required=True)
    parser.add_argument('-o', '--output_directory', help='download images in a specific main directory', type=str,
                        required=False)
    parser.add_argument('-c', '--class_directory', help='download images in a specific sub-directory', action='store_true',
                        required=False)
    parser.add_argument('-l', '--limit', help='number', type=int, required=False)
    parser.add_argument('-e', '--engine', help='delimited list input', type=str, required=False)

    args = parser.parse_args()
    arguments = vars(args)
    search_keywords = [str(item) for item in arguments['keywords'].split(',')]
    limit = arguments['limit']
    available_engines = ["unsplash", "google", "bing", "duckduckgo", "all"]
    if arguments['engine']:
        if arguments['engine'] == "all":
            search_engines = available_engines
            search_engines.remove("all")
        else:
            search_engines = [str(item) for item in arguments['engine'].split(',')]
            for engine in search_engines:
                if engine not in available_engines:
                    print("[ERROR]Unsupported search engine\nAvailable search engines: " +
                        (', '.join(available_engines)))
    else:
        search_engines = ["unsplash"]

    if arguments['output_directory']:
        output_directory = arguments['output_directory']
    else:
        output_directory = "downloads"

    class_directory = True if arguments['class_directory'] else None
    images = search_images(search_keywords, limit, output_directory, class_directory, search_engines)
    filter_images(images)