#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import time
import re
import codecs
from ADC_function import *
from OOF_core import *
import json
import shutil
from configparser import ConfigParser

def delExistFile(path): #重命名已存在的文件，加上时间戳
    if os.path.exists(path):  
        time_stamp = int(time.time()) #时间戳
        file_timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime(time_stamp))#YYYYMMDDhh24miss  
        filename=os.path.splitext(path)[0] #文件名
        filetype=os.path.splitext(path)[1]
        Newpath=os.path.join(filename+"_"+file_timestamp+filetype)
        try:
            os.rename(path,Newpath) 
            print("[!]"+path+" 已存在! 已重命名为"+Newpath)
        except:
            print("[-]failed!can not rename file 'failed'\n[-](Please run as Administrator)")
            os._exit(0)


def getNumber(filepath,absolute_path = False):  #从路径中得到番号
    if absolute_path == True:
        filepath=filepath.replace('\\','/')
        file_number = str(re.findall(r'(.+?)\.', str(re.search('([^<>/\\\\|:""\\*\\?]+)\\.\\w+$', filepath).group()))).strip("['']").replace('_', '-')
        return file_number
    if '-' in filepath or '_' in filepath:  # 普通提取番号 主要处理包含减号-和_的番号
        filepath = filepath.replace("_", "-")
        filepath.strip('22-sht.me').strip('-HD').strip('-hd')
        filename = str(re.sub("\[\d{4}-\d{1,2}-\d{1,2}\] - ", "", filepath))  # 去除文件名中时间
        if 'FC2' or 'fc2' in filename:
            filename = filename.replace('-PPV', '').replace('PPV-', '').replace('FC2PPV-', 'FC2-').replace('FC2PPV_', 'FC2-')
            filename = filename.replace('-ppv', '').replace('ppv-', '').replace('fc2ppv-', 'FC2-').replace('fc2ppv_', 'FC2-')
        file_number = re.search(r'\w+-\w+', filename, re.A).group()
        return file_number
    else:  # 提取不含减号-的番号，FANZA CID
        try:
            return str(re.findall(r'(.+?)\.', str(re.search('([^<>/\\\\|:""\\*\\?]+)\\.\\w+$', filepath).group()))).strip("['']").replace('_', '-')
        except:
            return re.search(r'(.+?)\.', filepath)[0]


if __name__ == '__main__':
    config_file = 'config.ini'
    config = ConfigParser()
    config.read(config_file, encoding='UTF-8')
    input_file = config['common']['input_file']  # 输入文件  
    success_folder = config['common']['success_output_folder']  # 成功输出目录 
    failed_file = config['common']['failed_output_file']  # 失败输出    
    print('[*]================== 开始重命名，请联网 ===================')

    #备份旧文件和文件夹
    delExistFile(success_folder)
    delExistFile(failed_file)

    for l in open(input_file,'r'): #遍历txt文件，交给core
        link=l.split('|')
        filename=link[0]
        try:
            print("[!]Making Data for   [" + filename + "], the number is [" + getNumber(filename) + "]")
            core_main(l, getNumber(filename))
            print("[*]======================================================")
        except Exception as e:  # 番号提取异常
            print('[-]' + filename + ' ERRPR :')
            print('[-]',e)
            try:
                print('[-]Move ' + filename + ' to failed file')
                #输出链接到失败文件               
                open_failed= codecs.open(failed_file,'a+', encoding='utf-8')
                open_failed.write(l)
                open_failed.close()
            except Exception as e2:
                print('[!]', e2)
            continue

    print("[+]All finished!!!")
    input("[+][+]Press enter key exit, you can check the error messge before you exit.")
