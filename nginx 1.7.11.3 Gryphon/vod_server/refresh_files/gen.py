#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import json
import os
import config

FILE_JSON = config.CONFIGS['FILE_JSON']

FILE_CONFIG = config.CONFIGS['FILE_CONFIG']

FILE_FFMPEG = config.CONFIGS['FILE_FFMPEG']

FILE_NGINX_CONFIG = config.CONFIGS['FILE_NGINX_CONFIG']

md5 = hashlib.md5()


def read_folder_config(file_config):
    folders = []
    with open(file_config, encoding="utf-8") as f:
        for line in f:
            line = line.strip().replace('\n', '')
            if len(line) > 0:
                folders.append(line)
    return folders


def create_ffmpeg_img(video_file, img_path, size=(300, 200)):
    """
    生成FFmpeg预览图片
    :param video_file:
    :param img_root:
    :param size:
    :return:
    """
    size_str = 'x'.join(str(x) for x in size)

    parent_path = os.path.dirname(img_path)
    if not os.path.isdir(parent_path):
        os.mkdir(parent_path)
    video_file = os.path.abspath(video_file)
    img_path = os.path.abspath(img_path)

    if not os.path.isfile(img_path):
        cwd = os.getcwd()
        dirname = os.path.dirname(FILE_FFMPEG)
        dir_valid = len(dirname) > 0
        ffmpeg = FILE_FFMPEG
        if dir_valid:
            os.chdir(dirname)
            ffmpeg = os.path.basename(FILE_FFMPEG)
        cmd = ffmpeg + " -itsoffset -1 -i \"{}\" -vcodec mjpeg -vframes 1 -an -f rawvideo -s {} \"{}\"".format(
            video_file, size_str, img_path)
        os.system(cmd)
        if dir_valid:
            os.chdir(cwd)


def walk_files_by_suffix(folder, suffixs):
    # folder F:/其他/影音
    relativeFiles = []
    for rt, dirs, files in os.walk(folder):
        for f in files:
            fname = os.path.splitext(f)
            if len(fname) < 2:
                break
            suffix = fname[1].lower().replace('.', '')
            if suffix in suffixs:
                # F:/其他/影音\釜山行.HD1280高清韩语中字.mp4 mp4
                # print(os.path.join(rt, f), suffix)

                # 釜山行.HD1280高清韩语中字.mp4
                # print(f.replace(folder, ''))

                # F: / 其他 / 影音
                # print(os.path.commonprefix([folder, rt]))
                rpath = rt.replace(folder, '')
                if len(rpath) > 0 and rpath[0] == os.path.sep:
                    rpath = rpath[1:]

                absolute_file = os.path.join(rt, f)
                uid = str(md5.hexdigest())

                img_file = uid + '.png'
                img_path = os.path.join("images", img_file)

                create_ffmpeg_img(absolute_file, img_path)

                md5.update(absolute_file.encode("utf-8"))

                data = {
                    'uid': uid,
                    'path': os.path.join(rpath, f),
                    'name': fname[0],
                    'suffix': suffix,
                    'ctime': int(os.stat(absolute_file).st_ctime) * 1000,
                    'thumb_path': img_path
                }
                relativeFiles.append(data)

    return relativeFiles


def handle(suffixs, file_config=FILE_CONFIG, file_json=FILE_JSON):
    folders = read_folder_config(file_config)
    data = []
    size = 0
    for folder in folders:
        files = walk_files_by_suffix(folder, suffixs)
        size += len(files)
        if len(files) > 0:
            md5.update(folder.encode("utf-8"))
            data.append(
                {'folder': folder, 'name': os.path.basename(folder), 'files': files,
                 'uid': str(md5.hexdigest())})
    write_json(data, file_json)
    print("files total count:%d" % size)
    return data


def write_json(data, file_json=FILE_JSON):
    rs_json = json.dumps(data, indent=4, separators=(',', ':'), )
    f = open(file_json, 'w')
    f.write(rs_json)


def generate_nginx_conf(datas, file_nginx_config=FILE_NGINX_CONFIG):
    f = open(file_nginx_config, 'w', encoding="utf-8")
    f.write('#generated file,do not edit\n')
    for data in datas:
        f_str = '''
        location /{} {{
        alias {};
        }}'''
        f.write(f_str.format(data['uid'], data['folder']))


def main():
    data = handle(["mp4"])
    generate_nginx_conf(data)


if __name__ == "__main__":
    main()
