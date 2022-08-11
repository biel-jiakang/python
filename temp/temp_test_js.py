import sys,time,struct,pymysql
import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md
from pyecharts.globals import ThemeType
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QApplication, QHBoxLayout, QWidget, QGridLayout, QLabel, QSpinBox, \
    QSpacerItem, QSizePolicy, QComboBox,QPushButton,QTextBrowser,QDateTimeEdit
from PyQt5 import QtCore
from pyecharts.charts import  Line
from pyecharts import options as opts
from PyQt5.QtCore import  QTimer
from sqlalchemy import true

TITLE_TEXT = "图表"
TITLE_SUBTEXT = "副标题"
ATTR = ["采集下限", "采集周期", "获取数据", "起始时间", "结束时间"]
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
global x_data, y1_data, y2_data, y3_data, y4_data,dx_data, dy1_data, dy2_data, dy3_data,dy4_data
    
x_data = ["A", "B", "C", "D", "E", "F", "G"]
y1_data = [0, 0, 0, 0, 0, 0, 0]
y2_data = [420, 632, 701, 534, 890, 1130, 1120]
y3_data = [150, 232, 201, 154, 190, 330, 410]
y4_data = [320, 332, 301, 334, 390, 330, 320]
dy1_data =[0,0,0,0,0,0,0,0,0,0,0,0,0]
dx_data=[0,0,0,0,0,0,0,0,0,0,0,0,0]
dy2_data=[0,0,0,0,0,0,0,0,0,0,0,0,0]
dy3_data=[0,0,0,0,0,0,0,0,0,0,0,0,0]
dy4_data=[0,0,0,0,0,0,0,0,0,0,0,0,0]
def trans (mes):
            a=[str(i) for i in mes]
            b= ' '.join (a)
            return b

def tranfloat(x):
    y=(float(x))*0.1
    y= round(y,2)
    return y

class Form(QDialog):
    def __init__(self):
        super(Form, self).__init__()
        self.view = None
        self.echarts = False
        self.initUi()
        self.load_url()
        self.timer = QTimer()
        self.timer.timeout.connect(self.connecttcp) if setdone>0 else ''

    def initUi(self):
        self.hl = QHBoxLayout(self)
        self.widget = QWidget()
        self.gl = QGridLayout(self.widget)
        #ATTR1
        label1 = QLabel(ATTR[0] + ':'+'℃')
        self.gl.addWidget(label1, 1 - 1, 0, 1, 1)
        self.spinbox1 = QSpinBox()
        self.spinbox1.setSingleStep(100)
        self.spinbox1.setObjectName('spinbox')
        self.spinbox1.valueChanged.connect(self.set_options)
        self.spinbox1.setMaximum(400)
        
        self.gl.addWidget(self.spinbox1, 1 - 1, 1, 1, 1)
        # ATTR2
        label2 = QLabel(ATTR[1] + ':'+'ms')
        self.gl.addWidget(label2, 2 - 1, 0, 1, 1)
        self.spinbox2 = QSpinBox()
        self.spinbox2.setSingleStep(100)
        self.spinbox2.setObjectName('spinbox')
        self.spinbox2.valueChanged.connect(self.set_options)
        self.spinbox2.setMaximum(100000)
        self.spinbox2.setProperty("value", 10000)
        self.gl.addWidget(self.spinbox2, 2 - 1, 1, 1, 1)
        # 连接设备按钮
        self.push =  QPushButton()
        #self.push.setGeometry(QtCore.QRect(330, 140, 75, 24))
        #self.push.setAutoFillBackground(True)
        self.push.setObjectName("push")
        self.push.setText( "连接设备")
        self.push.clicked.connect(self.clickButton)
        self.gl.addWidget(self.push, 3 - 1, 1, 1, 1)
        # ATTR4
        label4 = QLabel(ATTR[2] + ':')
        self.gl.addWidget(label4, 4 - 1, 0, 1, 1)
        
        # 显示读取状态
        self.textBrowser = QTextBrowser()
        self.textBrowser.setObjectName("textBrowser")  
        self.gl.addWidget(self.textBrowser, 5 - 1, 1, 1, 1)
        # ATTR6
        label6 = QLabel(ATTR[3] + ':')
        self.gl.addWidget(label6, 6 - 1, 0, 1, 1)
        self.dateTimeEdit = QDateTimeEdit()
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.dateTimeEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2022, 5, 3), QtCore.QTime(0, 0, 0)))
        self.gl.addWidget(self.dateTimeEdit, 6 - 1, 1, 1, 1)
        # ATTR7
        label7 = QLabel(ATTR[4] + ':')
        self.gl.addWidget(label7, 7 - 1, 0, 1, 1)
        self.dateTimeEdit_2 = QDateTimeEdit()
        self.dateTimeEdit_2.setObjectName("dateTimeEdit_2")
        self.dateTimeEdit_2.setDateTime(QtCore.QDateTime(QtCore.QDate(2022, 5, 4), QtCore.QTime(0, 0, 0)))
        self.gl.addWidget(self.dateTimeEdit_2, 7 - 1, 1, 1, 1)
        # 显示温度曲线
        self.push_2 =  QPushButton()
        self.push_2.setObjectName("push_2")
        self.push_2.setText( "显示温度曲线")
        self.push_2.clicked.connect(self.displayclick)
        self.gl.addWidget(self.push_2, 8 - 1, 1, 1, 1)



        self.hl.addWidget(self.widget)
        vs = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gl.addItem(vs, 8, 0, 1, 2)
        self.combobox_type = QComboBox()
        self.combobox_type.currentIndexChanged.connect(self.reload_canvas)
        self.combobox_type.addItems(['实时曲线', '温度堆叠图', '温度折线图'])
        self.gl.addWidget(self.combobox_type, 8, 0, 1, 2)
        # self.combobox_theme = QComboBox()
        # self.combobox_theme.currentTextChanged.connect(self.change_theme)
        # self.combobox_theme.addItems(['light', 'dark'])
        # self.gl.addWidget(self.combobox_theme, 8, 0, 1, 2)
        # 添加web view
        self.view = QWebEngineView()
        self.view.setContextMenuPolicy(Qt.NoContextMenu)
        self.hl.addWidget(self.view)

    def change_theme(self, theme):
        if not self.view:
            return
        options = self.get_options(x_data, y1_data, y2_data, y3_data, y4_data,dx_data, dy1_data, dy2_data, dy3_data, dy4_data)
        if not options:
            return
        self.view.page().runJavaScript(
            f'''
                myChart.dispose();
                var myChart = echarts.init(document.getElementById('container'), '{theme}', {{renderer: 'canvas'}});
                myChart.clear();
                var option = eval({options});
                myChart.setOption(option);
            '''
        )

    def load_url(self):
        url = QUrl("file:///template.html")
        self.view.load(url)
        self.view.loadFinished.connect(self.set_options)

    def reload_canvas(self):
        if not self.view:
            return
            # 重载画布
        options = self.get_options(x_data, y1_data, y2_data, y3_data, y4_data,dx_data, dy1_data, dy2_data, dy3_data, dy4_data)
        if not options:
            return
        self.view.page().runJavaScript(
            f'''
                myChart.clear();
                var option = eval({options});
                myChart.setOption(option);
            '''
        )
    def clickButton(self):
        global  IP,hold_add,hold_qua,setdone,low_temperature,cycle
        IP ="127.0.0.1"
        hold_add=0
        hold_qua=4
        low_temperature=float(self.spinbox1.text())
        cycle=int(self.spinbox2.text())-15       
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
            global x_data, y1_data, y2_data, y3_data, y4_data
            x_data=  [str(i[0]) for i in data]
            y1_data= [float(i[1]) for i in data]
            y2_data= [float(i[2]) for i in data]
            y3_data= [float(i[3]) for i in data]
            y4_data= [float(i[4]) for i in data]
            print(x_data, y1_data, y2_data, y3_data, y4_data)
            

        except:
            print ("Error: unable to fetch data")
        # 关闭数据库连接
        
    def connecttcp(self):    
        self.timer.start(cycle)
        master = mt.TcpMaster(IP, 502)
        master.set_timeout(5.0)
        try:
            Hold_value = master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=hold_add, quantity_of_x=hold_qua, output_value=5)  if hold_qua>0 else ''               
            datetime1 = time.strftime("%Y/%m/%d %H:%M:%S")
            self.textBrowser.append(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()))
            self.textBrowser.append("设备连接成功")              
            insert_data=[datetime1,tranfloat(Hold_value[0]),tranfloat(Hold_value[1]),tranfloat(Hold_value[2]),tranfloat(Hold_value[3])]
            display_data=[tranfloat(Hold_value[0]),tranfloat(Hold_value[1]),tranfloat(Hold_value[2]),tranfloat(Hold_value[3])]
            self.textBrowser.append(trans (display_data))
            
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
        dx_data.pop(0)
        dx_data.append(datetime1)
        dy1_data.pop(0)
        dy2_data.pop(0)
        dy3_data.pop(0)
        dy4_data.pop(0)
        dy1_data.append(display_data[0])
        dy2_data.append(display_data[1])
        dy3_data.append(display_data[2])
        dy4_data.append(display_data[3])
        print(datetime1,display_data[0])
        print('dx_data',dx_data)
        print('dy1_data',dy1_data)
        print('x_data',x_data)
        self.reload_canvas()

    def set_options(self):
        if not self.view:
            return
        if not self.echarts:
            # 初始化echarts
            self.view.page().runJavaScript(
                '''
                    var myChart = echarts.init(document.getElementById('container'), 'light', {renderer: 'canvas'});
                '''
            )
            self.echarts = True

        options = self.get_options(x_data, y1_data, y2_data, y3_data, y4_data,dx_data, dy1_data, dy2_data, dy3_data, dy4_data)
        #options = self.displayclick()
        if not options:
            return

        self.view.page().runJavaScript(
            f'''
                var option = eval({options});
                myChart.setOption(option);
            '''
        )


    def get_options(self,x_data, y1_data, y2_data, y3_data, y4_data,dx_data, dy1_data, dy2_data, dy3_data, dy4_data):
        # v1, v2, v3, v4, v5, v6 = self.spinbox1.value(), self.spinbox2.value(), self.spinbox3.value(), self.spinbox4.value(), \
        #                          self.spinbox5.value(), self.spinbox6.value()
        # v = [v1, v2, v3, v4, v5, v6]
        
        if self.combobox_type.currentIndex() == 0:
            # 实时曲线
             options = self.stline_bar(dx_data, dy1_data, dy2_data, dy3_data, dy4_data)
        elif self.combobox_type.currentIndex() == 1:
            # 堆叠图
            options = self.create_line_bar(x_data, y1_data, y2_data, y3_data, y4_data)
        elif self.combobox_type.currentIndex() == 2:
            # 折线图
             options = self.create_line(x_data, y1_data, y2_data, y3_data, y4_data)
        elif self.combobox_type.currentIndex() == 3:
            # 折线、柱状图
            
            options = self.create_line_bar(x_data, y1_data, y2_data, y3_data, y4_data)
        else:
            return
        return options
   

    def create_line(self, x_data, y1_data, y2_data, y3_data, y4_data):
        # line = Line()
        # line.add_xaxis(ATTR)
        # line.add_yaxis('商家', v)
        # line.set_global_opts(title_opts=opts.TitleOpts(title=TITLE_TEXT, subtitle=TITLE_SUBTEXT))
        # return line.dump_options()
        line=Line(init_opts=opts.InitOpts(width="1000px", height="600px"))
        line.add_xaxis(xaxis_data=x_data)
        line.add_yaxis(
            series_name="温度1",
            y_axis=y1_data,
            label_opts=opts.LabelOpts(is_show=False),
            # 显示最大值和最小值
            # markpoint_opts=opts.MarkPointOpts(
            #     data=[
            #         opts.MarkPointItem(type_="max", name="最大值"),
            #         opts.MarkPointItem(type_="min", name="最小值"),
            #     ]
            # ),
            # 显示平均值
            # markline_opts=opts.MarkLineOpts(
            #     data=[opts.MarkLineItem(type_="average", name="平均值")]
            # ),
        )
        line.add_yaxis(
            series_name="温度2",
            y_axis=y2_data,
            label_opts=opts.LabelOpts(is_show=False),
            # 设置刻度标签
            # markpoint_opts=opts.MarkPointOpts(
            #     data=[opts.MarkPointItem(value=-2, name="周最低", x=1, y=-1.5)]
            # ),
            # markline_opts=opts.MarkLineOpts(
            #     data=[
            #         opts.MarkLineItem(type_="average", name="平均值"),
            #         opts.MarkLineItem(symbol="none", x="90%", y="max"),
            #         opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
            #     ]
            # ),
        )
        line.add_yaxis(
            series_name="温度3",
            y_axis=y3_data,
            label_opts=opts.LabelOpts(is_show=False),
        )
        line.add_yaxis(
            series_name="温度4",
            y_axis=y4_data,
            label_opts=opts.LabelOpts(is_show=False),
        )
        line.set_global_opts(
            title_opts=opts.TitleOpts(title="加硬温度历史曲线"),
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
                                        )))
        return line.dump_options()                 

    
    
    def create_line_bar(self,x_data, y1_data, y2_data, y3_data, y4_data):
        line=Line({"theme": ThemeType.MACARONS})
        line.add_xaxis(xaxis_data=x_data)
        line.add_yaxis(
            series_name="温度1",
            stack="总量",
            y_axis = y1_data,
            label_opts=opts.LabelOpts(is_show=False),
        )
        line.add_yaxis(
            series_name="温度2",
            stack="总量",
            y_axis=y2_data,
            label_opts=opts.LabelOpts(is_show=False),
        )
        line.add_yaxis(
            series_name="温度3",
            stack="总量",
            y_axis=y3_data,
            label_opts=opts.LabelOpts(is_show=False),
        )
        line.add_yaxis(
            series_name="温度4",
            stack="总量",
            y_axis=y4_data,
            label_opts=opts.LabelOpts(is_show=False),
        )
        line.set_global_opts(
            title_opts=opts.TitleOpts(title="加硬温度历史曲线"),
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
        
        
        return line.dump_options()

    def stline_bar(self,x_data, y1_data, y2_data, y3_data, y4_data):
        line=Line({"theme": ThemeType.MACARONS})
        line.add_xaxis(xaxis_data=x_data)
        line.add_yaxis(
            series_name="温度1",
            stack="总量",
            y_axis = y1_data,
            label_opts=opts.LabelOpts(is_show=True),
        )
        line.add_yaxis(
            series_name="温度2",
            stack="总量",
            y_axis=y2_data,
            label_opts=opts.LabelOpts(is_show=True),
        )
        line.add_yaxis(
            series_name="温度3",
            stack="总量",
            y_axis=y3_data,
            label_opts=opts.LabelOpts(is_show=True),
        )
        line.add_yaxis(
            series_name="温度4",
            stack="总量",
            y_axis=y4_data,
            label_opts=opts.LabelOpts(is_show=True),
        )
        line.set_global_opts(
            title_opts=opts.TitleOpts(title="加硬温度实时曲线"),
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
        
        
        return line.dump_options()


       
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle('fusion')
    form = Form()
    form.show()
    sys.exit(app.exec_())
