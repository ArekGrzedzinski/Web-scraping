# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 21:10:34 2019

@author: Arek

Simple website crawler to collect German vocabulary into Excel file for printing.
"""

import requests
from bs4 import BeautifulSoup

def setUserAgent(pick):
    global s
    user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0','Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0','Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.107','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36']
    s.headers.update({'user-agent':user_agents[pick%len(user_agents)]})
    
def crawlURL(path):
    attempts=0
    pageContent=''
    global s
    while attempts<5:
        try:
            pageContent = s.get(url_path).text
            attempts = 10 # dummy break condition
        except:
            attempts+=1;    
            print('crawl error URL') 
    return pageContent



s = requests.Session()
setUserAgent(10)

s.headers.update({'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/web'})
s.headers.update({'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'})

FileOut = open('Vocab.txt','w', encoding = 'utf-8')

for i in range(1,47,1):
    url_path = "https://www.memrise.com/course/531306/german-a1-schritte-plus-with-audio/"+str(i)+"/"
    pageContent = crawlURL(url_path)
    soup = BeautifulSoup(pageContent, 'html.parser')
    title = soup.find('title').text
    print(str(i)+". "+str(title))
    attributes={}
    German=[]
    English=[]
    for vocab in soup.find_all("div", class_='col_a col text'):
        German.append(vocab.text)
    for vocab in soup.find_all("div", class_='col_b col text'):
        English.append(vocab.text)
    for i in range(len(German)):
        attributes["German"]= German[i]
        attributes["English"] = English[i]
        FileOut.write(str(attributes)+"\n")
        
import ast
import pandas as pd

dict_list=[]
with open('Vocab.txt','r',encoding='utf-8') as crawl_file:
    line= crawl_file.readline()
    while line:
        dict_list.append(ast.literal_eval(line[:-1]))       
        line = crawl_file.readline()

csd_table = pd.DataFrame(dict_list)
csd_table.to_excel('Vocab.xlsx', sheet_name='Vocab')
    
FileOut.close()
