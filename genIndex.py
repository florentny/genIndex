import os
from PIL import Image
from PIL.ExifTags import TAGS

folder_root = "/home/fc/php/Album2/"
#folder_root = "/home/fc/dev/photo3"
size_images = dict()
image_list = []


def get_start(header, dir_path):
    html = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>Photo Album</title>
<style type="text/css">
    body {
         padding: 2rem;
    }

    .pig-wrapper {
        position: relative;
        margin-top: 20px;
    }
</style>
<script type="text/javascript" src="_PATH_js/jquery-3.1.1.min.js"></script>
<script src="_PATH_js/jquery.fancybox.js"></script>
<link rel="stylesheet" type="text/css" href="_PATH_css/jquery.fancybox.css">
<link rel="stylesheet" type="text/css" href="_PATH_css/album.css">
</head>
<body>
    <div class="titlealbum">
    '''
    with open(header, 'r') as headerfile:
        html += headerfile.read()

    html += '''
    </div>
    <div class="pig-wrapper">
        <div id="pig"></div>
    </div>
    <script type="text/javascript" src="_PATH_js/pig_fancy.js"></script>
    <script type="text/javascript">
        var imageData = [
    '''
    path_str = os.path.relpath(folder_root, dir_path) + "/"
    return html.replace("_PATH_", path_str)


def get_part2():
    html = '''
];
        var pig = new Pig(imageData, {
            urlForSize: function(filename, size) {
                return 'img/' + size + '/' + filename;
            }
        }).enable();
    </script>
'''
    return html;


def getcaption(dirpath):
    d = {}
    if not os.path.isfile(dirpath + "/captions"):
        return d
    with open(dirpath + "/captions") as f:
        for line in f:
            (key, val) = line.split('|')
            d[key] = val
    return d


for dirpath, _, filenames in os.walk(folder_root):
    size_images = dict()
    image_list = []
    if not os.path.isfile(dirpath + "/header.html"):
        continue
    if os.path.isfile(dirpath + "/inplace.html"):
        continue
    captions = getcaption(dirpath)
    html = get_start(dirpath + "/header.html", dirpath);
    for path_image in filenames:
        if not path_image.lower().endswith("jpg"):
            continue
        if path_image == "albumthumb.jpg":
            continue
        image = os.path.abspath(os.path.join(dirpath, path_image))
        with Image.open(image) as img:
            width, height = img.size
            ratio = width / height
            info = img._getexif()
            size_images[path_image] = (width, height, ratio, info)
            image_list.append(path_image)
    image_list.sort()
    for filename in image_list:
        html += f"{{\"filename\":\"{filename}\",\"aspectRatio\":{size_images[filename][2]}}},"
    html += get_part2()
    for filename in image_list:
        date = iso = speed = focal = make = aperture = ""
        if size_images[filename][3] is None:
            date = iso = speed = focal = make = ""
        else:
            make = (size_images[filename][3][272]) if (272 in size_images[filename][3]) else ""
            date = (size_images[filename][3][36867] + " - ") if (36867 in size_images[filename][3]) else ""
            iso = (" iso " + str(size_images[filename][3][34855]) + " - ") if (34855 in size_images[filename][3]) else ""
            focal = (" focal: " + str(size_images[filename][3][37386][0]/size_images[filename][3][37386][1]) + "mm - ") if (37386 in size_images[filename][3]) else ""
            speed = (" speed: " + str(size_images[filename][3][33434][0]) + "/" + str(size_images[filename][3][33434][1]) + " - ") if (33434 in size_images[filename][3]) else ""
            aperture = (" f/" + str(
                round(size_images[filename][3][33437][0] / size_images[filename][3][33437][1], 1)) + "mm - ") if (
                    33437 in size_images[filename][3]) else ""
        caption = "" if captions.get(filename) is None else captions.get(filename)
        html += f"<a href=\"{filename}\" data-caption=\"{caption}|{date}{iso}{focal}{speed}{aperture}{make}\" data-fancybox=\"photo3\" />"
    existing = ""
    if os.path.isfile(dirpath + "/index.html"):
        with open(dirpath + "/index.html") as fe:
            existing = fe.read()

    if existing != html:
        print(dirpath + '/index.html')
        with open(dirpath + '/index.html', 'w+') as fh:
            fh.write(html)

# print("\n\n\n\n" + os.path.relpath("/home/fc/dev/photo3/", "/home/fc/dev/photo3/photo_dir/maui"))

#print(get_start())

# for tag, value in size_images["IMG_4076.jpg"][3].items():
#    print(tag, TAGS.get(tag, tag), value)

# print("========")
# print(info[36867])
# print(size_images["IMG_0111.jpg"][3])
