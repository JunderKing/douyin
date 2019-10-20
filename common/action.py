# -*- coding: utf-8 -*-
import random
from PIL import Image
from common import config, apiutil
from common.adb import adb

# 配置信息
config = config.open_accordant_config()

class action():
    def __init__(self, device_id):
        self.adb = adb(device_id)
        self.device_id = device_id

    # 加入随机
    def _random_bias(self, num):
        return random.randint(-num, num)

    # 翻到下一页
    def next_page(self):
        x1 = config['center_point']['x']
        y1 = config['center_point']['y'] + config['center_point']['ry']
        x2 = config['center_point']['x']
        y2 = config['center_point']['y'] - config['center_point']['ry']
        self.adb.swipe(x1, y1, x2, y2)
        print(self.device_id + ': 下一个')

    def to_detail(self):
        x1 = config['center_point']['x'] + config['center_point']['rx']
        y1 = config['center_point']['y']
        x2 = config['center_point']['x']
        y2 = config['center_point']['y']
        self.adb.swipe(x1, y1, x2, y2)
        print(self.device_id + ': 详情')

    def detail(self):
        x = config['detail_center']['x'] + self._random_bias(10)
        y = config['detail_center']['y'] + self._random_bias(10)
        self.adb.tap(x, y)
        print(self.device_id + ': 进入详情')

    # 关注
    def follow(self):
        x = config['follow_bottom']['x'] + self._random_bias(10)
        y = config['follow_bottom']['y'] + self._random_bias(10)
        self.adb.tap(x, y)
        print(self.device_id + ': 关注')

    # 点赞
    def like(self):
        x = config['star_bottom']['x'] + self._random_bias(10)
        y = config['star_bottom']['y'] + self._random_bias(10)
        self.adb.tap(x, y)
        print(self.device_id + ': 点赞')

    # 回复
    def reply(self, msg):
        # 点击评论按钮
        self.adb.tap(config['comment_bottom']['x'], config['comment_bottom']['y'])
        time.sleep(1)

        # 弹出评论列表后点击输入评论框
        self.adb.tap(config['comment_text']['x'], config['comment_text']['y'])
        time.sleep(1)

        # 输入文字 ，注意要使用ADB keyboard  否则不能自动输入，参考： https://www.jianshu.com/p/2267adf15595
        self.adb.input(msg)
        time.sleep(1)

        # 点击发送按钮
        self.adb.tap(config['comment_send']['x'], config['comment_send']['y'])
        time.sleep(1)

        # 触发返回按钮, keyevent 4 对应安卓系统的返回键，参考KEY 对应按钮操作：  https://www.cnblogs.com/chengchengla1990/p/4515108.html
        self.adb.back()
        print(self.device_id + ': 评论')

    def get_type(self):
        self.adb.screen_shot()
        border_x = config['detail_border']['x']
        border_y = config['detail_border']['y']
        bottom_x = config['detail_bottom']['x']
        bottom_y = config['detail_bottom']['y']

        img = Image.open('{}_screen.png'.format(self.device_id).replace('127.0.0.1:', ''))
        border_r, border_g, border_b, border_a = img.getpixel((border_x, border_y))
        bottom_r, bottom_g, bottom_b, bottom_a = img.getpixel((bottom_x, bottom_y))
        if border_r < 200 or border_g < 200 or border_b < 200:
            print(self.device_id + ': 直播')
            return 'live'
        elif bottom_r > 200 and (bottom_g > 200 or bottom_b > 200):
            print(self.device_id + ': 广告')
            return 'adv'
        print(self.device_id + ': 未关注用户')
        return 'user'

    def back(self):
        self.adb.back()
        print(self.device_id + ': 返回')

    def get_number(self, string):
        try:
            if string[-1:] == 'w':
                return int(float(string[:-1]) * 10000)
            else:
                return int(float(string))
        except BaseException as e:
            return 0

    def get_screen_data(self):
        app_id = '2123030292'
        app_key = 'WKsdxmqtBUmNSwCO'
        self.adb.screen_shot()
        img = Image.open('{}_screen.png'.format(self.device_id).replace('127.0.0.1:', ''))
        img.resize((int(img.width / 2), int(img.height / 2))).save('optimized.png')
        with open('{}optimized.png'.format(self.device_id), 'rb') as bin_data:
            image_data = bin_data.read()

        ai_obj = apiutil.AiPlat(app_id, app_key)
        rsp = ai_obj.ocr(image_data, 0)
        if rsp['ret'] != 0:
            print(rsp)
            return False
        for text_data in rsp['data']['item_list']:
            text = text_data['itemstring']
            if text.find('获赞') != -1:
                like_num, follow_num, fan_num = text.replace(' ', '').replace('粉丝', '').replace('获赞', ',').replace('关注', ',',).split(',')
                like_num = self.get_number(like_num)
                follow_num = self.get_number(follow_num)
                fan_num = self.get_number(fan_num)
            elif text.find('作品') != -1:
                video_num = self.get_number(text.replace(' ', '').replace('作品', ''))
            elif text.find('动态') != -1:
                blog_num = self.get_number(text.replace(' ', '').replace('动态', ''))
            elif text.find('喜欢') != -1:
                interest_num = self.get_number(text.replace(' ', '').replace('喜欢', ''))
        return {
            'like_num': like_num,
            'follow_num': follow_num,
            'fan_num': fan_num,
            'video_num': video_num,
            'blog_num': blog_num,
            'interest_num': interest_num
        }
