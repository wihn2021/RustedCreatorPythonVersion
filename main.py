# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
# 篮球场5号柜A30  取件码  13827940

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

bil = './lib/turret/builtinlib/'
prl = './project/testunit/'


class turret:
    id = ''
    img = QImage()
    json = {}


class unit:
    id = ''
    json = {}


def copyfile(a, b):
    i = open(a, 'rb')
    o = open(b, 'wb')
    o.write(i.read())
    i.close()
    o.close()


class turdlg(QDialog):
    turlst = []
    diclist = {}

    def __init__(self, parent):
        super().__init__()
        self.load()
        self.pic = QPixmap()
        self.pp = QLabel(self)
        self.pp.setGeometry(120, 50, 280, 300)
        self.setGeometry(600, 300, 300, 430)
        self.xzk = QComboBox(self)
        self.xzk.setGeometry(10, 10, 280, 30)
        self.xzk.addItems(self.turlst)
        self.xzk.currentIndexChanged.connect(lambda: self.refresh())
        addbtn = QPushButton(self)
        addbtn.setText('Add')
        addbtn.setGeometry(70, 370, 60, 30)
        addbtn.clicked.connect(lambda: parent.addtur(self.diclist[self.xzk.currentText()],
                                                     bil + self.diclist[self.xzk.currentText()]['image']))
        editbtn = QPushButton(self)
        editbtn.setText('Edit')
        editbtn.setGeometry(170, 370, 60, 30)
        self.setWindowTitle('炮塔库')
        self.show()

    def refresh(self):
        print(self.xzk.currentIndex())
        self.pic = QPixmap(bil + self.diclist[self.xzk.currentText()]['image'])
        self.pp.setPixmap(self.pic)

    def load(self):
        t = open('./lib/turret/builtinlib/info.txt')
        self.turlst = eval(t.read())
        print(self.turlst)
        for i in self.turlst:
            tf = open(bil + i + '.txt')
            tmp = eval(tf.read())
            self.diclist[i] = tmp
        print(self.diclist)


class RC(QWidget):
    paintlist = []

    def __init__(self):
        super().__init__()
        self.mainfileurl = ''
        self.mainfiledir = ''
        self.itisanewfile = False
        self.setGeometry(200, 200, 1000, 800)
        self.setWindowTitle('Rusted Creator v0 --by wihn')
        self.dic = {}
        self.newdraw = QLabel(self)
        self.pic = QPixmap()
        self.pen = QPainter(self)
        self.menu = QMenuBar(self)
        self.filemenu = self.menu.addMenu('File')
        self.newaction = self.filemenu.addAction('New')
        self.newaction.triggered.connect(lambda: self.newfile())
        self.openaction = self.filemenu.addAction('Open')
        self.openaction.triggered.connect(lambda: self.loadunitfile())
        self.savefileaction = self.filemenu.addAction('Save')
        self.savefileaction.triggered.connect(lambda: self.savefile())
        self.initUI()
        self.dic['component'] = {}
        self.td = turdlg(self)
        self.td.show()

    def initUI(self):

        # self.setGeometry(300, 300, 300, 200)
        # self.setWindowTitle('Tooltips')
        self.show()

    def addtur(self, attrs, q):
        tid, ok = QInputDialog.getText(self, 'Enter an id for the turret', '不要重复（重复会覆盖）')
        if ok:
            self.dic['component'][tid] = attrs.copy()
            i = open(q, 'rb')
            o = open(self.mainfiledir + tid + '.png', 'wb')
            o.write(i.read())
            i.close()
            o.close()
            self.dic['component'][tid]['image'] = tid + '.png'
            self.dic['component'][tid]['x'] = 0
            self.dic['component'][tid]['y'] = 0
            self.dic['component'][tid]['visible'] = True
            self.refresh()

    def printpix(self, png, x, y):
        # pen = QPainter()
        self.pen.drawPixmap(x, y, self.pic)
        t = QLabel(self)
        t.setGeometry(50 + x, 50 + y, 300, 300)
        t.setPixmap(png)
        print('I\'m painting')
        t.show()
        self.paintlist.append(t)

    def refresh(self):
        print('Im refreshing')
        for i in self.paintlist:
            i.hide()
        for i in self.dic['component'].values():
            if i['visible']:
                p = QPixmap(self.mainfiledir + i['image'])
                self.printpix(p, i['x'], i['y'])

        self.newdraw.setGeometry(30, 30, 100, 100)
        self.newdraw.setPixmap(self.pic)
        self.newdraw.show()

    def newfile(self):
        self.itisanewfile = True
        self.mainfiledir = './tmp/'
        self.mainfileurl = './tmp/untitled.rc0'
        copyfile('./lib/blank.rc0', self.mainfileurl)

    def loadunitfile(self):
        arg, ok = QFileDialog.getOpenFileName(self, '打开文件', './doc', 'Rusted Creator v0文件(*.rc0)')
        if ok:
            f = open(arg, 'r')
            self.dic = eval(f.read())
            f.close()
            self.mainfileurl = arg
            self.mainfiledir = ''
            tmp = arg.split('/')
            tmp.pop()
            for i in tmp:
                self.mainfiledir += i
                self.mainfiledir += '/'

            self.refresh()
            self.pr = propdlg(self)
            self.pr.show()

    def savefile(self):
        if self.dic != {} and self.itisanewfile:
            arg, ok = QFileDialog.getSaveFileName(self, '保存文件', './doc', '*.rc0')
            if ok:
                print(self.dic)
                f = open(arg, 'w')
                sys.stdout = f
                print(self.dic)
                f.close()
                # 上面是主文件保存

        elif self.dic != {} and self.mainfileurl != '':
            g = open(self.mainfileurl, 'w')
            sys.stdout = g
            print(self.dic)
            g.close()

    def loadtodlg(self, sth):
        pass


class propdlg(QDialog):

    def __init__(self, parent: RC):
        super(propdlg, self).__init__()
        self.c = 0
        xin = open('./lib/tr.txt', 'r', encoding='utf-8')
        trd = eval(xin.read())
        self.setWindowTitle('属性')
        self.resize(400, 600)
        # conlo = QHBoxLayout()
        self.mo = QStandardItemModel(20, 2)
        self.table = QTableView(self)
        self.table.setModel(self.mo)
        # conlo.addWidget(self.table)
        self.mo.setHorizontalHeaderLabels(['property', 'value'])
        self.table.setGeometry(20, 20, 300, 400)
        self.generate(parent.dic['core']['basic'], trd, self.mo)
        self.table.show()
        self.show()

    def refresh(self, dic):
        self.c = 0
        for i in dic:
            self.table.setItem()

    def generate(self, dic1, tr, mo: QStandardItemModel):
        c = 0
        for i in dic1:
            item = QStandardItem(tr[i])
            mo.setItem(c, 0, item)
            item2 = QStandardItem(dic1[i])
            mo.setItem(c, 1, item2)
            c += 1


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RC()
    sys.exit(app.exec_())
