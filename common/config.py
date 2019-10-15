# -*- coding: utf-8 -*-
import os
import sys
import json
import re

from common.adb import adb

def open_accordant_config(device_id = None):

    screen_size = 'default'
    if device_id:
        screen_size = _get_screen_size(device_id)
    print(screen_size)

    config_file = "{path}/config/{screen_size}/config.json".format(
        path=sys.path[0],
        screen_size=screen_size
    )

    # 优先获取执行文件目录的配置文件
    here = sys.path[0]
    for file in os.listdir(here):
        if re.match(r'(.+)\.json', file):
            file_name = os.path.join(here, file)
            with open(file_name, 'r') as f:
                print("Load config file from {}".format(file_name))
                return json.load(f)

    # 根据分辨率查找配置文件
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            print("正在从 {} 加载配置文件".format(config_file))
            return json.load(f)
    else:
        with open('{}/config/default.json'.format(sys.path[0]), 'r') as f:
            print("Load default config")
            return json.load(f)


def _get_screen_size(device_id):
    global adb
    adb_obj = adb(device_id)

    size_str = adb_obj.get_screen()
    m = re.search(r'(\d+)x(\d+)', size_str)
    if m:
        return "{height}x{width}".format(height=m.group(2), width=m.group(1))
    return "1920x1080"
