#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import sys
import logging
import asyncio
import random
from time import strftime
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from emoji import emojize

# 初始化日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ===== 可配置参数 =====
UPDATE_SECOND_05 = 5    # 每分钟的第5秒执行更新
UPDATE_SECOND_35 = 35   # 每分钟的第35秒执行更新

# 可选的字体名称（选择其中一个）
FONT_NAME = "Sans-serif Bold"  # 可选值："Serif Bold Italic", "Sans-serif Bold", "CIRCULAR Regular", "Moonscape Regular", "MonoSpace Regular"

# 根据选择的字体名称返回对应的转换函数
def get_font_converter(font_name):
    if font_name == "Serif Bold Italic":
        # 使用数学字母符号模拟Serif Bold Italic
        math_symbols = {
            'A': '𝒜', 'B': 'ℬ', 'C': '𝒞', 'D': '𝒟', 'E': 'ℰ', 'F': 'ℱ', 'G': '𝒢',
            'H': 'ℋ', 'I': 'ℐ', 'J': '𝒥', 'K': '𝒦', 'L': 'ℒ', 'M': 'ℳ', 'N': '𝒩',
            'O': '𝒪', 'P': '𝒫', 'Q': '𝒬', 'R': 'ℛ', 'S': '𝒮', 'T': '𝒯', 'U': '𝒰',
            'V': '𝒱', 'W': '𝒲', 'X': '𝒳', 'Y': '𝒴', 'Z': '𝒵',
            'a': '𝒶', 'b': '𝒷', 'c': '𝒸', 'd': '𝒹', 'e': 'ℯ', 'f': '𝒻', 'g': 'ℊ',
            'h': '𝒽', 'i': '𝒾', 'j': '𝒿', 'k': '𝓀', 'l': '𝓁', 'm': '𝓂', 'n': '𝓃',
            'o': 'ℴ', 'p': '𝓅', 'q': '𝓆', 'r': '𝓇', 's': '𝓈', 't': '𝓉', 'u': '𝓊',
            'v': '𝓋', 'w': '𝓌', 'x': '𝓍', 'y': '𝓎', 'z': '𝓏',
            '0': '𝟘', '1': '𝟙', '2': '𝟚', '3': '𝟛', '4': '𝟜', '5': '𝟝', '6': '𝟞',
            '7': '𝟟', '8': '𝟠', '9': '𝟡'
        }
        return lambda text: ''.join([math_symbols.get(c, c) for c in text])
    
    elif font_name == "Sans-serif Bold":
        # 使用数学字母符号模拟Sans-serif Bold
        math_symbols = {
            'A': '𝗔', 'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚',
            'H': '𝗛', 'I': '𝗜', 'J': '𝗝', 'K': '𝗞', 'L': '𝗟', 'M': '𝗠', 'N': '𝗡',
            'O': '𝗢', 'P': '𝗣', 'Q': '𝗤', 'R': '𝗥', 'S': '𝗦', 'T': '𝗧', 'U': '𝗨',
            'V': '𝗩', 'W': '𝗪', 'X': '𝗫', 'Y': '𝗬', 'Z': '𝗭',
            'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳', 'g': '𝗴',
            'h': '𝗵', 'i': '𝗶', 'j': '𝗷', 'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻',
            'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿', 's': '𝘀', 't': '𝘁', 'u': '𝘂',
            'v': '𝘃', 'w': '𝘄', 'x': '𝘅', 'y': '𝘆', 'z': '𝘇',
            '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲',
            '7': '𝟳', '8': '𝟴', '9': '𝟵'
        }
        return lambda text: ''.join([math_symbols.get(c, c) for c in text])
    
    elif font_name == "CIRCULAR Regular":
        # 使用特殊字符模拟CIRCULAR Regular
        special_chars = {
            'A': 'Ⓐ', 'B': 'Ⓑ', 'C': 'Ⓒ', 'D': 'Ⓓ', 'E': 'Ⓔ', 'F': 'Ⓕ', 'G': 'Ⓖ',
            'H': 'Ⓗ', 'I': 'Ⓘ', 'J': 'Ⓙ', 'K': 'Ⓚ', 'L': 'Ⓛ', 'M': 'Ⓜ', 'N': 'Ⓝ',
            'O': 'Ⓞ', 'P': 'Ⓟ', 'Q': 'Ⓠ', 'R': 'Ⓡ', 'S': 'Ⓢ', 'T': 'Ⓣ', 'U': 'Ⓤ',
            'V': 'Ⓥ', 'W': 'Ⓦ', 'X': 'Ⓧ', 'Y': 'Ⓨ', 'Z': 'Ⓩ',
            'a': 'ⓐ', 'b': 'ⓑ', 'c': 'ⓒ', 'd': 'ⓓ', 'e': 'ⓔ', 'f': 'ⓕ', 'g': 'ⓖ',
            'h': 'ⓗ', 'i': 'ⓘ', 'j': 'ⓙ', 'k': 'ⓚ', 'l': 'ⓛ', 'm': 'ⓜ', 'n': 'ⓝ',
            'o': 'ⓞ', 'p': 'ⓟ', 'q': 'ⓠ', 'r': 'ⓡ', 's': 'ⓢ', 't': 'ⓣ', 'u': 'ⓤ',
            'v': 'ⓥ', 'w': 'ⓦ', 'x': 'ⓧ', 'y': 'ⓨ', 'z': 'ⓩ',
            '0': '⓪', '1': '⓫', '2': '⓬', '3': '⓭', '4': '⓮', '5': '⓯', '6': '⓰',
            '7': '⓱', '8': '⓲', '9': '⓳'
        }
        return lambda text: ''.join([special_chars.get(c, c) for c in text])
    
    elif font_name == "Moonscape Regular":
        # 使用Emoji模拟Moonscape Regular（这里只是示例，实际可能需要其他方式）
        return lambda text: text  # 实际上无法直接模拟，这里返回原文本
    
    elif font_name == "MonoSpace Regular":
        # 使用等宽字符模拟MonoSpace Regular
        monospace_chars = {
            'A': 'Ａ', 'B': 'Ｂ', 'C': 'Ｃ', 'D': 'Ｄ', 'E': 'Ｅ', 'F': 'Ｆ', 'G': 'Ｇ',
            'H': 'Ｈ', 'I': 'Ｉ', 'J': 'Ｊ', 'K': 'Ｋ', 'L': 'Ｌ', 'M': 'Ｍ', 'N': 'Ｎ',
            'O': 'Ｏ', 'P': 'Ｐ', 'Q': 'Ｑ', 'R': 'Ｒ', 'S': 'Ｓ', 'T': 'Ｔ', 'U': 'Ｕ',
            'V': 'Ｖ', 'W': 'Ｗ', 'X': 'Ｘ', 'Y': 'Ｙ', 'Z': 'Ｚ',
            'a': 'ａ', 'b': 'ｂ', 'c': 'ｃ', 'd': 'ｄ', 'e': 'ｅ', 'f': 'ｆ', 'g': 'ｇ',
            'h': 'ｈ', 'i': 'ｉ', 'j': 'ｊ', 'k': 'ｋ', 'l': 'ｌ', 'm': 'ｍ', 'n': 'ｎ',
            'o': 'ｏ', 'p': 'ｐ', 'q': 'ｑ', 'r': 'ｒ', 's': 'ｓ', 't': 'ｔ', 'u': 'ｕ',
            'v': 'ｖ', 'w': 'ｗ', 'x': 'ｘ', 'y': 'ｙ', 'z': 'ｚ',
            '0': '０', '1': '１', '2': '２', '3': '３', '4': '４', '5': '５', '6': '６',
            '7': '７', '8': '８', '9': '９'
        }
        return lambda text: ''.join([monospace_chars.get(c, c) for c in text])
    
    else:
        # 默认返回原文本
        return lambda text: text

# 获取当前选择的字体转换函数
font_converter = get_font_converter(FONT_NAME)

# 选择一组表情符号（可自定义）
random_emojis = [
    ":smile:", ":heart:", ":star:", ":fire:", ":rocket:", 
    ":tada:", ":sparkles:", ":clap:", ":thumbsup:", ":ok_hand:"
]

# API 认证
api_auth_file = 'api_auth'
if not os.path.exists(api_auth_file + '.session'):
    api_id = input('api_id: ')
    api_hash = input('api_hash: ')
else:
    api_id = 123456  # 默认值（仅测试用）
    api_hash = '00000000000000000000000000000000'

client1 = TelegramClient(api_auth_file, api_id, api_hash)

# 主逻辑：每秒检查时间，按规则更新 Last Name
async def change_name_auto():
    while True:
        try:
            # 获取当前时间（格式：HH:MM:SS）
            current_time = strftime("%H:%M:%S", time.localtime())
            hour, minute, second = current_time.split(':')
            
            # 检查是否是每分钟的第5秒
            if int(second) == UPDATE_SECOND_05:
                # 构造时间部分（只显示hh:mm）
                time_part = f"{hour}:{minute}"
                
                # 转换为选择的字体样式
                styled_time = font_converter(time_part)
                
                # 构造 Last Name（当前时间 + 随机Emoji）
                last_name = f"{styled_time} {emojize(random.choice(random_emojis), use_aliases=True)}"
                
                # 更新 Telegram Last Name
                await client1(UpdateProfileRequest(last_name=last_name))
                logger.info(f'Updated at 05s -> {last_name}')
            
            # 检查是否是每分钟的第35秒
            if int(second) == UPDATE_SECOND_35:
                # 计算下一分钟
                next_minute = int(minute) + 1
                next_hour = int(hour)
                if next_minute >= 60:
                    next_minute = 0
                    next_hour += 1
                    if next_hour >= 24:
                        next_hour = 0
                
                # 格式化下一分钟时间
                next_time = f"{next_hour:02d}:{next_minute:02d}"
                
                # 转换为选择的字体样式
                styled_next_time = font_converter(next_time)
                
                # 随机选择一个表情
                random_emoji = random.choice(random_emojis)
                
                # 构造 Last Name（下一分钟时间 + 随机Emoji）
                last_name = f"{styled_next_time} {emojize(random_emoji, use_aliases=True)}"
                
                # 更新 Telegram Last Name
                await client1(UpdateProfileRequest(last_name=last_name))
                logger.info(f'Updated at 35s -> {last_name}')
        
        except KeyboardInterrupt:
            print('\nResetting Last Name...')
            await client1(UpdateProfileRequest(last_name=''))
            sys.exit()
        
        except Exception as e:
            print(f'Error: {type(e)} - {e}')
        
        # 每秒检查一次
        await asyncio.sleep(1)

# 主函数
async def main(loop):
    await client1.start()  # 启动 Telegram 客户端
    task = loop.create_task(change_name_auto())  # 创建异步任务
    await task
    print('Bot is running...')
    await client1.run_until_disconnected()  # 保持连接
    task.cancel()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
