import shutil
import subprocess
import paramiko
import os
from Editabl.settings import BASE_DIR


class SshUtil:
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client._policy = paramiko.WarningPolicy()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_config = paramiko.SSHConfig()
        user_config_file = os.path.expanduser("~/.ssh/config")
        if os.path.exists(user_config_file):
            with open(user_config_file) as f:
                self.ssh_config.parse(f)
        self.cfg = {'hostname': 'colab', 'username': 'root'}

        user_config = self.ssh_config.lookup(self.cfg['hostname'])
        for k in ('hostname', 'username', 'port'):
            if k in user_config:
                self.cfg[k] = user_config[k]

        if 'proxycommand' in user_config:
            self.cfg['sock'] = paramiko.ProxyCommand(user_config['proxycommand'])

    def __enter__(self):
        self.client.connect(**self.cfg, banner_timeout=200)
        self.ftpClient = self.client.open_sftp()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
        self.ftpClient.close()

    def runCommand(self, cmd, arguments=None, cmdInput=None):
        argStr = str()
        if arguments:
            for option, value in arguments.items():
                if len(option) == 1:
                    argStr = argStr + ' -' + option
                    if value:
                        argstr = argStr + ' ' + value
                else:
                    argStr = argStr + ' --' + option
                    if value:
                        argstr = argStr + ' ' + value
            cmd = cmd + ' ' + argStr
        stdin, stdout, stderr = self.client.exec_command(cmd)
        if cmdInput:
            for inp in cmdInput:
                stdin.write(inp)
        stdin.close()
        exitCode = stdout.channel.recv_exit_status()
        return exitCode, stdout, stderr

    def sendFile(self, localPath, remotePath):
        self.ftpClient.put(localpath=localPath, remotepath=remotePath)

    def getFile(self, localPath, remotePath):
        self.ftpClient.get(localpath=localPath, remotepath=remotePath)

    def changeDir(self, dirPath):
        exitcode, stdout, stderr = self.runCommand('cd ' + dirPath)
        if exitcode == 0:
            return True
        else:
            return False

    def removeDir(self, directory):
        self.runCommand('rm -rf ' + directory)

    def getDir(self, srcDir, destDir, numFrames):
        getElementsCmd = "ls " + srcDir
        ec, op, err = self.runCommand(getElementsCmd)
        if ec == 0:
            files = op.readlines()

            def filterImages(file):
                if os.path.splitext(file)[-1] == '.jpg':
                    return True
                return False

            files = filter(filterImages, [file.replace('\n', '') for file in files])
            resAbsDir = os.path.join(BASE_DIR, destDir)
            if os.path.isdir(resAbsDir):
                shutil.rmtree(resAbsDir)
            os.makedirs(resAbsDir, exist_ok=True)
            while True:
                for file in list(files):
                    remotePath = os.path.join(srcDir, file)
                    self.getFile(localPath=os.path.join(resAbsDir, file), remotePath=remotePath)
                print(resAbsDir)
                print(len(os.listdir(resAbsDir)))
                if len(os.listdir(resAbsDir)) == int(numFrames):
                    break


