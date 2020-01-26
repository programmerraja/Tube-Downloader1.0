import requests as r
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os ,time
import subprocess as sub
import sys
class scrap:
    def __init__(self):
        self.play_link=""
        while(not self.play_link):
            self.play_link=input("Enter the link for playlist")
        self.search()
    def search(self):
        self.vid_src=[]
        self.save_link="https://en.savefrom.net/"
        self.tube_link="https://www.youtube.com"
        
        #getting video link
        try:
        
            html_code=r.get(self.play_link).text
            msg=soup(html_code,"html.parser")
            for link in msg.find_all('a',{"class":"spf-link playlist-video clearfix yt-uix-sessionlink spf-link"}):
                    self.vid_src.append(self.tube_link+link["href"])
                    
            self.no_video=int(input("Enter the video number   to download(default=0)"))
            #getting input for no of video 
            if(self.no_video>len(self.vid_src) or( self.no_video<0)):
                            print("Out of range")
                            self.no_video=0
            self.chrome_browser()
        except :
            print("Opps! No Internet Connection")
        
        
    def chrome_browser(self,error=0,):
        if(error==0): 
                try:
                 self.driver=webdriver.Chrome(os.getcwd()+"\\chromedriver.exe")
                except:
                    print("Chrome drive not found")

        #to find link entry input box
        try:
                 self.driver.get(self.save_link)
                 time.sleep(5)
                 link_entry=self.driver.find_element_by_id("sf_url")
        except:
            print("Something wrong while opening save from net \n Please make sure have internet connection")
        time.sleep(2)
        #to skip 360 video 
        self.time=0
        #putting each link in a input box 
        for i in self.vid_src[self.no_video-1:]:
                try:
                 #if the 360 video is skipped mean this excute 
                 if(self.time==1):
                     #link for savefromnet
                     self.driver.get(self.save_link)
                     time.sleep(5)
                     link_entry=self.driver.find_element_by_id("sf_url")
                     
                 time.sleep(5)
                 link_entry.send_keys(i)
                 link_entry.send_keys(Keys.RETURN)
                 time.sleep(10)
                 link_entry.clear()

                except  :
                    print(i)
                    try:
                       f=open("logfiles/video link.txt","a")
                    except:
                        f=open("logfiles/video link.txt","w")
                    print("Link Not Found You Try To Download 360 Mp4 Video")
                    f.write("\n")
                    f.write(i)
                    f.close()
                    self.time=1
                    continue
                #getting download link for the viedeo 
                try:
                     download_link_html=soup(self.driver.page_source,"html.parser")
                     download_link=download_link_html.find("div",{"class":"def-btn-box"})
                     self.driver.get(download_link.find("a")["href"])
                     time.sleep(7)
                except:
                     print("Download Link Not Found!!!")
        self.driver.quit()
                
app=scrap()
