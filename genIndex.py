import os
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import time
import ntpath

#folder_root = "/home/fc/php/Album2/"
folder_root = "/home/fc/dev/photo3"
size_images = dict()
image_list = []


def get_start_video(header, dir_path):
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Photo Album</title>
    <script
      src="https://code.jquery.com/jquery-3.3.1.min.js"
      integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
      crossorigin="anonymous"></script>
    <script src="_PATH_js/jquery.fancybox.min.js"></script>
    <link rel="stylesheet" type="text/css" href="_PATH_css/jquery.fancybox.css">
    <link rel="stylesheet" type="text/css" href="_PATH_css/album.css">
    
    <style type="text/css">
    .pict {
        vertical-align: top;
        display: inline-block;
        text-align: center;
        padding-right: 30px;
        padding-left: 30px;
        padding-top: 25px;
        padding-bottom: px;
    }
    span.caption {
        display: block;
        font-size: 14pt; 
        text-decoration: none; 
        color: #0D0EBF;
        font-weight: bold;
        width: 250px;
    }
    </style>

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
                    <a href="_PATH_" title="go Home" class="active"><img class="top" src="_PATH_icon/home.png" /></a>
                    <img class="top" src="_PATH_icon/div.png" style="padding-top: 4px;"/>
                    <a href="#top" title="go to top"><img class="top" src="_PATH_icon/chevron-up.png" /></a>
                    <a href="#bottom" title="go to bottom"><img class="top" src="_PATH_icon/chevron-down.png" /></a>
                    <img class="top" src="_PATH_icon/div.png" style="padding-top: 4px;"/>
                    <a href="../." title=""><img class="top" src="_PATH_icon/chevron-left.png" /><span class="backto">&nbsp;Back to _FOLDER_ albums</span></a>
                    <a href="_PATH_info.html" style="float:right"><img class="top" src="_PATH_icon/info.png" /></a>
                      <i class="fa fa-bars"></i>
                    </a>
            </div>

        <div class="titlealbum">
        '''
    with open(header, 'r') as headerfile:
        html += headerfile.read()

    if os.path.isfile(dirpath + "/../title"):
        with open(dirpath + "/../title") as fe:
            folder_name = fe.read()
        html = html.replace("_FOLDER_", folder_name)
    else:
        html = html.replace("_FOLDER_", "previous")

    zzz = os.path.relpath(dir_path + "/..", folder_root)
    html = html.replace("_BACK_", zzz)
    html += "</div><div style=\"text-align: center;\">"
    path_str = os.path.relpath(folder_root, dir_path) + "/"
    return html.replace("_PATH_", path_str)


def get_start(header, dir_path):
    html = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Photo Album</title>

<script
  src="https://code.jquery.com/jquery-3.3.1.min.js"
  integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
  crossorigin="anonymous"></script>
<script src="_PATH_js/jquery.fancybox.min.js"></script>
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
                <a href="_PATH_" title="go Home" class="active"><img class="top" src="_PATH_icon/home.png" /></a>
                <img class="top" src="_PATH_icon/div.png" style="padding-top: 4px;"/>
                <a href="#top" title="go to top"><img class="top" src="_PATH_icon/chevron-up.png" /></a>
                <a href="#bottom" title="go to bottom"><img class="top" src="_PATH_icon/chevron-down.png" /></a>
                <img class="top" src="_PATH_icon/div.png" style="padding-top: 4px;"/>
                <a href="../." title=""><img class="top" src="_PATH_icon/chevron-left.png" /><span class="backto">&nbsp;Back to _FOLDER_ albums</span></a>
                <a href="_PATH_info.html" style="float:right"><img class="top" src="_PATH_icon/info.png" /></a>
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
    <script type="text/javascript" src="_PATH_js/pig_fancy.min.js"></script>
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
            (key, val) = line.rstrip().split('|')
            d[key] = val
    return d


def getalbumlist(dirpath):
    d = []
    if not os.path.isfile(dirpath + "/albumlist"):
        return d
    with open(dirpath + "/albumlist") as f:
        for line in f:
            key = line.rstrip().split('|')[0]
            d.append(key)
    return d


def getalbumtitle(dirpath):
    d = {}
    if not os.path.isfile(dirpath + "/albumlist"):
        return d
    with open(dirpath + "/albumlist") as f:
        for line in f:
            key, val = line.rstrip().split('|')
            d[key] = val
    return d


def gen_video(dirpath):
    l = []
    if not os.path.isfile(dirpath + "/video"):
        return
    with open(dirpath + "/video") as f:
        for line in f:
            l.append(line.rstrip().split('|'))

    html = get_start_video(dirpath + "/header.html", dirpath);
    for item in l:
        html += f"<div class=\"pict\"><a data-fancybox href=\"https://{item[2]}\"><img width=\"300px\" class=\"card-img-top img-fluid\" data-caption=\"{item[1]}\" src=\"{item[0]}\"></a >"
        html += f"<span class=\"caption\">{item[1]}</span></div>"
    html += "</div></body></html>"
    existing = ""
    if os.path.isfile(dirpath + "/index.html"):
        with open(dirpath + "/index.html") as fe:
            existing = fe.read()
    if existing != html:
        print(dirpath + '/index.html')
        with open(dirpath + '/index.html', 'w+') as fh:
            fh.write(html)
    pic_count[dirpath] = str(len(l)) + " videos"
    pic_mov_count[dirpath] = (0, len(l))
    return


pic_count = {}
pic_mov_count = {}
for dirpath, _, filenames in os.walk(folder_root, False):
    size_images = dict()
    image_list = []
    if os.path.isfile(dirpath + "/inplace.html"):
        pic_count[dirpath] = "1"
        continue
    if os.path.isfile(dirpath + "/albumlist"):
        continue
    if not os.path.isfile(dirpath + "/header.html"):
        continue
    if os.path.isfile(dirpath + "/video"):
        gen_video(dirpath)
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
    pic_count[dirpath] = str(len(image_list)) + " pictures"
    pic_mov_count[dirpath] = (len(image_list), 0)
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
                round(size_images[filename][3][33437][0] / size_images[filename][3][33437][1], 1)) + " - ") if (
                    33437 in size_images[filename][3]) else ""
            size = f"{size_images[filename][0]}x{size_images[filename][1]} - "
        caption = "" if captions.get(filename) is None else captions.get(filename)
        html += f"<a href=\"{filename}\" data-caption=\"{caption}|{filename} - {date}{iso}{focal}{speed}{aperture}{size}{make}\" data-fancybox=\"photo3\" />"
    existing = ""
    html += "\n\n</body></html>"
    if os.path.isfile(dirpath + "/index.html"):
        with open(dirpath + "/index.html") as fe:
            existing = fe.read()

    if existing != html:
        print(dirpath + '/index.html')
        with open(dirpath + '/index.html', 'w+') as fh:
            fh.write(html)


subfolders = [f.path for f in os.scandir(folder_root) if f.is_dir()]


def get_albumlist_name(folder):
    name = ntpath.basename(folder)
    dir = os.path.dirname(folder)
    d = getalbumtitle(dir)
    if name in d:
        return d[name]
    return "&nbsp;"


def gen_album_list_index(folder, fcount, tcount, level):
    smtimes = sorted(tcount, key=tcount.__getitem__, reverse=True)
    html = '''
<html>
<head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>__TITLE__</title>
        <link rel="stylesheet" type="text/css" href="_PATH_css/albumlist.css">
        <link rel="stylesheet" type="text/css" href="_PATH_css/album.css">
        <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
</head>

<body>
 <div class="topnav" id="myTopnav">
<a href="_PATH_" title="go Home" class="active"><img class="top" src="_PATH_icon/home.png" /></a>
 <img class="top topback" src="_PATH_icon/div.png" style="padding-top: 4px;"/>
<a href="../." title="" class="topback"><img class="top"src="_PATH_icon/chevron-left.png" />
 <span style="vertical-align:top"></span></a>
 <a href="_PATH_info.html" style="float:right"><img class="top" src="_PATH_icon/info.png" /></a>
  <i class="fa fa-bars"></i>
 </a>
</div>
<script type="text/javascript">
    var banner_link = "_PATH_banner.html";
    var level = _LEVEL_;
</script>
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
<div id="banner"></div>

<div id="title2">
'''
    title = get_albumlist_name(folder)
    html = html.replace("_LEVEL_", str(level))
    if title == "&nbsp;":
        html = html.replace("__TITLE__", "Photo Album")
    else:
        html = html.replace("__TITLE__", title)
    html += title + "</div>"

    cell = '''<div class="pict"><a href="_FOLDER_/index.html"><img src="_FOLDER_/albumthumb.jpg" width="250px"><span class="caption">_TITLEALBUM_</span></a><span class="caption2">_COUNT_<br/>Updated _TIME_</span></div>'''

    # for name, val in fcount.items():
    a_title = getalbumtitle(folder)
    for name in smtimes:
        val = fcount[name]
        if val == 1:
            if (folder + "/" + name) in pic_count:
                c = pic_count[folder + "/" + name]
            else:
                c = ""
        else:
            c = str(val) + " albums"
        path_str = os.path.relpath(folder_root, folder) + "/"
        html = html.replace("_PATH_", path_str)
        html += cell.replace("_FOLDER_", name).replace("_TITLEALBUM_", a_title[name]).replace("_COUNT_", c).replace("_TIME_", time.strftime("%b %e %Y", time.gmtime(tcount[name])))
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


def gen_info_page(folder, pix, mov, album):
    html =    '''<html>
<head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=640">
        <title>Photo Album</title>
        <link rel="stylesheet" type="text/css" href="./css/albumlist.css">
        <link rel="stylesheet" type="text/css" href="./css/album.css">
        <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
</head>

<body>
 <div class="topnav" id="myTopnav">
<a href="./" title="go Home" class="active"><img class="top"  src="./icon/home.png" /></a>
 <a href="./info.html" style="float:right"><img class="top" src="./icdeon/info.png" /></a>
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
<body>

        <div id="content">
                <br /><br />
                Number of Albums: __ALBUM__<br />Number of Photos: __PIX__<br />Number of Movies: __MOV__<br /><br /><br />
                 All pictures on this site are &#169; Florent Charpin. All rights reserved.
                 <br />
                 Web Software &#169; 2019 Florent Charpin
                <br /><br />
<div>For any info or questions please email &#119;&#119;&#119;&#064;&#099;&#104;&#097;&#114;&#112;&#105;&#110;&#046;&#110;&#101;&#116;</div>

             </div>

</body></html>
'''
    html = html.replace("__PIX__", str(pix)).replace("__MOV__", str(mov)).replace("__ALBUM__", str(album))
    existing = ""
    if os.path.isfile(folder + "/info.html"):
        with open(folder + "/info.html") as fe:
            existing = fe.read()

    if existing != html:
        print(folder + '/info.html')
        with open(folder + '/info.html', 'w+') as fh:
            fh.write(html)


def gen_album_list_page(folder, count, level):
    pix_count = 0
    mov_count = 0
    if not os.path.isfile(folder + "/albumlist"):
        if os.path.isfile(folder + "/header.html"):
            if os.path.isfile(folder + "/timestamp"):
                return 1, os.path.getmtime(folder + "/timestamp"), pic_mov_count[folder]
            else:
                return 1, 0, pic_mov_count[folder]
        else:
            return 0, 0, (0, 0)
    sub_folders = getalbumlist(folder)
    if len(sub_folders) == 0:
        return 0, 0, (0, 0)
    fcount = {}
    tcount = {}
    timestamp = 0
    for name in sub_folders:
            num, ts, pixmov = gen_album_list_page(folder + "/" + name, 0, level+1)
            fcount[name] = num
            tcount[name] = ts
            count += num
            if ts > timestamp:
                timestamp = ts
            pix_count += pixmov[0]
            mov_count += pixmov[1]
    gen_album_list_index(folder, fcount, tcount, level)
    gen_info_page(folder, pix_count, mov_count, count)
    # print("folder: " + folder + " albums: " + str(count) + " pix: " + str(pix_count) + " video: " + str(mov_count))
    return count, timestamp, (pix_count, mov_count);


gen_album_list_page(folder_root, 0, 0)

# print("\n\n\n\n" + os.path.relpath("/home/fc/dev/photo3/", "/home/fc/dev/photo3/photo_dir/maui"))

#print(get_start())

# for tag, value in size_images["IMG_4076.jpg"][3].items():
#    print(tag, TAGS.get(tag, tag), value)

# print("========")
# print(info[36867])
# print(size_images["IMG_0111.jpg"][3])

