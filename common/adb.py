# -*- coding: utf-8 -*-
import os
import subprocess
import platform

class adb():
    def __init__(self, device_id = None):
        self.device_id = device_id
        self.adb_path = 'adb'

    # 检查环境
    def check_env(self):
        try:
            subprocess.Popen([self.adb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError:
            if platform.system() == 'Windows':
                self.adb_path = os.path.join('Tools', "adb", 'adb.exe')
                try:
                    subprocess.Popen([self.adb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                except OSError:
                    print('请安装 ADB 及驱动并配置环境变量')
                    exit(1)
            else:
                print('请安装 ADB 及驱动并配置环境变量')
                exit(1)
        print('ADB 环境安装成功')

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
        self.shell('screencap -p /sdcard/screen.png')
        self.run('pull /sdcard/{}_screen.png .'.format(self.device_id))

    ###########################################################

    def test_device(self):
        print('检查设备是否连接...')
        command_list = [self.adb_path, 'devices']
        process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()

        if output[0].decode('utf8') == 'List of devices attached\n\n':
            print('未找到设备')
            print('adb 输出:')
            for each in output:
                print(each.decode('utf8'))
            exit(1)
        print('设备已连接')
        print('adb 输出:')
        for each in output:
            print(each.decode('utf8'))

    def test_density(self):
        process = os.popen(self.adb_path + ' shell wm density')
        output = process.read()
        return output

    def test_device_detail(self):
        process = os.popen(self.adb_path + ' shell getprop ro.product.device')
        output = process.read()
        return output

    def test_device_os(self):
        process = os.popen(self.adb_path + ' shell getprop ro.build.version.release')
        output = process.read()
        return output

    def adb_path(self):
        return self.adb_path
