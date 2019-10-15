# -*- coding: utf-8 -*-
import random
from common import config
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
        y2 = config['center_point']['y']
        self.adb.swipe(x1, y1, x2, y2)
        print(self.device_id + ': swipe')

    # 关注
    def follow(self):
        x = config['follow_bottom']['x'] + self._random_bias(10)
        y = config['follow_bottom']['y'] + self._random_bias(10)
        self.adb.tap(x, y)
        print(self.device_id + ': follow')

    # 点赞
    def like(self):
        x = config['star_bottom']['x'] + self._random_bias(10)
        y = config['star_bottom']['y'] + self._random_bias(10)
        self.adb.tap(x, y)
        print(self.device_id + ': like')

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
        print(self.device_id + ': reply')
