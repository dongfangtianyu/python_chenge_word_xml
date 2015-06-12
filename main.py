#-*- coding: utf-8 -*-


import sys
import time
from db import db
from contents import contents

def MakeXML():
    print(zhCN('\r\n\r\n生成采购合同\r\n=====================\r\n'))
    print(zhCN('现在，请将表格中的产品清单复制到剪贴板\r\n\r\n完成后按下回车键继续'))
    raw_input()
    mydb = db()
    job = contents(mydb)
    nums = str(job.compile())
    mydb.close_db()
    print(zhCN('\r\n\r\n==================\r\n'))
    print(time.strftime('\r\n\r\n%Y-%m-%d %H:%M:%S  ') + zhCN(nums +'份 合同生成完毕！已经保存在\\out目录下'))
    print_meun()

def CompanyMng():
    mydb = db()
    companylist = mydb.get_list()
    companylist = mydb.data['company']
    print(zhCN('\r\n\r\n公司列表\r\n=====================\r\n'))
    for company in companylist:
        print(' %s . %s\r\n' % (company, companylist[company]['Name']))
    print('\r\n %s . %s' % ('0', zhCN('返回上一层菜单')))
    print(' %s . %s' % ('+', zhCN('录入公司信息')))
    company_id = raw_input(zhCN('\r\n请输入公司ID:'))
    if company_id =='0':
        pass
    elif company_id == '+':
        data={}
        data['Name']=zhCN_INPUT(raw_input(zhCN('公司名称: ')))
        data['Address']=zhCN_INPUT(raw_input(zhCN('地    址: ')))
        data['Tel']=zhCN_INPUT(raw_input(zhCN('电    话: ')))
        data['BankName'] = zhCN_INPUT(raw_input(zhCN('银    行: ')))
        data['BankNo'] = zhCN_INPUT(raw_input(zhCN('银行帐号: ')))
        data['TaxID'] = zhCN_INPUT(raw_input(zhCN('税    号: ')))
        mydb.insert(data, 'company')
        print(zhCN('\r\n\r\n录入成功 - %s' % data['Name']) )
    else:
        company = mydb.get(int(company_id))
        print(zhCN('\r\n\r\n公司信息\r\n=====================\r\n'))
        print(zhCN('公司名称: %s' % company['Name']))
        print(zhCN('地    址: %s' % company['Address']))
        print(zhCN('电    话: %s' % company['Tel']))
        print(zhCN('银    行: %s' % company['BankName']))
        print(zhCN('银行帐号: %s' % company['BankNo']))
        print(zhCN('税    号: %s' % company['TaxID']))
        print(zhCN('\r\n修改 - 输入 e \r\n删除 - 输入 d \r\n返回 - 输入 0'))

        command = raw_input(zhCN('\r\n指令:'))
        if command =='d':
            print(zhCN('\r\n\r\n删除成功 - %s' % company['Name']) )
            mydb.delete(company['ID'], 'company')
        elif command =='e':
            print(zhCN('\r\n\r\n编辑公司信息\r\n=====================\r\n'))
            datainfo = mydb.datainfo['company']
            i = 1
            for feild in datainfo[1:]:
                print(zhCN('  %d . %s' % (i, company[feild])))
                i += 1
            feild_id = input(zhCN('\r\n要修改的内容编号:'))
            company[datainfo[feild_id]]= zhCN_INPUT(raw_input(zhCN('新的内容: ')))
            mydb.update(company, 'company')
            print(zhCN('\r\n\r\n修改成功 - %s' % company['Name']) )


    mydb.close_db()
    return print_meun()

def zhCN(sss):
    return sss.decode('utf-8').encode('gb2312')
def zhCN_INPUT(sss):
    return sss.decode('gb2312')

def help():
    print('help')

def exit():
    sys.exit(0)

def print_meun():
    global menu
    i = 1
    print(zhCN('\r\n\r\n主菜单\r\n=====================\r\n'))
    for m in menu[1:]:
        print('  %d.  %s\r\n'% ( i ,zhCN(menu[i][0])))
        i += 1
    print('\r\n  %d.  %s'% ( 0 ,zhCN(menu[0][0])))



if __name__=='__main__':

    menu= (('退出','exit'),
           ('生成采购合同','MakeXML'),
           ('管理公司信息','CompanyMng'),
           ('帮助','help')
           )
    print_meun()

    while(True):
        command = input(zhCN('\r\n请输入要选择的功能(序号):'))

        if (isinstance(command,int) is True) and ( len(menu) > command )is True:
            eval(menu[command][1])()
        elif command =='exit' :
            exit()
        elif command == 'help' :
            help()
        elif command == 'menu':
            print_meun()
        else:
            print(zhCN('错误: 请输入菜单中存在的选项序号 !'))
            print(type(command))