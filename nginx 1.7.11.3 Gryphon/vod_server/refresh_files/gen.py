#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import uuid

FILE_JSON = "../www/files.json"

FILE_CONFIG = "folders.ini"


def read_folder_config(file_config):
    folders = []
    with open(file_config, encoding="utf-8") as f:
        for line in f:
            line = line.strip().replace('\n', '')
            if len(line) > 0:
                folders.append(line)
    return folders


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
                # print(rpath, os.path.join(rpath, f))
                relativeFiles.append(os.path.join(rpath, f))

    return relativeFiles


def handle(suffixs, file_config=FILE_CONFIG, file_json=FILE_JSON):
    folders = read_folder_config(file_config)
    data = []
    size = 0
    for folder in folders:
        files = walk_files_by_suffix(folder, suffixs)
        size += len(files)
        if len(files) > 0:
            data.append({'folder': folder, 'files': files, 'uid': str(uuid.uuid1())})
    write_json(data, file_json)
    print("files total count:%d" % size)
    return data


def write_json(data, file_json=FILE_JSON):
    rs_json = json.dumps(data, separators=(',', ':'))
    f = open(file_json, 'w')
    f.write(rs_json)

if __name__ == "__main__":
    datas = handle(["mp4", "mp3"])
    f = open("../confs/datas.conf", 'w', encoding="utf-8")
    f.write('#generated file,do not edit\n')
    for data in datas:
        # print(data['uid'], data['folder'])
        f_str = '''
    location /{} {{
        alias {};
    }}'''
        f.write(f_str.format(data['uid'], data['folder']))
