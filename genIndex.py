import os
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import time
import ntpath

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
<meta name="viewport" content="width=640">
<title>Photo Album</title>

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

<div class="topnav" id="myTopnav">
                <a href="_PATH_" title="go Home" class="active"><img src="_PATH_icon/home.png" /></a>
                <a>|</a>
                <a href="#top" title="go to top"><img src="_PATH_icon/chevron-up.png" /></a>
                <a href="#bottom" title="go to bottom"><img src="_PATH_icon/chevron-down.png" /></a>
                <a>|</a>
                <a href="_PATH_index.php?nav=_BACK_" title=""><img src="_PATH_icon/chevron-left.png" /><span style="vertical-align:top">&nbsp;Back to _FOLDER_ albums</span></a>
                <a>|</a>
                <a href="_PATH_info.php"><img src="_PATH_icon/info.png" /></a>
                <a href="javascript:void(0);" class="icon" onclick="myFunction()">
                  <i class="fa fa-bars"></i>
                </a>
        </div>

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

    zzz = os.path.relpath(dir_path + "/..", folder_root + "/photo_dir")
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


def getalbumlist(dirpath):
    d = []
    if not os.path.isfile(dirpath + "/albumlist"):
        return d
    with open(dirpath + "/albumlist") as f:
        for line in f:
            key = line.split('|')[0]
            d.append(key)
    return d


def getalbumtitle(dirpath):
    d = {}
    if not os.path.isfile(dirpath + "/albumlist"):
        return d
    with open(dirpath + "/albumlist") as f:
        for line in f:
            key, val = line.split('|')
            d[key] = val
    return d


pic_count = {}
for dirpath, _, filenames in os.walk(folder_root, False):
    size_images = dict()
    image_list = []
    if os.path.isfile(dirpath + "/inplace.html"):
        pic_count[dirpath] = "1"
        continue
    if os.path.isfile(dirpath + "/albumlist"):
        # print(dirpath + "/albumlist")
        continue
    if not os.path.isfile(dirpath + "/header.html"):
        continue
    captions = getcaption(dirpath)
    html = get_start(dirpath + "/header.html", dirpath);
    mtime = 0
    for path_image in filenames:
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
    image_list.sort()
    # print(dirpath + ": " + str(len(image_list)))
    pic_count[dirpath] = str(len(image_list))
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
            size = f"{size_images[filename][0]}x{size_images[filename][1]} - "
        caption = "" if captions.get(filename) is None else captions.get(filename)
        html += f"<a href=\"{filename}\" data-caption=\"{caption}|{date}{iso}{focal}{speed}{aperture}{size}{make}\" data-fancybox=\"photo3\" />"
    existing = ""
    html += "</body></html>"
    if os.path.isfile(dirpath + "/index.html"):
        with open(dirpath + "/index.html") as fe:
            existing = fe.read()

    if existing != html:
        print(dirpath + '/index.html')
        with open(dirpath + '/index.html', 'w+') as fh:
            fh.write(html)


subfolders = [f.path for f in os.scandir(folder_root + "photo_dir") if f.is_dir()]
# print(subfolders);


def get_albumlist_name(folder):
    name = ntpath.basename(folder)
    dir = os.path.dirname(folder)
    d = getalbumtitle(dir)
    if name in d:
        return d[name]
    return "&nbsp;"


def gen_album_list_index(folder, fcount, tcount):
    smtimes = sorted(tcount, key=tcount.__getitem__, reverse=True)
    html = '''
<html>
<head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=700">
        <title>__TITLE__</title>
        <link rel="stylesheet" type="text/css" href="_PATH_css/albumlist.css">
        <link rel="stylesheet" type="text/css" href="_PATH_css/album.css">
        <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
</head>

<body>
 <div class="topnav" id="myTopnav">
<a href="_PATH_" title="go Home" class="active"><img src="_PATH_icon/home.png" /></a>
 <a>|</a>
<a href="../." title=""><img src="_PATH_icon/chevron-left.png" />
 <span style="vertical-align:top"></span></a>
 <a>|</a>
 <a href="_PATH_info.html"><img src="_PATH_icon/info.png" /></a>
 <a href="javascript:void(0);" class="icon" onclick="myFunction()">
  <i class="fa fa-bars"></i>
 </a>
</div>
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

<script src="_PATH_js/showhide.js"></script>
<object class="included" name="foo" type="text/html" data="_PATH_banner.html"></object>

<div id="title2">
'''
    title = get_albumlist_name(folder)
    if title == "&nbsp;":
        html = html.replace("__TITLE__", "Photo Album")
    else:
        html = html.replace("__TITLE__", title)
    html += title + "</div><div id=\"title3\">"
    if title == "Scuba Diving\n":
        html += "&nbsp;</div>"
    else:
        html += title + "</div>"

    cell = '''<div class="pict"><a href="_FOLDER_/index.html"><img src="_FOLDER_/albumthumb.jpg" width="250px"><span class="caption">_TITLEALBUM_</span></a><span class="caption2">_COUNT_<br/>Updated _TIME_</span></div>'''

    # for name, val in fcount.items():
    a_title = getalbumtitle(folder)
    for name in smtimes:
        val = fcount[name]
        if val == 1:
            if (folder + "/" + name) in pic_count:
                c = pic_count[folder + "/" + name] + " Picures"
            else:
                c = "0 Picures"
        else:
            c = str(val) + " Albums"
        path_str = os.path.relpath(folder_root + "photo_dir/", folder) + "/"
        html = html.replace("_PATH_", path_str)
        html += cell.replace("_FOLDER_", name).replace("_TITLEALBUM_", a_title[name]).replace("_COUNT_", c).replace("_TIME_", time.strftime("%b %e %Y", time.gmtime(tcount[name])))
        #print(time.strftime("%b %e %Y", time.gmtime(tcount[name])))
    html += "</body></html>"
    # print(folder + '/index.html')

    if os.path.isfile(folder + "/index.html"):
        with open(folder + "/index.html") as fe:
            existing = fe.read()

    if existing != html:
        print(folder + '/index.html')
        with open(folder + '/index.html', 'w+') as fh:
            fh.write(html)

    return


def gen_album_list_page(folder, count):
    if not os.path.isfile(folder + "/albumlist"):
        if os.path.isfile(folder + "/header.html"):
            if os.path.isfile(folder + "/timestamp"):
                return 1, os.path.getmtime(folder + "/timestamp")
            else:
                return 1, 0
        else:
            return 0, 0
    sub_folders = getalbumlist(folder)
    if len(sub_folders) == 0:
        return 0, 0
    fcount = {}
    tcount = {}
    timestamp = 0
    for name in sub_folders:
            num, ts = gen_album_list_page(folder + "/" + name, 0)
            fcount[name] = num
            tcount[name] = ts
            count += num
            if ts > timestamp:
                timestamp = ts
    gen_album_list_index(folder, fcount, tcount)
    # print(folder + " total sub: " + str(count))
    return count, timestamp;





print("\n\n\n")
gen_album_list_page(folder_root + "photo_dir", 0)

# print("\n\n\n\n" + os.path.relpath("/home/fc/dev/photo3/", "/home/fc/dev/photo3/photo_dir/maui"))

#print(get_start())

# for tag, value in size_images["IMG_4076.jpg"][3].items():
#    print(tag, TAGS.get(tag, tag), value)

# print("========")
# print(info[36867])
# print(size_images["IMG_0111.jpg"][3])

