import random
from tkinter import *
from tkinter import ttk, filedialog, dialog, messagebox
import re
import os
import winreg
import yaml
import json
import xlrd
import win32clipboard
import time

class GUI():
    def __init__(self):
        self.__slot_list = {
            '头盔': 'head',
            '胸甲': 'chest',
            '腿甲': 'legs',
            '靴子': 'feet',
            '主手': 'mainhand',
            '副手': 'offhand'
        }
        self.__items = []
        self.__datas = []
        self.__yamls = {}
        self.__init_window = Tk()
        self.__dict = {'display': {'Name': '', 'Lore': []}, 'AttributeModifiers': []}
        self.__set_init_window()
        self.__init_window.mainloop()

    def __set_init_window(self):
        self.__init_window.title("指令生成器 - Ver 1.5.0.2")
        x, y = self.__init_window.winfo_screenwidth(), self.__init_window.winfo_screenheight()
        self.__init_window.geometry('610x520+{0}+{1}'.format(int(x / 3), int(y / 4)))
        self.__init_window.resizable(0, 0)
        # self.__init_window.attributes("-alpha",0.9) 半透明
        self.__Menu_menu = Menu(self.__init_window)
        self.__Menu_subMenu_file = Menu(self.__init_window, tearoff=False)
        self.__Menu_subMenu_file.add_command(label="打开", command=self.__open_file)
        self.__Menu_subMenu_file.add_command(label="保存", command=self.__save_file)
        self.__Menu_subMenu_file.add_command(label="导入 Excel", command=self.__open_file_excel)
        self.__Menu_subMenu_file.add_command(label="导出 YAML", command=self.__save_file_yaml)

        self.__Menu_subMenu_list = Menu(self.__init_window, tearoff=False)
        self.__Menu_subMenu_list.add_command(label="从列表生成", command=self.__output_all)
        self.__Menu_subMenu_list.add_command(label="清空列表", command=self.__clear_all)

        self.__Menu_menu.add_cascade(label="文件", menu=self.__Menu_subMenu_file)
        self.__Menu_menu.add_cascade(label="列表", menu=self.__Menu_subMenu_list)
        self.__Menu_menu.add_cascade(label="关于", command=self.__about)
        self.__init_window.config(menu=self.__Menu_menu)

        self.__itemList = ttk.Treeview(self.__init_window, columns=["序号", "物品名称"], show='headings', selectmode="browse", height=12)
        self.__Scrollbar_itemList = ttk.Scrollbar(self.__itemList, orient="vertical", command=self.__itemList.yview)
        self.__Scrollbar_itemList.place(relx=0.925, rely=0.02, relwidth=0.07, relheight=0.97)
        self.__itemList.configure(yscrollcommand=self.__Scrollbar_itemList.set)
        self.__itemList.column("序号", width=50)
        self.__itemList.column("物品名称", width=180)
        self.__itemList.heading("序号", text="序号")
        self.__itemList.heading("物品名称", text="物品名称")
        self.__itemList.place(x=350, y=20)

        self.__Label_name = Label(self.__init_window, text='名称：')
        self.__Label_name.place(x=20, y=20)
        self.__StringVar_name = StringVar()
        self.__StringVar_name.set('')
        self.__Entry_name = Entry(self.__init_window, textvariable=self.__StringVar_name)
        self.__Entry_name.place(x=70, y=20, width=90)

        self.__Label_id = Label(self.__init_window, text='id：')
        self.__Label_id.place(x=175, y=20)
        self.__StringVar_id = StringVar()
        self.__StringVar_id.set('')
        self.__Entry_id = Entry(self.__init_window, textvariable=self.__StringVar_id)
        self.__Entry_id.place(x=200, y=20, width=60)

        self.__Label_lore = Label(self.__init_window, text='说明：')
        self.__Label_lore.place(x=20, y=60)
        self.__StringVar_lore = StringVar()
        self.__StringVar_lore.set('')
        self.__Entry_lore = Entry(self.__init_window, textvariable=self.__StringVar_lore)
        self.__Entry_lore.place(x=70, y=60, width=189)

        self.__Label_part = Label(self.__init_window, text='部位：')
        self.__Label_part.place(x=20, y=100)
        self.__StringVar_part = StringVar()
        self.__StringVar_part.set("头盔")
        self.__OptionMenu_part = OptionMenu(self.__init_window, self.__StringVar_part, "头盔", "胸甲", "腿甲", "靴子", "主手", "副手")
        self.__OptionMenu_part.place(x=70, y=90)

        self.__Label_maxHealth = Label(self.__init_window, text='生命值：')
        self.__Label_maxHealth.place(x=20, y=140)
        self.__StringVar_maxHealth = StringVar()
        self.__StringVar_maxHealth.set('')
        self.__Entry_maxHealth = Entry(self.__init_window, textvariable=self.__StringVar_maxHealth)
        self.__Entry_maxHealth.place(x=70, y=140, width=40)

        self.__Label_unbreakable = Label(self.__init_window, text='不可破坏：')
        self.__Label_unbreakable.place(x=145, y=140)
        self.__StringVar_unbreakable = StringVar()
        self.__StringVar_unbreakable.set("否")
        self.__OptionMenu_unbreakable = OptionMenu(self.__init_window, self.__StringVar_unbreakable, "是", "否")
        self.__OptionMenu_unbreakable.place(x=205, y=130)

        self.__Label_attackDamage = Label(self.__init_window, text='伤害值：')
        self.__Label_attackDamage.place(x=20, y=180)
        self.__StringVar_attackDamage = StringVar()
        self.__StringVar_attackDamage.set('')
        self.__Entry_attackDamage = Entry(self.__init_window, textvariable=self.__StringVar_attackDamage)
        self.__Entry_attackDamage.place(x=70, y=180, width=40)

        self.__Label_armor = Label(self.__init_window, text='护甲值：')
        self.__Label_armor.place(x=145, y=180)
        self.__StringVar_armor = StringVar()
        self.__StringVar_armor.set('')
        self.__Entry_armor = Entry(self.__init_window, textvariable=self.__StringVar_armor)
        self.__Entry_armor.place(x=220, y=180, width=40)

        self.__Label_attackSpeed = Label(self.__init_window, text='攻速：')
        self.__Label_attackSpeed.place(x=20, y=220)
        self.__StringVar_attackSpeed = StringVar()
        self.__StringVar_attackSpeed.set('')
        self.__Entry_attackspeed = Entry(self.__init_window, textvariable=self.__StringVar_attackSpeed)
        self.__Entry_attackspeed.place(x=70, y=220, width=40)

        self.__Label_movementSpeed = Label(self.__init_window, text='移速：')
        self.__Label_movementSpeed.place(x=145, y=220)
        self.__StringVar_movementSpeed = StringVar()
        self.__StringVar_movementSpeed.set('')
        self.__Entry_movementSpeed = Entry(self.__init_window, textvariable=self.__StringVar_movementSpeed)
        self.__Entry_movementSpeed.place(x=220, y=220, width=40)

        self.__Label_armorToughness = Label(self.__init_window, text='韧性：')
        self.__Label_armorToughness.place(x=20, y=260)
        self.__StringVar_armorToughness = StringVar()
        self.__StringVar_armorToughness.set('')
        self.__Entry_armorToughness = Entry(self.__init_window, textvariable=self.__StringVar_armorToughness)
        self.__Entry_armorToughness.place(x=70, y=260, width=40)

        self.__Label_knockbackResistance = Label(self.__init_window, text='抗击退：')
        self.__Label_knockbackResistance.place(x=145, y=260)
        self.__StringVar_knockbackResistance = StringVar()
        self.__StringVar_knockbackResistance.set('')
        self.__Entry_knockbackResistance = Entry(self.__init_window, textvariable=self.__StringVar_knockbackResistance)
        self.__Entry_knockbackResistance.place(x=220, y=260, width=40)

        self.__Button_save = Button(self.__init_window, text="-->", command=self.__save_to_list, width=6)
        self.__Button_save.place(x=280, y=70)

        self.__Button_load = Button(self.__init_window, text="<--",command=self.__load_from_list, width=6)
        self.__Button_load.place(x=280, y=130)

        self.__Button_delete = Button(self.__init_window, text="删除",command=self.__delete_Select, width=6)
        self.__Button_delete.place(x=280, y=190)

        self.__Button_reset = Button(self.__init_window, text="重置", command=self.__reset, width=6)
        self.__Button_reset.place(x=280, y=250)

        self.__Text_showData = Text(self.__init_window, height=10, width=77)
        self.__Scrollbar_showData = Scrollbar(self.__init_window)
        self.__Scrollbar_showData.place(x=565, y=350,relheight=0.27)
        self.__Text_showData.config(yscrollcommand=self.__Scrollbar_showData.set)
        self.__Text_showData.place(x=20, y=350)

        self.__Scrollbar_showData.config(command=self.__Text_showData.yview)

        # self.__Label_check = Label(self.__init_window, text='MM 隐藏项目：')
        # self.__Label_check.place(x=20, y=300)

        self.__IntVar_ATTRIBUTES = IntVar(value=0)
        self.__CheckButton_ATTRIBUTES = Checkbutton(self.__init_window, text='ATTRIBUTES', variable=self.__IntVar_ATTRIBUTES)
        self.__CheckButton_ATTRIBUTES.place(x=20, y=290)

        self.__IntVar_ENCHANTS = IntVar(value=0)
        self.__CheckButton_ENCHANTS = Checkbutton(self.__init_window, text='ENCHANTS', variable=self.__IntVar_ENCHANTS)
        self.__CheckButton_ENCHANTS.place(x=150, y=290)

        self.__IntVar_DESTROYS = IntVar(value=0)
        self.__CheckButton_DESTROYS = Checkbutton(self.__init_window, text='DESTROYS', variable=self.__IntVar_DESTROYS)
        self.__CheckButton_DESTROYS.place(x=280, y=290)

        self.__IntVar_PLACED_ON = IntVar(value=0)
        self.__CheckButton_PLACED_ON = Checkbutton(self.__init_window, text='PLACED_ON', variable=self.__IntVar_PLACED_ON)
        self.__CheckButton_PLACED_ON.place(x=20, y=320)

        self.__IntVar_POTION_EFFECTS = IntVar(value=0)
        self.__CheckButton_POTION_EFFECTS = Checkbutton(self.__init_window, text='POTION_EFFECTS', variable=self.__IntVar_POTION_EFFECTS)
        self.__CheckButton_POTION_EFFECTS.place(x=150, y=320)

        self.__IntVar_UNBREAKABLE = IntVar(value=0)
        self.__CheckButton_UNBREAKABLE = Checkbutton(self.__init_window, text='UNBREAKABLE', variable=self.__IntVar_UNBREAKABLE)
        self.__CheckButton_UNBREAKABLE.place(x=280, y=320)

        self.__Label_statusText = Label(self.__init_window, text='{0} 程序初始化完成'.format(self.__getTime()))
        self.__Label_statusText.place(x=20, y=490)

    def __about(self):
        messagebox.showinfo("关于", "开发者：Miranda")

    def __get_desktop(self):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',)
        return winreg.QueryValueEx(key, "Desktop")[0]

    def __open_file(self):
        desktop = self.__get_desktop()
        file_path = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser(desktop)))
        if file_path is not '':
            with open(file=file_path, mode='r', encoding='utf-8') as file:
                try:
                    self.__items += json.load(file)
                except:
                    self.__Label_statusText['text'] = '{0} 打开文件 {1} 时发生错误'.format(self.__getTime(), file_path)
                    return
                self.__Label_statusText['text'] = '{0} 成功打开文件 {1}'.format(self.__getTime(), file_path)
                self.__refreshList()

    def __open_file_excel(self):
        desktop = self.__get_desktop()
        file_path = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser(desktop)))
        try:
            table = xlrd.open_workbook(file_path)
            sheet = table.sheets()[0]
        except:
            self.__Label_statusText['text'] = '{0} 打开文件 {1} 时发生错误'.format(self.__getTime(), file_path)
            return
        for i in range(sheet.nrows):
            if sheet.cell(i, 3).value not in ["头盔", "胸甲", "腿甲", "靴子", "主手", "副手"] or sheet.cell(i, 5).value not in ["是", "否"]:
                continue
            temp = {}
            temp['Name'] = sheet.cell(i, 0).value
            if sheet.cell(i, 1).value == '':
                temp['id'] = 0
            else:
                temp['id'] = int(sheet.cell(i, 1).value)
            temp['lore'] = sheet.cell(i, 2).value
            temp['maxHealth'] = sheet.cell(i, 4).value
            temp['attackDamage'] = sheet.cell(i, 6).value
            temp['armor'] = sheet.cell(i, 7).value
            temp['attackSpeed'] = sheet.cell(i, 8).value
            temp['movementSpeed'] = sheet.cell(i, 9).value
            temp['armorToughness'] = sheet.cell(i, 10).value
            temp['knockbackResistance'] = sheet.cell(i, 11).value
            temp['part'] = sheet.cell(i, 3).value
            temp['unbreakable'] = sheet.cell(i, 5).value
            temp['hides'] = {}
            temp['hides']['ATTRIBUTES'] = self.__zero_conv(sheet.cell(i, 12).value)
            temp['hides']['ENCHANTS'] = self.__zero_conv(sheet.cell(i, 13).value)
            temp['hides']['DESTROYS'] = self.__zero_conv(sheet.cell(i, 14).value)
            temp['hides']['PLACED_ON'] = self.__zero_conv(sheet.cell(i, 15).value)
            temp['hides']['POTION_EFFECTS'] = self.__zero_conv(sheet.cell(i, 16).value)
            temp['hides']['UNBREAKABLE'] = self.__zero_conv(sheet.cell(i, 17).value)
            self.__items.append(temp)
            self.__refreshList()
            self.__Label_statusText['text'] = '{0} 成功导入文件 {1}'.format(self.__getTime(), file_path)

    def __zero_conv(self, string):
        if string == '':
            return 0
        else:
            return int(string)

    def __getTime(self):
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        formatTime = "[" + time.strftime("%H:%M:%S", timeArray) + "]"
        return formatTime

    def __setText(self, text): 
        win32clipboard.OpenClipboard()  
        win32clipboard.EmptyClipboard()  
        win32clipboard.SetClipboardText(text)  
        win32clipboard.CloseClipboard()

    def __save_file(self):
        file_path = filedialog.asksaveasfilename(title=u'保存文件')
        if file_path is not '':
            with open(file=file_path, mode='w', encoding='utf-8') as file:
                json.dump(self.__items, file)
            self.__Label_statusText['text'] = '{0} 保存成功'.format(self.__getTime())

    def __save_file_yaml(self):
        self.__output_all_yaml()
        file_path = filedialog.asksaveasfilename(title=u'保存文件')
        if file_path is not '':
            with open(file=file_path, mode='w', encoding='utf-8') as file:
                yaml.safe_dump(self.__yamls, file, default_flow_style=False,encoding='utf-8',allow_unicode=True)
            self.__Label_statusText['text'] = '{0} 导出成功'.format(self.__getTime())

    def __selectItem(self):
        if len(self.__itemList.selection()) != 0:
            return self.__itemList.item(self.__itemList.selection()[0])['values'][0]

    def __clear_show_data(self):
        self.__Text_showData.delete(1.0, END)

    def __clearList(self):
        items = self.__itemList.get_children()
        for item in items:
            self.__itemList.delete(item)

    def __refreshList(self):
        self.__clearList()
        count = 0
        for i in range(len(self.__items)):
            self.__itemList.insert('', END, value=[i + 1 ,self.__items[i]['Name']])

    def __save_to_list(self):
        if self.__StringVar_name.get() == '':
            return
        temp = {}
        temp['Name'] = self.__StringVar_name.get()
        temp['id'] = self.__StringVar_id.get()
        temp['lore'] = self.__StringVar_lore.get()
        temp['maxHealth'] = self.__StringVar_maxHealth.get()
        temp['attackDamage'] = self.__StringVar_attackDamage.get()
        temp['armor'] = self.__StringVar_armor.get()
        temp['attackSpeed'] = self.__StringVar_attackSpeed.get()
        temp['movementSpeed'] = self.__StringVar_movementSpeed.get()
        temp['armorToughness'] = self.__StringVar_armorToughness.get()
        temp['knockbackResistance'] = self.__StringVar_knockbackResistance.get()
        temp['part'] = self.__StringVar_part.get()
        temp['unbreakable'] = self.__StringVar_unbreakable.get()
        temp['hides'] = {}
        temp['hides']['ATTRIBUTES'] = self.__IntVar_ATTRIBUTES.get()
        temp['hides']['ENCHANTS'] = self.__IntVar_ENCHANTS.get()
        temp['hides']['DESTROYS'] = self.__IntVar_DESTROYS.get()
        temp['hides']['PLACED_ON'] = self.__IntVar_PLACED_ON.get()
        temp['hides']['POTION_EFFECTS'] = self.__IntVar_POTION_EFFECTS.get()
        temp['hides']['UNBREAKABLE'] = self.__IntVar_UNBREAKABLE.get()
        self.__items.append(temp)
        self.__refreshList()
        self.__setText(self.__generate())
        self.__Label_statusText['text'] = '{0} 已复制到剪切板'.format(self.__getTime())


    def __delete_Select(self):
        select = self.__itemList.focus()
        if select == '' or None:
            return
        selected = self.__selectItem() - 1
        self.__itemList.delete(select)
        del self.__items[selected]
        self.__refreshList()
        self.__reset()
        self.__clear_show_data()

    def __load_from_list(self):
        select = self.__selectItem()
        if select == None:
            return
        selected = self.__selectItem() - 1
        if selected == '':
            return
        temp = self.__items[selected]
        self.__StringVar_name.set(temp['Name'])
        self.__StringVar_id.set(temp['id'])
        self.__StringVar_lore.set(temp['lore'])
        self.__StringVar_maxHealth.set(temp['maxHealth'])
        self.__StringVar_attackDamage.set(temp['attackDamage'])
        self.__StringVar_armor.set(temp['armor'])
        self.__StringVar_attackSpeed.set(temp['attackSpeed'])
        self.__StringVar_movementSpeed.set(temp['movementSpeed'])
        self.__StringVar_armorToughness.set(temp['armorToughness'])
        self.__StringVar_knockbackResistance.set(temp['knockbackResistance'])
        self.__StringVar_part.set(temp['part'] )
        self.__StringVar_unbreakable.set(temp['unbreakable'])
        self.__IntVar_ATTRIBUTES.set(temp['hides']['ATTRIBUTES'])
        self.__IntVar_ENCHANTS.set(temp['hides']['ENCHANTS'])
        self.__IntVar_DESTROYS.set(temp['hides']['DESTROYS'])
        self.__IntVar_PLACED_ON.set(temp['hides']['PLACED_ON'])
        self.__IntVar_POTION_EFFECTS.set(temp['hides']['POTION_EFFECTS'])
        self.__IntVar_UNBREAKABLE.set(temp['hides']['UNBREAKABLE'])
        self.__setText(self.__generate())
        self.__Label_statusText['text'] = '{0} 已复制到剪切板'.format(self.__getTime())

    def __reset(self):
        self.__StringVar_name.set('')
        self.__StringVar_id.set('')
        self.__StringVar_lore.set('')
        self.__StringVar_maxHealth.set('')
        self.__StringVar_attackDamage.set('')
        self.__StringVar_armor.set('')
        self.__StringVar_attackSpeed.set('')
        self.__StringVar_movementSpeed.set('')
        self.__StringVar_armorToughness.set('')
        self.__StringVar_knockbackResistance.set('')
        self.__StringVar_part.set("头盔")
        self.__StringVar_unbreakable.set("否")
        self.__IntVar_ATTRIBUTES.set(0)
        self.__IntVar_ENCHANTS.set(0)
        self.__IntVar_DESTROYS.set(0)
        self.__IntVar_PLACED_ON.set(0)
        self.__IntVar_POTION_EFFECTS.set(0)
        self.__IntVar_UNBREAKABLE.set(0)

    def __handle_number(self, string):
        number = re.search(r"[\d|.-]+", string)
        if re.search(r'%', string) == None:
            if number != None:
                number = number.group(0)
                return number
        else:
            if number != None:
                number = int(number.group(0)) / 100
                return number

    def __clear_all(self):
        self.__items = []
        self.__refreshList()
        self.__reset()
        self.__clear_show_data()
        self.__Label_statusText['text'] = '{0} 列表已清空'.format(self.__getTime())

    def __output_all(self):
        self.__clear_show_data()
        self.__datas = []
        for i in self.__items:
            temp = i
            self.__StringVar_name.set(temp['Name'])
            self.__StringVar_id.set(temp['id'])
            self.__StringVar_lore.set(temp['lore'])
            self.__StringVar_maxHealth.set(temp['maxHealth'])
            self.__StringVar_attackDamage.set(temp['attackDamage'])
            self.__StringVar_armor.set(temp['armor'])
            self.__StringVar_attackSpeed.set(temp['attackSpeed'])
            self.__StringVar_movementSpeed.set(temp['movementSpeed'])
            self.__StringVar_armorToughness.set(temp['armorToughness'])
            self.__StringVar_knockbackResistance.set(temp['knockbackResistance'])
            self.__StringVar_part.set(temp['part'])
            self.__StringVar_unbreakable.set(temp['unbreakable'])
            tempData = self.__generate()
            self.__datas.append(tempData)
        self.__Text_showData.delete(1.0, END)
        for i in range(len(self.__datas)):
            self.__Text_showData.insert('insert', self.__datas[i])
            self.__Text_showData.insert('insert', '\n\n')
        self.__reset()
        if len(self.__datas) != 0:
            self.__Label_statusText['text'] = '{0} 生成完成'.format(self.__getTime())

    def __output_all_yaml(self):
        for i in self.__items:
            temp = i
            self.__yamls[temp['Name']] = {}
            currentItem = self.__yamls[temp['Name']]
            if temp['id'] == '':
                currentItem['id'] = 0
            else:
                currentItem['id'] = int(temp['id'])
            currentItem['Data'] = 0
            currentItem['Display'] = temp['Name']
            currentItem['Lore'] = [temp['lore']]
            currentItem['Attributes'] = {}
            currentItem['Attributes'][self.__slot_list[temp['part']]] = {}
            selectedHides = temp['hides']
            hides = []
            for i in selectedHides:
                if selectedHides[i] == 1:
                    hides.append(i)
            currentItem['Hide'] = hides
            if temp['unbreakable'] == '是':
                currentItem['Unbreakable'] = True
            else:
                currentItem['Unbreakable'] = False
            for i in ['maxHealth', 'attackDamage', 'armor', 'attackSpeed', 'movementSpeed', 'armorToughness', 'knockbackResistance']:
                if temp[i] == '':
                    continue
                else:
                    currentItem['Attributes'][self.__slot_list[temp['part']]][i] = float(self.__handle_number(str(temp[i])))

    def __random_Number(self, digit):
        numbers = '0123456789'
        random_number = ''
        for i in range(digit):
            index = random.randint(0, len(numbers)-1)
            random_number += str(index)
        return random_number

    def __handle_name(self):
        if self.__StringVar_name.get() == '':
            return
        self.__dict['display']['Name'] = self.__StringVar_name.get()

    def __handle_lore(self):
        if self.__StringVar_lore.get() == '':
            return
        self.__dict['display']['Lore'] = [self.__StringVar_lore.get()]

    def __handle_unbreakable(self):
        if self.__StringVar_unbreakable.get() == '是':
            self.__dict['Unbreakable'] = 1

    def __handle_data(self, target, generic):
        if target == '':
            return
        temp = {}
        temp['AttributeName'] = generic
        temp['Name'] = self.__random_Number(3)
        int_value = re.search(r"[\d|.-]+", target)
        if int_value != None:
            int_value = int_value.group(0)
        else:
            return
        if re.search(r'%', target) == None:
            temp['Operation'] = 0
            temp['Amount'] = float(int_value)
        elif re.search(r'[+|-]', target) == None:
            temp['Operation'] = 2
            temp['Amount'] = float(int_value) / 100
        else:
            temp['Operation'] = 1
            temp['Amount'] = float(int_value) / 100
        temp['UUIDLeast'] = int(self.__random_Number(3))
        temp['UUIDMost'] = int(self.__random_Number(3))
        temp['Slot'] = self.__slot_list[self.__StringVar_part.get()]
        self.__dict['AttributeModifiers'].append(temp)

    def __generate(self):
        self.__dict = {'display': {'Name': '', 'Lore': []}, 'AttributeModifiers': []}
        self.__handle_name()
        self.__handle_lore()
        self.__handle_unbreakable()
        self.__handle_data(self.__StringVar_maxHealth.get(), 'generic.maxHealth')
        self.__handle_data(self.__StringVar_attackDamage.get(), 'generic.attackDamage')
        self.__handle_data(self.__StringVar_armor.get(), 'generic.armor')
        self.__handle_data(self.__StringVar_attackSpeed.get(), 'generic.attackSpeed')
        self.__handle_data(self.__StringVar_movementSpeed.get(), 'generic.movementSpeed')
        self.__handle_data(self.__StringVar_armorToughness.get(), 'generic.armorToughness')
        self.__handle_data(self.__StringVar_knockbackResistance.get(), 'generic.knockbackResistance')

        data = str(self.__dict)
        exp = "'([0-9a-zA-Z]+)': "
        pat = re.compile(exp)
        data = re.sub(exp, r'\g<1>: ', data)
        data = data.replace("'head'", 'head')
        data = data.replace("'chest'", 'chest')
        data = data.replace("'legs'", 'legs')
        data = data.replace("'feet'", 'feet')
        data = data.replace("'", "\"")
        if self.__Entry_id.get() == '':
            self.__StringVar_id.set('0')
        data = '/give @p {0} 1 '.format(self.__Entry_id.get()) + data
        self.__Text_showData.delete(1.0, END)
        self.__Text_showData.insert('insert', data)
        return data


if __name__ == '__main__':
    GUI()
