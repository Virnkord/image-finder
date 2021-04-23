import argparse
from img_downloader.img_scraper import search_google, search_bing, search_ddg, search_unsplash

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
print(search_engines)

for keyword in search_keywords:
    if "unsplash" in search_engines:
        ak = input("Paste your access key here\n")
        search_unsplash(keyword, limit, output_directory, ak, class_directory)
    if "google" in search_engines:
        search_google(keyword, limit, output_directory, class_directory)
    if "bing" in search_engines:
        search_bing(keyword, limit, output_directory, class_directory)
    if "duckduckgo" in search_engines:
        search_ddg(keyword, limit, output_directory, class_directory)
