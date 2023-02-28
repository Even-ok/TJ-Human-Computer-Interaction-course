import  win32api
from kivy.core.audio import SoundLoader
import webbrowser

class voiceControl:
    def __init__(self):
        pass

    def judgeOrder(self,text):
        result = "处理完毕"
        if text=="播放音乐" or "音乐" in text or "music" in text:
            self.playMusic()
            return result
        elif text == "查看文件" or "文件" in text or "file" in text:
            self.openTxtFile()
            return result
        elif text == "查看图片" or "图片" in text or "image" in text:
            self.openImage()
            return result
        elif text == "打开浏览器" or "浏览器" in text or "explorer" in text:
            self.openExplorer()
            return result
        elif text == "打开记事本" or "记事本" in text or "notepad" in text:
            self.openNotepad()
            return result
        elif text == "画图" or "画图" in text or "draw" in text or "Draw" in text:
            self.drawPicture()
            return result
        elif text == "查看新闻" or "新闻" in text or "newspaper" in text:
            self.ViewNewspaper()
            return result
        elif text =="":
            result = "我没有听清，请再说一次"
            return result
        else:
            result = "没有该指令"
            return result
        

    def playMusic(self):
        sound = SoundLoader.load('./music/audio_sample_little.wav')
        if sound:
            print("Sound found at %s" % sound.source)
            print("Sound is %.3f seconds" % sound.length)
            sound.play()
    
    def openExplorer(self):
         webbrowser.open('www.baidu.com')

    def ViewNewspaper(self):
         webbrowser.open('www.chinanews.com.cn')

    def openTxtFile(self):
        filename =  'D:\\1课程资料\\大三下\\人机交互\\kivy\\TalkToMe\\file\\hello.txt'
        win32api.ShellExecute(0, 'open', filename, '', '', 1)

    def openImage(self):
        filename =  'D:\\1课程资料\\大三下\\人机交互\\kivy\\TalkToMe\\image\\tweet.png'
        win32api.ShellExecute(0, 'open', filename, '', '', 1)

    def openNotepad(self):
        win32api.ShellExecute(0, 'open', 'D:\\APP\\Notepad++\\Notepad++.exe', '', '', 0)

    def drawPicture(self):
        win32api.ShellExecute(0, 'open', 'C:\\Users\\12849\\AppData\\Local\\Microsoft\\WindowsApps\\Microsoft.Paint_8wekyb3d8bbwe\\mspaint.exe', '', '', 1)