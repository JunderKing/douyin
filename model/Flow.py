#-*- coding: UTF-8 -*-
import time
from model.Action import Action
from model.Action import get_int

class Flow(object):
    def __init__(self, device_id):
        self.action = Action(device_id)
        self.device_id = device_id

    def test(self):
        print(self.device_id, '开始测试流程')
        self.action.screen_shot()
        status_dict = self.action.get_home_data()
        print(status_dict)
        #  flag = self.action.get_home_data()
        #  print(flag)
        #  rtn = get_int('1 1')
        #  print(rtn)
        #  print(home_data)

    def skim_video(self):
        print(self.device_id, '浏览视频')
        start_time = int(time.time())
        while True:
            # 运行3个小时，休息9个小时
            cur_time = int(time.time())
            if cur_time - start_time >= 3 * 3600:
                self.adb.home()
                time.sleep(9 * 3600)
                start_time = int(time.time())
                self.adb.open_douyin()
                time.sleep(30)
            self.action.next_video()
            time.sleep(5)
            self.action.screen_shot()

            # 判断是否已关注
            status_dict = self.action.get_status()
            if status_dict['followed'] or status_dict['liked']:
                print(self.device_id, '已关注或者已点赞', status_dict)
                continue;

            # 获取首页数据
            home_data = self.action.get_home_data()
            if not home_data:
                print(self.device_id, '获取页面数据失败')
                continue
            else:
                print(self.device_id, '点赞数：{}，评论数：{}'.format(home_data['like_num'], home_data['reply_num']))

            time.sleep(5)

            # 给少于1万点赞数的人关注和点赞
            if home_data['like_num'] < 10000:
                # 点赞
                if not status_dict['liked']:
                    self.action.like()
                    time.sleep(2)
                # 关注
                if not status_dict['followed']:
                    self.action.follow()
                    time.sleep(2)
                # 评论
                if home_data.__contains__('desc'):
                    question = home_data['desc']
                    print(self.device_id, '描述:', question)
                    answer = self.action.get_answer(question)
                    if answer:
                        print(self.device_id, '评论:', answer)
                        self.action.reply(answer)
                        time.sleep(2)
                    else:
                        print(self.device_id, '获取评论失败')
            else:
                print(self.device_id, '点赞数超过一万:', home_data['like_num'])
