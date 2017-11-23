import requests
import re
from bs4 import BeautifulSoup
class BDTB:
    def __init__(self,baseurl,seelz):
        self.baseurl=baseurl
        self.seelz='?see_lz='+str(seelz)
    #请求url，返回Response对象
    def getpage(self,pagenum):
        try:
            url=self.baseurl+self.seelz+'&pn='+str(pagenum)
            response=requests.get(url)
            #print(response.text)
            return response
        except TimeoutError as e:
            print(e.msg)
            return None
    #用于获取标题，没实际用处
    # def gettitle(self):
    #     page=self.getpage(1).text
    #     soup=BeautifulSoup(page,'lxml')
    #     result=soup.find('h3',attrs={'class':re.compile("core_title_txt")})
    #     return result.get_text()
    #获取页数，因为需要全部爬取
    def getpagenum(self):
        page=self.getpage(1).text
        soup=BeautifulSoup(page,'lxml')
        result=soup.find('li',attrs={'class':re.compile("l_reply_num")}).find_all('span',attrs={'class':'red'})
        return result[1].get_text()
    #获取具体内容并写入文件中
    def getcontent(self):
        page = self.getpage(1).text
        soup = BeautifulSoup(page, 'lxml')
        result = soup.find('li', attrs={'class': re.compile("l_reply_num")}).find_all('span', attrs={'class': 'red'})
        pagenum=int(result[1].get_text())
        with open('nba.txt','w') as f:
            for i in range(1,pagenum+1):
                page1=self.getpage(i).text
                soup1=BeautifulSoup(page1,'lxml')
                result1=soup1.find_all('div',attrs={'id':re.compile("post_content_.*?")})
                for content in result1:
                    f.write(content.get_text()+'\n')
baseurl='http://tieba.baidu.com/p/3138733512'
bdtb=BDTB(baseurl,1)
#bdtb.getpage(1)
#print(bdtb.gettitle())
#print(bdtb.getpagenum()
bdtb.getcontent()