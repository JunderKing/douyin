#-*- coding: UTF-8 -*-
import time
from model.Action import Action

class Flow(object):
    def __init__(self, device_id):
        self.action = Action(device_id)
        self.device_id = device_id

    def test(self):
        print('{}: 开始测试流程'.format(self.device_id))
        self.action.screen_shot()
        pass

    def skim_video(self):
        print('{}: 浏览视频'.format(self.device_id))
        while True:
            self.action.next_page()
            sleep(1)
