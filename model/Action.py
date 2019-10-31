# -*- coding: utf-8 -*-
import random
import time
import sys
import traceback
import pyperclip
from PIL import Image
from util.Adb import Adb
from util.Ai import Ai
from config import screen

# 配置信息
def get_int(string):
    string = string.replace(' ', '')
    try:
        if string[-1:] == 'w' or string[-1:] == 'W':
            return int(float(string[:-1]) * 10000)
        else:
            return int(float(string))
    except BaseException as e:
        return False

class Action():
    def __init__(self, device_id):
        self.adb = Adb(device_id)
        self.device_id = device_id
        resolution = self.adb.get_resolution()
        self.screen = screen.config[resolution]
        self.image_path = 'static/screen_shot/'

    # 加入随机
    def _random_bias(self, num):
        return random.randint(-num, num)

    # 截图
    def screen_shot(self):
        self.adb.screen_shot()
    
    # 检查首页数据
    def check_home(self):
        img = Image.open('{}{}_screen.png'.format(self.image_path, self.device_id).replace('127.0.0.1:', ''))
        kb_r, kb_g, kb_b, kb_a = img.getpixel(self.screen['check_kb'])
        bg_r, bg_g, bg_b, bg_a = img.getpixel(self.screen['check_bg'])
        cd_r, cd_g, cd_b, cd_a = img.getpixel(self.screen['check_cd'])
        if cd_r < 200 or cd_g < 200 or cd_b < 200:
            # 视频界面
            return True
        elif kb_r < 100 or kb_g < 100 or kb_b < 100:
            # 已打开键盘
            self.adb.back()
            time.sleep(1)
            self.adb.back()
            time.sleep(1)
            self.adb.back()
            return False
        elif bg_r < 150 or bg_g < 150 or bg_b < 150:
            # 已打开输入
            self.adb.back()
            time.sleep(1)
            self.adb.back()
            return False
        else:
            self.adb.back()
            return False
    
    # 跳转至首页
    def to_home(self):
        self.adb.home()

    # 打开抖音
    def open_douyin(self):
        self.adb.open('com.ss.android.ugc.aweme/.main.MainActivity')

    # 退出抖音
    def quit_douyin(self):
        self.adb.quit('com.ss.android.ugc.aweme')

    # 重启抖音
    def restart_douyin(self):
        self.quit_douyin()
        time.sleep(10)
        self.open_douyin()
        time.sleep(30)

    # 滑动页面
    def swipe_page(self, direction):
        x, y = self.screen['screen_center']
        if direction == 'down':
            self.adb.swipe(x, y * 0.5, x, y * 1.5)
        elif direction == 'up':
            self.adb.swipe(x, y * 1.5, x, y * 0.5)
        elif direction == 'left':
            self.adb.swipe(x * 1.5, y, x * 0.5, y)
        else:
            self.adb.swipe(x * 0.5, y, x * 1.5, y)

    # 点击
    def click(self, name):
        x, y = self.screen[name]
        self.adb.tap(x, y)
    
    def long_tap(self, name):
        x1, y1 = self.screen[name]
        self.adb.swipe(x1, y1, x1, y1, 1000)
    
    # 复制到剪贴板
    def input(self, text, text_name = 'paste_point', btn_name = 'paste_btn'):
        # print(text)
        # self.adb.input(text)
        # return False
        # pyperclip.copy(text)
        self.adb.set_clipboard(text)
        self.adb.get_clipboard()
        print('copy', text)
        return false
        time.sleep(1)
        self.long_tap(text_name)
        time.sleep(1)
        self.click(btn_name)

    # 进入详情
    def to_detail(self):
        self.swipe_page('left')
        print(self.device_id, '详情')

    # 翻到下一页
    def next_video(self):
        self.swipe_page('up')
        print(self.device_id, '下一个')

    # 关注
    def follow(self):
        self.click('video_follow')
        print(self.device_id, '关注')

    # 点赞
    def like(self):
        self.click('video_like')
        print(self.device_id, '点赞')

    # 回复
    def reply(self, msg):
        # 点击评论按钮
        self.click('reply_btn')
        time.sleep(1)

        # 弹出评论列表后点击输入评论框
        self.click('reply_input')
        time.sleep(1)

        # 输入文字 ，注意要使用ADB keyboard  否则不能自动输入，参考： https://www.jianshu.com/p/2267adf15595
        self.adb.input(msg)
        time.sleep(1)

        # 点击发送按钮
        self.click('reply_send')
        time.sleep(1)

        # 触发返回按钮, keyevent 4 对应安卓系统的返回键，参考KEY 对应按钮操作：  https://www.cnblogs.com/chengchengla1990/p/4515108.html
        self.adb.back()
        print(self.device_id, '评论完成')
    
    # 获取视频状态
    def get_status(self):
        img = Image.open('{}{}_screen.png'.format(self.image_path, self.device_id).replace('127.0.0.1:', ''))
        rtn = {'followed': True, 'liked': False}
        r, g, b, a = img.getpixel(self.screen['follow_status'])
        if r >= 200 and g < 100 and b < 100:
            rtn['followed'] = False
        r, g, b, a = img.getpixel(self.screen['like_status'])
        if r < 200 or g < 200 or b < 200:
            rtn['liked'] = True
        return rtn

    def back(self):
        self.adb.back()
        print(self.device_id, '返回')

    # 获取数量
    def get_number(self, string):
        try:
            if string[-1:] == 'w':
                return int(float(string[:-1]) * 10000)
            else:
                return int(float(string))
        except BaseException as e:
            print(e)
            return 0

    # 获取详情页面的数据
    def get_detail_data(self):
        app_id = '2123030292'
        app_key = 'WKsdxmqtBUmNSwCO'
        self.adb.screen_shot()
        img = Image.open('{}_screen.png'.format(self.device_id).replace('127.0.0.1:', ''))
        img.resize((int(img.width / 2), int(img.height / 2))).save('{}_optimized.png'.format(self.device_id).replace('127.0.0.1:', ''))
        with open('{}_optimized.png'.format(self.device_id), 'rb') as bin_data:
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
    
    def get_home_data(self):
        img = Image.open('{}{}_screen.png'.format(self.image_path, self.device_id).replace('127.0.0.1:', ''))
        img = self.mask_image(img, self.screen['home_mask'])
        img = self.mask_image(img, self.screen['home_mask2'])
        img.crop(self.screen['home_crop']).save('{}{}_optimized.png'.format(self.image_path, self.device_id).replace('127.0.0.1:', ''))
        # img.resize((int(img.width / 2), int(img.height / 2))).save('{}_optimized.png'.format(self.device_id).replace('127.0.0.1:', ''))
        with open('{}{}_optimized.png'.format(self.image_path, self.device_id).replace('127.0.0.1:', ''), 'rb') as bin_data:
            image_data = bin_data.read()

        for index in range(5):
            ai = Ai()
            res = ai.ocr(image_data)
            if res['ret'] == 0:
                # print(res)
                break
            print(self.device_id, '页面数据失败重试', index + 1)
            time.sleep(1)
        if res['ret'] != 0:
            print(self.device_id, '页面数据失败次数过去，跳过！')
            return False
        rtn_dict = {}
        text_list = res['data']['item_list']
        for index, text_obj in enumerate(text_list):
            text = text_obj['itemstring']
            if text.find('广告') != -1:
                print(self.device_id, '广告跳过！')
                return False
            if index <= 1:
                number = get_int(text)
                if type(number) == bool:
                    print(self.device_id, '数据格式错误，跳过！')
                    return False
                if index == 0:
                    rtn_dict['like_num'] = number
                elif index == 1:
                    rtn_dict['reply_num'] = number
                # elif index == 2:
                    # rtn_dict['share_num'] = number
            else:
                symbol_index_1 = text.find('@')
                symbol_index_2 = text.find('#')
                if symbol_index_1 == 0:
                    rtn_dict['desc'] = ''
                    continue
                # if symbol_index_2 == 0 and rtn_dict.__contains__('desc') and rtn_dict['desc'] != '':
                    # continue
                if symbol_index_1 != -1:
                    text = text[:symbol_index_1]
                if symbol_index_2 != -1:
                    text = text[:symbol_index_2]
                if rtn_dict.__contains__('desc'):
                    rtn_dict['desc'] += text
                else:
                    rtn_dict['desc'] = text
                if symbol_index_1 != -1 or symbol_index_2 != -1:
                    break
        return rtn_dict
    
    def mask_image(self, img, area):
        for w in range(img.width):
            for h in range(img.height):
                if (w >= area[0] and w <= area[2] and h >= area[1] and h <= area[3]):
                    img.putpixel((w, h), (0, 0, 0))
        return img

    # 看图说话
    def get_screen_desc(self):
        app_id = '2123030292'
        app_key = 'WKsdxmqtBUmNSwCO'
        self.adb.screen_shot()
        img = Image.open('{}_screen.png'.format(self.device_id).replace('127.0.0.1:', ''))
        img.resize((int(img.width / 2), int(img.height / 2))).save('{}_optimized.png'.format(self.device_id).replace('127.0.0.1:', ''))
        with open('{}_optimized.png'.format(self.device_id), 'rb') as bin_data:
            image_data = bin_data.read()

        ai_obj = apiutil.AiPlat(app_id, app_key)
        rsp = ai_obj.image_to_text(image_data)
        # print(rsp)
        if rsp['ret'] != 0:
            # print(rsp)
            return False
    
    # 获取视频点赞数
    def get_like_num(self):
        app_id = '2123030292'
        app_key = 'WKsdxmqtBUmNSwCO'
        self.adb.screen_shot()

        region_left = config['text_region']['left']
        region_top = config['text_region']['top']
        region_right = config['text_region']['right']
        region_bottom = config['text_region']['bottom']

        img = Image.open('{}_screen.png'.format(self.device_id).replace('127.0.0.1:', ''))
        img.crop(region_left, region_top, region_right, region_bottom).save('{}_optimized.png'.format(self.device_id).replace('127.0.0.1:', ''))
        with open('{}_optimized.png'.format(self.device_id), 'rb') as bin_data:
            image_data = bin_data.read()

        ai_obj = apiutil.AiPlat(app_id, app_key)
        rsp = ai_obj.ocr(image_data, 0)
        if rsp['ret'] != 0:
            print(rsp)
            return False

        print(rsp)
    
    # 获取聊天
    def get_answer(self, question):
        for index in range(5):
            ai = Ai()
            res = ai.get_answer(question)
            if res['ret'] == 0:
                break
            print(self.device_id, '评论数据失败重试', index + 1)
            time.sleep(1)
        if res['ret'] != 0:
            return False
        return res['data']['answer']
