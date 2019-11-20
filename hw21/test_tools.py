# -*- coding: UTF-8 -*-
"""Пример тестов ssh, sftp"""
import os

import paramiko


def find_file(file_name):
    """ Find file in sub dirs """

    rootdir = os.getcwd()

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            filepath = subdir + os.sep + file

            if filepath.endswith(file_name):
                return filepath
    raise Exception("Files not found" + file_name + "\n")


class paramiko_ssh_client():
    """docstring"""

    def __init__(self, host='localhost', user='master', pwd='master', port=2222):
        """Constructor"""
        self.host = host
        self.user = user
        self.pwd = pwd
        self.port = port
        self.client = None

    def create_client(self):
        """
        Connect by SSH
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.host, username=self.user, password=self.pwd, port=self.port)
        self.client = client
        return self.client

    def execute_command(self, cmd):
        """
        Execute ssh or sftp command
        """
        stdin, stdout, stderr = self.client.exec_command(cmd)
        return stdout.read() + stderr.read()

    def __del__(self):
        self.client.close()


def test_ssh():
    """
     Test ssh
    """
    ssh_client = paramiko_ssh_client()
    ssh_client.create_client()
    ssh_client.execute_command('rm -rf *')
    data = ssh_client.execute_command('echo "hello world">> test.txt')
    print(data)
    data = ssh_client.execute_command('ls')
    assert data == b'test.txt\n'


def test_sftp_upload():
    """
     Test sftp upload
    """
    ssh_client = paramiko_ssh_client()
    ssh_client.create_client()
    ftp = ssh_client.create_client().open_sftp()
    data = ftp.put(find_file('README.md'), 'README.md')
    data = ssh_client.execute_command('ls')
    assert data == b'README.md\ntest.txt\n'


def test_reset_apache():
    """
    Reset apache vi ssh and test response
    :return:
    """
    ssh_client = paramiko_ssh_client()
    ssh_client.create_client()
    data = ssh_client.execute_command('systemctl restart apache2')
    print(data)
    data = ssh_client.execute_command('systemctl is-active apache2')
    # вдокере не доступна systemd
    assert data == b'bash: systemctl: command not found\n'
