import os
import shutil
import random
import time
import json
import ssh_upload as upload

config = {}

#扫描u盘是否插入
def scanUSB(file_path):
    if not os.path.exists(file_path) :
        print("no USB (sleep 5s)")
        time.sleep(30)
        return 0
    else:
        try:
            backup(file_path)
        except:
            pass
#遍历usb中的所有目录
def getallpath(file_path):
    path_collection = []
    for dirpath, dirnames, filenames in os.walk(file_path):
        for file in filenames:
            fullpath = os.path.join(dirpath, file)
            fullpath = os.path.abspath(fullpath)
            path_collection.append(fullpath)
    return path_collection

#开始复制usb中的内容
def backup(root_path):
    print("scan usb ...")
    path = getallpath(root_path)
    remoteORlocal = config['remoteORlocal']
    tar = []
    for oneFile in path:
        exc = os.path.splitext(oneFile)[1]
        #过滤不合适的文件
        if exc in config['mateAss']:
            tar.append(oneFile)
    flag = remoteORlocal
    if  flag == 'True':
        #复制到本地
        for oneFile in tar:
            backupFile(oneFile, config['backupPath'])
    else:
        #复制到远程服务器
        for oneFile in tar:
            upload.ssh_win_to_linux(config['server_ip'],config['server_user'],config['server_passwd'],config['server_port'],oneFile,config['remote_dir'])
    print('have backuped ')
#复制内容
def backupFile(file_from, file_end):
    if not os.path.isdir(file_end):
        os.makedirs(file_end)
    fTo = file_end + '\\' + os.path.basename(file_from)
    shutil.copyfile(file_from, fTo)
    print (fTo)
    print ('copy file success....')
#启动
def main():
    config = json.load(open('config.ini', encoding='utf-8'))
    while(1):
        for onePath in config['usbPath']:
            scanUSB(onePath)

if __name__ == '__main__':
    config = json.load(open('config.ini', encoding='utf-8'))
    while(1):
        for onePath in config['usbPath']:
            scanUSB(onePath)