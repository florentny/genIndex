import os
from PIL import Image


folder_root = "/home/fc/php/Album2/"
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


for dirpath, _, filenames in os.walk(folder_root):
    size_images = dict()
    image_list = []
    if not os.path.isfile(dirpath + "/header.html"):
        continue
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
            # print(path_image,width, heigth, ratio)
    image_list.sort()
    # for filename, d in size_images.items():
    #    print(f"{{\"filename\":\"{filename}\",\"aspectRatio\":{d[2]}}},")
    for filename in image_list:
        # print(f"{{\"filename\":\"{filename}\",\"aspectRatio\":{size_images[filename][2]}}},")
        html += f"{{\"filename\":\"{filename}\",\"aspectRatio\":{size_images[filename][2]}}},"
    html += get_part2()
    for filename in image_list:
        if size_images[filename][3] is None:
            date = iso = ""
        else:
            date = ("Date: " + size_images[filename][3][36867]) if (36867 in size_images[filename][3]) else ""
            iso = (" ISO: " + str(size_images[filename][3][34855])) if (34855 in size_images[filename][3]) else ""
        # print(f"<a href=\"{filename}\" data-caption=\"{filename}<br/>{date}{iso}\" data-fancybox=\"photo3\" />")
        html += f"<a href=\"{filename}\" data-caption=\"{filename}<br/>{date}{iso}\" data-fancybox=\"photo3\" />"
    print(dirpath + '/index.html')
    with open(dirpath + '/index.html', 'w+') as fh:
        fh.write(html)

# print("\n\n\n\n" + os.path.relpath("/home/fc/dev/photo3/", "/home/fc/dev/photo3/photo_dir/maui"))

#print(get_start())

# for tag, value in info.items():
#    print(tag, TAGS.get(tag, tag), value)
#
# print("========")
# print(info[36867])
# print(size_images["IMG_0111.jpg"][3])
