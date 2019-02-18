import os
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import time
import ntpath


def get_title_from_header(header):
    if not os.path.isfile(header):
        return "Photo Album"
    else:
        with open(header) as f:
            title = f.readlines()[1].rstrip()
    return title


def get_start_video(header, dir_path):
    html = '''<!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Copyright (c) 2019 Florent Charpin -->
    <title>_TITLE_</title>
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
            </div>

        <div class="titlealbum">
        '''
    with open(header, 'r') as headerfile:
        html += headerfile.read()

    if os.path.isfile(dir_path + "/../title"):
        with open(dir_path + "/../title") as fe:
            folder_name = fe.read()
        html = html.replace("_FOLDER_", folder_name)
    else:
        html = html.replace("_FOLDER_", "previous")
    html = html.replace("_TITLE_", get_title_from_header(header))
    zzz = os.path.relpath(dir_path + "/..", folder_root)
    html = html.replace("_BACK_", zzz)
    html += "</div><div style=\"text-align: center;\">"
    path_str = os.path.relpath(folder_root, dir_path) + "/"
    return html.replace("_PATH_", path_str)


def get_start(header, dir_path):
    html = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Copyright (c) 2019 Florent Charpin -->
<title>_TITLE_</title>

<script
  src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
<script src="_PATH_js/jquery.fancybox.min.js"></script>
<link rel="stylesheet" type="text/css" href="_PATH_css/jquery.fancybox.css">
<link rel="stylesheet" type="text/css" href="_PATH_css/album.css">
</head>
<body id="myTopnav">

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

<div class="topnav">
                <a href="_PATH_" title="Go Home" class="active"><img class="top" src="_PATH_icon/home.png" /></a>
                <img class="top" src="_PATH_icon/div.png" style="padding-top: 4px;"/>
                <a href="#top" title="Go to top"><img class="top" src="_PATH_icon/chevron-up.png" /></a>
                <a href="#bottom" title="Go to bottom"><img class="top" src="_PATH_icon/chevron-down.png" /></a>
                <img class="top" src="_PATH_icon/div.png" style="padding-top: 4px;"/>
                <a href="../." title=""><img class="top" src="_PATH_icon/chevron-left.png" /><span class="backto">&nbsp;Back to _FOLDER_ albums</span></a>
                <a href="_PATH_info.html" title="Info" style="float:right"><img class="top" src="_PATH_icon/info.png" /></a>
                <a href="_ORDER_INDEX_" class="order" title="Switch order"><img class="top" src="_PATH_icon/order.png" /></a>
                  <i class="fa fa-bars"></i>
        </div>

    <div class="titlealbum">
    '''
    with open(header, 'r') as header_file:
        html += header_file.read()

    html += '''
    </div>
    <div id="top"   class="pig-wrapper">
        <div id="pig"></div>
    </div>
    <script type="text/javascript" src="_PATH_js/pig_fancy.min.js"></script>
    <script type="text/javascript">
        var imageData = [
    '''

    if os.path.isfile(dir_path + "/../title"):
        with open(dir_path + "/../title") as fe:
            folder_name = fe.read()
        html = html.replace("_FOLDER_", folder_name)
    else:
        html = html.replace("_FOLDER_", "previous")
    html = html.replace("_TITLE_", get_title_from_header(header))
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


def get_part3():
    html = '''
];
        var pig = new Pig(imageData, {
            urlForSize: function(filename, size) {
                var pos = filename.lastIndexOf('/')
                return filename.substring(0,pos) + '/img/' + size + filename.substring(pos, filename.length)
            }
        }).enable();
    </script>
    <br />
<div id="bottom">&copy; 2019 Florent Charpin</div>
'''
    return html;


def get_caption(dirpath):
    d = {}
    if not os.path.isfile(dirpath + "/captions"):
        return d
    with open(dirpath + "/captions") as f:
        for line in f:
            (key, val) = line.rstrip().split('|')
            d[key] = val
    return d


def get_album_list(dir_path):
    d = []
    if not os.path.isfile(dir_path + "/albumlist"):
        return d
    with open(dir_path + "/albumlist") as f:
        for line in f:
            key = line.rstrip().split('|')[0]
            d.append(key)
    return d


def get_album_title(dir_path):
    d = {}
    if not os.path.isfile(dir_path + "/albumlist"):
        return d
    with open(dir_path + "/albumlist") as f:
        for line in f:
            key, val = line.rstrip().split('|')
            d[key] = val
    return d


def gen_video(dir_path):
    vl = []
    if not os.path.isfile(dir_path + "/video"):
        return
    with open(dir_path + "/video") as f:
        for line in f:
            vl.append(line.rstrip().split('|'))

    html = get_start_video(dir_path + "/header.html", dir_path);
    for item in vl:
        html += f"<div class=\"pict\"><a data-fancybox href=\"https://{item[2]}\"><img width=\"300px\" class=\"card-img-top img-fluid\" data-caption=\"{item[1]}\" src=\"{item[0]}\"></a >"
        html += f"<span class=\"caption\">{item[1]}</span></div>"
    html += "</div></body></html>"
    existing = ""
    if os.path.isfile(dir_path + "/index.html"):
        with open(dir_path + "/index.html") as fe:
            existing = fe.read()
    if existing != html:
        print(dir_path + '/index.html')
        with open(dir_path + '/index.html', 'w+') as fh:
            fh.write(html)
    pic_count[dir_path] = str(len(vl)) + " videos"
    pic_mov_count[dir_path] = (0, len(vl))
    return


def most_recent_list(img_file, ts, si):
    recent_list.append((os.path.relpath(img_file, folder_root), ts, si))


def gen_index_photos(dir_path, image_list, html, size_images, captions, page_name):
    for filename in image_list:
        if size_images[filename][3] is None:
            date = iso = speed = focal = make = aperture = size = ""
            f_name = filename
        else:
            f_name = filename + " - "
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
        html += f"<a href=\"{filename}\" data-caption=\"{caption}|{f_name}{date}{iso}{focal}{speed}{aperture}{size}{make}\" data-fancybox=\"photo3\" />"
    existing = ""
    html += "\n\n</body></html>"
    if os.path.isfile(dir_path + "/" + page_name):
        with open(dir_path + "/" + page_name) as fe:
            existing = fe.read()

    if existing != html:
        print(dir_path + "/" + page_name)
        with open(dir_path + "/" + page_name, 'w+') as fh:
            fh.write(html)


def main_photos():
    for dir_path, _, file_names in os.walk(folder_root, False):
        if os.path.isfile(dir_path + "/inplace.html"):
            pic_count[dir_path] = "1"
            continue
        if os.path.isfile(dir_path + "/albumlist"):
            continue
        if not os.path.isfile(dir_path + "/header.html"):
            continue
        if os.path.isfile(dir_path + "/video"):
            gen_video(dir_path)
            continue
        captions = get_caption(dir_path)

        m_time = 0
        t_count = {}
        size_images = dict()
        image_list = []
        for path_image in file_names:
            if not path_image.lower().endswith("jpg"):
                if not path_image.lower().endswith("jpeg"):
                    continue
            if path_image == "albumthumb.jpg":
                continue
            image = os.path.abspath(os.path.join(dir_path, path_image))
            with Image.open(image) as img:
                width, height = img.size
                ratio = width / height
                info = img._getexif()
                size_images[path_image] = (width, height, ratio, info)
                image_list.append(path_image)
                t_count[path_image] = os.path.getmtime(image)
            fm_time = os.path.getmtime(dir_path + "/" + path_image)
            most_recent_list(dir_path + "/" + path_image, fm_time, size_images[path_image])
            if fm_time > m_time:
                m_time = fm_time;
        Path(dir_path + "/" + "timestamp").touch()
        os.utime(dir_path + "/" + "timestamp", (m_time, m_time))
        image_list.sort()
        image_list1 = sorted(t_count, key=t_count.__getitem__, reverse=True)
        if os.path.isfile(dir_path + "/reverse_time"):
            image_list, image_list1 = image_list1, image_list
        pic_count[dir_path] = str(len(image_list)) + " pictures"
        pic_mov_count[dir_path] = (len(image_list), 0)
        gen_photo_html(dir_path, image_list, size_images, captions, "index.html", "index1.html")
        gen_photo_html(dir_path, image_list1, size_images, captions, "index1.html", "index.html")
    r_list = []
    size_images = dict()
    html = get_start(folder_root + "/header_recent.html", folder_root)
    for item in sorted(recent_list, key=lambda tup: tup[1], reverse=True)[0:500]:
        r_list.append(item[0])
        size_images[item[0]] = item[2]
    for filename in r_list:
        html += f"{{\"filename\":\"{filename}\",\"aspectRatio\":{size_images[filename][2]}}},"
    html += get_part3()
    gen_index_photos(folder_root, r_list, html, size_images, {}, "recent.html")


def gen_photo_html(dir_path, image_list, size_images, captions, index_name, index_name1):
    html = get_start(dir_path + "/header.html", dir_path)
    html = html.replace("_ORDER_INDEX_", index_name1)
    for filename in image_list:
        html += f"{{\"filename\":\"{filename}\",\"aspectRatio\":{size_images[filename][2]}}},"
    html += get_part2()
    gen_index_photos(dir_path, image_list, html, size_images, captions, index_name)


def get_album_list_name(folder):
    name = ntpath.basename(folder)
    dir_name = os.path.dirname(folder)
    d = get_album_title(dir_name)
    if name in d:
        return d[name]
    return "&nbsp;"


def gen_album_list_index(folder, fcount, tcount, level):
    sm_times = sorted(tcount, key=tcount.__getitem__, reverse=True)
    html = '''<!DOCTYPE html>
<html>
<head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- Copyright (c) 2019 Florent Charpin -->
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
    title = get_album_list_name(folder)
    html = html.replace("_LEVEL_", str(level))
    if title == "&nbsp;":
        html = html.replace("__TITLE__", "Photo Album")
    else:
        html = html.replace("__TITLE__", title)
    html += title + "</div>"

    cell = '''<div class="pict"><a href="_FOLDER_/index.html"><img class="albumthumb" src="_FOLDER_/albumthumb.jpg"><span class="caption">_TITLEALBUM_</span></a><span class="caption2">_COUNT_<br/>Updated _TIME_</span></div>'''

    # for name, val in fcount.items():
    a_title = get_album_title(folder)
    for name in sm_times:
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
    existing = ""
    if os.path.isfile(folder + "/index.html"):
        with open(folder + "/index.html") as fe:
            existing = fe.read()

    if existing != html:
        print(folder + '/index.html')
        with open(folder + '/index.html', 'w+') as fh:
            fh.write(html)
    return


def gen_info_page(folder, pix, mov, album):
    html = '''<!DOCTYPE html>
<html>
<head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=640">
        <!-- Copyright (c) 2019 Florent Charpin -->
        <title>Photo Album</title>
        <link rel="stylesheet" type="text/css" href="./css/albumlist.css">
        <link rel="stylesheet" type="text/css" href="./css/album.css">
        <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
        <style>
        @keyframes spinit {
        from {transform: scale(0) rotate(0deg); filter: grayscale(0%) blur(20px);border-radius: 50%;}
        to {transform: scale(1.0) rotate(360deg);filter: grayscale(100%) blur(0);}
    }

    .self {
        width: 250px;
        border-radius: 50%;
        animation-name: spinit;
        animation-duration: 4s;
        filter: grayscale(100%) blur(0);
    }

    .selfie {
        margin: auto;
        text-align: center;

    }
        </style>
</head>

<body>
 <div class="topnav" id="myTopnav">
<a href="./" title="go Home" class="active"><img class="top"  src="./icon/home.png" /></a>
 <a href="./info.html" style="float:right"><img class="top" src="./icdeon/info.png" /></a>
  <i class="fa fa-bars"></i>
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
                <br /><br />
                <div class="selfie">
                <img class="self" src="img/me.jpg">
      </div>
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
    sub_folders = [f.path for f in os.scandir(folder_root) if f.is_dir()]
    if not os.path.isfile(folder + "/albumlist"):
        if os.path.isfile(folder + "/header.html"):
            if os.path.isfile(folder + "/timestamp"):
                return 1, os.path.getmtime(folder + "/timestamp"), pic_mov_count[folder]
            else:
                return 1, 0, pic_mov_count[folder]
        else:
            return 0, 0, (0, 0)
    sub_folders = get_album_list(folder)
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


if __name__ == "__main__":
    # folder_root = "/home/fc/php/Album2/"
    folder_root = "/home/fc/dev/photo3"
    recent_list = []
    recent_max = 100
    pic_count = {}
    pic_mov_count = {}
    main_photos()
    gen_album_list_page(folder_root, 0, 0)
    print(len(recent_list))

# print("\n\n\n\n" + os.path.relpath("/home/fc/dev/photo3/", "/home/fc/dev/photo3/photo_dir/maui"))

#print(get_start())

# for tag, value in size_images["IMG_4076.jpg"][3].items():
#    print(tag, TAGS.get(tag, tag), value)

# print("========")
# print(info[36867])
# print(size_images["IMG_0111.jpg"][3])

