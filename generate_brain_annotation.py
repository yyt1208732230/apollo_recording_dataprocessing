import os
import shutil
import pandas as pd
import re
from util import *
from envload import *

def get_pname_from_path(path):

    PName= 'PNone'

    # 使用正则表达式提取"PXX"
    match = re.search(r'P(\d+)', path)
    if match:
        PName = match.group(0)
    else:
        PName = PName
    
    return PName

def get_text_annotation_for_eeg(path, standard_time_eeg):

    # path = "F://ORED_Dataset//P07//7.CANBus/timedivision--20230508154543.record.csv"

    PName = PNAME

    # 读取Excel文件
    df = pd.read_csv(path, skiprows=[1])

    # 设置标准相对时间
    # standard_time_eeg

    # 计算latency、type和duration列的值
    df['latency'] = (df['relative_time'] + standard_time_eeg).round(3)
    df['type'] = df['state']
    df['duration'] = df['duration'].round(3)  # 将duration列的值精确到3位小数

    # 选择需要的列并保存为文本文件
    df[['latency', 'type', 'duration']].to_csv('EEGannotation/' + PName + '-event.txt', sep='\t', index=False)

    return 'succeed'

def get_text_annotation_for_eeg_adjust(path, standard_time_eeg, adjust):

    # path = "F://ORED_Dataset//P07//7.CANBus/timedivision--20230508154543.record.csv"

    PName = PNAME

    # 读取Excel文件
    df = pd.read_csv(path, skiprows=[1])

    # 设置标准相对时间
    # standard_time_eeg

    # 计算latency、type和duration列的值
    df['latency'] = (df['relative_time'] + standard_time_eeg).round(3) - adjust
    df['type'] = df['state']
    df['duration'] = df['duration'].round(3)  # 将duration列的值精确到3位小数

    # 选择需要的列并保存为文本文件
    df[['latency', 'type', 'duration']].to_csv('EEGannotation/' + PName + '-event-adjustbefore' + str(int(adjust*1000)) + '.txt', sep='\t', index=False)

    return 'succeed'

def copyfile(source_path, target_path):
    try:
        shutil.copy(source_path, target_path)
        print(f"{source_path} 拷贝成功")
    except Exception as e:
        print(f"{source_path} 拷贝失败: {str(e)}")
