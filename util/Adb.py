# -*- coding: utf-8 -*-
import os
import subprocess
import platform

class Adb():
    def __init__(self, device_id = None):
        self.device_id = device_id
        self.adb_path = 'adb'

    # 执行命令并返回结果
    def run(self, raw_command):
        command = '{} {}'.format(self.adb_path, raw_command)
        process = os.popen(command)
        output = process.read()
        return output

    # 执行设备shell命令
    def shell(self, cmd):
        output = self.run('-s ' + self.device_id + ' shell ' + cmd)
        return output

    # 获取设备列表
    def get_device_list(self):
        output = self.run('devices')
        line_arr = output.split('\n')
        device_list = []
        for line_str in line_arr:
            word_arr = line_str.split('\t')
            if len(word_arr) != 2 or word_arr[1] != 'device':
                continue
            device_list.append(word_arr[0])
        if len(device_list) == 0:
            print('请连接手机或者模拟器')
            exit(0)

        return device_list

    # 点击
    def tap(self, x, y):
        self.shell('input tap {} {}'.format(x, y))

    # 滑动
    def swipe(self, x1, y1, x2, y2, duration = 200):
        self.shell('input swipe {} {} {} {} {}'.format(x1, y1, x2, y2, duration))

    # 输入文字
    def input(self, content):
        self.shell('am broadcast -a ADB_INPUT_TEXT --es msg {}'.format(content))

    # 返回
    def back(self):
        self.shell('input keyevent 4')

    # 获取屏幕分辨率
    def get_screen(self):
        output = self.shell('wm size')
        return output

    # 屏幕截图
    def screen_shot(self):
        self.shell('screencap -p /sdcard/{}_screen.png'.format(self.device_id).replace('127.0.0.1:', ''))
        self.run('pull /sdcard/{}_screen.png .'.format(self.device_id).replace('127.0.0.1:', ''))
