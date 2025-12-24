#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time        : 2025/3/11 20:46
@Author      : SiYuan
@Email       : 863909694@qq.com
@File        : wxManager-2-contact.py
@Description :
"""
import time
import sys
import io

from wxManager import DatabaseConnection

# 设置输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def safe_print(obj):
    """安全打印，处理编码错误"""
    try:
        print(obj)
    except UnicodeEncodeError:
        try:
            # 尝试使用GBK编码
            print(str(obj).encode('gbk', errors='replace').decode('gbk'))
        except:
            # 如果GBK也失败，使用UTF-8并替换错误字符
            print(str(obj).encode('utf-8', errors='replace').decode('utf-8'))

db_dir = r'C:\Users\14564\Downloads\WeChatMsg\example\wxid_wbew2odtd20t11\db_storage'  # 第一步解析后的数据库路径，例如：./wxid_xxxx/db_storage
db_version = 4  # 数据库版本，4 or 3

conn = DatabaseConnection(db_dir, db_version)  # 创建数据库连接
database = conn.get_interface()  # 获取数据库接口

st = time.time()
cnt = 0
contacts = database.get_contacts()
for contact in contacts:
    safe_print(contact)
    contact.small_head_img_blog = database.get_avatar_buffer(contact.wxid)
    cnt += 1
    if contact.is_chatroom:
        safe_print('*' * 80)
        safe_print(contact)
        chatroom_members = database.get_chatroom_members(contact.wxid)
        safe_print(f"{contact.wxid} 群成员个数：{len(chatroom_members)}")
        for wxid, chatroom_member in chatroom_members.items():
            chatroom_member.small_head_img_blog = database.get_avatar_buffer(wxid)
            safe_print(chatroom_member)
            cnt += 1

et = time.time()

safe_print(f'联系人个数：{cnt} 耗时：{et - st:.2f}s')