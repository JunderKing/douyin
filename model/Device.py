# -*- coding: utf-8 -*-
from model.Flow import Flow

class Device:
    def __init__(self, device_id):
        self.device_id = device_id

    def start(self):
        print("设备启动: {}".format(self.device_id))
        flow = Flow(self.device_id)
        flow.test()
