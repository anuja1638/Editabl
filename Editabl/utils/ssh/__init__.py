import os
from Editabl.settings import BASE_DIR
sshConfigFilePath = '/home/kaustubh/.ssh/config'

if not os.path.isfile(sshConfigFilePath):
    open(sshConfigFilePath, 'r').close()

open(sshConfigFilePath, 'w').close()
sshConfigTxtFile = os.path.join(BASE_DIR, 'utils', 'ssh', 'sshConfig.txt')

with open(sshConfigTxtFile, 'r') as firstFile, open(sshConfigFilePath, 'w') as secondFile:
    for line in firstFile:
        secondFile.write(line)
