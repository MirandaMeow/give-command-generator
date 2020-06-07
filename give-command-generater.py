import random
from tkinter import *
from tkinter import ttk, filedialog, dialog, messagebox
import re
import os
import yaml
import json
import xlrd
import win32clipboard
import time

class GUI():
    def __init__(self):
        self.__slot_conv = {
            '头盔': 'head',
            '胸甲': 'chest',
            '腿甲': 'legs',
            '靴子': 'feet',
            '主手': 'mainhand',
            '副手': 'offhand'
        }
        self.__ench_Conv = {
        '保护': 0,
        '火焰保护': 1,
        '摔落保护': 2,
        '爆炸保护': 3,
        '弹射物保护': 4,
        '水下呼吸': 5,
        '水下速掘': 6,
        '荆棘': 7,
        '深海探索者': 8,
        '绑定诅咒': 10,
        '锋利': 16,
        '亡灵杀手': 17,
        '节肢杀手': 18,
        '击退': 19,
        '火焰附加': 20,
        '抢夺': 21,
        '效率': 32,
        '精准采集': 33,
        '耐久': 34,
        '时运': 35,
        '力量': 48,
        '冲击': 49,
        '火矢': 50,
        '无限': 51,
        '海之眷顾': 61,
        '饵钓': 62,
        '经验修补': 70,
        '消失诅咒': 71
        }
        self.__items = []
        self.__datas = []
        self.__yamls = {}
        self.__enchantment_name_lvl = []
        self.__enchantment_id_lvl = []
        self.__init_window = Tk()
        self.__open_flag = False
        self.__egg = 0
        self.__title = '指令生成转换器 - Ver 1.7.0.9'
        self.__itemDict = {'display': {'Name': '', 'Lore': []}, 'AttributeModifiers': [], 'ench': []}
        self.__set_init_window()
        self.__init_window.mainloop()

    def __set_init_window(self):
        self.__init_window.title(self.__title)
        x, y = self.__init_window.winfo_screenwidth(), self.__init_window.winfo_screenheight()
        self.__init_window.geometry('600x500+{0}+{1}'.format(int(x / 3), int(y / 4)))
        self.__init_window.resizable(0, 0)
        # self.__init_window.attributes("-alpha", 0.6)
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

        self.__itemList = ttk.Treeview(self.__init_window, columns=["序号", "物品名称"], show='headings', selectmode="browse", height=13)
        self.__Scrollbar_itemList = ttk.Scrollbar(self.__init_window, orient="vertical", command=self.__itemList.yview)
        self.__Scrollbar_itemList.place(x=563, y=20, relheight=0.574)
        self.__itemList.configure(yscrollcommand=self.__Scrollbar_itemList.set)
        self.__itemList.column("序号", width=40)
        self.__itemList.column("物品名称", width=170)
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
        self.__Label_lore.place(x=20, y=50)
        self.__StringVar_lore = StringVar()
        self.__StringVar_lore.set('')
        self.__Entry_lore = Entry(self.__init_window, textvariable=self.__StringVar_lore)
        self.__Entry_lore.place(x=70, y=50, width=190)

        self.__Label_part = Label(self.__init_window, text='部位：')
        self.__Label_part.place(x=20, y=80)
        self.__StringVar_part = StringVar()
        self.__StringVar_part.set("头盔")
        self.__Combobox_part = ttk.Combobox(self.__init_window, textvariable=self.__StringVar_part, width=4)
        self.__Combobox_part['value'] = ("头盔", "胸甲", "腿甲", "靴子", "主手", "副手")
        self.__Combobox_part['state'] = 'readonly'
        self.__Combobox_part.place(x=70, y=80, relwidth=0.083)

        self.__Button_enchantment = Button(self.__init_window, text='附魔设置', command=self.__init_enchantment)
        self.__Button_enchantment.place(x=148, y=80, height=23, width=112)

        self.__Label_maxHealth = Label(self.__init_window, text='生命值：')
        self.__Label_maxHealth.place(x=20, y=110)
        self.__StringVar_maxHealth = StringVar()
        self.__StringVar_maxHealth.set('')
        self.__Entry_maxHealth = Entry(self.__init_window, textvariable=self.__StringVar_maxHealth)
        self.__Entry_maxHealth.place(x=70, y=110, width=50)

        self.__Label_unbreakable = Label(self.__init_window, text='不可破坏：')
        self.__Label_unbreakable.place(x=145, y=110)
        self.__StringVar_unbreakable = StringVar()
        self.__StringVar_unbreakable.set("否")
        self.__Combobox_unbreakable = ttk.Combobox(self.__init_window, textvariable=self.__StringVar_unbreakable, width=2)
        self.__Combobox_unbreakable['value'] = ("是", "否")
        self.__Combobox_unbreakable['state'] = 'readonly'
        self.__Combobox_unbreakable.place(x=210, y=110, relwidth=0.083)

        self.__Label_attackDamage = Label(self.__init_window, text='伤害值：')
        self.__Label_attackDamage.place(x=20, y=140)
        self.__StringVar_attackDamage = StringVar()
        self.__StringVar_attackDamage.set('')
        self.__Entry_attackDamage = Entry(self.__init_window, textvariable=self.__StringVar_attackDamage)
        self.__Entry_attackDamage.place(x=70, y=140, width=50)

        self.__Label_armor = Label(self.__init_window, text='护甲值：')
        self.__Label_armor.place(x=145, y=140)
        self.__StringVar_armor = StringVar()
        self.__StringVar_armor.set('')
        self.__Entry_armor = Entry(self.__init_window, textvariable=self.__StringVar_armor)
        self.__Entry_armor.place(x=210, y=140, width=50)

        self.__Label_attackSpeed = Label(self.__init_window, text='攻速：')
        self.__Label_attackSpeed.place(x=20, y=170)
        self.__StringVar_attackSpeed = StringVar()
        self.__StringVar_attackSpeed.set('')
        self.__Entry_attackspeed = Entry(self.__init_window, textvariable=self.__StringVar_attackSpeed)
        self.__Entry_attackspeed.place(x=70, y=170, width=50)

        self.__Label_movementSpeed = Label(self.__init_window, text='移速：')
        self.__Label_movementSpeed.place(x=145, y=170)
        self.__StringVar_movementSpeed = StringVar()
        self.__StringVar_movementSpeed.set('')
        self.__Entry_movementSpeed = Entry(self.__init_window, textvariable=self.__StringVar_movementSpeed)
        self.__Entry_movementSpeed.place(x=210, y=170, width=50)

        self.__Label_armorToughness = Label(self.__init_window, text='韧性：')
        self.__Label_armorToughness.place(x=20, y=200)
        self.__StringVar_armorToughness = StringVar()
        self.__StringVar_armorToughness.set('')
        self.__Entry_armorToughness = Entry(self.__init_window, textvariable=self.__StringVar_armorToughness)
        self.__Entry_armorToughness.place(x=70, y=200, width=50)

        self.__Label_knockbackResistance = Label(self.__init_window, text='抗击退：')
        self.__Label_knockbackResistance.place(x=145, y=200)
        self.__StringVar_knockbackResistance = StringVar()
        self.__StringVar_knockbackResistance.set('')
        self.__Entry_knockbackResistance = Entry(self.__init_window, textvariable=self.__StringVar_knockbackResistance)
        self.__Entry_knockbackResistance.place(x=210, y=200, width=50)

        self.__Button_save = Button(self.__init_window, text="-->", command=self.__save_to_list, width=6)
        self.__Button_save.place(x=280, y=40)

        self.__Button_delete = Button(self.__init_window, text="删除", command=self.__delete_Select, width=6)
        self.__Button_delete.place(x=280, y=110)

        self.__Button_load = Button(self.__init_window, text="<--", command=self.__load_from_list, width=6)
        self.__Button_load.place(x=280, y=180)

        self.__Button_reset = Button(self.__init_window, text="重置", command=self.__reset, width=6)
        self.__Button_reset.place(x=280, y=250)

        self.__Text_showData = Text(self.__init_window, height=10, width=77)
        self.__Scrollbar_showData = Scrollbar(self.__init_window)
        self.__Scrollbar_showData.place(x=563, y=330, relheight=0.268)
        self.__Text_showData.config(yscrollcommand=self.__Scrollbar_showData.set)
        self.__Text_showData.place(x=20, y=330)
        self.__Scrollbar_showData.config(command=self.__Text_showData.yview)

        self.__IntVar_ATTRIBUTES = IntVar(value=0)
        self.__CheckButton_ATTRIBUTES = Checkbutton(self.__init_window, text='ATTRIBUTES', variable=self.__IntVar_ATTRIBUTES)
        self.__CheckButton_ATTRIBUTES.place(x=20, y=230)

        self.__IntVar_ENCHANTS = IntVar(value=0)
        self.__CheckButton_ENCHANTS = Checkbutton(self.__init_window, text='ENCHANTS', variable=self.__IntVar_ENCHANTS)
        self.__CheckButton_ENCHANTS.place(x=150, y=230)

        self.__IntVar_DESTROYS = IntVar(value=0)
        self.__CheckButton_DESTROYS = Checkbutton(self.__init_window, text='DESTROYS', variable=self.__IntVar_DESTROYS)
        self.__CheckButton_DESTROYS.place(x=20, y=260)

        self.__IntVar_PLACED_ON = IntVar(value=0)
        self.__CheckButton_PLACED_ON = Checkbutton(self.__init_window, text='PLACED_ON', variable=self.__IntVar_PLACED_ON)
        self.__CheckButton_PLACED_ON.place(x=150, y=260)

        self.__IntVar_POTION_EFFECTS = IntVar(value=0)
        self.__CheckButton_POTION_EFFECTS = Checkbutton(self.__init_window, text='POTION_EFFECTS', variable=self.__IntVar_POTION_EFFECTS)
        self.__CheckButton_POTION_EFFECTS.place(x=20, y=290)

        self.__IntVar_UNBREAKABLE = IntVar(value=0)
        self.__CheckButton_UNBREAKABLE = Checkbutton(self.__init_window, text='UNBREAKABLE', variable=self.__IntVar_UNBREAKABLE)
        self.__CheckButton_UNBREAKABLE.place(x=150, y=290)

        self.__Label_statusText = Label(self.__init_window, text='{0} 程序初始化完成'.format(self.__getTime()))
        self.__Label_statusText.place(x=20, y=470)

    def __about(self):
        self.__egg += 1
        if self.__egg ==3:
            self.__egg = 0
            self.__init_window.title("指令生成转换器 - OAO")
        else:
            self.__init_window.title(self.__title)
        messagebox.showinfo("关于", "开发者：MirandaMeow")

    def __init_enchantment(self):
        self.__init_window.update()
        main_x, main_y = self.__init_window.winfo_x(), self.__init_window.winfo_y()
        if self.__open_flag == True:
            self.__init_enchantment_window.destroy()
            self.__open_flag = False
            return
        self.__open_flag = True
        self.__init_enchantment_window = Toplevel()
        self.__init_enchantment_window.title('附魔设置')
        self.__init_enchantment_window.resizable(0, 0)
        if main_x < self.__init_window.winfo_screenwidth() - 600 - 250:
            self.__init_enchantment_window.geometry('250x460+{0}+{1}'.format(main_x + 600, main_y))
        else:
            self.__init_enchantment_window.geometry('250x460+{0}+{1}'.format(main_x - 250, main_y))

        self.__enchantmentList = ttk.Treeview(self.__init_enchantment_window, columns=["序号", "附魔名称", "等级"], show='headings', selectmode="browse", height=15)
        self.__enchantmentList.column("序号", width=50)
        self.__enchantmentList.column("附魔名称", width=110)
        self.__enchantmentList.column("等级", width=83)
        self.__enchantmentList.heading("序号", text="序号")
        self.__enchantmentList.heading("附魔名称", text="附魔名称")
        self.__enchantmentList.heading("等级", text="等级")
        self.__enchantmentList.place(x=2, y=2)

        self.__Button_add_enchantment = Button(self.__init_enchantment_window, text="+", command=self.__add_enchantment, width=6)
        self.__Button_add_enchantment.place(x=40, y=340)

        self.__Button_add_enchantment = Button(self.__init_enchantment_window, text="-", command=self.__remove_enchantment, width=6)
        self.__Button_add_enchantment.place(x=155, y=340)

        self.__Label_enchantment_name = Label(self.__init_enchantment_window, text='附魔名称：')
        self.__Label_enchantment_name.place(x=20, y=380)
        self.__StringVar_enchantment_name = StringVar()
        self.__StringVar_enchantment_name.set("保护")
        self.__Combobox_enchantment_name = ttk.Combobox(self.__init_enchantment_window, textvariable=self.__StringVar_enchantment_name, width=12)
        self.__Combobox_enchantment_name['value'] = ('保护', '火焰保护', '摔落保护', '爆炸保护', '弹射物保护', '水下呼吸', '水下速掘', '荆棘', '深海探索者', '绑定诅咒', '锋利', '亡灵杀手', '节肢杀手', '击退', '火焰附加', '抢夺', '效率', '精准采集', '耐久', '时运', '力量', '冲击', '火矢', '无限', '海之眷顾', '饵钓', '经验修补', '消失诅咒')
        self.__Combobox_enchantment_name['state'] = 'readonly'
        self.__Combobox_enchantment_name.place(x=80, y=380)

        self.__Label_enchantment_level = Label(self.__init_enchantment_window, text='附魔等级：')
        self.__Label_enchantment_level.place(x=20, y=420)
        self.__StringVar_enchantment_level = IntVar()
        self.__StringVar_enchantment_level.set("1")
        self.__Combobox_enchantment_level = ttk.Combobox(self.__init_enchantment_window, textvariable=self.__StringVar_enchantment_level, width=12)
        ench_level = []
        for i in range(1, 128):
            ench_level.append(i)
        self.__Combobox_enchantment_level['value'] = ench_level
        self.__Combobox_enchantment_level['state'] = 'readonly'
        self.__Combobox_enchantment_level.place(x=80, y=420)
        self.__enchantment_id_lvl = self.__itemDict['ench']
        self.__refresh_enchantment()
        self.__init_enchantment_window.protocol('WM_DELETE_WINDOW', self.__close_window)
        self.__enchantmentList.bind("<<TreeviewSelect>>", self.__enchantment_select)
        self.__init_enchantment_window.mainloop()
        self.__open_flag = False

    def __close_window(self):
        self.__init_enchantment_window.destroy()
        self.__open_flag = False

    def __find_key(self, dictObj, target):
        for i in dictObj:
            if dictObj[i] == target:
                return i

    def __find_index(self, listObj, target):
        for i in range(len(listObj)):
            if listObj[i] == target:
                return i

    def __enchantment_select(self, event):
        selected = self.__enchantmentList.item(self.__enchantmentList.selection()[0])['values']
        self.__StringVar_enchantment_name.set(selected[1])
        self.__StringVar_enchantment_level.set(selected[2])


    def __conv_id_to_name(self):
        self.__enchantment_name_lvl = []
        for i in range(len(self.__enchantment_id_lvl)):
            self.__enchantment_name_lvl.append({'id': self.__find_key(self.__ench_Conv, self.__enchantment_id_lvl[i]['id']), 'lvl': self.__enchantment_id_lvl[i]['lvl']})

    def __update_id_list(self):
        self.__enchantment_id_lvl = []
        for i in range(len(self.__enchantment_name_lvl)):
            self.__enchantment_id_lvl.append({'id': self.__ench_Conv[self.__enchantment_name_lvl[i]['id']], 'lvl': self.__enchantment_name_lvl[i]['lvl']})

    def __refresh_enchantment(self):
        self.__clearList(self.__enchantmentList)
        count = 0
        for i in self.__enchantment_name_lvl:
            ench_name = i['id']
            ench_level = i['lvl']
            count += 1
            self.__enchantmentList.insert('', END, value=[count, ench_name, ench_level])
        self.__update_id_list()

    def __add_enchantment(self):
        ench_name = self.__StringVar_enchantment_name.get()
        ench_level = self.__StringVar_enchantment_level.get()
        enchantment_name_lvl = {'id': ench_name, 'lvl': ench_level}
        all_enches = []
        for i in range(len(self.__enchantment_name_lvl)):
            all_enches.append(self.__enchantment_name_lvl[i]['id'])
        if ench_name not in all_enches:
            self.__enchantment_name_lvl.append(enchantment_name_lvl)
        else:
            index_ench = self.__find_index(all_enches, ench_name)
            self.__enchantment_name_lvl[index_ench] = enchantment_name_lvl
        self.__refresh_enchantment()

    def __remove_enchantment(self):
        select = self.__enchantmentList.focus()
        if select == '' or None:
            return
        selected = self.__selectItem(self.__enchantmentList) - 1
        self.__enchantmentList.delete(select)
        del self.__enchantment_name_lvl[selected]
        self.__refresh_enchantment()

    def __open_file(self):
        file_path = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser('.')), filetypes=[('数据文件', '*.json'), ('所有文件', '*')])
        if file_path is not '':
            with open(file=file_path, mode='r', encoding='utf-8') as file:
                try:
                    fileJson = json.load(file)
                    for i in range(len(fileJson)):
                        if fileJson[i]['part'] not in ["头盔", "胸甲", "腿甲", "靴子", "主手", "副手"] or fileJson[i]['unbreakable'] not in ["是", "否"]:
                            self.__Label_statusText['text'] = '{0} 数据格式不正确'.format(self.__getTime())
                            return
                    all_items = []
                    for i in range(len(self.__items)):
                        all_items.append(self.__items[i]['Name'])
                    for i in range(len(fileJson)):
                        if fileJson[i]['Name'] not in all_items:
                            self.__items.append(fileJson[i])
                        else:
                            item_index = self.__find_index(all_items, fileJson[i]['Name'])
                            self.__items[item_index] = fileJson[i]
                except:
                    self.__Label_statusText['text'] = '{0} 打开文件 {1} 时发生错误'.format(self.__getTime(), file_path)
                    return
                self.__Label_statusText['text'] = '{0} 成功打开文件 {1}'.format(self.__getTime(), file_path)
                self.__refreshList()

    def __open_file_excel(self):
        file_path = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser('.')), filetypes=[('Excel 工作簿', '*.xlsx'), ('Excel 97-2003 工工作簿', '*.xls'), ('所有文件', '*')])
        if file_path is not '':
            try:
                table = xlrd.open_workbook(file_path)
                sheet = table.sheets()[0]
            except:
                self.__Label_statusText['text'] = '{0} 打开文件 {1} 时发生错误'.format(self.__getTime(), file_path)
                return
            count = 0
            for i in range(sheet.nrows):
                # try:
                if sheet.cell(i, 3).value not in ["头盔", "胸甲", "腿甲", "靴子", "主手", "副手"] or sheet.cell(i, 5).value not in ["是", "否"]:
                    continue
                temp = {}
                temp['Name'] = sheet.cell(i, 0).value
                if sheet.cell(i, 1).value == '':
                    temp['id'] = 0
                else:
                    temp['id'] = int(sheet.cell(i, 1).value)
                temp['lore'] = sheet.cell(i, 2).value
                temp['attributes'] = {}
                temp['attributes']['maxHealth'] = sheet.cell(i, 4).value
                temp['attributes']['attackDamage'] = sheet.cell(i, 6).value
                temp['attributes']['armor'] = sheet.cell(i, 7).value
                temp['attributes']['attackSpeed'] = sheet.cell(i, 8).value
                temp['attributes']['movementSpeed'] = sheet.cell(i, 9).value
                temp['attributes']['armorToughness'] = sheet.cell(i, 10).value
                temp['attributes']['knockbackResistance'] = sheet.cell(i, 11).value
                temp['part'] = sheet.cell(i, 3).value
                temp['unbreakable'] = sheet.cell(i, 5).value
                temp['hides'] = {}
                temp['hides']['ATTRIBUTES'] = self.__zero_conv(sheet.cell(i, 12).value)
                temp['hides']['ENCHANTS'] = self.__zero_conv(sheet.cell(i, 13).value)
                temp['hides']['DESTROYS'] = self.__zero_conv(sheet.cell(i, 14).value)
                temp['hides']['PLACED_ON'] = self.__zero_conv(sheet.cell(i, 15).value)
                temp['hides']['POTION_EFFECTS'] = self.__zero_conv(sheet.cell(i, 16).value)
                temp['hides']['UNBREAKABLE'] = self.__zero_conv(sheet.cell(i, 17).value)
                temp['ench'] = []
                all_items = []
                for i in range(len(self.__items)):
                    all_items.append(self.__items[i]['Name'])
                if temp['Name'] not in all_items:
                    self.__items.append(temp)
                else:
                    item_index = self.__find_index(all_items, temp['Name'])
                    self.__items[item_index] = temp
                self.__refreshList()
                count += 1
                # except:
                #     self.__Label_statusText['text'] = '{0} 数据格式不正确'.format(self.__getTime())
                #     return
            if count != 0:
                self.__Label_statusText['text'] = '{0} 成功导入文件 {1}'.format(self.__getTime(), file_path)
            else:
                self.__Label_statusText['text'] = '{0} 文件为空或数据格式不正确'.format(self.__getTime())

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
        file_path = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[('数据文件', '*.json')], defaultextension=".json")
        if file_path is not '':
            with open(file=file_path, mode='w', encoding='utf-8') as file:
                json.dump(self.__items, file, ensure_ascii=False)
            self.__Label_statusText['text'] = '{0} 保存成功'.format(self.__getTime())

    def __save_file_yaml(self):
        self.__output_all_yaml()
        file_path = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[('YAML 数据文件', '*.yml')], defaultextension=".yml")
        if file_path is not '':
            with open(file=file_path, mode='w', encoding='utf-8') as file:
                yaml.safe_dump(self.__yamls, file, default_flow_style=False, encoding='utf-8', allow_unicode=True)
            self.__Label_statusText['text'] = '{0} 导出成功'.format(self.__getTime())

    def __selectItem(self, listObj):
        if len(listObj.selection()) != 0:
            return listObj.item(listObj.selection()[0])['values'][0]

    def __clear_show_data(self):
        self.__Text_showData.delete(1.0, END)

    def __clearList(self, listObj):
        items = listObj.get_children()
        for item in items:
            listObj.delete(item)

    def __refreshList(self):
        self.__clearList(self.__itemList)
        count = 0
        for i in range(len(self.__items)):
            self.__itemList.insert('', END, value=[i + 1, self.__items[i]['Name']])

    def __save_to_list(self):
        if self.__StringVar_name.get() == '':
            self.__Label_statusText['text'] = '{0} 必须填写物品名称'.format(self.__getTime())
            return
        temp = {}
        temp['Name'] = self.__StringVar_name.get()
        temp['id'] = self.__StringVar_id.get()
        temp['lore'] = self.__StringVar_lore.get()
        temp['attributes'] = {}
        temp['attributes']['maxHealth'] = self.__StringVar_maxHealth.get()
        temp['attributes']['attackDamage'] = self.__StringVar_attackDamage.get()
        temp['attributes']['armor'] = self.__StringVar_armor.get()
        temp['attributes']['attackSpeed'] = self.__StringVar_attackSpeed.get()
        temp['attributes']['movementSpeed'] = self.__StringVar_movementSpeed.get()
        temp['attributes']['armorToughness'] = self.__StringVar_armorToughness.get()
        temp['attributes']['knockbackResistance'] = self.__StringVar_knockbackResistance.get()
        temp['part'] = self.__StringVar_part.get()
        temp['unbreakable'] = self.__StringVar_unbreakable.get()
        temp['hides'] = {}
        temp['hides']['ATTRIBUTES'] = self.__IntVar_ATTRIBUTES.get()
        temp['hides']['ENCHANTS'] = self.__IntVar_ENCHANTS.get()
        temp['hides']['DESTROYS'] = self.__IntVar_DESTROYS.get()
        temp['hides']['PLACED_ON'] = self.__IntVar_PLACED_ON.get()
        temp['hides']['POTION_EFFECTS'] = self.__IntVar_POTION_EFFECTS.get()
        temp['hides']['UNBREAKABLE'] = self.__IntVar_UNBREAKABLE.get()
        try:
            temp['ench'] = self.__enchantment_id_lvl
        except:
            temp['ench'] = []
        all_items = []
        for i in range(len(self.__items)):
            all_items.append(self.__items[i]['Name'])
        if temp['Name'] not in all_items:
            self.__items.append(temp)
            self.__Label_statusText['text'] = '{0} 物品信息已保存至列表，指令已复制到剪切板'.format(self.__getTime())
        else:
            self.__Label_statusText['text'] = '{0} 列表中的物品已经更新，指令已复制到剪切板'.format(self.__getTime())
            item_index = self.__find_index(all_items, temp['Name'])
            self.__items[item_index] = temp
        self.__refreshList()
        self.__setText(self.__generate())
        
    def __delete_Select(self):
        select = self.__itemList.focus()
        if select == '' or None:
            self.__Label_statusText['text'] = '{0} 没有选择物品'.format(self.__getTime())
            return
        selected = self.__selectItem(self.__itemList) - 1
        self.__itemList.delete(select)
        del self.__items[selected]
        self.__refreshList()
        self.__clear_show_data()
        self.__Label_statusText['text'] = '{0} 选择的物品已删除'.format(self.__getTime())

    def __load_from_list(self):
        select = self.__selectItem(self.__itemList)
        if select == None:
            self.__Label_statusText['text'] = '{0} 没有选择物品'.format(self.__getTime())
            return
        selected = self.__selectItem(self.__itemList) - 1
        temp = self.__items[selected]
        self.__StringVar_name.set(temp['Name'])
        self.__StringVar_id.set(temp['id'])
        self.__StringVar_lore.set(temp['lore'])
        self.__StringVar_maxHealth.set(temp['attributes']['maxHealth'])
        self.__StringVar_attackDamage.set(temp['attributes']['attackDamage'])
        self.__StringVar_armor.set(temp['attributes']['armor'])
        self.__StringVar_attackSpeed.set(temp['attributes']['attackSpeed'])
        self.__StringVar_movementSpeed.set(temp['attributes']['movementSpeed'])
        self.__StringVar_armorToughness.set(temp['attributes']['armorToughness'])
        self.__StringVar_knockbackResistance.set(temp['attributes']['knockbackResistance'])
        self.__StringVar_part.set(temp['part'])
        self.__StringVar_unbreakable.set(temp['unbreakable'])
        self.__IntVar_ATTRIBUTES.set(temp['hides']['ATTRIBUTES'])
        self.__IntVar_ENCHANTS.set(temp['hides']['ENCHANTS'])
        self.__IntVar_DESTROYS.set(temp['hides']['DESTROYS'])
        self.__IntVar_PLACED_ON.set(temp['hides']['PLACED_ON'])
        self.__IntVar_POTION_EFFECTS.set(temp['hides']['POTION_EFFECTS'])
        self.__IntVar_UNBREAKABLE.set(temp['hides']['UNBREAKABLE'])
        self.__enchantment_id_lvl = temp['ench']
        self.__conv_id_to_name()
        try:
            self.__refresh_enchantment()
        except:
            None

        self.__setText(self.__generate())
        self.__Label_statusText['text'] = '{0} 已从列表载入物品信息，指令已复制到剪切板'.format(self.__getTime())

    def __reset_window(self):
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
        self.__enchantment_name_lvl = []
        try:
            self.__clearList(self.__enchantmentList)
        except:
            return

    def __reset(self):
        self.__reset_window()
        self.__clear_show_data()
        self.__Label_statusText['text'] = '{0} 面板已重置'.format(self.__getTime())

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
        self.__Label_statusText['text'] = '{0} 列表已清空'.format(self.__getTime())

    def __output_all(self):
        self.__clear_show_data()
        self.__datas = []
        for i in self.__items:
            temp = i
            self.__StringVar_name.set(temp['Name'])
            self.__StringVar_id.set(temp['id'])
            self.__StringVar_lore.set(temp['lore'])
            self.__StringVar_maxHealth.set(temp['attributes']['maxHealth'])
            self.__StringVar_attackDamage.set(temp['attributes']['attackDamage'])
            self.__StringVar_armor.set(temp['attributes']['armor'])
            self.__StringVar_attackSpeed.set(temp['attributes']['attackSpeed'])
            self.__StringVar_movementSpeed.set(temp['attributes']['movementSpeed'])
            self.__StringVar_armorToughness.set(temp['attributes']['armorToughness'])
            self.__StringVar_knockbackResistance.set(temp['attributes']['knockbackResistance'])
            self.__StringVar_part.set(temp['part'])
            self.__StringVar_unbreakable.set(temp['unbreakable'])
            self.__enchantment_name_lvl = temp['ench']
            tempData = self.__generate()
            self.__datas.append(tempData)
        self.__Text_showData.delete(1.0, END)
        for i in range(len(self.__datas)):
            self.__Text_showData.insert('insert', self.__datas[i])
            self.__Text_showData.insert('insert', '\n\n')
        self.__reset_window()
        if len(self.__datas) != 0:
            self.__Label_statusText['text'] = '{0} 生成完成'.format(self.__getTime())
        else:
            self.__Label_statusText['text'] = '{0} 列表为空'.format(self.__getTime())

    def __output_all_yaml(self):
        self.__yamls = {}
        for temp in self.__items:
            self.__yamls[temp['Name']] = {}
            currentItem = self.__yamls[temp['Name']]
            if temp['id'] == '':
                currentItem['Id'] = 0
            else:
                currentItem['Id'] = int(temp['id'])
            currentItem['Data'] = 0
            currentItem['Display'] = temp['Name']
            currentItem['Lore'] = temp['lore'].split(';')
            currentItem['Attributes'] = {}
            currentItem['Attributes'][self.__slot_conv[temp['part']]] = {}
            currentItem['Enchantments'] = []
            ench = temp['ench']
            for i in range(len(ench)):
                currentItem['Enchantments'].append('{0}:{1}'.format(ench[i]['id'], ench[i]['lvl']))
            selectedHides = temp['hides']
            hides = []
            for i in selectedHides:
                if selectedHides[i] == 1:
                    hides.append(i)
            currentItem['Hide'] = hides
            if temp['unbreakable'] == '是':
                currentItem['Options'] = {}
                currentItem['Options']['Unbreakable'] = True
            for i in ['maxHealth', 'attackDamage', 'armor', 'attackSpeed', 'movementSpeed', 'armorToughness', 'knockbackResistance']:
                if temp['attributes'][i] == '':
                    continue
                else:
                    currentItem['Attributes'][self.__slot_conv[temp['part']]][i] = float(self.__handle_number(str(temp['attributes'][i])))

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
        self.__itemDict['display']['Name'] = self.__StringVar_name.get()

    def __handle_lore(self):
        if self.__StringVar_lore.get() == '':
            return
        self.__itemDict['display']['Lore'] = self.__StringVar_lore.get().split(';')

    def __handle_unbreakable(self):
        if self.__StringVar_unbreakable.get() == '是':
            self.__itemDict['Unbreakable'] = 1

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
        temp['Slot'] = self.__slot_conv[self.__StringVar_part.get()]
        self.__itemDict['AttributeModifiers'].append(temp)

    def __generate(self):
        self.__itemDict = {'display': {'Name': '', 'Lore': []}, 'AttributeModifiers': [], 'ench': []}
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
        self.__itemDict['ench'] = self.__enchantment_id_lvl

        data = str(self.__itemDict)
        exp = "'([0-9a-zA-Z]+)': "
        pat = re.compile(exp)
        data = re.sub(exp, r'\g<1>: ', data)
        data = data.replace("'head'", 'head')
        data = data.replace("'chest'", 'chest')
        data = data.replace("'legs'", 'legs')
        data = data.replace("'feet'", 'feet')
        data = data.replace("'", "\"")
        try:
            set_id = int(self.__Entry_id.get())
        except:
            self.__StringVar_id.set('0')
            set_id = 0
        data = '/give @p {0} 1 '.format(set_id) + data
        self.__Text_showData.delete(1.0, END)
        self.__Text_showData.insert('insert', data)
        return data


if __name__ == '__main__':
    main = GUI()
