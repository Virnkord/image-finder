from image_finder.image_finder import *
# images = search_images(["boat", "car", "glasses", "horse","cat","dog", "sculpture", "fish"], 3, "downloads", True, ["bing"])
images = search_images(["sculpture", "dog"], 2, "downloads", True,
                       ["unsplash", "google", "bing", "duckduckgo"])
filter_images(images)


# import pickle
# lb = pickle.loads(open(r"D:\\Development\\oidv6\\lb-20210515.pickle", 'rb').read())
# print(lb.classes_)
