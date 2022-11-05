from pytube import YouTube
import sys
import os
import ffmpeg


link = sys.argv[1]
path = sys.argv[2]

yt = YouTube(link)
#yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
print("Title:", yt.title)
print("Author:", yt.author)
print("Published date:", yt.publish_date.strftime("%Y-%m-%d"))
print("Number of views:", yt.views)
print("Length of video:", int(yt.length/60) ,":" , yt.length%60)
print("\n")
type = input("file Extention mp4 or mp3 :  ")

if type=="mp4":
    nb=0
    quality = list()

    for i in yt.streams.order_by('resolution').filter(file_extension=type):
        if quality.count(i.resolution) == 0 :
            nb+=1
            quality.append(i.resolution)
            print(f"{nb} - "+i.resolution)

    resolution = int(input(f"file Resolution 1 - {nb} :  "))-1
    #download audio only
    yt.streams.filter(abr="160kbps", progressive=False).first().download(filename="audio.mp3")
    audio = ffmpeg.input("audio.mp3")
    #download video only
    yt.streams.filter(res=quality[resolution],progressive=False).first().download(filename="video.mp4")
    video = ffmpeg.input("video.mp4")
    #merge
    (ffmpeg.output(audio, video, f'{yt.title}.mp4').run(overwrite_output=True))
    os.remove("audio.mp3")
    os.remove("video.mp4")
    print("Done :)")

elif type=="mp3":
    yt.streams.filter(abr="160kbps", progressive=False).first().download(path)
    print("Done :)")

else:
    print("options : mp4 or mp3 \nTry Again ! !")


#mp4_files = yt.streams.filter(progressive=True,file_extension="mp4")
#mp4_369p_files = mp4_files.filter(res=quality[resolution]).first()
#mp4_369p_files.download(path)

