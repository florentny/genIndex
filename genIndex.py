import os
import sys
# sys.path.append("/home/florent/scuba.florent.us/bin")
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path

folder_root = "/run/media/fc/spare/photo"
# folder_root = "/home/fc/dev/photo3"
size_images = dict()
image_list = []


def get_start(header, dir_path):
    html = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=640">
<title>Photo Album</title>
<style type="text/css">
    body {
	 padding-top: 0.5rem;
         padding-right: 2rem;
         padding-left: 2rem;
         padding-bottom: 2rem;
    }

    .pig-wrapper {
        position: relative;
        margin-top: 20px;
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<script
  src="https://code.jquery.com/jquery-3.3.1.min.js"
  integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
  crossorigin="anonymous"></script>
<script src="_PATH_js/jquery.fancybox.js"></script>
<link rel="stylesheet" type="text/css" href="_PATH_css/jquery.fancybox.css">
<link rel="stylesheet" type="text/css" href="_PATH_css/album.css">
</head>
<body>

<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-3281928-2']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>


    <div class="titlealbum">
    '''
    with open(header, 'r') as headerfile:
        html += headerfile.read()

    html += '''
    </div>
    <div id="top"   class="pig-wrapper">
        <div id="pig"></div>
    </div>
    <script type="text/javascript" src="_PATH_js/pig_fancy.js"></script>
    <script type="text/javascript">
        var imageData = [
    '''


    if os.path.isfile(dirpath + "/../title"):
        with open(dirpath + "/../title") as fe:
            folder_name = fe.read()
        html = html.replace("_FOLDER_", folder_name)
    else:
        html = html.replace("_FOLDER_", "previous")

    zzz = os.path.relpath(dir_path + "/..", folder_root)
    html = html.replace("_BACK_", zzz)
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
    <br />
<div id="bottom">&copy; 2019 Florent Charpin</div>
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


def getlocation(dirpath):
    d = {}
    if not os.path.isfile(dirpath + "/locations"):
        return d
    with open(dirpath + "/locations") as f:
        for line in f:
            (key, val) = line.split('|')
            d[key] = val
    return d



dirpath = folder_root
pix_order = []
nlist = os.listdir(folder_root)
captions = getcaption(dirpath)
locations = getlocation(dirpath)
html = get_start(dirpath + "/header.html", dirpath);
mtime = 0
for path_image in nlist:
    if not path_image.lower().endswith("jpg"):
        if not path_image.lower().endswith("jpeg"):
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
    fmtime = os.path.getmtime(dirpath + "/" + path_image)
    if fmtime > mtime:
        mtime = fmtime;
Path(dirpath + "/" + "timestamp").touch()
os.utime(dirpath + "/" + "timestamp", (mtime, mtime))
# image_list.sort()
for filename in image_list:
    html += "{{\"filename\":\"{}\",\"aspectRatio\":{}}},".format(filename, size_images[filename][2])
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
        size = "{}x{} - ".format(size_images[filename][0],size_images[filename][1])
    caption = "" if captions.get(filename) is None else captions.get(filename)
    location = "" if locations.get(filename) is None else locations.get(filename)
    # html += "<a href=\"{}\" data-caption=\"{}|{}{}{}{}{}{}{}\" data-fancybox=\"photo3\" />".format(filename, caption, date, iso, focal, speed, aperture, size, make)
    html += "<a href=\"{}\" data-caption=\"{}|{}\" data-fancybox=\"photo3\" />".format(filename, location, caption)
existing = ""
html += "</body></html>"
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
