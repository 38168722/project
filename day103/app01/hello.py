from app01 import deem

class Test01(object):
    def getInfo(self):
        return "第一个info"

    getInfo.text="这是一个什么文本"
    getInfo.name="这是一个什么姓名"

    def printInfo(self):
        print("""
            getInfo.text=%s
            getInfo.name=%s
        """%(self.getInfo.text,self.getInfo.name))

abc=Test01()
abc.printInfo()

