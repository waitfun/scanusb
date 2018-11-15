import paramiko,time
import os,datetime
import json
import socket

#从windows上将文件上传至linux
def ssh_win_to_linux(server_ip,server_user,server_passwd,server_port,local_dir,remote_dir):
    #print (os.path.exists(local_dir),os.path.isdir(local_dir))
    client = paramiko.Transport((server_ip,server_port))
    client.connect(username=server_user, password=server_passwd)
    sftp = paramiko.SFTPClient.from_transport(client)
    strx = os.path.split(local_dir)[-1]
    dir_name = socket.gethostname()
    if strx:
        dir_name = socket.gethostname()
        cmdStr = 'sudo mkdir '+remote_dir+'/'+dir_name
        cmdStr_1 = 'sudo chmod -R 777 '+remote_dir+'/'+dir_name
        ssh_exec_command(server_ip,server_user,server_passwd,server_port,cmdStr)
        ssh_exec_command(server_ip,server_user,server_passwd,server_port,cmdStr_1)
    print(strx)
    sftp.put(local_dir,os.path.join(remote_dir+'/'+dir_name+'/',strx))
    print ('Uploading file success....')
    client.close()
#创建目录
def mkdir(path):
    dir_name = socket.gethostname()
    isExists=os.path.exists(path+'/'+dir_name)
    if not isExists:
        os.makedirs(path+'/'+dir_name)
    else:
        print(path+'/'+dir_name)
#远程执行命令
def ssh_exec_command(server_ip,server_user,server_passwd,server_port,cmdStr):
   # paramiko.util.log_to_file('paramiko.log')
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname = server_ip,username=server_user, password=server_passwd)   
    stdin,stdout,stderr=ssh.exec_command(cmdStr)   
    #print (stdout.read())
    ssh.close()
# if __name__ == '__main__':
#     #ssh_win_to_linux(local_dir,remote_dir)
#     #mkdir(config['backupPath'])
#     print(233)