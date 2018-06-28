#! python3
# -*- coding: utf-8 -*-
import io
import importlib
import sys
import random
import re
from urllib.request import urlopen
from urllib.request import Request
from pdfminer.converter import PDFPageAggregator
# from pdfminer.converter import TextConverter
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument


'''解析pdf 文本，保存到txt文件中'''
importlib.reload(sys)

user_agent = ['Mozilla/5.0 (Windows NT 10.0; WOW64)', 'Mozilla/5.0 (Windows NT 6.3; WOW64)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
              'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
              'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko']

def parse(_path):
    # 判断是不是本地文件
    result = re.match("http",_path)
    if result == None:
          fp = open(_path, 'rb')  # rb以二进制读模式打开本地pdf文件
    else:
          request = Request(url=_path, headers={'User-Agent': random.choice(user_agent)})  # 随机从user_agent列表中抽取一个元素
          fp = urlopen(request) #打开在线PDF文档

    # 用文件对象来创建一个pdf文档分析器
    praser_pdf = PDFParser(fp)

    # 创建一个PDF文档
    doc = PDFDocument()

    # 连接分析器 与文档对象
    praser_pdf.set_document(doc)
    doc.set_parser(praser_pdf)

    # 提供初始化密码doc.initialize("123456")
    # 如果没有密码 就创建一个空的字符串
    #这边是要进行解密的处理
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()

        # 创建一个PDF参数分析器
        laparams = LAParams()
        # retstr = io.StringIO()

        # 创建聚合器
        # device = TextConverter(rsrcmgr, retstr,laparams=laparams)
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # 创建一个PDF页面解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一页的内容
        # doc.get_pages() 获取page列表
        for page in doc.get_pages():
            # 使用页面解释器来读取
            interpreter.process_page(page)

            # 使用聚合器获取内容
            layout = device.get_result()

            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for out in layout:
                if (isinstance(out, LTTextBoxHorizontal)):
                    with open(r'C:\Users\Administrator\Desktop\pdf测试\2014 Automatic Generation of the Domain Module from Electronic Textbooks.txt', "a+",encoding='utf-8') as f:

                        results = out.get_text()
                        print(results)
                        f.write(results  +'\n')
        print("----转换成功----")
                        #f.write(results.encode('utf-8')+'\n')

if __name__ == '__main__':
    #url = "http://www.sac.net.cn/hysj/zqgsyjpm/201707/P020170717564197883913.pdf"
    #url = "https://www.tencent.com/zh-cn/articles/8003451510737482.pdf"
    #url = "file:///C:/Users/wakaka/Desktop/1.pdf"in
    #url = r'C:\Users\wakaka\Desktop\1.pdf'
    url = r'C:\Users\Administrator\Desktop\pdf测试\2014 Automatic Generation of the Domain Module from Electronic Textbooks.pdf'
    #url = "http://www.docin.com/p-353873394.html"

    parse(url)
