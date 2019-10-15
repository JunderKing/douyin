# -*- coding: utf-8 -*-
import sys
import random
import time
from PIL import Image
import argparse
import multiprocessing
import threading
from concurrent.futures import ThreadPoolExecutor

if sys.version_info.major != 3:
    print('Please run under Python3')
    exit(1)

try:
    #  from common import debug, config, screenshot, UnicodeStreamFilter
    #  from common.adb import adb
    #  from common import apiutil
    #  from common.compression import resize_image
    from common import config, debug
    from common.adb import adb
    from common.action import action
except BaseException as ex:
    print(ex)
    print('请将脚本放在项目根目录中运行')
    print('请检查项目根目录中的 common 文件夹是否存在')
    exit(1)

VERSION = "0.0.1"

# 腾讯AI 申请地址 http://ai.qq.com
AppID = '1106858595'
AppKey = 'bNUNgOpY6AeeJjFu'

DEBUG_SWITCH = True
FACE_PATH = 'face/'
adb = adb()
config = config.open_accordant_config()



def robot(device_id):
    print('robot: ' + device_id)
    global action
    action = action(device_id)

    while True:
        # 下一页
        action.next_page()
        time.sleep(5)

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

# 入口
def main():
    # 检查ADB环境
    adb.check_env()
    # 获取设备列表
    device_list = adb.get_device_list()

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
        print(device_id)
        pool.apply_async(robot, args = (device_id,))
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

# 寻找美女
def find_girl(device_id):
    # 审美标准
    BEAUTY_LIKE = 80
    BEAUTY_FOLLOW = 90
    BEAUTY_REPLY = 95

    # 最小年龄
    GIRL_MIN_AGE = 3

    # 检查截屏
    screenshot.check_screenshot()

    while True:
        next_page()

        time.sleep(1)
        screenshot.pull_screenshot()

        resize_image('autojump.png', 'optimized.png', 1024*1024)

        with open('optimized.png', 'rb') as bin_data:
            image_data = bin_data.read()

        ai_obj = apiutil.AiPlat(AppID, AppKey)
        rsp = ai_obj.face_detectface(image_data, 0)

        major_total = 0
        minor_total = 0

        if rsp['ret'] == 0:
            beauty = 0
            for face in rsp['data']['face_list']:

                msg_log = '[INFO] gender: {gender} age: {age} expression: {expression} beauty: {beauty}'.format(
                    gender=face['gender'],
                    age=face['age'],
                    expression=face['expression'],
                    beauty=face['beauty'],
                )
                print(msg_log)
                face_area = (face['x'], face['y'], face['x']+face['width'], face['y']+face['height'])
                img = Image.open("optimized.png")
                cropped_img = img.crop(face_area).convert('RGB')
                cropped_img.save(FACE_PATH + face['face_id'] + '.png')
                # 性别判断
                if face['beauty'] > beauty and face['gender'] < 50:
                    beauty = face['beauty']

                if face['age'] > GIRL_MIN_AGE:
                    major_total += 1
                else:
                    minor_total += 1

            # 是个美人儿~关注点赞走一波
            if beauty >= BEAUTY_LIKE and major_total > minor_total:
                print('发现漂亮妹子！！！')
                like_user()

                if beauty >= BEAUTY_FOLLOW:
                    follow_user()

                if cmd_args['reply'] and beauty >= BEAUTY_REPLY:
                    auto_reply()

        else:
            print(rsp)
            continue


# 获取命令行输入
cmd_args = parser()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        adb.run('kill-server')
        print('谢谢使用')
        exit(0)
    except BaseException as e:
        print(e)
        exit(0)
