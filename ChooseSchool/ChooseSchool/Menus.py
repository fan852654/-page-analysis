import os
class Menus:
    def __init__(self, args):
        self.dbconer = args
    def showInput(self):
        return input(">>")
    def showInputEx(self,name):
        return input(name + ">>")
    def showHr(self):
        print("****************************")
    def showNowCount(self):
        countres = self.dbconer.ExecQuery("select count(id) from dbo.School")
        print("当前数据表有" +str(countres[0][0])+"条记录")
    def showMainMenu(self):
        self.showHr()
        self.showNowCount()
        print("1：检索列表并加入数据库")
        print("2：清理数据表所有内容（慎重选择）")
        print("3：进入查询筛选系统")
        print("4：退出")
        print("5：清屏")
        self.showHr()
    def showErrorEx(self):
        print("失败，请检查网络情况和数据库情况！")
    def showStartEx(self):
        print("开始执行.......")
    def NotInIndex(self):
        print("请输入准确的数字！")
    def showSelectMenu(self):
        self.showHr()
        self.showNowCount()
        print("1：列出所有专业")
        print("2：列出所有研究方向")
        print("3：查询所需专业的信息")
        print("4：查询所需研究方向的信息")
        print("5：返回")
        print("6：清屏")
        self.showHr()
    def Clear(self):
        os.system('cls')