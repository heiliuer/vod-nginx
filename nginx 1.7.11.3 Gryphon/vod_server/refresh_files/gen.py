#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import json
import os
import re
import subprocess

import config

FILE_JSON = config.CONFIGS['FILE_JSON']

FILE_CONFIG = config.CONFIGS['FILE_CONFIG']

FILE_FFMPEG = config.CONFIGS['FILE_FFMPEG']

FILE_NGINX_CONFIG = config.CONFIGS['FILE_NGINX_CONFIG']

FILE_PATH_IMAGES = config.CONFIGS['FILE_PATH_IMAGES']


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
        cmd = ffmpeg + " -itsoffset -1 -i \"{}\" -vcodec mjpeg -vframes 10 -an -f rawvideo -s {} \"{}\" > nul".format(
            video_file, size_str, img_path)
        os.system(cmd)
        if dir_valid:
            os.chdir(cwd)


def get_video_info(video_file):
    info = dict()
    if os.path.isfile(video_file):
        cwd = os.getcwd()
        dirname = os.path.dirname(FILE_FFMPEG)
        dir_valid = len(dirname) > 0
        ffmpeg = FILE_FFMPEG
        if dir_valid:
            os.chdir(dirname)
            ffmpeg = os.path.basename(FILE_FFMPEG)
        cmd = ffmpeg + " -i  \"{}\"".format(video_file)

        try:
            result = subprocess.check_output(cmd, shell=False, stderr=subprocess.STDOUT)
        except Exception as e:
            result = e.output.decode()
        p_result = re.findall(r",[\s]*([\d]*)x([\d]*),", result)
        if len(p_result) > 0:
            size = p_result[0]
            info.update({'size': size})
        p_result = re.findall(r"Duration: ([\d.:]+),", result)
        if len(p_result) > 0:
            info.update({'time': p_result[0]})
        if dir_valid:
            os.chdir(cwd)
    return info


def walk_files_by_suffix(folder, suffixs, old_data=dict()):
    # folder F:/其他/影音
    relativeFiles = []
    for rt, dirs, files in os.walk(folder):
        for f in files:
            rpath = rt.replace(folder, '')
            if len(rpath) > 0 and rpath[0] == os.path.sep:
                rpath = rpath[1:]

            path = os.path.join(rpath, f)

            file = find_old_file_by_folder(old_data, path)

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
                absolute_file = os.path.join(rt, f)
                md5 = hashlib.md5()
                md5.update(absolute_file.encode("utf-8"))
                uid = str(md5.hexdigest())
                img_file = uid + '.png'
                img_path = os.path.join(FILE_PATH_IMAGES, img_file)
                create_ffmpeg_img(absolute_file, img_path)

                if file is not None:
                    data = file
                else:
                    info = get_video_info(absolute_file)
                    data = {
                        'uid': uid,
                        'path': path,
                        'name': fname[0],
                        'suffix': suffix,
                        'ctime': int(os.stat(absolute_file).st_ctime) * 1000,
                        'info': info
                    }
                data['thumb_path'] = os.path.join(os.path.basename(os.path.dirname(os.path.abspath(img_path))),
                                                  img_file)
                relativeFiles.append(data)
    relativeFiles = sorted(relativeFiles, key=sort_time, reverse=True)
    return relativeFiles


def sort_time(data):
    return data['ctime']


def handle(suffixs, file_config=FILE_CONFIG, file_json=FILE_JSON):
    old_datas = read_old_datas()
    folders = read_folder_config(file_config)
    data = []
    size = 0

    for folder in folders:
        old_data = find_old_data_by_folder(old_datas, folder)
        files = walk_files_by_suffix(folder, suffixs, old_data)
        size += len(files)
        if len(files) > 0:
            md5 = hashlib.md5()
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
            mp4_buffer_size       1m;
            mp4_max_buffer_size   5m;
            alias {};
        }}'''
        f.write(f_str.format(data['uid'], data['folder']))


def read_old_datas(file_json=FILE_JSON):
    if os.path.isfile(file_json):
        data = json.load(open(file_json))
        return data
    return []


def find_old_data_by_folder(old_datas, folder):
    for data in old_datas:
        if data["folder"] == folder:
            return data
    return None


def find_old_file_by_folder(old_data, path):
    if old_data is not None and "files" in old_data:
        for file in old_data["files"]:
            if file["path"] == path:
                return file
    return None


def main():
    data = handle(["mp4"])
    generate_nginx_conf(data)


if __name__ == "__main__":
    main()
