# coding=utf-9
import configparser
from subprocess import Popen, PIPE, STDOUT
import logging
import paramiko
import os, sys

LOG = logging.getLogger(__name__)


def shell_cmd(cmd):
    obj = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
    if obj.stdout:
        for line in obj.stdout.readlines():
            print(line)
            LOG.info("--- %s" % line)
    elif obj.stderr:
        for line in obj.stderr.readlines():
            print(line)
            LOG.info("### %s" % line)


def remote_shell(remote_ip, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_ip)
    if cmd == None:
        return ssh
    else:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.readlines())
        for line in stdout.readlines():
            print(line)
        ssh.close()


def copy_file(remote_ip, local_file, remote_file, to_remote=True):
    ssh = remote_shell(remote_ip, None)
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    if to_remote:
        print("将文件从本地%s 上传到 %s:%s" % (local_file, remote_ip, remote_file))
        sftp.put(local_file, remote_file)
    else:
        print("将文件从 %s:%s 下载到本地的%s " % (remote_ip, remote_file, local_file))
        sftp.get(remote_file, local_file)
    ssh.close()


def replace_content(file, content_old, content_new):
    with open(file, "r") as f:
        content = f.read()
    content1 = content.replace(content_old, content_new)
    print("%s  -->>  %s" % (content_old, content_new))
    with open(file, "w") as f:
        f.write(content1)


def rename_file(path, old_name, new_name):
    files = os.listdir(path)
    for file in files:
        if old_name in file:
            name_0, name_2 = file.split(old_name)
            file_new = name_0 + new_name + name_2
            os.rename(path + "/" + file, path + "/" + file_new)
            print(path + "/" + file)
            print("↓↓↓↓↓ 重命名为 ↓↓↓↓↓ ")
            print(path + "/" + file_new)
            print('-' * 11)


def get_envs(server):
    config = configparser.ConfigParser()
    config.read("mfwlog.ini")
    return config[server]


def main():
    pass


if __name__ == '__main__':
    main()
