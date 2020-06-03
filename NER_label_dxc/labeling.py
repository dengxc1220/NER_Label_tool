#1.3 版本 提供JSON格式文件的输入及导出以及标注的键盘绑定
from tkinter import *
# from tkinter.ttk import *
import hashlib
import time
from tkinter import filedialog
import chardet
import math
import tkinter
import numpy as np
from tkinter.scrolledtext import ScrolledText
import tkinter.font as tkFont
import os
from tkinter.messagebox import showinfo
import json

LOG_LINE_NUM = 0

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
        self.max1=""
        self.filename=""
        self.filePath = ""
        self.content = ""
        # self.btns_names=['人名','年龄','毕业院校','工作单位','其他数值']
        self.btns_names=['person','birthyear','age','scho','work_loc']

    #设置窗口
    def set_init_window(self):
        # 设置输入输出框字体
        # ft = tkFont.Font(family='宋体', size=15)
        ft = tkFont.Font(family='微软雅黑', size=15)

        self.init_window_name.title("履历命名实体识别")           #窗口名
        #self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1500x1000+10+10')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签
        self.init_data_label = Label(self.init_window_name, text="待处理数据")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = Label(self.init_window_name, text="日志")
        self.log_label.grid(row=12, column=0)

        #文本框
        self.init_data_Text = ScrolledText(self.init_window_name, width=67, height=35,font=ft)  #原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = ScrolledText(self.init_window_name, width=70, height=49,font=ft)  #处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = Text(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        self.init_data_Text.bind("<Button-1>", self.button_start)
        self.init_data_Text.bind("<ButtonRelease-1>", self.button_end)

        #按钮
        # self.str_trans_to_md5_button = Button(self.init_window_name, text="字符串转MD5", bg="lightblue", width=10,command=self.str_trans_to_md5)  # 调用内部方法  加()为直接调用
        # self.str_trans_to_md5_button.grid(row=1, column=11)
        #导入文件按钮
        self.input_button = Button(self.init_window_name,text="导入文件",bg="lightgreen",width=8,command=self.openfile)
        self.input_button.grid(row=0, column=2)

        self.input_button = Button(self.init_window_name,text="上一文本",bg="lightgreen",width=8,command=self.openLastfile)
        self.input_button.grid(row=0, column=5)

        self.input_button = Button(self.init_window_name,text="下一文本",bg="lightyellow",width=8,command=self.openNextfile)
        self.input_button.grid(row=0, column=7)
        # 输入窗口清空按钮
        self.delet_input_button = Button(self.init_window_name, text="一键清空", bg="#DB7093", width=8,command=self.delet_ofInput)
        self.delet_input_button.grid(row=0, column=3)
        #展示窗口清空按钮
        self.delet_result_button = Button(self.init_window_name, text="一键清空", bg="#DB7093", width=8,command=self.delet_ofResult)
        self.delet_result_button.grid(row=0,column=13)
        #导出文件按钮
        self.output_button = Button(self.init_window_name,text="导出文件",bg="lightgreen",width=8,command=self.outputfile)
        self.output_button.grid(row=0,column=14)
        #标记解剖部位按钮
        self.show_button = Button(self.init_window_name,text=self.btns_names[0],bg="lightblue",width='8',command=self.show_jpbw)
        self.show_button.grid(row=2, column=10)
        # 标记症状描述按钮
        self.show_button = Button(self.init_window_name, text=self.btns_names[1],bg="lightyellow", width='8', command=self.show_zzms)
        self.show_button.grid(row=3, column=10)
        # 标记独立症状按钮
        self.show_button = Button(self.init_window_name, text=self.btns_names[2], bg="lightgreen",width='8', command=self.show_dlzz)
        self.show_button.grid(row=4, column=10)
        # 标记药物按钮
        self.show_button = Button(self.init_window_name, text=self.btns_names[3],bg="#DB7093", width='8', command=self.show_yw)
        self.show_button.grid(row=5, column=10)
        # 标记手术按钮
        self.show_button = Button(self.init_window_name, text=self.btns_names[4],bg="lightpink", width='8', command=self.show_ss)
        self.show_button.grid(row=1, column=10)
        # 恢复操作按钮
        self.recover_button = Button(self.init_window_name, text="恢复", width='8', command=self.recover)
        self.recover_button.grid(row=0,column =15)
        # 标注撤销功能ctrl+z实现
        self.back_button = Button(self.init_window_name, text="撤销", width='8', command=self.backToHistory)
        self.back_button.grid(row=0, column=16)
        self.result_data_Text.bind('<Control-Key-z>',self.backToHistory)

        self.result_data_Text.edit_separator()

    #功能函数
    def str_trans_to_md5(self):
        src = self.init_data_Text.get(1.0,END).strip().replace("\n","").encode()
        #print("src =",src)
        if src:
            try:
                myMd5 = hashlib.md5()
                myMd5.update(src)
                myMd5_Digest = myMd5.hexdigest()
                #print(myMd5_Digest)
                #输出到界面
                self.result_data_Text.delete(1.0,END)
                self.result_data_Text.insert(1.0,myMd5_Digest)
                self.write_log_to_Text("INFO:str_trans_to_md5 success")
            except:
                self.result_data_Text.delete(1.0,END)
                self.result_data_Text.insert(1.0,"字符串转MD5失败")
        else:
            self.write_log_to_Text("ERROR:str_trans_to_md5 failed")
    #获取鼠标选中文本
    def button_start(self,event):
        global s
        global line_no
        s = self.init_data_Text.index('@%s,%s' % (event.x, event.y))
        line_no=str(s).split('.')[0]
        s=str(s).split('.')[1]

    def button_end(self,event):
        global e
        e = self.init_data_Text.index('@%s,%s' % (event.x, event.y))
        e = str(e).split('.')[1]

    # 处理选中位置参数
    def get_loc(self):
        print("get_loc",self.init_data_Text.selection_get(),self.init_data_Text.index('insert'),self.init_data_Text.index('insert').split('.'))
        e=int(str(self.init_data_Text.index('insert')).split('.')[1])-1 # 末尾列数
        ll=int(str(self.init_data_Text.index('insert')).split('.')[0])-1 # 行号
        con_num=len(self.init_data_Text.selection_get())
        s=e-con_num+1 # 开始列数
        return s,e,ll

    def get_RMRB_res(self, text, string):
        # 注意：导入时需要将文字都进行多余字符删除。
        # 存放数据集
        print("t&string",string)
        sentences = []
        # 临时存放每一个句子
        sentence = []
        content = text
        res_dict = {}
        # for line in open(label_filepath, encoding='UTF-8'):
        for line in string.split('\n'):
            # res = line.strip().split('  ')
            print("line", line)
            res = line.strip().split('\t')
            if res[0] == "":
                continue;
            print("res: ", res)
            start = int(res[1])
            end = int(res[2])
            label = res[4]
        #     label_id = label_dict.get(label)
            label_id = label
            distance = end - start + 1
            for i in range(start, end + 1):
                #bioes
                if i == start and distance == 1:
                    label_cate = 'S-' + label_id
                elif i == start and distance != 1:
                    label_cate = 'B-' + label_id
                elif i == end:
                    label_cate = 'I-' + label_id
                else:
                    label_cate = 'I-' + label_id
                res_dict[i] = label_cate
        print("res_dict: ",res_dict)
        res_text = ''
        for indx, char in enumerate(content):
            if char == "。":
                sentences.append(sentence)
                sentence = []
            elif char != " ":
                char_label = res_dict.get(indx, 'O')
        #         f.write(char + '\t' + char_label + '\n')
                res_text += (char + '\t' + char_label + '\n')
                sentence.append([char, char_label])
            else:
                continue
        return res_text
        

    #标记1
    def show_jpbw(self):
        self.result_data_Text.edit_separator()

        start_index,end_index,ll=self.get_loc()

        print(self.init_data_Text.selection_get()+"\t"+str(self.btns_names[0])+"\n")
        self.result_data_Text.insert(END,self.init_data_Text.selection_get()+"\t" + str(start_index) + "\t" + str(end_index) + "\t"+ str(ll)+ "\t" +str(self.btns_names[0])+"\n")
        print(self.result_data_Text.get(END))
        self.max1 =self.result_data_Text.get('1.0',END)
        self.result_data_Text.edit_separator()

    # 标记2
    def show_zzms(self,):
        self.result_data_Text.edit_separator()
        start_index,end_index,ll=self.get_loc()

        print(self.init_data_Text.selection_get() + "\t" + str(start_index) + "\t" + str(end_index)+ "\t"+ str(ll)+ "\t" + str(self.btns_names[1]) + "\n")
        self.result_data_Text.insert(END, self.init_data_Text.selection_get() + "\t" + str(start_index) + "\t" + str(end_index)  +"\t"+ str(ll)+ "\t" + str(self.btns_names[1]) + "\n")
        self.max1 = self.result_data_Text.get('1.0', END)
        self.result_data_Text.edit_separator()

    # 标记3
    def show_dlzz(self):
        self.result_data_Text.edit_separator()
        start_index,end_index,ll=self.get_loc()

        print(self.init_data_Text.selection_get() + "\t"+ str(start_index) + "\t" + str(end_index)  + str(self.btns_names[2]) + "\n")
        self.result_data_Text.insert(END, self.init_data_Text.selection_get() + "\t" + str(start_index) + "\t" + str(end_index) + "\t"+ str(ll)+ "\t" +str(self.btns_names[2]) + "\n")
        self.max1 = self.result_data_Text.get('1.0', END)
        self.result_data_Text.edit_separator()

    # 标记4
    def show_yw(self):
        self.result_data_Text.edit_separator()
        start_index,end_index,ll=self.get_loc()

        print(self.init_data_Text.selection_get() + "\t" + str(self.btns_names[3]) + "\n")
        self.result_data_Text.insert(END, self.init_data_Text.selection_get() + "\t" + str(start_index) + "\t" + str(end_index) + "\t"+ str(ll)+ "\t" +str(self.btns_names[3]) + "\n")
        self.max1 = self.result_data_Text.get('1.0', END)
        self.result_data_Text.edit_separator()

    # 标记5
    def show_ss(self):
        self.result_data_Text.edit_separator()
        start_index,end_index,ll=self.get_loc()

        print(self.init_data_Text.selection_get() + "\t" + str(self.btns_names[4]) + "\n")
        self.result_data_Text.insert(END, self.init_data_Text.selection_get() + "\t"+ str(start_index) + "\t" + str(end_index) + "\t"+ str(ll)+ "\t" +str(self.btns_names[4]) + "\n")
        self.max1 = self.result_data_Text.get('1.0', END)
        self.result_data_Text.edit_separator()

    #标注操作撤销功能
    def callback(self,event):
        # 每当有字符插入的时候，就自动插入一个分割符，主要是防止每次撤销的时候会全部撤销
        self.result_data_Text.edit_separator()

    def backToHistory(self):  #撤销操作
        if len(self.result_data_Text.get('1.0','end'))!=0:
            self.result_data_Text.edit_undo()
        else:  #无字符时不能撤销
            return

    def recover(self):   #恢复操作
        if len(self.max1) == len(self.result_data_Text.get('1.0',END)):
            return
        self.result_data_Text.edit_redo()

    #输入窗口一键清空功能
    def delet_ofInput(self):
        self.init_data_Text.delete('1.0','end')

    #结果窗口一键清空功能
    def delet_ofResult(self):
        self.result_data_Text.delete('1.0','end')

    def text_preprocess(self, text):
        text = text.replace('\n','')
        return text
    #打开文件功能
    def openfile(self):
    	# 清空
        self.init_data_Text.delete('1.0','end') 

        fname = filedialog.askopenfilename(title='打开文件', filetypes=[('All Files', '*')])
        # print()
        # self.filename=os.path.basename(fname)
        self.filePath ,self.filename = os.path.split(fname)
        f=open(fname,'r',encoding='utf-8',errors='ignore')
        f_content=''.join(f.read())
        self.content = f_content
        f_content = self.text_preprocess(f_content)
        print(self.content ) 
        self.init_data_Text.insert(END,f_content)

	#打开上一个文件功能
    def openLastfile(self):
    	# 清空
        self.init_data_Text.delete('1.0','end') 

        # this_dir_path = r'C:\Users\86137\Desktop\sequence_label-master\sequence_label-master\data\in' # 写死了，后续需要注意修改
        this_dir_path = self.filePath # 写死了，后续需要注意修改
        this_dir = list(os.walk(this_dir_path))[0][2]
        this_file = self.filename
        idx = this_dir.index(this_file)
        if idx+1 > 1:
            last_file = this_dir_path + r'/' +this_dir[idx-1]
        else:
            last_file = this_dir_path + r'/' +this_dir[0]
        print("last_file: ",last_file)
        self.filename = os.path.basename(last_file)
        f = open(last_file,'r',encoding='utf-8',errors='ignore')
        # f_contet = ''.join(f.readlines())        
        f_contet=''.join(f.read())
        self.content = f_contet
        f_contet = self.text_preprocess(f_contet)
        self.init_data_Text.insert(END,f_contet)

	#打开下一个文件功能
    def openNextfile(self):
    	# 清空
        self.init_data_Text.delete('1.0','end') 
        # this_dir_path = r'C:\Users\86137\Desktop\sequence_label-master\sequence_label-master\data\in' # 写死了，后续需要注意修改
        this_dir_path = self.filePath # 写死了，后续需要注意修改
        this_dir = list(os.walk(this_dir_path))[0][2]
        this_file = self.filename
        idx = this_dir.index(this_file)
        print('idx: ',idx)
        if idx+1 < len(this_dir):
            next_file = this_dir_path + r'/' +this_dir[idx+1]
        else:
            next_file = this_dir_path + r'/' +this_dir[-1]
        print("next_file: ",next_file)
        self.filename=os.path.basename(next_file)
        f = open(next_file,'r', encoding='utf-8', errors='ignore')
        f_contet=''.join(f.read())
        self.content = f_contet
        f_contet = self.text_preprocess(f_contet)
        self.init_data_Text.insert(END,f_contet)


    # 导出文件功能
    def outputfile(self):
        if self.filename!="":
          # os.chdir(r'E:\GitTest\untitled\文本标注1.1\Annoation')
          # os.chdir(r'data/out')
          f = open("data/out/ann"+self.filename, 'w', encoding='utf-8', errors='ignore')
          print(self.result_data_Text.get("1.0", "end"))
          res_text = self.result_data_Text.get("1.0", "end")
          print("res_text",res_text)

          res_text = self.get_RMRB_res(self.content ,res_text)
          print("res_text",res_text)

          f.write(res_text)
          json1 = json.dumps(self.result_data_Text.get("1.0",END))
          print(json1)
          showinfo(title="成功",message="标注文件已导出至Annoation文件夹，文件名为"+self.filename)
        else:
            showinfo(title="错误",message="未找到指定文件")
        
        # 清空
        self.result_data_Text.delete('1.0','end') 


    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time

    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)







def gui_start():
    init_window = tkinter.Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()



    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

gui_start()

