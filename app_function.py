from yt_dlp import YoutubeDL
import googleapiclient.discovery
import ffmpeg
import glob
import os
import shutil

class AppFunc:
    def __init__(self):
        self.DEVELOPER_KEY = 'AIzaSyCVc8bePfeI3YwhRpbko0MXRKKwoOlG_OA'
        self.SERVICE_NAME = 'youtube'
        self.API_VERSION = 'v3'
        self.savedir= str(os.path.dirname(__file__)) + "/cloud"

    def youtube_dl(self, url_list):
        shutil.rmtree(self.savedir)
        os.mkdir(self.savedir)
        
        option = {'outtmpl':self.savedir +'/%(title)s.%(ext)s',
                'format':'best'}

        ydl = YoutubeDL(option)
        ydl.download(url_list)

        for mp4, path in zip(os.listdir(self.savedir), glob.glob(self.savedir +"/*.mp4")):
            os.rename(path, self.savedir + "/" + mp4.replace("⧸", ""))


    def convert_dl(self, title_list, format_list):
        for title, format in zip(title_list, format_list):
            file_path = self.savedir +"/"+ title.replace("/", "") +".mp4"
            
            if format == "mp4":
                pass

            else:
                mp4_file =  ffmpeg.input(file_path)
                convert_file = ffmpeg.output(mp4_file, file_path.replace(".mp4", "."+format))
                ffmpeg.run(convert_file, overwrite_output=False)
                os.remove(file_path)
    
    def connecton(self, url):
        youtube = googleapiclient.discovery.build(self.SERVICE_NAME, 
                                                  self.API_VERSION, 
                                                  developerKey=self.DEVELOPER_KEY)
        if "https://youtu.be/" in url:
            id = url.replace("https://youtu.be/", "")
        elif "https://www.youtube.com/watch?v=" in url:
            id = url.replace("https://www.youtube.com/watch?v=", "")
        else:
            raise Exception

        search_response = youtube.videos().list(
            part='snippet,statistics',
            id='{},'.format(id)
            ).execute()['items'][0]["snippet"]
        
        title = search_response['title']
        channel = search_response['channelTitle']
        thumbnail_src = search_response['thumbnails']['standard']['url']

        return title, channel, thumbnail_src

    

### test
if __name__ == '__main__':
    # url_list = ['https://youtu.be/Mzmepf8MUwU',
    #             'https://youtu.be/aqblTlwiO2E',
    #             'https://youtu.be/wcxwjSVP8oI']

    # af = AppFunc()
    # x = af.connecton(url_list[2])
    # print(x)
    print(os.path.dirname(__file__))

