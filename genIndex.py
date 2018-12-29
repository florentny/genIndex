import os
from PIL import Image


folder_images = "/home/fc/dev/photo3/"
size_images = dict()
image_list = []

for dirpath, _, filenames in os.walk(folder_images):
    if not os.path.isfile(dirpath + "header.html"):
        continue
    for path_image in filenames:
        if not path_image.lower().endswith("jpg"):
            continue
        # print(path_image)
        image = os.path.abspath(os.path.join(dirpath, path_image))
        with Image.open(image) as img:
            width, heigth = img.size
            ratio = width/heigth
            info = img._getexif()
            size_images[path_image] = (width, heigth, ratio, info)
            image_list.append(path_image)
            print(path_image,width, heigth, ratio)
    image_list.sort()
    # for filename, d in size_images.items():
    #    print(f"{{\"filename\":\"{filename}\",\"aspectRatio\":{d[2]}}},")
    for filename in image_list:
        print(f"{{\"filename\":\"{filename}\",\"aspectRatio\":{size_images[filename][2]}}},")
    for filename in image_list:
        date = ("Date: " + size_images[filename][3][36867]) if (36867 in size_images[filename][3]) else ""
        iso = (" ISO: " + str(size_images[filename][3][34855])) if (34855 in size_images[filename][3]) else ""
        print(f"<a href=\"{filename}\" data-caption=\"{filename}<br/>{date}{iso}\" data-fancybox=\"photo3\" />")




# for tag, value in info.items():
#    print(tag, TAGS.get(tag, tag), value)
#
# print("========")
# print(info[36867])
# print(size_images["IMG_0111.jpg"][3])
