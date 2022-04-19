# -*- encoding:utf-8 -*-

import sys
# import hashlib
# from hashlib import sha1
# import hmac
# import base64
from socket import *
import json
import time
import threading
from websocket import create_connection
import websocket
import logging

# from pydub import AudioSegment

import random
import string
import os

import datetime
import subprocess
# import eventlet
import pyaudio

import requests

sys.path.append("..")

from plugins import utils

# from apscheduler.schedulers.blocking import BlockingScheduler
import functools

# reload(sys)
# sys.setdefaultencoding("utf8")
# logging.basicConfig()

g_record_stream = None
g_CHUNK = None

base_url = "wss://ivs.iflyos.cn/embedded/v1"

# Implicit_authorization Information
access_token = ''
device_id = ''

print(os.getcwd() )

# Implicit_authorization file
authorization_file = './src/shell/implicit_authorization.sh'
access_token_file = './src/shell/access_token.json'

# recordAudio file
#audio_file_path = "./wav.fifo"
audio_file_path = "./wav.wav"
audio_file_opus_path = "./opus.fifo"
# audio_file_opus_path = "./opus.opus"


audio_file_speex_path = "./spx.pcm"
# audio_file_speex_path = "./spx.fifo"
# audio_file_speex_path = "./opus.opus"

end_tag = b'__END__'

def rprint(text):
    print('\033[1;31m%s\033[0m' % text)


def gprint(text):
    print('\033[1;32m%s\033[0m' % text)


def yprint(text):
    print('\033[1;33m%s\033[0m' % text)


def bprint(text):
    print('\033[1;34m%s\033[0m' % text)


def volume_control(action, volume=10):
    if action == 'set':
        os.system('./src/shell/shell_control_center.sh -v -s %d' % (volume))
    elif action == 'get':
        return os.popen('./src/shell/shell_control_center.sh -v -g', 'r').read()
    elif action == 'up' or action == 'down':
        os.system('./src/shell/shell_control_center.sh -v -%s' % action[0])


def excuteCommand(com):
    ex = subprocess.Popen(com, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    out, err = ex.communicate()
    status = ex.wait()
    #print("cmd in:", com)
    #print("cmd out: ", out.decode())
    return out.decode()


def playback_play_tts(url):
    print("playback_play:" + url)
    excuteCommand('./src/shell/shell_control_center.sh -p -b %s' % url)
    print('playback_play end!')


def playback_play(url, wait=False):
    print("playback_play:" + url)
    if wait:
        excuteCommand('./src/shell/shell_control_center.sh -p -b %s' % url)
    else:
        os.system('./src/shell/shell_control_center.sh -p -b %s' % url)
    print('playback_play end!')


def playback_pause():
    os.system('./src/shell/shell_control_center.sh -p -p')


def playback_stop():
    os.system('./src/shell/shell_control_center.sh -p -s')


def playback_resume():
    os.system('./src/shell/shell_control_center.sh -p -r')


def record_start():
    # format = 'AUDIO_L16_RATE_16000_CHANNELS_1'
    # client.sendAudioRequest(format)
    chunk = read_stream()
    client.send_audio_chunk(chunk)

def recordAudio_start():
    global g_start_record

    rprint("record start time:%s" % datetime.datetime.now())
    # global audio_file_path
    # 先停止正在播放的
    playback_stop()

    g_start_record = True

    format = 'AUDIO_L16_RATE_16000_CHANNELS_1'
    client.sendAudioRequest(format)

    # num = 1
    while g_start_record:
        # print(num)
        # num += 1
        record_start()
    

    '''
    os.system('./shell/RECORDER_CONTROL.sh %s' % audio_file_path)
    os.system('./shell/CONVERT_CONTROL.sh %s %s' %
              (audio_file_path, audio_file_opus_path))

    writeRecogAudio(format='OPUS')
    '''
def recordAudioTrans_start():
    global g_start_record

    rprint("record start time:%s" % datetime.datetime.now())
    # global audio_file_path
    # 先停止正在播放的
    playback_stop()

    g_start_record = True

    format = 'AUDIO_L16_RATE_16000_CHANNELS_1'
    client.sendAudioTransRequest(format)

    # num = 1
    while g_start_record:
        # print(num)
        # num += 1
        record_start()

def get_evaluate_levels():
    return client.sendEvaluateLevels()

def get_evaluate_questions(level):
    return client.sendEvaluateQuestions(level)

def evaluate_start():
    levels_choice = ''
    levels_id = []
    levels_result = get_evaluate_levels()
    if 'levels' in levels_result.keys():
        for value in levels_result.get('levels'):
            levels_id.append(value['level_id'])
            levels_choice += value['level_id'] + '、' + value['title'] + '\n'
    
    print(levels_choice)
    levels_num = len(levels_result.get('levels'))
    choice = ''
    choice = utils.user_choice('请选择试题难度:', lambda f: f and (f in levels_id), choice)
    choice = int(choice)

    question = get_evaluate_questions(choice)

    

    evaluate_text = '[choice]\n'
    if 'question' in question.keys():
        question_keyword = question.get('question').get('keyword').strip(' ')
        
        # 显示题目
        if 'text' in question.get('question').keys():
            question_text = question.get('question').get('text')
            print(f'题目:{question_text}')
        # 播放音频
        question_audio = question.get('question').get('audio_url')
        if question_audio:
            playback_play(question_audio, wait=True)
        # 拼凑评测text
        for index, answer in enumerate(question.get('question').get('answers')):
            evaluate_text += f'{index + 1}. {answer}\n'
        evaluate_text += f'[keywords]\n{question_keyword}'

        # 发起评测请求
        recordAudioEvalute_start(evaluate_text)

    print(question)


def recordAudioEvalute_start(text):
    global g_start_record

    rprint("record start time:%s" % datetime.datetime.now())
    # global audio_file_path
    # 先停止正在播放的
    # playback_stop()

    g_start_record = True

    format = 'AUDIO_L16_RATE_16000_CHANNELS_1'
    client.sendAudioEvaluteRequest(format, text)

    # num = 1
    while g_start_record:
        # print(num)
        # num += 1
        record_start() 
    

def recordAudio_stop():
    global g_start_record

    rprint("recordAudio_stop")
    g_start_record = False

    '''
    os.system('./shell/RECORDER_CONTROL.sh STOP')
    os.system('./shell/CONVERT_CONTROL.sh STOP')
    '''
    
    # 停止写入，立即送识别
    # writeRecogAudio()


application_dic = {u'微信': 'wechat', u'浏览器': 'google-chrome'}


def application_open(target):
    try:
        application = application_dic.get(target)
        os.system('./shell/system_open %s &' % application)
    except Exception as err:
        print('application_open err:' + err)


def resolveJson(path):
    file = open(path, "rb")
    fileJson = json.load(file)

    return fileJson['access_token'], str(fileJson['device_id'])


def covertToOpus(input=audio_file_path, output=audio_file_opus_path):
    os.system('./shell/opus %s %s' % (input, output))


# def timeout_callback():
#     print('超时回调')
#
#
# def time_out(interval, callback=None):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             t = threading.Thread(target=func, args=args, kwargs=kwargs)
#             t.setDaemon(True)  # 设置主线程技术子线程立刻结束
#             t.start()
#             t.join(interval)  # 主线程阻塞等待interval秒
#             if t.is_alive() and callback:
#                 return threading.Timer(0, callback).start()  # 立即执行回调函数
#             else:
#                 return
#         return wrapper
#     return decorator


class TaskList:
    def __init__(self):

        self.cond = threading.Condition()
        self.data = []

    def isFull(self):
        return len(self.data) == 1

    def isEmpty(self):
        return len(self.data) == 0

    def get(self):

        self.cond.acquire()

        

        while self.isEmpty():
            self.cond.wait()

        print('[TaskList]->get:', self.data)
        temp = self.data.pop(0)

        self.cond.notify()
        self.cond.release()
        return temp

    def put(self, putInfo):
        self.cond.acquire()

        while self.isFull():
            self.cond.wait()
        print('[TaskList]->put:', putInfo)
        self.data.append(putInfo)

        self.cond.notify()
        self.cond.release()


class DeviceCapability():
    def __init__(self):
        self.friends = None

        # Debug Information
        self.request_id = lambda: "-".join(map(lambda x: "".join(map(lambda y: random.choice(
            string.ascii_lowercase + string.digits), range(x))), [8, 4, 4, 4, 12]))

        # Recorder
        self.DETECT_VAD_BACK = False
        self.reply_key = ''

        # Player
        self.resource_id = ''
        self.offset = 0
        self.audio_player_state = 'IDLE'
        self.payload_type = 'STARTED'
        #self.volume = volume_control('get')
        self.volume = ''


        
        # self.textCondition = TaskList()
        #self.textCondition.put(0)

        # DeviceCapability
        self.deviceCapability = {}

        # attachDeviceCapability
        self.attachDeviceCapability()

    def attachClient(self, friends):
        self.friends = friends

    def attachDeviceCapability(self):
        self.registerDeviceCapability('audio_player.audio_out', {
                                      'key': 'player', 'value': self.audioPlayerTreatment})
        self.registerDeviceCapability('interceptor.custom', {
                                      'key': 'interceptor', 'value': self.interceptorCustomTreatment})
        self.registerDeviceCapability('recognizer.stop_capture', {
                                      'key': 'recognizerstop', 'value': self.recognizerStopTreatment})

        self.registerDeviceCapability('recognizer.expect_reply', {
            'key': 'recognizerExpectReply', 'value': self.recognizerExpectReplyTreatment})
        self.registerDeviceCapability('speaker.set_volume',   {
                                      'key': 'speaker', 'value': self.speakerTreatment})
        self.registerDeviceCapability('recognizer.evaluate_result',   {
                                      'key': 'evaluate', 'value': self.evaluateTreatment})
        self.registerDeviceCapability('recognizer.trans_result',   {
                                      'key': 'translate', 'value': self.translateTreatment})


    def registerDeviceCapability(self, key, value):
        self.deviceCapability[key] = value

    def getDeviceCapability(self, key):
        if key in self.deviceCapability.keys() and self.deviceCapability.get(key).get('value') != None:
            yprint('getDeviceCapability: %s' % key)
            return self.deviceCapability.get(key).get('value')
        else:
            yprint('getDeviceCapability fails, %s is not in deviceCapability' % key)

    def implementDeviceCapability(self, **kwargs):
        rootNode = kwargs.get('rootNode')
        childNode = kwargs.get('childNode')

        try:
            # childNode = childNode.decode('utf-8')
            result = self.getDeviceCapability(childNode)

            if result:
                result(**kwargs)

        except Exception as err:
            print('implementDeviceCapability err: %s' % err)
        finally:
            pass

    def audioPlayTts(self, url):
        # 播放TTS提示音
        #rprint(url)
        # self.playerCondition.get()
        playback_play_tts(url)
        # self.playerCondition.put(0)

    def audioPlayerTreatment(self, *args, **kwargs):
        rootNode = kwargs.get('rootNode')
        if rootNode.get('payload').get('type') == 'TTS':

            # url = rootNode.get('payload').get('secure_url')
            result = rootNode.get('payload').get('url')

            # 播放TTS提示音
            self.audioPlayTts(result)

         
            print('[audioPlayerTreatment]kwargs', kwargs)
            # return 
            if 'header_name' in kwargs.keys() and kwargs.get('header_name') == kwargs.get("childNode"):
                if 'callback' in kwargs.keys():
                    kwargs.get('callback')(result)
                if 'scheduler' in kwargs.keys() and 'scheduler_id' in kwargs.keys():
                    print('remove job:', kwargs['scheduler_id'])
                    kwargs['scheduler'].remove_job(kwargs['scheduler_id'])
                if 'timer' in kwargs.keys():
                    kwargs.get('timer').stop()
                if 'condition' in kwargs.keys():
                    kwargs.get('condition').put(result)
                    # print(f'audioPlayerTreatment put:[{result}]')
                    # print('audioPlayerTreatment condition', kwargs.get('condition').data)

                    

       
        elif rootNode.get('payload').get('type') == 'RING':
            url = rootNode.get('payload').get('url')

            # 播放TTS提示音
            self.audioPlayTts(url)

        elif rootNode.get('payload').get('type') == 'PLAYBACK':
            resource_id = rootNode.get('payload').get('resource_id')
            offset = rootNode.get('payload').get('offset')

            if rootNode.get('payload').get('control') == 'PLAY':
                url = rootNode.get('payload').get('url')

                if self.resource_id == resource_id and self.offset == offset:
                    # 继续播放歌曲
                    self.audioPlayerSyncRequest(
                        resource_id, offset, "STARTED", "PLAYING")
                    playback_resume()
                else:
                    playback_stop()
                    self.audioPlayerSyncRequest(
                        resource_id, offset, "STARTED", "PLAYING")
                    # 开始播放歌曲
                    playback_play(url)

            elif rootNode.get('payload').get('control') == 'PAUSE':
                self.audioPlayerSyncRequest(
                    self.resource_id, self.offset, "PAUSED", "PAUSED")
                # 暂停歌曲
                playback_pause()

            elif rootNode.get('payload').get('control') == 'RESUME':
                self.audioPlayerSyncRequest(
                    self.resource_id, self.offset, "STARTED", "PLAYING")
                # 继续播放歌曲
                playback_resume()
        

    def interceptorCustomTreatment(self, *args, **kwargs):
        rootNode = kwargs.get('rootNode')
        intent = rootNode.get('payload').get('headerName')
        if intent == 'system.open.app':
            slots = rootNode.get('payload').get('data').get('contact')
            # 打开应用: 微信 .etc
            application_open(slots)

    def recognizerStopTreatment(self, *args, **kwargs):
        rootNode = kwargs.get('rootNode')

        self.DETECT_VAD_BACK = True

        bprint("send end tag start")

        try:
            self.friends.ws.send(bytes(end_tag))
        except Exception as err:
            rprint('recognizerStopTreatment: ' + err)

        bprint("send end tag success")
        # 检测到后端点则结束录音
        recordAudio_stop()

        # bprint("recognizerStopTreatment")
        # self.ws.send(bytes(end_tag))
    '''
    @param:
                        reply_key: string
                        timeout: int

    '''

    def recognizerExpectReplySubThread(self, reply_key, timeout):
        """
        # eventlet.monkey_patch()  #必须加这条代码
        # with eventlet.Timeout(4, False):   #设置超时时间为2秒
        #     print('consumer is ready...')
        #     self.playerCondition.get() #condition.get()
        #     self.playerCondition.put(0) #condition.get()
        #     self.reply_key = reply_key
        #     print('consumer is working...')
        #     recordAudio_start()
        #     print('consumer is end')
        #
        # print('跳过了输出')

        def timeout_callback():
            print('超时回调')


        def time_out(interval, callback=None):
            def decorator(func):
                def wrapper(*args, **kwargs):
                    t = threading.Thread(target=func, args=args, kwargs=kwargs)
                    t.setDaemon(True)  # 设置主线程技术子线程立刻结束
                    t.start()
                    t.join(interval)  # 主线程阻塞等待interval秒
                    if t.is_alive() and callback:
                        return threading.Timer(0, callback).start()  # 立即执行回调函数
                    else:
                        return
                return wrapper
            return decorator

        @time_out(2, timeout_callback)
        def subThread(self):
            print('consumer is ready...')
            self.playerCondition.get() #condition.get()
            bprint('consumer is get condition')

        subThread(self)
        gprint('consumer is jump out..')
        if self.playerCondition.isEmpty:
            self.playerCondition.put(0) #condition.get()

        self.reply_key = reply_key
        print('consumer is working...')
        recordAudio_start()
        print('consumer is end')


        """

    def recognizerExpectReplyTreatment(self, *args, **kwargs):
        rootNode = kwargs.get('rootNode')
        reply_key = rootNode.get('payload').get('reply_key')
        timeout = rootNode.get('payload').get('timeout')


        recognizerSubThread = threading.Thread(
            target= self.recognizerExpectReplySubThread, args=(reply_key, timeout, ))
        recognizerSubThread.start()

        # 原文链接：https://blog.csdn.net/weixin_42368421/article/details/101354628
        # my_timer = Timer(timeout, timeout_callback, [p])
        # my_timer.start()

        # recognizerExpectReplySubThread(self.playerCondition, reply_key, time_out)

    def speakerTreatment(self, *args, **kwargs):
        rootNode = kwargs.get('rootNode')
        volume = rootNode.get('payload').get('volume')
        volume_control('set', volume)
        self.volume = volume
        self.systemStateSyncRequest()

    def evaluateTreatment(self, *args, **kwargs):
        rootNode = kwargs.get('rootNode')
        total_score = rootNode.get('payload').get('data').get('simple_expression').get('total_score')
        rprint(f'total_score: {total_score}')

        self.sendGenerateText(f'得分为: {total_score}')

    def translateTreatment(self, *args, **kwargs):
        rootNode = kwargs.get('rootNode')
        original_text = rootNode.get('payload').get('data').get('src')
        translation_text = rootNode.get('payload').get('data').get('dst')
        rprint(f'original_text: [{original_text}], translation_text: [{translation_text}]')

        result = {'translation': translation_text, 'original': original_text}
        if 'header_name' in kwargs.keys() and kwargs.get('header_name') == kwargs.get("childNode"):
                if 'callback' in kwargs.keys():
                    kwargs.get('callback')(result)
                if 'scheduler' in kwargs.keys() and 'scheduler_id' in kwargs.keys():
                    print('remove job:', kwargs['scheduler_id'])
                    kwargs['scheduler'].remove_job(kwargs['scheduler_id'])
                if 'timer' in kwargs.keys():
                    kwargs.get('timer').stop()
                if 'condition' in kwargs.keys():
                    kwargs.get('condition').put(result)


    def parse_result_subThread(self, data_dict):

        result = data_dict.get('result')

        result_dict = json.loads(result)
        header_name_list = []
        feed_back = ''
        try:
            for i in result_dict.get('iflyos_responses'):
                headerName = str(i.get('header').get('name'))

           
                data_dict['rootNode'] = i
                data_dict['childNode'] = headerName
                self.implementDeviceCapability(**data_dict)
     

        except Exception as err:
            print('parse_result err: %s!' % err)

    def parse_result(self, *args, **kwargs):

        self.tparse = threading.Thread(
            target=self.parse_result_subThread, args=(kwargs, ))
        self.tparse.start()

    def systemStateSyncRequest(self):
        data = {'iflyos_header': {'authorization': 'Bearer ' + access_token,
                                  'device': {'device_id': device_id, 'ip': '192.168.1.1',
                                             'location': {'latitude': 22.5385, 'longitude': 113.936539},
                                             'platform': {'name': 'Linux', 'version': '8.1'}
                                             }},
                'iflyos_context': {'system': {'version': '1.0'},
                                   'recognizer': {'version': '1.0'},
                                   'speaker': {'version': '1.0', 'volume': self.volume, 'type': 'percent'},
                                   'audio_player': {'version': '1.0', 'playback': {'offset': self.offset, 'resource_id': self.resource_id, 'state': self.audio_player_state}},
                                   'playback_controller': {'version': '1.0'}
                                   },
                'iflyos_request': {'header': {
                    'name': 'system.state_sync',
                    'request_id': self.request_id()},
                "payload": {
                    "type": self.payload_type,
                    "resource_id": self.resource_id,
                    "offset": self.offset
                }
        }
        }

        jsondata = json.dumps(data)
        print(data)

        self.friends.ws.send(str(jsondata))

    '''
    @param:
                        resource_id: string
                        offset: int
                        payload_type: STARTED FAILED NEARLY_FINISHED FINISHED PAUSED
                        audio_player_state: PLAYING IDLE PAUSED
    '''

    def audioPlayerSyncRequest(self, resource_id, offset, payload_type, audio_player_state):

        self.audio_player_state = audio_player_state
        self.payload_type = payload_type
        self.offset = offset
        self.resource_id = resource_id

        data = {'iflyos_header': {'authorization': 'Bearer ' + access_token,
                                  'device': {'device_id': device_id, 'ip': '192.168.1.1',
                                             'location': {'latitude': 22.5385, 'longitude': 113.936539},
                                             'platform': {'name': 'Linux', 'version': '8.1'}
                                             }},
                'iflyos_context': {'system': {'version': '1.0'},
                                   'recognizer': {'version': '1.0'},
                                   'speaker': {'version': '1.0', 'volume': self.volume, 'type': 'percent'},
                                   'audio_player': {'version': '1.0', 'playback': {'offset': offset, 'resource_id': resource_id, 'state': audio_player_state}},
                                   'playback_controller': {'version': '1.0'}
                                   },
                'iflyos_request': {'header': {
                    'name': 'audio_player.playback.progress_sync',
                    'request_id': self.request_id()},
                "payload": {
                    "type": payload_type,
                    "resource_id": resource_id,
                    "offset": offset
                    # "failure_code": 1001
                }
        }
        }

        jsondata = json.dumps(data)
        print(data)

        self.friends.ws.send(str(jsondata))

    '''
    @param:
                        format: AUDIO_L16_RATE_16000_CHANNELS_1
                                        OPUS
                                        SPEEX_WB_QUALITY_9
    '''

    def sendAudioRequest(self, format='AUDIO_L16_RATE_16000_CHANNELS_1'):
        # print('sendRequest', 'access_token:' + access_token, 'device_id:' + str(device_id)

        data = {'iflyos_header': {'authorization': 'Bearer ' + access_token,
                                  'device': {'device_id': device_id, 'ip': '192.168.1.1',
                                             # 'location': {'latitude': 19.56519545, 'longitude': 109.40746014},
                                             'location': {'latitude': 22.5385, 'longitude': 113.936539},
                                             'platform': {'name': 'Linux', 'version': '8.1'}
                                             }},
                'iflyos_context': {'system': {'version': '1.0'},
                                   'recognizer': {'version': '1.0'},
                                   'speaker': {'version': '1.0', 'volume': self.volume, 'type': 'percent'},
                                   'audio_player': {'version': '1.0', 'playback': {'offset': self.offset, 'resource_id': self.resource_id, 'state': self.audio_player_state}},
                                   "interceptor": {
                    "version": "1.0",
                    "key": "12345678910",
                    "custom": {
                        "access_token": 'Bearer ' + access_token,
                        "device_id": device_id
                    }
                }
        },
            'iflyos_request': {'header': {
                'name': 'recognizer.audio_in',
                'request_id': self.request_id()},
            'payload': {
                        'reply_key':  self.reply_key,
                        'enable_vad': 'true',
                        'vad_eos': 300,
                        'profile': 'CLOSE_TALK',
                        'format': format,
                        'iflyos_wake_up': {
                            'score': 666,
                            'start_index_in_samples': 50,
                            'end_index_in_samples': 150,
                            'word': '蓝小飞',
                            'prompt': '我在'
                        }
                        }
        }
        }

        jsondata = json.dumps(data)
        print(data)

        self.friends.ws.send(str(jsondata))
    '''
    @param:
                        format: AUDIO_L16_RATE_16000_CHANNELS_1
                                        OPUS
                                        SPEEX_WB_QUALITY_9
    '''

    def sendAudioTransRequest(self, format='AUDIO_L16_RATE_16000_CHANNELS_1'):
        # print('sendRequest', 'access_token:' + access_token, 'device_id:' + str(device_id)

        data = {'iflyos_header': {'authorization': 'Bearer ' + access_token,
                                  'device': {'device_id': device_id, 'ip': '192.168.1.1',
                                             # 'location': {'latitude': 19.56519545, 'longitude': 109.40746014},
                                             'location': {'latitude': 22.5385, 'longitude': 113.936539},
                                             'platform': {'name': 'Linux', 'version': '8.1'}
                                             }},
                'iflyos_context': {'system': {'version': '1.0'},
                                   'recognizer': {'version': '1.0'},
                                   'speaker': {'version': '1.0', 'volume': self.volume, 'type': 'percent'},
                                   'audio_player': {'version': '1.0', 'playback': {'offset': self.offset, 'resource_id': self.resource_id, 'state': self.audio_player_state}},
                                   "interceptor": {
                    "version": "1.0",
                    "key": "12345678910",
                    "custom": {
                        "access_token": 'Bearer ' + access_token,
                        "device_id": device_id
                    }
                }
        },
            'iflyos_request': {'header': {
                'name': 'recognizer.audio_in',
                'request_id': self.request_id()},
            'payload': {
                        'reply_key':  self.reply_key,
                        'enable_vad': False,
                        'vad_eos': 300,
                        'profile': 'CLOSE_TALK',
                        'translation': True,
                        'format': format
                        # 'iflyos_wake_up': {
                        #     'score': 666,
                        #     'start_index_in_samples': 50,
                        #     'end_index_in_samples': 150,
                        #     'word': '蓝小飞',
                        #     'prompt': '我在'
                        # }
                        }
        }
        }

        jsondata = json.dumps(data)
        print(data)

        self.friends.ws.send(str(jsondata))
    def sendEvaluateLevelsRequest(self):
        url_evaluate_levels = "https://api.iflyos.cn/external/ocr/evaluate/levels"
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        ret = requests.get(url_evaluate_levels, headers=headers)
        if ret:
            return ret.json()
        return ''

    def sendEvaluateQuestionsRequest(self, level):
        url_evaluate_questions = "https://api.iflyos.cn/external/ocr/evaluate/get_question"
        params = {
            'level_id': level,
            'type': 'answer'
        }
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        ret = requests.get(url_evaluate_questions, params=params, headers=headers)
        if ret:
            return ret.json()
        return ''

    '''
    @param:
                        format: AUDIO_L16_RATE_16000_CHANNELS_1
                                        OPUS
                                        SPEEX_WB_QUALITY_9
    '''

    def sendAudioEvaluteRequest(self, format='AUDIO_L16_RATE_16000_CHANNELS_1', text = ''):
        # print('sendRequest', 'access_token:' + access_token, 'device_id:' + str(device_id)

        data = {'iflyos_header': {'authorization': 'Bearer ' + access_token,
                                  'device': {'device_id': device_id, 'ip': '192.168.1.1',
                                             # 'location': {'latitude': 19.56519545, 'longitude': 109.40746014},
                                             'location': {'latitude': 22.5385, 'longitude': 113.936539},
                                             'platform': {'name': 'Linux', 'version': '8.1'}
                                             }},
                'iflyos_context': {'system': {'version': '1.0'},
                                   'recognizer': {'version': '1.0'},
                                   'speaker': {'version': '1.0', 'volume': self.volume, 'type': 'percent'},
                                   'audio_player': {'version': '1.0', 'playback': {'offset': self.offset, 'resource_id': self.resource_id, 'state': self.audio_player_state}},
                                   "interceptor": {
                    "version": "1.0",
                    "key": "12345678910",
                    "custom": {
                        "access_token": 'Bearer ' + access_token,
                        "device_id": device_id
                    }
                }
        },
            'iflyos_request': {'header': {
                'name': 'recognizer.audio_in',
                'request_id': self.request_id()},
            'payload': {
                        'reply_key':  self.reply_key,
                        'enable_vad': True,
                        'vad_eos': 300,
                        'profile': 'EVALUATE',
                        #'translation': True,
                        'format': format,
                        'evaluate':
                        {
                            'language': 'en_us',
                            'category': 'read_choice',
                            'text': text
                            # 'text': '[word]\nwelcome'
                        }
                        }
        }
        }

        jsondata = json.dumps(data)
        print(data)

        self.friends.ws.send(str(jsondata))
 

    '''
    @param:
                        text: string
    '''
    def sendTextRequest(self, text, translation = False, with_tts = True):
        # print('sendRequest', 'access_token:' + access_token, 'device_id:' + str(device_id)
        '''
                'iflyos_context': {'system': {'version': '1.0'},
                                   'recognizer': {'version': '1.0'},
                                   'speaker': {'version': '1.0', 'volume': self.volume, 'type': 'percent'},
                                   'audio_player': {'version': '1.0', 'playback': {'offset': self.offset, 'resource_id': self.resource_id, 'state': self.audio_player_state}},
                                   },
        '''

        data = {'iflyos_header': {'authorization': 'Bearer ' + access_token,
                                  'device': {'device_id': device_id, 'ip': '192.168.1.1',
                                             'location': {'latitude': 22.5385, 'longitude': 113.936539},
                                             'platform': {'name': 'Linux', 'version': '8.1'}
                                             }},
                'iflyos_context': {'system': {'version': '1.0'},
                                   'recognizer': {'version': '1.0'},
                                   'speaker': {'version': '1.0', 'volume': self.volume, 'type': 'percent'},
                                   'audio_player': {'version': '1.0', 'playback': {'offset': self.offset, 'resource_id': self.resource_id, 'state': self.audio_player_state}},
                                   },
                'iflyos_request': {'header': {
                    'name': 'recognizer.text_in',
                    'request_id': self.request_id()},
            'payload': {
                        'reply_key':  self.reply_key,
                        'query': text,
                        'with_tts': with_tts,
                        'translation': translation,
                        'iflyos_wake_up': {
                            'score': 666,
                            'start_index_in_samples': 50,
                            'end_index_in_samples': 150,
                            'word': '蓝小飞',
                            'prompt': '我在'
                        }}
        }
        }
        # print str(data)
        jsondata = json.dumps(data)
        print(data)

        self.friends.ws.send(str(jsondata))

    '''
    @param:
                        text: string
    '''
    def sendGenerateText(self, text):
        data = {'iflyos_header': {'authorization': 'Bearer ' + access_token,
                                  'device': {'device_id': device_id, 'ip': '192.168.1.1',
                                             'location': {'latitude': 22.5385, 'longitude': 113.936539},
                                             'platform': {'name': 'Linux', 'version': '8.1'}
                                             }},
                'iflyos_context': {'system': {'version': '1.3'},
                                   'recognizer': {'version': '1.2'},
                                   'speaker': {'version': '1.0', 'volume': self.volume, 'type': 'percent'},
                                   'audio_player': {'version': '1.0', 'playback': {'offset': self.offset, 'resource_id': self.resource_id, 'state': self.audio_player_state}},
                                   },
                'iflyos_request': {'header': {
                    'name': 'audio_player.tts.text_in',
                    'request_id': self.request_id()},
                    'payload': {
                    "text": text
                }
        }
        }
        
        # data = {"iflyos_header":{"authorization":'Bearer ' + access_token,"device":{"device_id":device_id,"platform":{"name":"FreeRTOS","version":"10.2.1"}}},"iflyos_context":{"system":{"version":"1.3","firmware_version":"1026"},"recognizer":{"version":"1.1"},"audio_player":{"version":"1.2","playback":{"state":"IDLE"}},"speaker":{"version":"1.0","volume":100}},"iflyos_request":{"header":{"name":"audio_player.tts.text_in","request_id":"manual-00000000-22cc-584f-9e00-0b7da1e7f5d2"},"payload":{"text":"从现在开始，我将教你学习“自然拼读”魔法。经过两年的学习"}}}
        # print str(data)
        jsondata = json.dumps(data)
        print(data)

        self.friends.ws.send(str(jsondata))

    def send_audio_chunk(self, chunk):
        # self.DETECT_VAD_BACK = False
        if self.friends:
            self.friends.ws.send_binary(chunk)

    '''
    @param:
                        file_path: string
                        format: AUDIO_L16_RATE_16000_CHANNELS_1
                                        OPUS
                                        SPEEX_WB_QUALITY_9
    '''

    def send(self, file_path, format='OPUS'):
        rprint("send time:%s" % datetime.datetime.now())
        self.DETECT_VAD_BACK = False

        print('DeviceCapability send {} format:{}'.format(file_path, format))
        # 读取fifo
        #file_object = open(file_path, 'rb', 1)
        file_object = open(file_path, 'rb')
        try:
            index = 1
            while True:
                if self.DETECT_VAD_BACK:
                    rprint("stop end time:%s" % datetime.datetime.now())
                    self.DETECT_VAD_BACK = False
                    break

                if format == 'AUDIO_L16_RATE_16000_CHANNELS_1':
                    # print('640')
                    chunk = file_object.read(640)
                elif format == 'OPUS':
                    # print('96')
                    chunk = file_object.read(96)
                    # chunk = file_object.read(96)
                elif format == 'SPEEX_WB_QUALITY_9':
                    # print('86')
                    chunk = file_object.read(86)

                # chunk = file_object.read(1280)
                if not chunk:
                    break

                # .send_binary
                # if index == 1:
                    # print type(chunk)

                self.friends.ws.send_binary(chunk)

                index += 1
                # time.sleep(0.04)
                # print("index:%d"%index)
        except Exception as err:
            print('send err:%s' % err)

        finally:
            # print str(index) + ", read len:" + str(len(chunk)) + ", file tell:" + str(file_object.tell())
            file_object.close()

        self.friends.ws.send(bytes(end_tag))
        bprint("------send end -------")
        rprint("end time:%s" % datetime.datetime.now())


class Client():
    def __init__(self):
        # 生成鉴权参数
        # ts = str(int (time.time()))
        # tmp = app_id + ts
        # hl = hashlib.md5()
        # hl.update(tmp.encode(encoding='utf-8'))
        # my_sign = hmac.new(api_key,  hl.hexdigest(), sha1).digest()
        # signa = base64.b64encode(my_sign)

        self.mDeviceCapability = None
        self.ws_recv_timer = None
        self.ws_custom_recv_timer = None

        self.task_list = TaskList()
        # self.scheduler = BlockingScheduler()

        # Connect to IFlyos
        # self.connect_iflyos()

    def attachDeviceCapability(self, friends):
        self.mDeviceCapability = friends

    def connect_iflyos(self):
        # Websocket To IFlyos
        # self.ws = websockets.connect(
        self.create_ws()
        self.create_run_ws_recv_task()

        gprint('[ws]connect_iflyos')

    def create_ws(self):
        param = base_url + "?token=" + access_token + "&device_id=" + device_id
        self.ws = create_connection(
            param)
        print(param)
    def create_run_ws_recv_task(self):
        def func_timer():
            self.ws_recv()
            self.ws_recv_timer = threading.Timer(1, func_timer)
            self.ws_recv_timer.start()
        def create_ws_recv_timer():
            self.ws_recv_timer = threading.Timer(1, func_timer)
            self.ws_recv_timer.start()
        # 创建定时任务自动接受
        create_ws_recv_timer()
        # self.trecv = threading.Thread(target=self.ws_recv)
        # self.trecv.start()
    def cancel_run_ws_recv_task(self):
        if self.ws_recv_timer.is_alive():
            self.ws_recv_timer.cancel()

    def get_ws_result(self, **kwargs):
        print('create_custom_ws_recv_task[func_timer]', kwargs)
        self.ws_recv(**kwargs)

    def create_custom_ws_recv_task(self, *args, **kwargs):
        print('[create_custom_ws_recv_task]', args, kwargs)
        # kwargs['scheduler'] = self.scheduler
        # kwargs['scheduler_id'] = "timer"

        def func_timer(kwargs):
            # nonlocal args
            # nonlocal kwargs
            print('create_custom_ws_recv_task[func_timer]', kwargs)
            self.ws_recv(**kwargs)
            # self.ws_custom_recv_timer = threading.Timer(1, func_timer)
            # self.ws_custom_recv_timer.start()
       
            # scheduler.remove_job(job_id=job_id)
            # self.ws_custom_recv_timer = threading.Timer(1, func_timer)
            # self.ws_custom_recv_timer.start()
        if 'timer' in kwargs.keys():
            print('123')
            timer_callback = functools.partial(self.ws_timer_receive, initParams=kwargs)
            kwargs['timer'].timeout.connect(timer_callback)
            print('456')
            kwargs['timer'].start(1000)
            print('789')


        # self.cancel_custom_ws_recv_task()
        # 创建定时任务自动接受
        # self.scheduler.add_job(func_timer, id = 'timer', trigger='interval', seconds=1, args=[kwargs,])
        # self.scheduler.start()

    def cancel_custom_ws_recv_task(self):
        if self.ws_custom_recv_timer and self.ws_custom_recv_timer.is_alive():
            print("cancel_custom_ws_recv_task")
            self.ws_custom_recv_timer.cancel()


    def ws_recv(self, *args, **kwargs):
        try:
            if self.ws.connected:

                result = self.ws.recv()
                # rprint(type(result))

                # result = str(result_raw, encoding="utf-8
                if len(result) == 0:
                    # print("receive result end"
                    rprint("ws : receive result end")
                    return

                bprint(result)
                kwargs['result'] = result
                self.mDeviceCapability.parse_result(*args, **kwargs)

        except websocket.WebSocketConnectionClosedException:
            print("receive result end")

    def sendAudioRequest(self, format):
        self.mDeviceCapability.sendAudioRequest(format)
        print('sendAudioRequest')
    def sendAudioTransRequest(self, format):
        self.mDeviceCapability.sendAudioTransRequest(format)
        print('sendAudioTransRequest')
    def sendAudioEvaluteRequest(self, format, text):
        self.mDeviceCapability.sendAudioEvaluteRequest(format, text)
    def sendEvaluateLevels(self):
        return self.mDeviceCapability.sendEvaluateLevelsRequest()
    def sendEvaluateQuestions(self, level):
        return self.mDeviceCapability.sendEvaluateQuestionsRequest(level)
    def send_audio_chunk(self, chunk):
        self.mDeviceCapability.send_audio_chunk(chunk)

    def send(self, audio_file_path, format=format):
        self.mDeviceCapability.send(audio_file_path, format=format)
        print('send audio')

    def sendTextRequest(self, text, translation = False, with_tts = True):
        self.mDeviceCapability.sendTextRequest(text, translation, with_tts)

    def sendGenerateText(self, text):
        self.mDeviceCapability.sendGenerateText(text)

    def close(self):
        self.ws.close()
        print("connection closed")


def showIntroduction(switch):
    if switch:
        print("demo示例为输入命令，调用对应的函数，使用IFLYOS SDK完成文本理解，语义理解，文本合成等功能，如：")
        print("auth命令，进行用户隐式授权，目前与IFLYOS 云端进行交互首先需要完成授权, 所以第一步必须是输入该命令；")
        print("c命令，创建IFLYOS代理，与IFLYOS 云端进行交互都是通过代理发送消息的方式进行, 所以第二步必须是输入该命令；")
        # print("w命令，发送外部唤醒命令唤醒AIUI，AIUI只有在唤醒过后才可以交互；")
        print("wr命令，单次读取本地pcm音频文件，写入sdk，sdk会返回云端识别的听写，语义结果；")
        print("wrt命令，字符串文本写入sdk，sdk会返回云端识别的语义结果；")
        print("r命令，开始录音, s命令停止录音，录音文件会更新wr所读取的本地pcm音频文件，进行语音识别；")
        print("rt命令，开始录音, s命令停止录音，录音文件会更新wr所读取的本地pcm音频文件，进行语音翻译；")
        print("re命令，开始录音, s命令停止录音，录音文件会更新wr所读取的本地pcm音频文件，进行口语评测；")
        print("s命令，停止录音, 录音文件会更新wr所读取的本地pcm音频文件；")
        print("rp命令，继续播放；")
        print("sp命令，停止播放；")
        print("pp命令，暂停播放；")
        print("gt命令，合成文本;   ")
        # print("stts命令，单合成示例，返回合成的音频，demo将音频保存为本地的pcm文件；")
        # print("ptts命令，单合成示例，暂停；")
        # print("rtts命令，单合成示例，恢复；")
        # print("ctts命令，单合成示例，取消；")
        print("help命令，显示本demo提供的示例的介绍；")


globalFuncIflytek = {}


def registerCallBack(key, value):
    global globalFuncIflytek
    globalFuncIflytek[key] = value


def createAgent():
    global client
    global gDeviceCapability

    try:
        client = Client()
        gDeviceCapability = DeviceCapability()
        gDeviceCapability.attachClient(client)
        client.attachDeviceCapability(gDeviceCapability)
        client.connect_iflyos()
    except Exception as err:
        rprint('createAgent err:%s' % err)

    gprint("[createAgent]success!")
    return (client, gDeviceCapability)


def writeRecogAudio(format='AUDIO_L16_RATE_16000_CHANNELS_1'):
    #format = 'OPUS'
    format = 'AUDIO_L16_RATE_16000_CHANNELS_1'
    # format = 'SPEEX_WB_QUALITY_9'

    if format == 'AUDIO_L16_RATE_16000_CHANNELS_1':
        print('format: ' + format + " audio_file_opus_path:" + audio_file_path)
        client.sendAudioRequest(format)
        client.send(audio_file_path, format=format)
    elif format == 'OPUS':
        print('format: ' + format + " audio_file_opus_path:" + audio_file_opus_path)
        # covertToOpus()
        client.sendAudioRequest(format)
        client.send(audio_file_opus_path, format=format)

    elif format == 'SPEEX_WB_QUALITY_9':

        # song = AudioSegment.from_wav(audio_file_path)
        # song.export(audio_file_opus_path, format="raw", bitrate='32k', parameters=["-ar", 16000, "-ac", 1, "-acodec", "libopus", "-ab", "32k", "-maxrate",  "32k",  "-minrate", "32k" ,"-application", "voip"])
        # covertToOpus()
        client.sendAudioRequest(format)
        client.send(audio_file_speex_path, format=format)


# def generate_text(text="好的,已帮您打开客厅灯"):
# 最后，告诉以上个小号门：在阅读处发段或小故事之前，先看
# def generate_text(text="i am fine."):
def generate_text(text="最后，告诉以上个小号门：在阅读处发段或小故事之前，先看"):
    client.sendGenerateText(text)


def writeText(inputText=''):
    if not inputText:
        inputText=input("请输入文本内容:")
    # client.sendTextRequest('给我定后天5点的闹钟')
    if inputText:
        client.sendTextRequest(inputText)

# task_list = TaskList()

def get_tts(*args, **kwargs):
    if 'text' in kwargs.keys():
        result = ''
        client.sendGenerateText(kwargs.get('text'))
        return result


        # kwargs['condition'] = client.task_list
        # kwargs['header_name'] = "audio_player.audio_out"

        # client.cancel_run_ws_recv_task()
        # client.create_custom_ws_recv_task(**kwargs)

        client.sendGenerateText(kwargs.get('text'))

        # result = client.task_list.get()
        # client.cancel_custom_ws_recv_task()

        # return result
    
        #self.textCondition.put(0)
    # client.create_custom_ws_recv_task(condition = client.task_list, header_name = "audio_player.audio_out")

    # client.sendGenerateText(text)
    # print('get_tts get condition [start]', client.task_list.data)
    # result = client.task_list.get()
    # print('get_tts get condition [end]', client.task_list.data)
    # client.cancel_custom_ws_recv_task()

    

def get_traslate_text(*args, **kwargs):
    if 'text' in kwargs.keys():
        kwargs['condition'] = client.task_list
        kwargs['header_name'] = "recognizer.trans_result"

        # client.cancel_run_ws_recv_task()
        client.create_custom_ws_recv_task(**kwargs)

        client.sendTextRequest(kwargs.get('text'), translation = True)

        result = client.task_list.get()
        # client.cancel_custom_ws_recv_task()

        return result


def wechatWriteText(text='现在几点'):
    writeText(text)
    client.mDeviceCapability.textCondition.get()
    reply_text = client.mDeviceCapability.text
    print('text receive:', reply_text)
    if reply_text:
        return reply_text
    else:
        return "这个问题太难了，问倒我了"


def recordAudio():
    global audio_file_path
    os.system('arecord -r 16000 -f S16_LE -c 1 %s &' % audio_file_path)


def stopRecordAudio():
    # cmd = 'kill \$\(ps -elf \| grep arecord \| grep -v grep \| awk \'\{ print \$4 \}\' \) '
    os.system('./shell/stop_record.sh')


def open_record_devce():
    global g_record_stream
    global g_CHUNK

    if g_record_stream == None:
        CHUNK = 640
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

        g_record_stream = stream
        g_CHUNK = CHUNK

def read_stream():
    try:
        return g_record_stream.read(g_CHUNK, exception_on_overflow = False)
    except Exception as err:
        print(err)

def close_record_device():
    if g_record_stream:
        g_record_stream.stop_stream()
        g_record_stream.close()


def authorization():
    import os
    global authorization_file
    global access_token_file

    if os.path.exists(authorization_file):
        print('access_token or device_id is not offered!')
        print('run this script[%s] to generate access_token' %
              authorization_file)
        dirname_local=os.path.dirname(authorization_file)
        filename_local=os.path.basename(authorization_file)
        os.system(f"cd {dirname_local} && ./{filename_local}")
        if os.path.exists(access_token_file):
            print('access_token and device_id generated success, refer this!')
            global access_token
            global device_id
            (access_token, device_id) = resolveJson(access_token_file)

            print(access_token, device_id)
            print('OK!')
    else:
        print('cannot find %s exit!' % authorization_file)
        return

def exit_app(_signum='', _frame=''):
    import traceback
    try:
        # 等一等子线程销毁
        # time.sleep(0.5)
        sys.exit(1)
    except:
        traceback.print_exc()
        os._exit(0)
    finally:
        close_record_device()

def init():
    import signal
    signal.signal(signal.SIGINT, exit_app)
    signal.signal(signal.SIGTERM, exit_app)

def evs_app_init():
    # init
    init()
    authorization()
    createAgent()
    # open_record_devce()

def main():
    showIntroduction(False)
    registerCallBack('c', createAgent)
    registerCallBack('wr', writeRecogAudio)
    registerCallBack('wrt', writeText)
    registerCallBack('wxwrt', wechatWriteText)
    registerCallBack('auth', authorization)
    registerCallBack('r', recordAudio_start)
    registerCallBack('rf', recordAudioTrans_start)
    registerCallBack('rt', recordAudioTrans_start)
    registerCallBack('re', evaluate_start)
    registerCallBack('s', recordAudio_stop)
    registerCallBack('rp', playback_resume)
    registerCallBack('sp', playback_stop)
    registerCallBack('pp', playback_pause)
    registerCallBack('gt', generate_text)

    print(globalFuncIflytek)
    print('目前系统的编码为：', sys.getdefaultencoding())

    # init
    init()
    authorization()
    createAgent()
    open_record_devce()

    while True:
        inputText = input('请输入:')
        # inputText = raw_input('请输入:')
        if inputText == 'break':
            print('GoodBye')
            sys.exit(1)
        if inputText == 'h':
            showIntroduction(True)

        try:
            inputTextList = inputText.split()
            if len(inputTextList) == 1:
                func = globalFuncIflytek.get(str(inputText))
                func()
            elif len(inputTextList) == 2:
                func = globalFuncIflytek.get(str(inputTextList[0]))
                print(inputTextList[1])
                func(inputTextList[1])
        except Exception as err:
            print('inputText err:{}'.format(err))
if __name__ == '__main__':
    main()
