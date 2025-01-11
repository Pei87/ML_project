from pydub import AudioSegment, silence 
import os
import librosa 
import matplotlib.pyplot as plt
import numpy as np
import cv2

ROOT_DIR="training"

def path_faltten(dir:list[str],path):
    if dir==[]:    
        soundPathList.append(path)
        return
    
    for i in iter(dir):
        newpath=path+"\\"+i
        if i == 'img': 
            writein_img([d for d in os.listdir(newpath) if os.path.isdir(os.path.join(newpath,d))],newpath)
            continue
        path_faltten([d for d in os.listdir(newpath) if os.path.isdir(os.path.join(newpath,d))],newpath)

def writein_img(dir:list[str],path):
    if dir==[]:
        imgPathList.append(path)

# create mel spectrogram
def create_mel(path):
    sound_data, rate = librosa.load(path)
    mel = librosa.feature.melspectrogram(y=sound_data, sr=rate, n_mels=128, fmax=8000)
    mel_dB = librosa.amplitude_to_db(mel, ref=np.max)
    plt.imshow(mel_dB, interpolation='nearest', origin='lower', aspect='auto')
    plt.tight_layout()
    plt.savefig(path+"Mel.jpg")
    plt.clf()
    melList.append(path+"Mel.jpg")

def sound_cutsilent(path:list[str]):
    for i in iter(path):
        item_list=os.listdir(i)
        print(i)
        for item in item_list:
            sound_file = AudioSegment.from_file(i+'\\'+item,format='wav')
            # filter out silent segments, below -45dB is considered as silence
            segments = silence.split_on_silence(sound_file, min_silence_len=50, silence_thresh=-45)
            if segments==[]:
                print(i+'contain a silent track')
            else :
                new_sound = segments[0]
                for segment in segments[1:]:
                    new_sound = new_sound.append(segment, crossfade=0)
                # save the new sound
                new_sound.export(i+"\\"+item, format="wav")
                afterCutSoundList.append(i+"\\"+item)
                create_mel(i+"\\"+item)

def output_txt():
    f = open(ROOT_DIR+'\\afterSound.txt', 'a')
    for i in range(len(afterCutSoundList)):
        f.write(afterCutSoundList[i])
        f.write('\n')
    f.close()
    f = open(ROOT_DIR+'\\mel.txt', 'a')
    for i in range(len(melList)):
        f.write(melList[i])
        f.write('\n')
    f.close()
    f = open(ROOT_DIR+'\\afterImg64.txt', 'a')
    for i in range(len(aftercut_img64)):
        f.write(aftercut_img64[i])
        f.write('\n')
    f.close()
    f = open(ROOT_DIR+'\\afterImg128.txt', 'a')
    for i in range(len(aftercut_img128)):
        f.write(aftercut_img128[i])
        f.write('\n')
    f.close()
    f = open(ROOT_DIR+'\\afterImg256.txt', 'a')
    for i in range(len(aftercut_img256)):
        f.write(aftercut_img256[i])
        f.write('\n')
    f.close()

def cut_img(x,y,width,height,path):
    item_list=os.listdir(path)
    for item in item_list:
        img = cv2.imread(path+"\\"+item)
        print(path)
        crop_img = img[y:y+height, x:x+width]
        crop_img64 = cv2.resize(crop_img, (64, 64))
        cv2.imwrite(path+"\\"+item+'crop64.jpg', crop_img64)
        crop_img128 = cv2.resize(crop_img, (128, 128))
        cv2.imwrite(path+"\\"+item+'crop128.jpg', crop_img128)
        crop_img256 = cv2.resize(crop_img, (256, 256))
        cv2.imwrite(path+"\\"+item+'crop256.jpg', crop_img256)
        aftercut_img64.append(path+"\\"+item+'crop64.jpg')
        aftercut_img128.append(path+"\\"+item+'crop128.jpg')
        aftercut_img256.append(path+"\\"+item+'crop256.jpg')

def img_process():
    for path in iter(imgPathList):
        if "cam-1" in path:
            cut_img(350,30,350,350,path)
        if "cam-2" in path:
            cut_img(50,150,768,550,path)


if __name__=="__main__":
    path=ROOT_DIR
    soundPathList=[]
    imgPathList=[]
    afterCutSoundList=[]
    melList=[]
    aftercut_img64=[]
    aftercut_img128=[]
    aftercut_img256=[]
    path_faltten([d for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))],path) 
    sound_cutsilent(soundPathList)
    img_process()
    output_txt()
    


