from PyQt5 import QtCore,QtWidgets
import sys,time,struct,pymysql
from PyQt5.QtWidgets import QApplication, QMainWindow
import modbus_tk.modbus_tcp as mtexport https_proxy=10.83.249.11:1080
import modbus_tk.defines as md
from PyQt5.QtCore import  QTimer
from PyQt5.QtChart import *
from pyecharts.globals import ThemeType
import pyecharts.options as opts
from pyecharts.charts import Line,Tab
from pyecharts.globals import CurrentConfig
CurrentConfig.ONLINE_HOST = "http://127.0.0.1:8080/assets/"
# 连接数据库
host = '127.0.0.1'  # 地址
user = 'root'  # 用户名
pwd = '123456'  # 密码
database = 'test'  # 数据库名
conn = pymysql.connect(host=host,
                       user=user, password=pwd,
                       database=database, charset='utf8')
cursor = conn.cursor()
# sql语句
sql = 'INSERT INTO temperature(time,tem1,tem2,tem3,tem4) VALUES ( %s, %s, %s, %s, %s)'
global  IP,hold_add,hold_qua,setdone
hold_add=hold_qua=input_add=input_qua=output_add=output_qua=setdone=0

def trans (mes):
            a=[str(i) for i in mes]
            b= ' '.join (a)
            return b


# 浮点数转换
# def ReadFloat(*args,reverse=True):
#     for n,m in args:
#         n,m = '%04x'%n,'%04x'%m
#     if reverse:
#         v = n + m
#     else:
#         v = m + n
#     y_bytes = bytes.fromhex(v)
#     y = struct.unpack('!f',y_bytes)[0]
#     y = round(y,2)
#     return y

def tranfloat(x):
    y=(float(x))*0.1
    y= round(y,2)
    return y

# def int2float(a,b):
#     f=0
#     try:
#         z0=hex(a)[2:].zfill(4) #取0x后边的部分 右对齐 左补零
#         z1=hex(b)[2:].zfill(4) #取0x后边的部分 右对齐 左补零
#         #z=z1+z0 #高字节在前 低字节在后
#         z=z0+z1 #低字节在前 高字节在后 
#         #print (z)  
#         f=round(struct.unpack('!f', bytes.fromhex(z))[0],1) #返回浮点数
#     except BaseException as e:
#         print(e)     
#     return f

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(658, 501)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(190, 140, 31, 16))
        self.label_5.setObjectName("label_5")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 110, 55, 16))
        self.label_2.setObjectName("label_2")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(100, 140, 71, 22))
        self.spinBox.setMinimumSize(QtCore.QSize(71, 22))
        self.spinBox.setMaximum(99999)
        self.spinBox.setObjectName("spinBox")
        self.spinBox_2 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_2.setGeometry(QtCore.QRect(240, 140, 71, 22))
        self.spinBox_2.setMaximum(99999)
        self.spinBox_2.setProperty("value", 4)
        self.spinBox_2.setObjectName("spinBox_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(100, 110, 121, 21))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(30, 140, 61, 16))
        self.label_8.setObjectName("label_8")
        self.push = QtWidgets.QPushButton(self.centralwidget)
        self.push.setGeometry(QtCore.QRect(330, 140, 75, 24))
        self.push.setAutoFillBackground(True)
        self.push.setObjectName("push")
        self.push.clicked.connect(self.clickButton)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(30, 230, 81, 16))
        self.label_9.setObjectName("label_9")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(30, 250, 561, 211))
        self.textBrowser.setObjectName("textBrowser")
        self.push_2 = QtWidgets.QPushButton(self.centralwidget)
        self.push_2.setGeometry(QtCore.QRect(400, 200, 81, 24))
        self.push_2.setObjectName("push_2")
        self.push_2.clicked.connect(self.displayclick)
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(30, 200, 91, 16))
        self.label_10.setObjectName("label_10")
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit.setGeometry(QtCore.QRect(80, 200, 121, 22))
        self.dateTimeEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2022, 5, 3), QtCore.QTime(0, 0, 0)))
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(210, 200, 111, 16))
        self.label_11.setObjectName("label_11")
        self.dateTimeEdit_2 = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit_2.setGeometry(QtCore.QRect(270, 200, 121, 22))
        self.dateTimeEdit_2.setDateTime(QtCore.QDateTime(QtCore.QDate(2022, 5, 1), QtCore.QTime(0, 0, 0)))
        self.dateTimeEdit_2.setObjectName("dateTimeEdit_2")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(30, 170, 71, 16))
        self.label_12.setObjectName("label_12")
        self.spinBox_3 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_3.setGeometry(QtCore.QRect(100, 170, 71, 22))
        self.spinBox_3.setMinimumSize(QtCore.QSize(71, 22))
        self.spinBox_3.setMaximum(99999)
        self.spinBox_3.setObjectName("spinBox_3")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(190, 170, 71, 16))
        self.label_17.setObjectName("label_17")
        self.spinBox_4 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_4.setGeometry(QtCore.QRect(240, 170, 71, 22))
        self.spinBox_4.setMinimumSize(QtCore.QSize(71, 22))
        self.spinBox_4.setMaximum(99999)
        self.spinBox_4.setProperty("value", 10000)
        self.spinBox_4.setObjectName("spinBox_4")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(310, 170, 31, 16))
        self.label_18.setObjectName("label_18")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(60, 80, 401, 18))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_13 = QtWidgets.QLabel(self.widget)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout.addWidget(self.label_13)
        self.label_14 = QtWidgets.QLabel(self.widget)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout.addWidget(self.label_14)
        self.label_15 = QtWidgets.QLabel(self.widget)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout.addWidget(self.label_15)
        self.label_16 = QtWidgets.QLabel(self.widget)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout.addWidget(self.label_16)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(40, 20, 381, 51))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.lcdNumber = QtWidgets.QLCDNumber(self.splitter)
        self.lcdNumber.setDigitCount(6)
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber.setStyleSheet("border: 2px solid black; color:red; background: white;") 
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.splitter)
        self.lcdNumber_2.setDigitCount(6)
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.lcdNumber_2.setStyleSheet("border: 2px solid black; color: red; background: white;") 
        self.lcdNumber_3 = QtWidgets.QLCDNumber(self.splitter)
        self.lcdNumber_3.setDigitCount(6)
        self.lcdNumber_3.setObjectName("lcdNumber_3")
        self.lcdNumber_3.setStyleSheet("border: 2px solid black; color: red; background: white;") 
        self.lcdNumber_4 = QtWidgets.QLCDNumber(self.splitter)
        self.lcdNumber_4.setDigitCount(6)
        self.lcdNumber_4.setStyleSheet("border: 2px solid black; color: red; background: white;") 
        self.lcdNumber_4.setObjectName("lcdNumber_4")
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(170, 170, 31, 16))
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21.setGeometry(QtCore.QRect(430, 50, 31, 16))
        self.label_21.setObjectName("label_21")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
       
    




    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_5.setText(_translate("MainWindow", "数量"))
        self.label_2.setText(_translate("MainWindow", "IP  地址"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "192.168.0.6"))
        self.label_8.setText(_translate("MainWindow", "起始地址"))
        self.push.setText(_translate("MainWindow", "连接设备"))
        self.label_9.setText(_translate("MainWindow", "获取数据："))
        self.push_2.setText(_translate("MainWindow", "显示温度曲线"))
        self.label_10.setText(_translate("MainWindow", "起始时间"))
        self.label_11.setText(_translate("MainWindow", "截至时间"))
        self.label_12.setText(_translate("MainWindow", "采集温度下限"))
        self.label_17.setText(_translate("MainWindow", "采集周期"))
        self.label_18.setText(_translate("MainWindow", "ms"))
        self.label_13.setText(_translate("MainWindow", "温度1"))
        self.label_14.setText(_translate("MainWindow", "温度2"))
        self.label_15.setText(_translate("MainWindow", "温度3"))
        self.label_16.setText(_translate("MainWindow", "温度4"))
        self.label_20.setText(_translate("MainWindow", "℃"))
        self.label_21.setText(_translate("MainWindow", "℃"))
    def __init__(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.connecttcp) if setdone>0 else ''
    def clickButton(self):
        global  IP,hold_add,hold_qua,setdone,low_temperature,cycle
        IP =self.lineEdit.text()
        hold_add=int(self.spinBox.text())
        hold_qua=int(self.spinBox_2.text())
        low_temperature=float(self.spinBox_3.text())
        cycle=int(self.spinBox_4.text())-15
        print(cycle)
        self.timer.start(500) if setdone==0 else ''
        self.timer.timeout.connect(self.connecttcp)  if setdone==0 else ''
        setdone=1

    def displayclick(self):
        start_time=self.dateTimeEdit.text()
        end_time=self.dateTimeEdit_2.text()
        try:   
            sql1 =f"""select * from temperature where time between '{start_time}' and '{end_time}'"""
            cursor.execute(sql1)
            data=list(cursor.fetchall())
            x_data=  [str(i[0]) for i in data]
            y1_data= [float(i[1]) for i in data]
            y2_data= [float(i[2]) for i in data]
            y3_data= [float(i[3]) for i in data]
            y4_data= [float(i[4]) for i in data]
            print(x_data, y1_data, y2_data, y3_data, y4_data)
        except:
            print ("Error: unable to fetch data")
        # 关闭数据库连接
        # conn.close()
        # get_line(x_data, y1_data, y2_data, y3_data, y4_data)
        # stinline(x_data, y1_data, y2_data, y3_data, y4_data)
        get_line=Line({"theme": ThemeType.MACARONS})
        get_line.add_xaxis(xaxis_data=x_data)
        get_line.add_yaxis(
                    series_name="温度1",
                    stack="总量",
                    y_axis = y1_data,
                    label_opts=opts.LabelOpts(is_show=False),
                )
        get_line.add_yaxis(
                    series_name="温度2",
                    stack="总量",
                    y_axis=y2_data,
                    label_opts=opts.LabelOpts(is_show=False),
                )
        get_line .add_yaxis(
                    series_name="温度3",
                    stack="总量",
                    y_axis=y3_data,
                    label_opts=opts.LabelOpts(is_show=False),
                )
        get_line .add_yaxis(
                    series_name="温度4",
                    stack="总量",
                    y_axis=y4_data,
                    label_opts=opts.LabelOpts(is_show=False),
                )
        get_line  .set_global_opts(
                    title_opts=opts.TitleOpts(title="加硬温度曲线"),
                    tooltip_opts=opts.TooltipOpts(trigger="axis"),
                    yaxis_opts=opts.AxisOpts(
                        type_="value",
                        axistick_opts=opts.AxisTickOpts(is_show=True),
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                        name='温度值（单位℃）',
                        name_location='middle',
                        name_gap=40,
                        name_textstyle_opts=opts.TextStyleOpts(
                            font_family='Times New Roman',
                            font_size=16
                            # font_weight='bolder',
                        )),
                    xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False,
                                            name='日期时间',
                                            name_location='middle',
                                            name_gap=30,  # 标签与轴线之间的距离，默认为20，最好不要设置20
                                            name_textstyle_opts=opts.TextStyleOpts(
                                                font_family='Times New Roman',
                                                font_size=16  # 标签字体大小
                                        )),
            )
        stinline1=Line(init_opts=opts.InitOpts(width="1000px", height="600px"))
        stinline1.add_xaxis(xaxis_data=x_data)
        stinline1.add_yaxis(
                    series_name="温度1",
                    y_axis=y1_data,
                    label_opts=opts.LabelOpts(is_show=False),
                   
                )
        stinline1.add_yaxis(
                    series_name="温度2",
                    y_axis=y2_data,
                    label_opts=opts.LabelOpts(is_show=False),
                   
                )
        stinline1.add_yaxis(
                    series_name="温度3",
                    y_axis=y3_data,
                    label_opts=opts.LabelOpts(is_show=False),
                )
        stinline1.add_yaxis(
                    series_name="温度4",
                    y_axis=y4_data,
                    label_opts=opts.LabelOpts(is_show=False),
                )       
        stinline1.set_global_opts(
                    title_opts=opts.TitleOpts(title="加硬温度曲线"),
                    tooltip_opts=opts.TooltipOpts(trigger="axis"),
                    yaxis_opts=opts.AxisOpts(
                        type_="value",
                        axistick_opts=opts.AxisTickOpts(is_show=True),
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                        name='温度值（单位℃）',
                        name_location='middle',
                        name_gap=40,
                        name_textstyle_opts=opts.TextStyleOpts(
                            font_family='Times New Roman',
                            font_size=16
                            # font_weight='bolder',
                        )),
                    xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False,
                                            name='日期时间',
                                            name_location='middle',
                                            name_gap=30,  # 标签与轴线之间的距离，默认为20，最好不要设置20
                                            name_textstyle_opts=opts.TextStyleOpts(
                                                font_family='Times New Roman',
                                                font_size=16  # 标签字体大小
                                        )),
            )
        tab = Tab()
        tab.add(get_line, tab_name="温度曲线1")
        tab.add(stinline1, tab_name="温度曲线2")
        tab.render()
        #tab.render_notebook()

    def connecttcp(self):    
        self.timer.start(cycle)
        master = mt.TcpMaster(IP, 502)
        master.set_timeout(5.0)
        try:
            Hold_value = master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=hold_add, quantity_of_x=hold_qua, output_value=5)  if hold_qua>0 else ''  
            datetime1 = time.strftime("%Y/%m/%d %H:%M:%S")
            insert_data=[datetime1,tranfloat(Hold_value[0]),tranfloat(Hold_value[1]),tranfloat(Hold_value[2]),tranfloat(Hold_value[3])]
            self.lcdNumber.display(insert_data[1])
            self.lcdNumber_2.display(insert_data[2])
            self.lcdNumber_3.display(insert_data[3])
            self.lcdNumber_4.display(insert_data[4])
            self.textBrowser.append(trans (insert_data))
            self.textBrowser.append("设备连接成功") 
            if insert_data[1]>low_temperature or insert_data[2]>low_temperature or insert_data[3]>low_temperature or insert_data[4]>low_temperature:
                try:               
                            res = cursor.execute(sql, insert_data) if hold_qua>0 else ''
                            self.textBrowser.append("数据库写入成功")  
                            conn.commit()
                except Exception as e:
                            self.textBrowser.append("数据库写入异常")
                            conn.rollback()
            else:
                pass
            # finally:
            # conn.close()
        except Exception as exc:
                self.textBrowser.append(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()))
                self.textBrowser.append("设备通讯异常")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui =Ui_MainWindow()# 这是类函数的名称
    ui.setupUi(MainWindow)# 运行类函数里的setupUi
    MainWindow.show()#显示窗口
    sys.exit(app.exec())


