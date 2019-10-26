# -*- coding: utf-8 -*-
from model.Flow import Flow
import traceback

class Device:
    def __init__(self, device_id):
        self.device_id = device_id

    def start(self):
        print("设备启动: {}".format(self.device_id))
        try:
            flow = Flow(self.device_id)
            #  flow.test()
            flow.skim_video()
        except KeyboardInterrupt as e:
            print(self.device_id, '结束')
        except Exception as e:
            print(traceback.format_exc())
