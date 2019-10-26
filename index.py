# -*- coding: utf-8 -*-
import sys
import time
import argparse
import traceback
import multiprocessing
from util.Adb import Adb
from model.Device import Device

if sys.version_info.major != 3:
    print('Please run under Python3')
    exit(1)

# 入口
def main():
    # 获取设备列表
    adb = Adb()
    device_list = adb.get_device_list()
    print('激活窗口并按 CONTROL + C 组合键退出')

    #  进程池
    pool = multiprocessing.Pool(len(device_list))
    for device_id in device_list:
        device = Device(device_id)
        pool.apply_async(device.start)
        time.sleep(1)
    pool.close()
    pool.join()
    print('完成!')

# 解析输入
def parser():
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--reply", action='store_true', help = "auto reply")
    args = vars(ap.parse_args())
    return args

# 获取命令行输入
cmd_args = parser()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('谢谢使用')
        exit(0)
    except BaseException as e:
        print('exception')
        print(traceback.format_exc())
        exit(0)
