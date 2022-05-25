import time

from django.shortcuts import render
from django.http import JsonResponse
from utils.basicUtils import dataURIToImg, imgToDataURI
from utils.ssh.sshUtility import SshUtil
import subprocess
from subprocess import PIPE
import os
from Editabl.settings import BASE_DIR
import shutil
from PIL import Image
import warnings
import numpy as np

# Create your views here.


def enableEncodingMode(imagePath):
    image = Image.open(imagePath, 'r')
    try:
        currBasePath = os.path.join(BASE_DIR, 'stylegan-encoder')
        alignedImageDirPath = os.path.join(currBasePath, 'aligned_images')
        if os.path.exists(alignedImageDirPath):
            shutil.rmtree(alignedImageDirPath)
        rawImageDirPath = os.path.join(currBasePath, 'raw_images')
        if os.path.exists(rawImageDirPath):
            shutil.rmtree(rawImageDirPath)
        os.mkdir(alignedImageDirPath)
        os.mkdir(rawImageDirPath)
        extension = os.path.splitext(imagePath)[-1]
        print(extension)
        image.save(os.path.join(rawImageDirPath, 'photo' + extension))
        os.chdir(os.path.join(BASE_DIR, 'stylegan-encoder'))
        return 0
    except Exception as e:
        print("Some Exception in enabling Encoding Mode")
        print("The exception is - \n", e)
        return 1


def disableEncodingMode():
    os.chdir(BASE_DIR)


def alignImage():
    print("Starting Alignment")
    encoderDir = 'stylegan-encoder'
    alignCmd = "python align_images.py raw_images/ aligned_images/ --output_size=1024"
    alignProcess = subprocess.run(alignCmd, shell=True, stdout=PIPE, stderr=PIPE)
    print(alignProcess.returncode, alignProcess.stdout.decode(), alignProcess.stderr.decode())
    print("Alignment Ended")


def encodeImage():
    print("Starting Encoding")
    encodeCmd = "python encode_images.py --optimizer=lbfgs " \
                "--face_mask=True --iterations=10 --use_lpips_loss=0 " \
                "--use_discriminator_loss=0 --output_video=False " \
                "aligned_images/ generated_images/ " \
                "latent_representations/"
    for _ in range(2):
        encodeProcess = subprocess.run(encodeCmd, stderr=PIPE, stdout=PIPE, shell=True)
        if encodeProcess.returncode == 0:
            print("Successfully Encoded!")
            break
        else:
            print(encodeProcess.stdout.decode(), '\n', encodeProcess.stderr.decode())
    print("Encoding Ended")


def saveOutputVector():
    latents = sorted(os.listdir('latent_representations'))

    outFile = 'imageLatents.npy'

    finalWvectors = []
    w = np.load('latent_representations/' + latents[0])
    finalWvectors.append(w)

    finalWvectors = np.array(finalWvectors)
    np.save(outFile, finalWvectors)
    print("Saved imageLatents.npy")


def latentWalk(walkDetails):
    print("Starting Latent Walk")
    latentsFile = os.path.join(BASE_DIR, 'stylegan-encoder', 'imageLatents.npy')
    if os.path.isfile(latentsFile):
        with SshUtil() as remote:
            def remotePath(*args):
                interFaceGanDir = '/content/InterFaceGAN'
                paths = list()
                for relPath in args:
                    paths.append(os.path.join(interFaceGanDir, relPath))
                if len(paths) == 1:
                    return paths[0]
                else:
                    return paths

            remoteLatentsFile = remotePath("imageLatents.npy")
            remote.sendFile(localPath=latentsFile, remotePath=remoteLatentsFile)
            for attribute, startDistance, endDistance, numFrames in walkDetails:
                cmd = "python %s -m stylegan_ffhq " \
                      "-b %s " \
                      "-s Wp " \
                      "-i '%s' " \
                      "-o %s " \
                      "--start_distance -%s " \
                      "--end_distance %s " \
                      "--steps=%s" % (tuple(remotePath('edit.py',
                                                      'boundaries/stylegan_ffhq_%s_w_boundary.npy'
                                                       % attribute,
                                                      'imageLatents.npy',
                                                      'results')) +
                                      (startDistance, endDistance, numFrames))
                print("Starting '%s' latent walk" % attribute)
                for _ in range(3):
                    remote.removeDir(remotePath('results'))
                    exitcode, stdout, stderr = remote.runCommand(cmd)
                    if exitcode == 0:
                        print("successful")
                        print("Ended '%s' latent walk" % attribute)
                        break
                    print("some Error in running on Colab")
                    print('stdout')
                    print('\n'.join(stdout.readlines()))
                    print('stderr')
                    print('\n'.join(stderr.readlines()))
                print("Copying Results")
                remote.getDir('/content/InterFaceGAN/results', 'results/' + attribute, numFrames)
    else:
        print("Does not exist")
    print("Latent Walk Ended")


def AIEditingView(request):
    return render(request, 'AIAssistedEditing/AIEditingPage.html')


def getImageResponse():
    RESULT_DIR = 'results'
    dirs = os.listdir(RESULT_DIR)
    response = dict()
    for attrDir in dirs:
        absAttrDir = os.path.join(RESULT_DIR, attrDir)
        files = os.listdir(absAttrDir)
        uriList = list()
        files.sort()
        for file in files:
            filePath = os.path.join(absAttrDir, file)
            imgDataUri = imgToDataURI(open(filePath, 'rb').read())
            uriList.append(str(imgDataUri))
        response[attrDir] = uriList
    return response


def processImageAsync(request):
    if request.method == "POST":
        timeStart = time.time()
        # image = dataURIToImg(request.POST['dataURIString'])
        # image = image.convert('RGBA')
        # image.save('testImage/image.png')
        # enableEncodingMode('testImage/image.png')
        # alignImage()
        # encodeImage()
        # saveOutputVector()
        # latentWalk([['smile', '0.5', '0.5', '10'],
        #             ['age', '1.7', '1.7', '10'],
        #             ['pose', '0.4', '0.4', '10'],
        #             ['gender', '1.5', '1.5', '10']])
        # disableEncodingMode()
        timeEnd = time.time()
        print("Execution Time - '%s' mins!" % str((timeEnd-timeStart)//60))
        response = getImageResponse()
        return JsonResponse({'status': 1, 'uriDict': response})
