# coding=utf-8
import importlib
import sys
importlib.reload(sys)

import time
time1=time.time()
import os.path
from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.layout import *

result=[]
class CPdf2TxtManager():
    def __init__(self):
        '''''
        Constructor
        '''

    def changePdfToText(self, filePath):
        file = open(path, 'rb') # 以二进制读模式打开
        #用文件对象来创建一个pdf文档分析器
        praser = PDFParser(file)
        # 创建一个PDF文档
        doc = PDFDocument()
        # 连接分析器 与文档对象
        praser.set_document(doc)
        doc.set_parser(praser)

        # 提供初始化密码
        # 如果没有密码 就创建一个空的字符串
        doc.initialize()

        # 检测文档是否提供txt转换，不提供就忽略
        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed

        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pdfStr = ''
        num_page, num_image, num_curve, num_figure = 0, 0, 0, 0
        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages(): # doc.get_pages() 获取page列表
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            for x in layout:
                #for x in layout:
                if isinstance(x, LTImage):  # 图片对象
                    num_image += 1
                if isinstance(x, LTCurve):  # 曲线对象
                    num_curve += 1
                if isinstance(x, LTFigure):  # figure对象
                    num_figure += 1
                if hasattr(x, "get_text"):
                    # print x.get_text()
                    result.append(x.get_text())
                    fileNames = os.path.splitext(filePath)
                    with open(fileNames[0] + '.txt','a+',encoding='utf-8') as f:
                        results = x.get_text()
                        print(results)
                        print(num_image)
                        print(num_curve)
                        print(num_figure)
                        f.write(results + '\n')




if __name__ == '__main__':
    '''''
     解析pdf 文本，保存到txt文件中
    '''

    path = r'C:\Users\Administrator\Desktop\888.pdf'
    pdf2TxtManager = CPdf2TxtManager()
    pdf2TxtManager.changePdfToText(path)

    # print result[0]
    time2 = time.time()

    print (u'ok,解析pdf结束!')
    print (u'总共耗时：' + str(time2 - time1) + 's')
