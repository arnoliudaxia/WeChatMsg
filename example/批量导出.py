#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Description: 批量导出微信聊天记录
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# 设置PYTHONPATH
os.environ['PYTHONPATH'] = r'C:\Users\14564\Downloads\WeChatMsg'

def extract_wxids(contact_file):
    """从联系人列表文件中提取所有不重复的wxid"""
    wxids = set()
    
    try:
        with open(contact_file, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                line = line.strip()
                if line.startswith('wxid:') and not line.startswith('wxid_wbew2odtd20t11'):
                    wxid = line.replace('wxid:', '').strip()
                    if wxid and wxid not in wxids:
                        wxids.add(wxid)
    except Exception as e:
        print(f"读取联系人列表失败: {e}")
        return set()
    
    return wxids

def export_chat(wxid, log_file):
    """导出单个联系人的聊天记录"""
    try:
        # 构建命令
        cmd = [sys.executable, '3-exporter.py', wxid]
        
        # 执行导出
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        # 记录日志
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"导出: {wxid}\n")
            f.write(f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"返回码: {result.returncode}\n")
            if result.stdout:
                f.write(f"输出: {result.stdout}\n")
            if result.stderr:
                f.write(f"错误: {result.stderr}\n")
        
        return result.returncode == 0
        
    except Exception as e:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"导出失败: {wxid}\n")
            f.write(f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"异常: {str(e)}\n")
        return False

def main():
    # 文件路径
    contact_file = '联系人列表.txt'
    log_file = '导出日志.txt'
    
    print("开始批量导出微信聊天记录...")
    print(f"日志文件: {log_file}")
    
    # 清空或创建日志文件
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"批量导出开始: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"联系人列表: {contact_file}\n")
        f.write("="*60 + "\n")
    
    # 提取所有wxid
    print("正在读取联系人列表...")
    wxids = extract_wxids(contact_file)
    
    if not wxids:
        print("错误: 未找到任何有效的wxid")
        return
    
    print(f"找到 {len(wxids)} 个不重复的联系人")
    
    # 显示前10个联系人作为预览
    print("\n前10个联系人预览:")
    for i, wxid in enumerate(list(sorted(wxids))[:10], 1):
        print(f"  {i}. {wxid}")
    
    if len(wxids) > 10:
        print(f"  ... 还有 {len(wxids) - 10} 个联系人")
    
    # 等待用户确认
    print(f"\n{'='*60}")
    response = input(f"是否开始导出这 {len(wxids)} 个联系人的聊天记录? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("操作已取消")
        return
    
    # 批量导出
    success_count = 0
    fail_count = 0
    
    for i, wxid in enumerate(sorted(wxids), 1):
        print(f"\n[{i}/{len(wxids)}] 正在导出: {wxid}")
        
        if export_chat(wxid, log_file):
            print(f"✓ 导出成功: {wxid}")
            success_count += 1
        else:
            print(f"✗ 导出失败: {wxid}")
            fail_count += 1
        
        # 每个之间暂停2秒
        time.sleep(2)
    
    # 总结
    print("\n" + "="*60)
    print("批量导出完成!")
    print(f"总计: {len(wxids)} 个联系人")
    print(f"成功: {success_count} 个")
    print(f"失败: {fail_count} 个")
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write("\n" + "="*60 + "\n")
        f.write(f"批量导出完成: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"总计: {len(wxids)} 个联系人\n")
        f.write(f"成功: {success_count} 个\n")
        f.write(f"失败: {fail_count} 个\n")

if __name__ == '__main__':
    main()