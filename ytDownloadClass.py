from fileinput import filename
from pytube import YouTube
import os
import ffmpeg
import threading
import GLBvar
from PyQt5.QtGui import QPixmap
import requests


class ytDownloadClass:
    def __init__(self, link, type):
        self.yt = YouTube(link)
        #yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
        self.type = type
       
    def desc(self):
        startGIF()
        t1 = threading.Thread(target=descTread, args=(self.yt,))
        t1.start()



    def Download_MP3(self,path):
        startGIF()
        GLBvar.status.setText("Downloading ...")
        t1 = threading.Thread(target=DownloadMP3Thread, args=(self.yt,path,))
        t1.start()
        
        return "Done :)"

    def Download_MP4(self,resolution,path):
        #Download and merge thread
        startGIF()
        t1 = threading.Thread(target=DownloadAndMerge, args=(self.yt,path,self.yt.title,resolution,))
        t1.start()
        GLBvar.status.setText("Downloading ...")
        return "Done :)"


    def get_Quality(self):
        startGIF()
        t1 = threading.Thread(target=GetQualityTread, args=(self.yt,))
        t1.start()
    
def DownloadAndMerge(yt,path,title,resolution):
    #download audio only
    yt.streams.filter(abr="160kbps", progressive=False).first().download(f'{GLBvar.tmpDir}',filename="audio.mp3")
    audio = ffmpeg.input(f'{GLBvar.tmpDir}\\audio.mp3')
    #download video only
    yt.streams.filter(res=resolution,progressive=False).first().download(f'{GLBvar.tmpDir}',filename='video.mp4')
    video = ffmpeg.input(f'{GLBvar.tmpDir}\\video.mp4')
    ffmpeg.output(audio, video,f'{path}\{title}.mp4').run(overwrite_output=True,capture_stdout=False, capture_stderr=False,quiet=True)
    GLBvar.status.setText("Download Completed")
    stopGIF()

def descTread(yt):
    GLBvar.status.setText("Getting Data")
    r= "Title:" + yt.title + "\n"
    r+="Author:" + yt.author + "\n" 
    r+="Published date:" + yt.publish_date.strftime("%Y-%m-%d") + "\n"
    r+="Number of views:" + str(yt.views) + "\n"
    r+="Length of video:" + str(int(yt.length/60)) + ":" + str(yt.length%60) + "\n"
    r+="\n"
    GLBvar.descLabel.setText(r)
    data = requests.get(yt.thumbnail_url)
    pixmap = QPixmap()
    pixmap.loadFromData(data.content)
    pixmap = pixmap.scaled(291, 171)
    GLBvar.imgViewer.setPixmap(pixmap)
    stopGIF()
    GLBvar.status.setText("Done Getting Data")
    GLBvar.downloadBtn.setEnabled(True)


def DownloadMP3Thread(yt,path):
    yt.streams.filter(abr="160kbps" , progressive=False).first().download(path)
    GLBvar.status.setText("Download Completed")
    stopGIF()

def GetQualityTread(yt):
    GLBvar.status.setText("Getting Data")
    nb=0
    quality = list()
    for i in yt.streams.order_by('resolution').filter(file_extension="mp4"):
        if quality.count(i.resolution) == 0 :
            nb+=1
            quality.append(i.resolution)
    
    n = 0
    for i in GLBvar.QualityGroup.children() :
        i.setText(quality[n])
        i.setEnabled(True)
        n+=1
        if n >= len(quality) :
            GLBvar.status.setText("Done Getting Data")
            GLBvar.downloadBtn.setEnabled(True)
            stopGIF()
            return
    GLBvar.status.setText("Done Getting Data")
    GLBvar.downloadBtn.setEnabled(True)
    stopGIF()
    return None

def startGIF():
    try:
        GLBvar.loading_label.setHidden(False)
        GLBvar.loading_movie.start()
    except:
        return

def stopGIF():
    try:
        GLBvar.loading_label.setHidden(True)
        GLBvar.loading_movie.stop()
    except:
        return

