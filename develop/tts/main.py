import enum
import os
import shutil
from time import sleep

import pyttsx3
from pydub import AudioSegment

outputType = ".mp3"

def createDir(dir):
    try: 
        if not os.path.exists(dir):
            print("make dir successfully")
            os.makedirs(dir)
        else :
            print("dir already exist, remove everything and remake dir")
            shutil.rmtree(dir)
            os.makedirs(dir)
    except OSError:
        print("Error")

def makeRawFiles(targetNumber : int):    
    directory = "./outputDir/"
    createDir(directory)

    # make audio files
    engine = pyttsx3.init()
    initialVolume = engine.getProperty('volume')
  
    fileList = []
    for i in range(targetNumber+1):
        number = str(i)
        destFile = directory+number+outputType
        engine.save_to_file(number, destFile)
        fileList.append(destFile)
    engine.runAndWait()
    print("raw files are ready")
    return fileList

def addSilence(rawFileList: list, termInMicroSecond : int):
    # add silence, trim each number to 5.5sec
    directory = "./outputDir/final/"
    createDir(directory)


    finalResult = AudioSegment.silent(duration=0)
    for i, file in enumerate(rawFileList) :
        if i == 0: continue
        number = str(i)
        sound = AudioSegment.from_file(file)
        five_second_silence = AudioSegment.silent(duration=termInMicroSecond)
        finalResult += (sound + five_second_silence)[:termInMicroSecond]
        print(i, "th number added")
    file_handle = finalResult.export(directory + "output" + outputType)

if __name__ == "__main__":
    files = makeRawFiles(targetNumber = 100)
    addSilence(rawFileList = files, termInMicroSecond=2000)
