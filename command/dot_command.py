import requests

from config import apiBaseUrl, apiGroupInfo, ADMIN_LIST
from command.command import send_public_msg, send_private_msg


def dot_send_msg(message_info:dict):
    raw_message = message_info['message'][5:].strip()
    if message_info['is_group']:
        api_url = apiBaseUrl + apiGroupInfo
        data = {
            'group_id':message_info.get('group_qq')
        }
        response = requests.post(api_url,data=data)
        if response.status_code == 200:
            group_name = response.json()['data']['group_name']
            send_string = f'来自群:{group_name},QQ:{message_info["sender_qq"]}的消息:\n{raw_message}'
            send_private_msg(send_string, ADMIN_LIST[0])
        else:
            return
    else:
        send_string = f'来自QQ:{message_info["sender_qq"]}的消息:\n{raw_message}'
        send_private_msg(send_string, ADMIN_LIST[0])


def show_command_doc(message_info):
    send_string = '签到/打卡\n单抽/十连/百连1-7\n要礼物 热榜\n冷知识 点歌\n'\
                  '搜索格式:\n百度/搜索1-3 内容\n百度：百度百科\n搜索1'\
                  '：wikipedia(暂不可用)\n搜索2：萌娘百科\n搜索3：touhouwiki'
    if message_info['is_private']:
        send_private_msg(send_string, message_info['sender_qq'])
    elif message_info['is_group']:
        send_public_msg(send_string, message_info['group_qq'])


def calculate_phasor(message_info):
    from math import sin, cos, radians, sqrt, atan, degrees
    raw_message:str = message_info['message'][7:]
    if raw_message[0] == '+':
        try:
            args:list = list(map(lambda x:int(x), raw_message[1:].split()))
            real = args[0] * cos(radians(args[1])) + args[2] * cos(radians(args[3]))
            imag = args[0] * sin(radians(args[1])) + args[2] * sin(radians(args[3]))
            magnitude = sqrt(real ** 2 + imag ** 2)
            angle = degrees(atan(float(real) / imag)) if imag != 0 else 0
            send_string = f'{args[0]}e^{args[1]}j + {args[2]}e^{args[3]}j = ' + '%.2fe^%.2fj'%(magnitude,angle)
            if message_info['is_private']:
                send_private_msg(send_string, message_info['sender_qq'])
            elif message_info['is_group']:
                send_public_msg(send_string, message_info['group_qq'])
        except Exception as e:
            send_private_msg(e, message_info['sender_qq'])
    elif raw_message[0] == '-':
        try:
            args: list = list(map(lambda x:int(x), raw_message[1:].split()))
            real = args[0] * cos(radians(args[1])) - args[2] * cos(radians(args[3]))
            imag = args[0] * sin(radians(args[1])) - args[2] * sin(radians(args[3]))
            magnitude = sqrt(real ** 2 + imag ** 2)
            angle = degrees(atan(float(real) / imag)) if imag != 0 else 0
            send_string = f'{args[0]}e^{args[1]}j + {args[2]}e^{args[3]}j = ' + '%.2fe^%.2fj'%(magnitude,angle)
            if message_info['is_private']:
                send_private_msg(send_string, message_info['sender_qq'])
            elif message_info['is_group']:
                send_public_msg(send_string, message_info['group_qq'])
        except Exception as e:
            send_private_msg(e, message_info['sender_qq'])
    elif raw_message[0] == '*':
        try:
            args: list = list(map(lambda x:int(x), raw_message[1:].split()))
            real = args[0] * args[2]
            imag = (args[1] + args[3]) % 360
            send_string = f'{args[0]}e^{args[1]}j * {args[2]}e^{args[3]}j = ' + '%.2fe^%.2fj'%(real, imag)
            if message_info['is_private']:
                send_private_msg(send_string, message_info['sender_qq'])
            elif message_info['is_group']:
                send_public_msg(send_string, message_info['group_qq'])
        except Exception as e:
            send_private_msg(e, message_info['sender_qq'])
    elif raw_message[0] == '/':
        try:
            args: list = list(map(lambda x:int(x), raw_message[1:].split()))
            real = float(args[0]) / args[2] if int(args[2]) != 0 else 0
            imag = (args[1] - args[3]) % 360
            if not real:
                send_string = '分母不能为等于或接近0的数'
            else:
                send_string = f'{args[0]}e^{args[1]}j * {args[2]}e^{args[3]}j = ' + '%.2fe^%.2fj'%(real, imag)
            if message_info['is_private']:
                send_private_msg(send_string, message_info['sender_qq'])
            elif message_info['is_group']:
                send_public_msg(send_string, message_info['group_qq'])
        except Exception as e:
            send_private_msg(e, message_info['sender_qq'])
    else:
        send_string = '表达式错误或不支持'
        if message_info['is_private']:
            send_private_msg(send_string, message_info['sender_qq'])
        elif message_info['is_group']:
            send_public_msg(send_string, message_info['group_qq'])

