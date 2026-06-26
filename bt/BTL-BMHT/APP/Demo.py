import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

import cx_Oracle


class WelcomeFrame(ttk.Frame):
    def __init__(self, info_frame, container):
        super().__init__(container)

        self.grid_propagate(0)
        self.config(height=140, width=600)
        self.config(style='Welcome.TFrame')

        self.welcome = ' ỨNG DỤNG DEMO\nNHÓM 3'
        self.welcome_label = ttk.Label(self, text=self.welcome,
                                       style='Welcome.TLabel',
                                       font=('Helvecati 40'),
                                       foreground='red',
                                       width=33, anchor='center',
                                       justify=tk.CENTER)
        self.welcome_label.grid(column=0, row=0, sticky=tk.NSEW,
                                pady=10, padx=10)

        self.grid(column=0, row=1, columnspan=3, padx=5, pady=80,
                  sticky=tk.NSEW)

        # style theme
        info_frame.style.configure('Welcome.TFrame', borderwidth=5,
                                   relief='ridge')
        info_frame.style.configure('Welcome.TLabel')


class SearchBar(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # attribute
        self.data_frame = container.data_frame
        self.tab = {'KHACHHANG': 'KHÁCH HÀNG',
                    'MATHANG': 'MẶT HÀNG',
                    'GIAOHANG': 'PHIẾU GIAO',
                    'QUANLY': 'NGƯỜI DÙNG',
                    'CONGNO': 'CÔNG NỢ'}
        self.options = {'padx': 5, 'pady': 5}

        # search label
        self.search_label = ttk.Label(self, width=18, anchor='center',
                                      text=f'XEM {self.tab[container.tbname]}',
                                      style='Result.TLabel')
        self.search_label.grid(column=0, row=0, sticky=tk.NSEW, **self.options)

        # slide button
        self.first_result_btn = ttk.Button(self, text='<<', width=3,
                                           style='Result.TButton')
        self.first_result_btn['command'] = lambda: self.update('s')
        self.first_result_btn.grid(column=1, row=0)

        self.left_btn = ttk.Button(self, text='<', width=2,
                                   style='Result.TButton')
        self.left_btn['command'] = lambda: self.update('l')
        self.left_btn.grid(column=2, row=0)

        self.current_txt = tk.StringVar()
        # str_txt = f'{self.data_frame.s_page+1}/{len(self.data_frame.rows)}'
        # self.current_txt.set(str_txt)
        self.current_btn = ttk.Button(self, textvariable=self.current_txt,
                                      width=6, style='Result.TButton')
        self.current_btn.grid(column=3, row=0)

        self.right_btn = ttk.Button(self, text='>', width=2,
                                    style='Result.TButton')
        self.right_btn['command'] = lambda: self.update('r')
        self.right_btn.grid(column=4, row=0)

        self.last_result_btn = ttk.Button(self, text='>>', width=3,
                                          style='Result.TButton')
        self.last_result_btn['command'] = lambda: self.update('e')
        self.last_result_btn.grid(column=5, row=0)

        # search entry
        self.search = tk.StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search,
                                      font=("Helvetica 15"), width=20)
        self.search_entry.grid(column=6, row=0, sticky=tk.E, padx=5)
        self.search_entry.focus()

        self.search_btn = ttk.Button(self, text='TÌM KIẾM',
                                     style='Result.TButton')
        self.search_btn.grid(column=7, row=0, padx=5)
        self.search_btn.configure(command=self.search)

        # add button
        self.add_btn = ttk.Button(self, text='THÊM MỚI',
                                  style='Result.TButton')
        self.add_btn.grid(column=8, row=0, padx=5)
        self.add_btn['command'] = lambda: self.add()

        self.update('s')

        # grid to ResultFrame
        self.grid(column=0, row=0, sticky=tk.NSEW)

    def search(self):
        print('search')

    def update(self, direction):
        if direction == 's':
            self.data_frame.fill_data(0)
        elif direction == 'e':
            self.data_frame.fill_data(99)
        elif direction == 'r':
            self.data_frame.fill_data(10)
        elif direction == 'l':
            self.data_frame.fill_data(-10)

        str_txt = f'{self.data_frame.s_page+1}/{len(self.data_frame.rows)}'
        self.current_txt.set(str_txt)

        for e in self.data_frame.add_entry:
            e.grid_forget()
        self.data_frame.add_btn.grid_forget()

    def add(self):
        for idx, e in enumerate(self.data_frame.add_entry):
            e.grid(column=idx,
                   row=len(self.data_frame.rows)+1, sticky=tk.NSEW)
        self.data_frame.add_btn.grid(column=len(self.data_frame.col),
                                     row=len(self.data_frame.rows)+1,
                                     sticky=tk.NSEW, columnspan=2)
        self.data_frame.add_entry[0].focus()


class DataFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.frames = container.frames
        self.csdl = container.csdl
        self.tbname = container.tbname
        self.col = container.cols[container.tbname]
        self.cur = container.cur
        self.sql = container.sql
        self.s_page = container.s_page
        self.e_page = container.e_page

        for idx, col in enumerate(self.col):
            ttk.Label(self, text=col, relief='raised',
                      anchor='center', font=('Helvecati 14'),
                      style='Result.TLabel'
                      ).grid(column=idx, row=0, ipadx=18,
                             pady=4, sticky=tk.NSEW)

        self.data = []
        self.entry_data = []
        self.edit_btn = []
        self.del_btn = []
        for num in range(10):
            for row in range(len(self.col)):
                idx = num*len(self.col)+row
                self.data.append(tk.StringVar())
                self.entry_data.append(tk.Entry(self,
                                                font=('Helvecati 12'),
                                                justify=tk.CENTER, width=2,
                                                state='readonly',
                                                readonlybackground='white',
                                                textvariable=self.data[idx]))
            # edit-del button
            self.edit_btn.append(ttk.Button(self, text='Sửa', width=4))
            self.edit_btn[num]['command'] = lambda x=num: self.edit_clicked(x)
            self.del_btn.append(ttk.Button(self, text='Xóa', width=4))
            self.del_btn[num]['command'] = lambda x=num: self.del_clicked(x)

        # add row
        self.add_entry = []
        self.add_txt = []
        for row in range(len(self.col)):
            self.add_txt.append(tk.StringVar())
            self.add_entry.append(tk.Entry(self,
                                           font=('Helvecati 12'),
                                           justify=tk.CENTER, width=2,
                                           textvariable=self.add_txt[row]))
        self.add_btn = ttk.Button(self, text='Thêm', width=2)
        self.add_btn['command'] = lambda: self.insert()

        self.grid(column=0, row=1, sticky=tk.NSEW, padx=5, pady=5)

    def fill_data(self, val):
        # get rows
        self.cur.execute(self.sql)
        self.rows = self.cur.fetchall()

        # get rid off old data and row visable
        for num in range(10):
            for row in range(len(self.col)):
                idx = num*len(self.col)+row
                self.data[idx].set('')
                self.entry_data[idx].grid_forget()
            self.edit_btn[num].grid_forget()
            self.del_btn[num].grid_forget()

        # update data and row visable
        if val == 0:
            self.s_page = 0
        elif val == 99:
            self.s_page = len(self.rows) - (len(self.rows) % 10)
        elif val < 0:
            self.s_page = max(0, self.s_page+val)
        else:
            if self.s_page + val < len(self.rows):
                self.s_page = self.s_page + val
        self.e_page = min(self.s_page + 10, len(self.rows))

        for num in range(self.s_page, self.e_page):
            for row in range(len(self.col)):
                idx = (num % 10)*len(self.col)+row
                self.data[idx].set(self.rows[num][row])
                self.entry_data[idx].grid(column=row, row=num+1, pady=3,
                                          sticky=tk.NSEW)
            self.edit_btn[num % 10].grid(column=len(self.col), row=num+1)
            self.del_btn[num % 10].grid(column=len(self.col)+1, row=num+1)

    def edit_clicked(self, line):
        s = line*len(self.col)
        e = (line+1)*len(self.col)
        for entry in self.entry_data[s:e]:
            entry.config(state='normal')
            entry.config(bg='cyan')

        self.edit_btn[line].config(text='OK')
        self.edit_btn[line]['command'] = lambda x=line: self.edit(x)

    def edit(self, line):
        sql = ''
        id = ''
        colnames = []
        if self.tbname == 'KHACHHANG':
            sql = f'UPDATE {self.csdl}KHACHHANG SET '
            colnames = ['MSKH', 'TENKH', 'SOCMND', 'DIACHI',
                        'MSTHUE', 'KHS', 'MSKV']
            id = 'MSKH'
        elif self.tbname == 'MATHANG':
            sql = f'UPDATE {self.csdl}MATHANG SET '
            colnames = ['MSMH', 'TENMH', 'SLTON', 'DVT', 'MOTA', 'MSLOAI']
            id = 'MSMH'
        elif self.tbname == 'CONGNO':
            sql = f'UPDATE {self.csdl}KHACHHANGSI SET '
            colnames = ['MSKH', 'DINHMUCCONGNO', 'CONGNO']
            id = 'MSKH'

        s = line*len(self.col)
        e = (line+1)*len(self.col)
        for colname, text in zip(colnames, self.data[s:e]):
            sql = sql + colname + '=\'' + text.get().upper() + '\','

        cond = '\'' + self.data[line*len(self.col)].get().upper() + '\''
        sql = sql.rstrip(',') + f' WHERE {id}=' + cond
        print(sql)
        try:
            self.cur.execute(sql)
        except cx_Oracle.DatabaseError as er:
            showinfo(title='Error',
                     message=er)
        else:
            self.cur.execute('COMMIT')
            self.edit_btn[line].config(text='Sửa')
            self.edit_btn[line]['command'
                                ] = lambda x=line: self.edit_clicked(x)

            for entry in self.entry_data[s:e]:
                entry.config(state='readonly')
                # entry.config(bg='cyan')

            # for frame in self.frames.values():
            #    frame.data_frame.fill_data(0)
            #    frame.search_bar.update('s')

    def del_clicked(self, line):
        sql = ''
        if self.tbname == 'KHACHHANG':
            sql = f'DELETE FROM {self.csdl}KHACHHANG WHERE MSKH='
        elif self.tbname == 'MATHANG':
            sql = f'DELETE FROM {self.csdl}MATHANG WHERE MSMH='
        elif self.tbname == 'GIAOHANG':
            sql = f'DELETE FROM {self.csdl}PHIEUGIAO WHERE MSPG='
        elif self.tbname == 'QUANLY':
            sql = f'DELETE FROM {self.csdl}KHUVUC WHERE MSKV='
        elif self.tbname == 'CONGNO':
            sql = f'DELETE FROM {self.csdl}KHACHHANGSI WHERE MSKH='

        sql = sql + '\'' + self.data[line*len(self.col)].get().upper() + '\''

        try:
            self.cur.callproc('CSDL.DISABLE_GIAO_HANG_DEL')
            self.cur.execute(sql)
        except cx_Oracle.DatabaseError as er:
            showinfo(title='Error',
                     message=er)
        else:
            self.cur.execute('COMMIT')
            self.cur.callproc('CSDL.ENABLE_GIAO_HANG_DEL')
            for frame in self.frames.values():
                frame.data_frame.fill_data(0)
                frame.search_bar.update('s')

    def insert(self):
        sql = ''
        if self.tbname == 'KHACHHANG':
            sql = f'INSERT INTO {self.csdl}KHACHHANG VALUES ('
            for text in self.add_txt:
                sql = sql + '\'' + text.get().upper() + '\','
        elif self.tbname == 'MATHANG':
            sql = f'INSERT INTO {self.csdl}MATHANG VALUES ('
            for text in self.add_txt:
                sql = sql + '\'' + text.get().upper() + '\','
        elif self.tbname == 'GIAOHANG':
            if self.add_txt[2].get() == '':
                sql = f'INSERT INTO {self.csdl}CHITIETDONDATHANG VALUES ('
                sql = sql + '\'' + self.add_txt[0].get().upper() + '\','
                sql = sql + '\'' + self.add_txt[1].get().upper() + '\','
                sql = sql + '\'' + self.add_txt[4].get().upper() + '\','
                sql = sql + '\'' + self.add_txt[5].get().upper() + '\','
            else:
                if self.add_txt[3].get() == '':
                    sql = f'INSERT INTO {self.csdl}DONDATHANG(MSKH) VALUES ('
                    sql = sql + '\'' + self.add_txt[2].get().upper() + '\','
                else:
                    sql = f'INSERT INTO {self.csdl}DONDATHANG(NGAYDH,MSKH) VALUES ('
                    sql = sql + 'TO_DATE(\'' + self.add_txt[3].get().upper() + '\','
                    sql = sql + '\'DD-MM-YYYY\'' + '),'
                    sql = sql + '\'' + self.add_txt[2].get().upper() + '\','
        elif self.tbname == 'QUANLY':
            sql = f'INSERT INTO {self.csdl}KHUVUC VALUES ('
        elif self.tbname == 'CONGNO':
            sql = f'INSERT INTO {self.csdl}KHACHHANGSI VALUES ('

        # for text in self.add_txt:
        #    sql = sql + '\'' + text.get().upper() + '\','
        sql = sql.rstrip(',') + ')'
        print(sql)
        try:
            self.cur.execute(sql)
        except cx_Oracle.DatabaseError as er:
            showinfo(title='Error',
                     message=er)
        else:
            self.cur.execute('COMMIT')
            for frame in self.frames.values():
                frame.data_frame.fill_data(0)
                frame.search_bar.update('s')


class ResultFrame(ttk.LabelFrame):
    def __init__(self, infoframe, tbname):
        super().__init__(infoframe.parent)

        self.frames = infoframe.frames
        self.cur = infoframe.cur
        self.csdl = infoframe.csdl
        self.tbname = tbname
        self.sql = ''
        self.s_page = 0
        self.e_page = 10
        self.val = 0

        # frame configure
        self.config(text='<<KẾT QUẢ>>')
        self.grid_propagate(0)
        self.config(height=425, width=980)
        self.config(style='Result.TLabelframe')

        # style theme
        infoframe.style.configure("Result.TLabelframe", borderwidth=5,
                                  relief='sunken')
        infoframe.style.configure('Result.TLabel', font=('Helvetica', 16),
                                  relief='groove')
        infoframe.style.configure('Result.TButton', font=('Helvetica', 12))

        self.cols = {
            'KHACHHANG': ('MÃ SỐ', 'KHÁCH HÀNG', 'CMND', 'ĐỊA CHỈ KHÁCH HÀNG',
                          'MS THUẾ', 'K.SỈ', 'K.VỰC'),
            'MATHANG': ('MÃ SỐ', 'HÀNG HÓA', 'TỒN', 'DVT', 'MÔ TẢ', 'LOẠI'),
            'GIAOHANG': ('MÃ ĐƠN HÀNG', 'MÃ MẶT HÀNG', 'MÃ KH',
                         'NGÀY ĐẶT HÀNG', 'SL', 'ĐÃ GIAO'),
            'QUANLY': ('MÃ KHU VỰC', 'TÊN KHU VỰC'),
            'CONGNO': ('MÃ KHÁCH HÀNG', 'ĐỊNH MỨC CÔNG NỢ', 'CÔNG NỢ')
        }

        # get sql
        self.get_sql()

        # create dataframe
        self.data_frame = DataFrame(self)
        # create search bar
        self.search_bar = SearchBar(self)
        # fill first few data
        # self.data_frame.fill_data(self.val)

        # grid to window
        self.grid(column=0, row=1, sticky=tk.NSEW, **infoframe.options)

    def get_sql(self):
        if self.tbname == 'KHACHHANG':
            self.sql = f'SELECT * FROM {self.csdl}KHACHHANG'
        elif self.tbname == 'MATHANG':
            self.sql = f'SELECT * FROM {self.csdl}MATHANG'
        elif self.tbname == 'GIAOHANG':
            self.sql = (f'SELECT {self.csdl}DONDATHANG.MSDH,MSMH,MSKH,NGAYDH,SLDAT,SLDAGIAO FROM '
                        f'{self.csdl}DONDATHANG LEFT OUTER JOIN '
                        f'{self.csdl}CHITIETDONDATHANG ON '
                        f'{self.csdl}DONDATHANG.MSDH={self.csdl}CHITIETDONDATHANG.MSDH')
            print(self.sql)
        elif self.tbname == 'QUANLY':
            self.sql = f'SELECT * FROM {self.csdl}KHUVUC'
        elif self.tbname == 'CONGNO':
            self.sql = f'SELECT * FROM {self.csdl}KHACHHANGSI'


class InfoFrame(ttk.LabelFrame):
    def __init__(self, container):
        super().__init__(container)

        # attribute
        self.parent = container
        self.conn = None
        self.cur = None
        self.server = 'orcl2'
        self.port = '1522'
        self.csdl = 'CSDL.'
        self.options = {'padx': 5, 'pady': 5}

        # frame configure
        self.config(text='<<NHÂN VIÊN - THÔNG TIN>>')
        self.grid_propagate(0)
        self.config(height=150, width=990)

        # style theme
        self.style = ttk.Style(self)
        self.style.theme_use('alt')
        # self.style.configure("Result.TLabelframe", borderwidth=5,
        #                     relief='sunken')
        self.style.configure('Info.TButton', font=('Helvetica', 13))
        self.style.configure('Info.TLabel', font=('Helvetica', 16),
                             relief='groove')
        self.style.configure('Table.TButton', font=('Helvetica', 17),
                             relief='sunken')
        self.style.configure('Selected.TButton', font=('Helvetica', 17),
                             relief='raised', foreground='blue')

        # username label
        self.user_label = ttk.Label(self, text='USER', style='Info.TLabel',
                                    relief='raised', anchor='center', width=12)
        self.user_label.grid(column=0, row=0, sticky=tk.NSEW, **self.options)

        # user label
        self.username = tk.StringVar()
        self.username.set('Not Login')
        self.username_label = ttk.Label(self, textvariable=self.username,
                                        style='Info.TLabel', foreground='red',
                                        relief='groove', width=15,
                                        anchor='center')
        self.username_label.grid(column=1, row=0, sticky=tk.NSEW, pady=5)

        # login/logout/change button
        self.login_text = tk.StringVar()
        self.login_text.set('>> Login <<')
        self.login_btn = ttk.Button(self, textvariable=self.login_text,
                                    style='Info.TButton', width=20)
        self.login_btn.grid(column=2, row=0, sticky=tk.NSEW, **self.options)
        self.login_btn['command'] = lambda: self.login_clicked()

        # username entry
        self.login_user = tk.StringVar()
        self.usr_entry = ttk.Entry(self, width=15, justify=tk.CENTER,
                                   font=('Helvetica', 15),
                                   textvariable=self.login_user)
        self.log_pass = tk.StringVar()
        self.pass_entry = ttk.Entry(self, show='*', width=10,
                                    justify=tk.CENTER,
                                    font=('Helvetica', 15),
                                    textvariable=self.log_pass)
        self.log_btn = ttk.Button(self, style='Info.TButton', text='Login',
                                  width=7)
        self.log_btn['command'] = lambda: self.login_valid()

        # database status label
        self.database_label = ttk.Label(self, text='DATABASE', relief='raised',
                                        style='Info.TLabel', anchor='center',
                                        width=12)
        self.database_label.grid(column=0, row=1, sticky='W', **self.options)

        # status label
        self.data_status = tk.StringVar()
        self.data_status.set('Disconnect')
        self.status_label = ttk.Label(self, textvariable=self.data_status,
                                      style='Info.TLabel', foreground='red',
                                      relief='groove', width=15,
                                      anchor='center')
        self.status_label.grid(column=1, row=1, sticky=tk.NSEW, pady=5)

        # configure database
        self.db_btn = ttk.Button(self, text='>> Config <<',
                                 style='Info.TButton', width=20)
        self.db_btn.grid(column=2, row=1, sticky='EW', **self.options)
        self.db_btn['command'] = lambda: self.configure_clicked()

        # configure entry
        self.config_frame = ttk.Frame(self)

        self.server_n = tk.StringVar()
        self.server_n.set(self.server)
        self.server_entry = ttk.Entry(self.config_frame, width=6,
                                      justify=tk.CENTER,
                                      font=('Helvetica', 15),
                                      textvariable=self.server_n)
        self.server_entry.grid(column=0, row=0, sticky=tk.NSEW, **self.options)
        self.port_n = tk.StringVar()
        self.port_n.set(self.port)
        self.port_entry = ttk.Entry(self.config_frame, width=6,
                                    justify=tk.CENTER,
                                    font=('Helvetica', 15),
                                    textvariable=self.port_n)
        self.port_entry.grid(column=1, row=0, sticky=tk.NSEW, **self.options)
        self.csdl_n = tk.StringVar()
        self.csdl_n.set(self.csdl.rstrip('.'))
        self.csdl_n_entry = ttk.Entry(self.config_frame, width=6,
                                      justify=tk.CENTER,
                                      font=('Helvetica', 15),
                                      textvariable=self.csdl_n)
        self.csdl_n_entry.grid(column=2, row=0, sticky=tk.NSEW, **self.options)
        self.ok_btn = ttk.Button(self.config_frame, style='Info.TButton',
                                 text='OK', width=4)
        self.ok_btn['command'] = lambda: self.data_config()
        self.ok_btn.grid(column=3, row=0, sticky=tk.NSEW, **self.options)

        # version label
        self.ver_label = ttk.Label(self, text='Ver: 0.1', anchor='center',
                                   foreground='white',
                                   style='Info.TLabel',
                                   background='red', width=12)
        self.ver_label.grid(column=0, row=2, sticky=tk.NSEW, **self.options)

        # tablename label
        self.tbname = {0: 'KHACHHANG', 1: 'MATHANG', 2: 'GIAOHANG',
                          3: 'QUANLY', 4: 'CONGNO'}
        self.tabs = {0: 'KHÁCH HÀNG', 1: 'MẶT HÀNG', 2: 'ĐƠN HÀNG',
                     3: 'QUẢN LÝ', 4: 'CÔNG NỢ'}
        self.table_selected = 0
        self.tbname_frame = ttk.Frame(self)

        self.tb_labels = []
        for idx in self.tbname.keys():
            self.tb_labels.append(ttk.Button(self.tbname_frame,
                                             text=self.tabs[idx],
                                             state='disable',
                                             style='Table.TButton'))
            self.tb_labels[idx].grid(column=idx, row=0, padx=4, pady=5)
            self.tb_labels[idx
                           ]['command'
                             ] = lambda idx=idx: self.cframe(idx)

        # grid tablename_labels to infoFrame
        self.tbname_frame.grid(column=1, row=2, columnspan=10, sticky=tk.NSEW)

        # grid to container
        self.grid(column=0, row=0, sticky=tk.NSEW, **self.options)

        # init welcome logo
        self.wel_frame = WelcomeFrame(self, container)

        # initialize resultframes
        self.frames = {}

    def configure_clicked(self):
        # self.server_entry.grid(column=3, row=1, sticky=tk.NSEW, pady=5)
        # self.port_entry.grid(column=4, row=1, sticky=tk.NSEW, pady=5)
        # self.csdl_n_entry.grid(column=5, row=1, sticky=tk.NSEW, pady=5)
        # self.ok_btn.grid(column=6, row=1, sticky=tk.NSEW, pady=5)
        self.config_frame.grid(column=3, row=1, columnspan=10,
                               sticky=tk.NSEW)

    def data_config(self):
        self.server = self.server_n.get()
        self.port = self.port_n.get()
        self.csdl = self.csdl_n.get() + '.'
        self.config_frame.grid_forget()
        print(self.server, self.csdl, self.port)

    def login_clicked(self):
        self.login_text.set('Nhập Thông Tin')
        self.usr_entry.grid(column=3, row=0, sticky=tk.NSEW, **self.options)
        self.usr_entry.focus()
        self.pass_entry.grid(column=4, row=0, sticky=tk.NSEW, **self.options)
        self.log_btn.grid(column=5, row=0, sticky=tk.NSEW, **self.options)

    def logout_clicked(self):
        # disable tbname
        for tb_label in self.tb_labels:
            tb_label.config(state='disable')
        # enable database config
        self.db_btn.config(state='enable')
        # destroy all frames
        for frame in self.frames.values():
            frame.destroy()
        # disconnect to database
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

        self.login_text.set('<< Login >>')
        self.username.set('Not Login')
        self.username_label.config(foreground='red')
        self.status_label.config(foreground='red')
        self.ver_label.config(background='red')
        self.tb_labels[self.table_selected].configure(style='Table.TButton')
        self.data_status.set('Disconnect')
        self.login_user.set('')
        self.log_pass.set('')
        self.login_btn['command'] = lambda: self.login_clicked()

    def login_valid(self):
        try:
            info = (f'{self.login_user.get().upper()}/'
                    f'{self.log_pass.get().upper()}@'
                    f'//localhost:{self.port}/{self.server}')
            self.conn = cx_Oracle.connect(info)
        except cx_Oracle.DatabaseError as er:
            showinfo(title='Oracle database error',
                     message=er)
        else:
            # get cursor
            self.cur = self.conn.cursor()
            # remove log_frame
            self.login_text.set('<< Logout >>')
            self.usr_entry.grid_forget()
            self.pass_entry.grid_forget()
            self.log_btn.grid_forget()
            # freeze database configure
            self.config_frame.grid_forget()
            self.db_btn.config(state='disable')

            # change status
            self.username.set(self.login_user.get().upper())
            self.username_label.config(foreground='blue')
            self.status_label.config(foreground='blue')
            self.ver_label.config(background='blue')
            self.data_status.set(self.conn.version)
            self.login_user.set('')
            self.log_pass.set('')
            self.login_btn['command'] = lambda: self.logout_clicked()

            # enable tbname
            for tb_label in self.tb_labels:
                tb_label.config(state='enable')

            # create resultframes
            for key, value in self.tbname.items():
                self.frames[key] = ResultFrame(self, value)

            self.cframe(0)

    def cframe(self, tab_no):
        self.tb_labels[self.table_selected].configure(style='Table.TButton')
        self.tb_labels[tab_no].configure(style='Selected.TButton')
        self.table_selected = tab_no
        frame = self.frames[self.table_selected]
        frame.tkraise()


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Demo UI')

        self.window_width = 1000
        self.window_height = 600
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.center_x = int(self.screen_width/2 - self.window_width/2)
        self.center_y = int(self.screen_height/2 - self.window_height/2)

        # set top screen
        self.center_y = 10

        self.geometry(f'{self.window_width}x{self.window_height}'
                      f'+{self.center_x}+{self.center_y}')

        self.resizable(False, False)


if __name__ == "__main__":
    app = App()
    infoFrame = InfoFrame(app)
    app.mainloop()
