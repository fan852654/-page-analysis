#!/usr/bin/python3
from DbUtil import *
from HtmlUti import *
from Menus import *
from lxml import *
from bs4 import BeautifulSoup
from SchoolClass import *
dbconer = ""
htmlconer= ""
postData= ""
maxpage= ""
ShowControl = ""

def Init():
    global dbconer,htmlconer,postData,maxpage,ShowControl
    #设置数据库的连接字符串 [主机地址，用户名，密码，使用的数据库]
    dbconer = Database(["192.168.0.100","sa","Fan.zs852654136","Schools"])
    ShowControl = Menus(dbconer)
    #研招网网站
    htmlconer = HtmlUtil("https://yz.chsi.com.cn")
    htmlconer.setSuffix("/zsml/queryAction.do")
    #设置所需查询的基础信息，不设置为所有
    postData = {"ssdm":"","dwmc":"","mldm":"zyxw","mlmc":"","zymc":"","xxfs":"","yjxkdm":"0854","pageno":""}
    #设置所需查询的页数，不能超过那个页面的最大页数
    maxpage = 11
    tabresult = dbconer.ExecQuery("select name from sys.tables")
    needinitdatabase = True
    for tbname in tabresult:
        if tbname[0] == 'School':
            needinitdatabase = False
            break
    if needinitdatabase:
        dbconer.ExecNoQuery("CREATE TABLE [dbo].[School]([id] [int] IDENTITY(1,1) NOT NULL,	[schoolname] [varchar](max) NULL,	[yuanxi] [varchar](max) NULL,	[zhuanye] [varchar](max) NULL,	[research] [varchar](max) NULL,	[number] [varchar](max) NULL, CONSTRAINT [PK_School] PRIMARY KEY CLUSTERED (	[id] ASC)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]")
    return

def decSchool():
    global dbconer,htmlconer,postData,maxpage
    listSchooles = []
    schoolsClassList = []
    i = 1
    while i <= maxpage:
        postData['pageno'] = i
        homepage = htmlconer.postPage(postData)
        homepage=BeautifulSoup(homepage,'html.parser')
        schoolchildren=homepage.select("tbody form a")
        for formschoolchildren in schoolchildren:
            sclass = School()
            sclass.setSchoolName(formschoolchildren.text)
            sclass.setUrl(formschoolchildren.attrs['href'])
            listSchooles.append(sclass)
        i = i+1
    for school in listSchooles:
        htmlconer.setSuffix(school.Urlsuffix)
        schoolpage = htmlconer.getPage()
        schoolpage = BeautifulSoup(schoolpage,'html.parser')
        schooltrs=schoolpage.select("table tbody tr")
        schoolname = school.SchoolName
        for schooltr in schooltrs:
            sclass = School()
            schooltd = schooltr.select("td")
            sclass.setSchoolName(schoolname)
            sclass.setYuanXi(schooltd[1].text) 
            sclass.setZhuanYe(schooltd[2].text)
            sclass.setResearchDirection(schooltd[3].text)
            sclass.setNumber(schooltd[6].select("script")[0].text.split('\'')[1])
            schoolsClassList.append(sclass)
    for scho in schoolsClassList:
        sql = "insert into School(schoolname,yuanxi,zhuanye,research,number) values('"+scho.SchoolName+"','"+scho.YuanXi+"','"+scho.ZhuanYe+"','"+scho.Research+"','"+scho.Number+"')"
        dbconer.ExecNoQuery(sql)
    return 1

def removeAlldata():
    global dbconer
    dbconer.ExecNoQuery("DELETE FROM [dbo].[School]")
    return 1
def showZhuanyeData():
    global dbconer
    result = dbconer.ExecQuery("SELECT [zhuanye]  FROM [dbo].[School]")
    i = 0
    strshow = ""
    for x in result:
        strshow = strshow + x[0] + "\t"
        i = i +1
        if i == 3:
            print(strshow)
            strshow = ""
            i = 0
    return
def showReData():
    global dbconer
    result = dbconer.ExecQuery("SELECT [research]  FROM [dbo].[School] group by [research] order by [research] ")
    i = 0
    strshow = ""
    for x in result:
        strshow = strshow + x[0] + "\t"
        i = i +1
        if i == 3:
            print(strshow)
            strshow = ""
            i = 0
    return
def selectNeedZhuanye(name):
    global dbconer
    result = dbconer.ExecQuery("SELECT [id],[schoolname],[yuanxi],[zhuanye],[research],[number] FROM [dbo].[School] where [zhuanye] like '%"+name +"%'")
    i = 0
    strshow = ""
    for x in result:
        print(getAllThing(x))
    return
def getAllThing(arg):
    return arg[1]+" "+arg[2]+" "+arg[3]+" "+arg[4]+ " "+arg[5]
def selectNeedRe(name):
    global dbconer
    result = dbconer.ExecQuery("SELECT [id],[schoolname],[yuanxi],[zhuanye],[research],[number] FROM [dbo].[School] where [research] like '%"+name +"%'")
    i = 0
    strshow = ""
    for x in result:
        strshow = strshow + getAllThing(x) + "\t"
        print(getAllThing(x))
    return
if __name__ == '__main__':
    Init()
    needExit = False
    ChooseIndex = 0
    while needExit is not True:
        ShowControl.showMainMenu()
        ChooseIndex = ShowControl.showInput()
        if ChooseIndex == "4":
            needExit = True
        elif ChooseIndex == "1":
            print("开始执行.......")
            result = decSchool()
            if result == 1:
                print("已经成功检索！")
                continue
            else:
                ShowControl.showErrorEx()
                continue
        elif ChooseIndex == "2":
            ShowControl.showStartEx()
            result = removeAlldata()
            if result == 1:
                print("已经成功清除！")
                continue
            else:
                ShowControl.showErrorEx()
                continue
            continue
        elif ChooseIndex == "3":
            needExitselect = False
            while needExitselect is not True:
                ShowControl.showSelectMenu()
                ChooseIndex = ShowControl.showInput()
                if ChooseIndex == "1":
                    showZhuanyeData()
                elif ChooseIndex == "2":
                    showReData()
                elif ChooseIndex == "3":
                    selectNeedZhuanye(ShowControl.showInputEx("清输入专业名称"))
                elif ChooseIndex == "4":
                    selectNeedRe(ShowControl.showInputEx("清输入研究方向名称"))
                elif ChooseIndex == "5":
                    needExitselect = True
                elif ChooseIndex == "6":
                    ShowControl.Clear()
            continue
        elif ChooseIndex == "5":
            ShowControl.Clear()
            continue
        else:
            ShowControl.NotInIndex()
            continue
    exit(0)