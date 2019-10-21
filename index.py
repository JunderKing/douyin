# -*- coding: utf-8 -*-
import sys
import random
import time
from PIL import Image
import argparse
import multiprocessing
# import threading
# from concurrent.futures import ThreadPoolExecutor

if sys.version_info.major != 3:
    print('Please run under Python3')
    exit(1)

try:
    #  from common import debug, config, screenshot, UnicodeStreamFilter
    #  from common.adb import adb
    from common import apiutil, config
    from common.adb import adb
    from common.action import action
except BaseException as ex:
    print(ex)
    print('请将脚本放在项目根目录中运行')
    print('请检查项目根目录中的 common 文件夹是否存在')
    exit(1)

VERSION = "0.0.1"

# 腾讯AI 申请地址 http://ai.qq.com
#  AppID = '1106858595'
#  AppKey = 'bNUNgOpY6AeeJjFu'
AppID = '2123030292'
AppKey = 'WKsdxmqtBUmNSwCO'

DEBUG_SWITCH = True
FACE_PATH = 'face/'
adb_obj = adb()
config = config.open_accordant_config()

def robot(device_id):
    print('robot: ' + device_id)
    global action
    action = action(device_id)

    try:
        while True:
            # 下一页
            action.next_page()
            time.sleep(random.randint(20, 40))
            # video_type = action.get_type()
            # screen_data = False
            # if video_type == 'user':
            #     time.sleep(10)
            #     action.detail()
            #     time.sleep(2)
                # try:
                #     screen_data = action.get_screen_data()
                # except BaseException as e:
                #     print('错误所在的行号：', e.__traceback__.tb_lineno)
                # time.sleep(2)
                # action.back()
                # time.sleep(2)
            # action.to_detail()
            # time.sleep(10)
            # action.back()
            # time.sleep(3)
            # continue

            if random.randint(1, 40) == 1:
                action.follow()
                time.sleep(2)
            elif random.randint(1, 20) == 1:
                action.like()
                time.sleep(2)

            # if screen_data == False:
            #     continue

            continue

            if random.randint(1, 20) == 1 and screen_data['fan_num'] < 10000 and screen_data['follow_num'] > 10:
                action.follow()
                time.sleep(2)
            elif random.randint(1, 10) == 1 and screen_data['like_num'] < 100000 and screen_data['follow_num'] > 10:
                action.like()
                time.sleep(2)

            # 点赞
            if random.randint(1, 2) == 1:
                action.like()
                time.sleep(0.5)

            # 关注
            if random.randint(1, 10) == 1:
                action.follow()
                time.sleep(0.5)

            # 评论
            if cmd_args['reply'] and random.randint(1, 50) == 1:
                msg = "垆边人似月，皓腕凝霜雪。就在刚刚，我的心动了一下，小姐姐你好可爱呀!"
                action.reply(msg)
                time.sleep(1)
    except BaseException as e:
        print('发生错误的文件：', e.__traceback__.tb_frame.f_globals['__file__'])
        print('错误所在的行号：', e.__traceback__.tb_lineno)
        print('错误信息', e)

# 入口
def main():
    # 检查ADB环境
    adb_obj.check_env()
    # 获取设备列表
    device_list = adb_obj.get_device_list()

    print('程序版本号：{}'.format(VERSION))
    print('激活窗口并按 CONTROL + C 组合键退出')
    # debug.dump_device_info()

    #  robot(device_list[0])
    #  exit(1)

    #  线程池
    #  with ThreadPoolExecutor(len(device_list)) as executor:
        #  for device_id in device_list:
            #  executor.submit(robot, device_id)

    #  多线程
    #  print('thread %s is running...' % threading.current_thread().name)
    #  for device_id in device_list:
        #  print(device_id)
        #  t = threading.Thread(target=robot, args=(device_id))
        #  t.start()
    #  print('thread %s ended.' % threading.current_thread().name)
    #  exit()

    #  进程池
    pool = multiprocessing.Pool(len(device_list))
    for device_id in device_list:
        pool.apply_async(robot, args = (device_id,))
        time.sleep(1)
    print('Waiting...')
    pool.close()
    pool.join()
    print('done!')

def process_cb(res):
    print('cb')


# 解析输入
def parser():
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--reply", action='store_true', help = "auto reply")
    args = vars(ap.parse_args())
    return args



# 获取命令行输入
cmd_args = parser()

if __name__ == '__main__':
    # adb_device = adb('CUYDU19524020220')
    # adb_device.screen_shot()
    # rtn_data = get_screen_data()
    # print(rtn_data)
    #  resize_image('autojump.png', 'optimized.png', 1024*1024)


     try:
         main()
     except KeyboardInterrupt:
         adb.run('kill-server')
         print('谢谢使用')
         exit(0)
     except BaseException as e:
         print(e)
         exit(0)
