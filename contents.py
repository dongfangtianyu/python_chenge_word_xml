#-*- coding: utf-8 -*-

import os
import sys
import win32clipboard
import win32con
reload(sys)
sys.setdefaultencoding("utf-8")
import re
from win32com.client import Dispatch, constants
from win32com.client.gencache import EnsureDispatch
from rmb_upper import to_rmb_upper


class contents:
    db = None
    home_dir = os.path.split(os.path.realpath(sys.argv[0]))[0]+'\\'

    def __init__(self, db):
        try:
            self.db = db
        except Exception, e:
            self.db = None

    def getclipb(self):
        win32clipboard.OpenClipboard()
        d = win32clipboard.GetClipboardData(win32con.CF_TEXT)
        win32clipboard.CloseClipboard()
        return d

    def get_data(self):
        data = self.getclipb()
        data2 =[]
        rows = data.split(os.linesep)
        for row in rows :
            column = row.split("\t")
            data2.append(column)

        data2 = data2[:-1]
        return data2

    def sort_data(self):
        MetaData = self.get_data()
        if len(MetaData)<= 1 :
            print(zhCN('\r\n\r\b错误：\r\n剪贴板内没有发现数据，请在复制好数据后重新操作'))
            return False
        #datainfo = {'PINo':u'合同编号', 'Date': u'签约时间', 'Name': u'产品名称', 'Spec':u'规格', 'Qty': u'数量', 'Amt':u'金额', 'Price':u'单价'}
        datainfo = {'PINo':'合同编号', 'Date': '签约时间', 'Name': '产品名称', 'Spec':'规格', 'Qty': '数量',
                    'Amt':'金额', 'Price':'单价', 'Seller':'供方', 'Buyer':'需方'}
        for name in datainfo:
            char = datainfo[name].decode('utf-8').encode('gb2312')
            if char in MetaData[0]:
                datainfo[name] = MetaData[0].index(char)
        self.datainfo = datainfo
        PI_data={}

        for row in MetaData[1:]:
            if PI_data.has_key(row[datainfo['PINo']]) is False:
                PI_data[row[datainfo['PINo']]]={}
                PI_data[row[datainfo['PINo']]]['List']=[]
                PI_data[row[datainfo['PINo']]]['Amt']=0
                PI_data[row[datainfo['PINo']]]['Date'] = row[datainfo['Date']]
                PI_data[row[datainfo['PINo']]]['PINo'] = row[datainfo['PINo']]
                PI_data[row[datainfo['PINo']]]['Seller'] = zhCN_INPUT(row[datainfo['Seller']])
                PI_data[row[datainfo['PINo']]]['Buyer'] = zhCN_INPUT(row[datainfo['Buyer']])
            PI_data[row[datainfo['PINo']]]['Amt'] += float(row[datainfo['Amt']].replace(',',''))
            PI_data[row[datainfo['PINo']]]['List'].append([row[datainfo['Name']], str(row[datainfo['Spec']]), row[datainfo['Price']], row[datainfo['Qty']], row[datainfo['Amt']] ])

        return PI_data

    def compile(self):
        PI_data = self.sort_data()
        if PI_data is False:
            print("test")
            return False
        i = 0
        for key in PI_data:
            with open(self.home_dir + '/in/dome-0.xml', 'r') as f:
                doc_xml = f.read()
            doc_xml = self.replece_key(doc_xml, PI_data[key])
            with open(self.home_dir + '/out/'+ PI_data[key]['PINo'] +'.xml','w') as f:
                f.write(doc_xml)
            i += 1
        return i


    def replece_key(self, xml=None, data=None):
        if xml is None or data is None:
            return False
        xml = xml.replace('{#PINo#}',data['PINo'])
        xml = xml.replace('{#Date#}',data['Date'].decode('gb2312').encode('utf-8'))
        xml = xml.replace('{#Amt#}',str(data['Amt']))
        xml = xml.replace('{#RMB#}',to_rmb_upper(data['Amt']))
        xml = xml.replace('{#bug_Name#}',to_rmb_upper(data['Amt']))
        #供需双方信息
        feildname = ['Name', 'Address', 'Tel', 'BankName', 'BankNo', 'TaxID']
        buyer = self.db.get_company_by_name(data['Buyer'])
        seller = self.db.get_company_by_name(data['Seller'])
        for feild in feildname:
            buyer_strs = str((buyer[feild]))
            xml = xml.replace('{#buy_' + feild + '#}', buyer_strs)

            seller_strs = str((seller[feild]))
            xml = xml.replace('{#seller_' + feild + '#}', seller_strs)

        with open(self.home_dir + '/in/tr.xml', 'r') as f:
            tr_xml = f.read()

        for porduct in data['List']:
            tr_xml_str =tr_xml
            tr_xml_str = tr_xml_str.replace('{#Name#}',porduct[0].decode('gb2312').encode('utf-8'))
            tr_xml_str = tr_xml_str.replace('{#Spec#}',porduct[1].decode('gb2312').encode('utf-8'))
            tr_xml_str = tr_xml_str.replace('{#Price#}',str(porduct[2]))
            tr_xml_str = tr_xml_str.replace('{#Qty#}',porduct[3])
            tr_xml_str = tr_xml_str.replace('{#Amt#}',porduct[4])
            xml = xml.replace('{#tr_xml_str#}', tr_xml_str )

        xml = xml.replace('{#tr#}', '')
        return xml
def zhCN(sss):
    return sss.decode('utf-8').encode('gb2312')
def zhCN_INPUT(sss):
    return sss.decode('gb2312')

