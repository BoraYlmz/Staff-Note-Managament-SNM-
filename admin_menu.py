from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,QFrame,QHBoxLayout,QLineEdit,QPushButton,QComboBox,QSizePolicy,QSpacerItem,QTableWidget,QTableWidgetItem,QMessageBox,QDateEdit,QTextEdit,QCheckBox,QScrollArea
from PySide6.QtCore import Qt,QDate,QTimer
from PySide6 import QtCore , QtWidgets
from PySide6.QtGui import QColor,QTextCharFormat,QTextCursor,QFont,QPalette,QBrush
from Common_Class import theme_color, CustomTitleBar,Cipher
import Common_Class
import sys
from plyer import notification
import os
import json
from pymongo import MongoClient
import certifi
from datetime import datetime,timedelta
import configparser
import getpass
import subprocess
from dotenv import load_dotenv
import ast

class Content_Button_Menu():
    def __init__(self,parent,main_class:None):
        btn_menu_frm = QFrame(parent)
        btn_menu_frm.setFixedSize(parent.width(),40)
        btn_menu_frm.setStyleSheet(f"border: 1px solid {main_class.BORDER_COLOR};background-color:{main_class.WIN_COLOR};border-radius:25px;border-bottom-right-radius:0px;border-top-right-radius:0px;border-bottom-left-radius:0px;")
        btn_menu_frm.move(0,0)

        self.btn_menu_h_layout = QHBoxLayout(btn_menu_frm)
        self.btn_menu_h_layout.setContentsMargins(0,0,0,0)
        self.btn_menu_h_layout.setSpacing(0)
        self.spacer = QSpacerItem(1,39,QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.btn_menu_h_layout.addItem(self.spacer)

        self.left_btn_sheet = f"""QPushButton {{color:{main_class.FONT_COLOR};background-color:{main_class.PANEL_COLOR};font-size:14px;border: 0;border-right:1px solid {main_class.BORDER_COLOR}; border-bottom:1px solid {main_class.BORDER_COLOR}; border-radius:0;border-top-left-radius:25px; font-weight:bold;}} QPushButton:hover{{background-color:{main_class.BORDER_COLOR};}} """
        self.left_btn_clicked_sheet = f"""QPushButton {{color:white;background-color:{main_class.OS_RED};font-size:14px;border: 0;border-right:1px solid {main_class.BORDER_COLOR}; border-bottom:1px solid {main_class.BORDER_COLOR}; border-radius:0;border-top-left-radius:25px; font-weight:bold;}} QPushButton:hover{{background-color:{main_class.ON_HOVER_OS_RED};}} """
        self.btn_sheet=f"""QPushButton {{color:{main_class.FONT_COLOR};background-color:{main_class.PANEL_COLOR};font-size:14px;border: 0;border-right:1px solid {main_class.BORDER_COLOR}; border-bottom:1px solid {main_class.BORDER_COLOR}; border-radius:0; font-weight:bold;}} QPushButton:hover{{background-color:{main_class.BORDER_COLOR};}} """
        self.btn_clicked_sheet = f"""QPushButton {{color:white;background-color:{main_class.OS_RED};font-size:14px;border: 0;border-right:1px solid {main_class.BORDER_COLOR}; border-bottom:1px solid {main_class.BORDER_COLOR}; border-radius:0; font-weight:bold;}} QPushButton:hover{{background-color:{main_class.ON_HOVER_OS_RED};}} """
        self.clicked_buttons = None
        self.first_btn = None

    def new_btn(self,btn_name:str,btn_con):
        self.btn_menu_h_layout.removeItem(self.spacer)
        button = QPushButton(btn_name)
        
        button.setFixedSize(100,39)
        button.move(self.btn_menu_h_layout.count()*100,0)
        if self.first_btn == None:
            button.setStyleSheet(self.left_btn_sheet)
            self.first_btn=button
        else:
            button.setStyleSheet(self.btn_sheet)

        self.btn_menu_h_layout.addWidget(button)
        self.spacer = QSpacerItem(self.btn_menu_h_layout.parent().width(),39,QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.btn_menu_h_layout.addItem(self.spacer)
        button.clicked.connect(lambda: self.btn_connect(button,btn_con))

    def btn_connect(self,self_btn,btn_con):
        if self_btn != self.clicked_buttons:
            
            if self.clicked_buttons == None:
                pass
            elif self.clicked_buttons == self.first_btn:
                self.clicked_buttons.setStyleSheet(self.left_btn_sheet)
            else:
                self.clicked_buttons.setStyleSheet(self.btn_sheet)

            self.clicked_buttons = self_btn

            if self.first_btn == self.clicked_buttons:
                self.clicked_buttons.setStyleSheet(self.left_btn_clicked_sheet)
            else:
                self.clicked_buttons.setStyleSheet(self.btn_clicked_sheet)
            btn_con()

class CustomTableWidget(QTableWidget):
    def __init__(self, rows, columns, parent=None):
        super().__init__(rows, columns, parent)
        
    def wheelEvent(self, event):
        # Shift tuşu basılı ise yatay kaydırma yap
        if event.modifiers() == Qt.ShiftModifier:
            delta = event.angleDelta().y()  # angleDelta().y() normalde x çekilir ama y çalışıyor
            step = 120  # Kaydırma için normalize edilmiş bir adım büyüklüğü
            horizontal_scroll = delta / step
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - horizontal_scroll)
        else:
            super().wheelEvent(event)

class TodoItem(QWidget):
    def __init__(self, todo_data, parent=None):
        super().__init__(parent)
        self.todo_data = todo_data  # Gelen veriyi sakla
        self.setFixedSize(parent.content_child_frame.width() - 25, 70)
        self.parent_class = parent
        
        todo_area_content = QWidget()   
        todo_area_content.setStyleSheet(f"border:1px solid {parent.BORDER_COLOR};border-radius:0;")
        todo_area_content.setFixedSize(self.width()-10, self.height()-10)
        todo_area_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        todo_area_content_layout = QHBoxLayout(todo_area_content)
        
        self.layout = QHBoxLayout(self)
        
        left_box = QVBoxLayout()
        right_box = QVBoxLayout()
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()
        chech_box = QCheckBox()
        chech_box.setStyleSheet(f"""
            QCheckBox {{
                border: 1px solid {parent.BORDER_COLOR};
                background-color: {parent.PANEL_COLOR};
                width: 26px;
                height: 26px;
                border-radius: 13px;  /* Yuvarlak yapma */
                padding: 0px;
                outline: none;
            }}
            QCheckBox:checked {{
                background-color: {parent.GREEN};  /* Tıklanmış durumda yeşil arka plan */
            }}
            QCheckBox:indicator {{
                width: 100%;
                height: 100%;
                border-radius: 50%;
            }}
        """)
        chech_box.setProperty("_id", self.todo_data["_id"])
        chech_box.stateChanged.connect(parent.change_state_todos)
        chech_box.setFixedSize(26, 26)
        
        todo_text_box = QLabel(self.todo_data["item_text"])
        todo_text_box.setStyleSheet(f"color:{parent.FONT_COLOR};font-size:17px;border:0;font-family: Arial, sans-serif;")
        todo_date_text = QLabel(str(self.todo_data["date"]))
        todo_date_text.setStyleSheet(f"color:{parent.FONT_COLOR};font-size:13px;border:0;font-family: Arial, sans-serif;")
        todo_meet_header = QLabel(self.todo_data["meet_header"])
        todo_meet_header.setStyleSheet(f"color:{parent.FONT_COLOR};font-size:13px;border:0;font-family: Arial, sans-serif;")

        todo_meet_date =QLabel(str(self.todo_data["meet_date"]))
        todo_meet_date.setStyleSheet(f"color:{parent.FONT_COLOR};font-size:13px;border:0;font-family: Arial, sans-serif;")
        # todo_meet_date.setFixedWidth(75)

        
        # Layout eklemeleri
        
        top_layout.addWidget(todo_text_box,0,Qt.AlignLeft)
        top_layout.addWidget(todo_date_text,0,Qt.AlignRight)
        bottom_layout.addWidget(todo_meet_header)
        bottom_layout.addWidget(todo_meet_date,0,Qt.AlignRight)
        left_box.addWidget(chech_box)
        right_box.addLayout(top_layout)
        right_box.addLayout(bottom_layout)
        todo_area_content_layout.addLayout(left_box)
        todo_area_content_layout.addLayout(right_box)
        self.layout.addWidget(todo_area_content)
    def mouseDoubleClickEvent(self, event):
        # Çift tıklama olayını burada yakalıyoruz
        self.parent_class.Meet_Details(self.todo_data["meet_id"])
        
class Upcome_Meets_Item(QWidget):
    def __init__(self, meet_data, parent=None):
        super().__init__(parent)
        self.meetdata = meet_data  # Gelen veriyi sakla
        self.setFixedSize(parent.content_child_frame.width() - 25, 70)
        self.parent_class = parent
        
        todo_area_content = QWidget()   
        todo_area_content.setStyleSheet(f"border:1px solid {parent.BORDER_COLOR};border-radius:0;")
        todo_area_content.setFixedSize(self.width()-10, self.height()-10)
        todo_area_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        todo_area_content_layout = QHBoxLayout(todo_area_content)
        
        self.layout = QHBoxLayout(self)
        
        left_box = QVBoxLayout()
        right_box = QVBoxLayout()
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()
        
        Meet_Header = QLabel(self.meetdata["cst_header"])
        Meet_Header.setStyleSheet(f"color:{parent.FONT_COLOR};font-size:17px;border:0;font-family: Arial, sans-serif;font-weight:bold;")
        frm_name = QLabel(str(self.meetdata["frm_name"]))
        frm_name.setStyleSheet(f"color:{parent.FONT_COLOR};font-size:13px;border:0;font-family: Arial, sans-serif;")
        person_name = QLabel(self.meetdata["person_name"])
        person_name.setStyleSheet(f"color:{parent.FONT_COLOR};font-size:13px;border:0;font-family: Arial, sans-serif;")

        meet_date =QLabel(str(self.meetdata["create_date"]))
        meet_date.setStyleSheet(f"color:{parent.FONT_COLOR};font-size:13px;border:0;font-family: Arial, sans-serif;font-weight:bold;")

        top_layout.addWidget(Meet_Header,0,Qt.AlignLeft)
        bottom_layout.addWidget(person_name)
        bottom_layout.addSpacing(800)
        bottom_layout.addWidget(frm_name,0,Qt.AlignRight)
        right_box.addWidget(meet_date,0,Qt.AlignCenter)

        left_box.addLayout(top_layout)
        left_box.addLayout(bottom_layout)
        todo_area_content_layout.addLayout(left_box)
        
        todo_area_content_layout.addLayout(right_box)
        self.layout.addWidget(todo_area_content)
    def mouseDoubleClickEvent(self, event):
        # Çift tıklama olayını burada yakalıyoruz
        self.parent_class.Meet_Details(self.meetdata["_id"])

class Frm_Based_Report_Detail():
    def __init__(self,date,tablo=QTableWidget,menu_id=None,main_class=None):
        self.menu_id = menu_id
        self.tablo = tablo
        self.date = date
        self.main_class = main_class
        self.sqlparts=[{
                            '$lookup':{
                                'from':'person_list',
                                'localField':'person_id',
                                'foreignField': '_id',
                                'as':'person_name'
                            }
                        },
                        {
                            '$unwind':{
                                'path':'$person_name',
                                'preserveNullAndEmptyArrays':True
                            }
                        },
                        {
                            "$project": {
                                "person_id": 1, 
                                "user_id":1,
                                "year-month":{"$dateToString":{"format":"%Y-%m-%d","date":"$create_date"}},
                                "create_date":1,
                                "person_name":"$person_name.fullname",
                                "person_mail":"$person_name.mail",
                                "person_frm_id":"$person_name.frm_id",
                                "cst_header":1
                            }
                        },
                        {
                            '$lookup':{
                                'from':'users_data',
                                'localField':'user_id',
                                'foreignField': '_id',
                                'as':'user_inf'
                            }
                        },
                        {
                            '$unwind':{
                                'path':'$user_inf',
                                'preserveNullAndEmptyArrays':True
                            }
                        },
                        {
                            "$project": {
                                "person_id": 1, 
                                "user_id":1,
                                "year-month":1,
                                "create_date":1,
                                "person_name":1,
                                "person_mail":1,
                                "person_frm_id":1,
                                "cst_header":1,
                                "real_name":"$user_inf.real_name",
                                "ws_id":"$user_inf.workspace_id"

                            }
                        },
                        {
                            '$lookup':{
                                'from':'workspace_list',
                                'localField':'ws_id',
                                'foreignField': '_id',
                                'as':'ws_inf'
                            }
                        },
                        {
                            '$unwind':{
                                'path':'$ws_inf',
                                'preserveNullAndEmptyArrays':True
                            }
                        },
                        {
                            "$project": {
                                "person_id": 1, 
                                "user_id":1,
                                "year-month":1,
                                "create_date":1,
                                "person_name":1,
                                "person_mail":1,
                                "person_frm_id":1,
                                "cst_header":1,
                                "real_name":1,
                                "ws_id":1,
                                "ws_name":"$ws_inf.name",
                                "ws_parent":"$ws_inf.parent"
                            }
                        },
                        {
                            '$lookup':{
                                'from':'frm_list',
                                'localField':'person_frm_id',
                                'foreignField': '_id',
                                'as':'frm_inf'
                            }
                        },
                        {
                            '$unwind':{
                                'path':'$frm_inf',
                                'preserveNullAndEmptyArrays':True
                            }
                        },
                        {
                            "$project": {
                                "person_id": 1, 
                                "user_id":1,
                                "year-month":1,
                                "create_date":1,
                                "person_name":1,
                                "person_mail":1,
                                "person_frm_id":1,
                                "cst_header":1,
                                "real_name":1,
                                "ws_id":1,
                                "ws_name":1,
                                "ws_parent":1,
                                "frm_name":"$frm_inf.name"
                            }
                        }]
    def click_table(self,row,col):
        sql = self.sqlparts.copy()
        sql.append({"$match":
                    {
                        "$expr": {
                            "$eq": [{ "$month": "$create_date" }, col+1]
                        }
                    }})
        if self.menu_id is None or self.menu_id == 1:
            sql.insert(0,{"$match":{"user_id":self.main_class.user_id}})
        if self.main_class.user_perm == "Müdür":
            sql.append({"$match":{"$or":[{"ws_id":self.main_class.user_workspace_id},{"ws_parent":self.main_class.user_workspace_id}]}})
        if self.date > 1 :
                        sql.append({
                            "$match":{
                                "$expr": {
                                 "$eq": [{ "$year": "$create_date" }, self.date]
                                 }
                                }
                        })
        visit_count = False
        if row == 0:
            for i in range(self.tablo.rowCount()):
                item = self.tablo.item(i,col)
                if item != None:
                    visit_count = True
                    break
        else: 
            item = self.tablo.item(row,col)
            if item != None:
                visit_count = True
            if self.menu_id == 1:
                person_id = self.tablo.verticalHeaderItem(row)
                person_id = person_id.data(Qt.UserRole)
                sql.append({ "$match":{"person_id":int(person_id)}}) 
            elif self.menu_id == 3:
                user_id = self.tablo.verticalHeaderItem(row)
                user_id = user_id.data(Qt.UserRole)
                sql.insert(0,{"$match":{"user_id":user_id}})
            else:
                frm_id = self.tablo.verticalHeaderItem(row)
                frm_id = frm_id.data(Qt.UserRole)
                sql.append({ "$match":{"person_frm_id":int(frm_id)}})                      

        if visit_count: # Eğer o ay içerisinde herhangi bir ziyaret varsa panelde detayları gösterecek
            self.main_class.ReportDetailsTable(sql,self.menu_id)
    def click_vheader(self,row):
        visit_count = False
        for i in range(self.tablo.columnCount()):
            item = self.tablo.item(row,i)
            if item != None:
                visit_count = True
                break
        if visit_count: # Eğer o ay içerisinde herhangi bir ziyaret varsa panelde detayları gösterecek
            sql = self.sqlparts.copy()
            if self.menu_id == 1:
                person_id = self.tablo.verticalHeaderItem(row)
                person_id = person_id.data(Qt.UserRole)
                sql.append({ "$match":{"person_id":int(person_id)}}) 
            elif self.menu_id == 3:
                user_id = self.tablo.verticalHeaderItem(row)
                user_id = user_id.data(Qt.UserRole)
                sql.insert(0,{"$match":{"user_id":user_id}})
            else:
                frm_id = self.tablo.verticalHeaderItem(row)
                frm_id = frm_id.data(Qt.UserRole)
                sql.append({ "$match":{"person_frm_id":int(frm_id)}})
            if self.menu_id is None or self.menu_id== 1:
                sql.insert(0,{"$match":{"user_id":self.main_class.user_id}})
            if self.main_class.user_perm == "Müdür":
                sql.append({"$match":{"$or":[{"ws_id":self.main_class.user_workspace_id},{"ws_parent":self.main_class.user_workspace_id}]}})
            if self.date > 1 :
                            sql.append({
                                "$match":{
                                    "$expr": {
                                    "$eq": [{ "$year": "$create_date" }, self.date]
                                    }
                                    }
                            })
            self.main_class.ReportDetailsTable(sql,self.menu_id)

class Person_Based_Report_Detail():
    def __init__(self,date,tablo=QTableWidget,main_class=None):
        self.tablo = tablo
        self.date = date
        self.main_class = main_class
        self.sqlparts=[{
                        '$lookup':{
                                'from':'person_list',
                                'localField':'person_id',
                                'foreignField': '_id',
                                'as':'person_name'
                            }
                        },
                        {
                            '$unwind':{
                                'path':'$person_name',
                                'preserveNullAndEmptyArrays':True
                            }
                        },
                        {
                            "$project": {
                                "person_id": 1, 
                                "user_id":1,
                                "year-month":{"$dateToString":{"format":"%Y-%m-%d","date":"$create_date"}},
                                "create_date":1,
                                "person_name":"$person_name.fullname",
                                "person_mail":"$person_name.mail",
                                "person_frm_id":"$person_name.frm_id",
                                "cst_header":1
                            }
                        },
                        {
                            '$lookup':{
                                'from':'users_data',
                                'localField':'user_id',
                                'foreignField': '_id',
                                'as':'user_inf'
                            }
                        },
                        {
                            '$unwind':{
                                'path':'$user_inf',
                                'preserveNullAndEmptyArrays':True
                            }
                        },
                        {
                            "$project": {
                                "person_id": 1, 
                                "user_id":1,
                                "year-month":1,
                                "create_date":1,
                                "person_name":1,
                                "person_mail":1,
                                "person_frm_id":1,
                                "cst_header":1,
                                "real_name":"$user_inf.real_name",
                                "ws_id":"$user_inf.workspace_id"

                            }
                        },
                        {
                            '$lookup':{
                                'from':'workspace_list',
                                'localField':'ws_id',
                                'foreignField': '_id',
                                'as':'ws_inf'
                            }
                        },
                        {
                            '$unwind':{
                                'path':'$ws_inf',
                                'preserveNullAndEmptyArrays':True
                            }
                        },
                        {
                            "$project": {
                                "person_id": 1, 
                                "user_id":1,
                                "year-month":1,
                                "create_date":1,
                                "person_name":1,
                                "person_mail":1,
                                "person_frm_id":1,
                                "cst_header":1,
                                "real_name":1,
                                "ws_id":1,
                                "ws_name":"$ws_inf.name",
                                "ws_parent":"$ws_inf.parent"
                            }
                        },
                        {
                            '$lookup':{
                                'from':'frm_list',
                                'localField':'person_frm_id',
                                'foreignField': '_id',
                                'as':'frm_inf'
                            }
                        },
                        {
                            '$unwind':{
                                'path':'$frm_inf',
                                'preserveNullAndEmptyArrays':True
                            }
                        },
                        {
                            "$project": {
                                "person_id": 1, 
                                "user_id":1,
                                "year-month":1,
                                "create_date":1,
                                "person_name":1,
                                "person_mail":1,
                                "person_frm_id":1,
                                "cst_header":1,
                                "real_name":1,
                                "ws_id":1,
                                "ws_name":1,
                                "ws_parent":1,
                                "frm_name":"$frm_inf.name"
                            }
                        }]

class SuperAdminMenu(QMainWindow):
    def __init__(self,THEME_ID,user,user_id,ws_id,perm):
        super().__init__()
        self.THEME_ID = THEME_ID
        self.user_id = user_id
        self.user_workspace_id = ws_id
        self.resize(800, 800)
        self.cp = Cipher()
        self.user_perm = perm
        theme_colors = theme_color(THEME_ID)
        theme_colors.set_color()
        self.WIN_COLOR,self.PANEL_COLOR,self.BORDER_COLOR,self.OS_RED,self.ON_HOVER_OS_RED,self.GREEN,self.ON_HOVER_GREEN,self.ORANGE,self.FONT_COLOR = theme_colors.get_color()
        MenuPanel = None
        
        load_dotenv(dotenv_path='db_inf.env')
        uri = os.getenv('SERVER_URI')
        client = MongoClient(uri, tlsCAFile=certifi.where())
        database = client["VisitPanelDB"]
        self.workspacedb = database["workspace_list"]
        self.usersdatadb = database["users_data"]
        self.frmdb = database["frm_list"]
        self.prsdb = database["person_list"]
        self.conversations = database['conversations']
        self.todos = database['meet_to_do']
        self.contentpanel = None
        self.content_child_frame = None
        

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(f"background-color:{self.WIN_COLOR};border-radius:10px")
        self.setAttribute(Qt.WA_TranslucentBackground)
        title_bar = CustomTitleBar(self.WIN_COLOR,self.FONT_COLOR,self.BORDER_COLOR,self.OS_RED,self)
        self.setMenuWidget(title_bar)

        central_widget = QWidget()
        central_widget.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.PANEL_COLOR};border-top-right-radius:0px;border-top-left-radius:0px")
        self.setCentralWidget(central_widget)

        self.layout = QHBoxLayout(central_widget)
        self.layout.setContentsMargins(0,0,0,0)
        if perm in ("Admin","Personel","Müdür"):    
            MenuPanel = QFrame()
            MenuPanel.setFixedSize(200, self.frameGeometry().height()-60)
            MenuPanel.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius:25px;border-bottom-left-radius:0px;border-top-left-radius:0px")

            self.Menu_layout = QVBoxLayout(MenuPanel)
            self.Menu_layout.setContentsMargins(0,0,0,0)

            # Takvim , Öğretmen Bazlı Rapor, Okul Bazlı Rapor , Ayarlar , Öğretmen Ekleme Talebi
            spacer = QSpacerItem(1, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)  # Yatay, Dikey
            self.Menu_layout.addItem(spacer) 

            self.normal_button = f"""QPushButton{{
                                    border: 1px solid {self.BORDER_COLOR};
                                    border-radius:5px;
                                    color:white;
                                    font-weight: bold;
                                    font-family: Arial;
                                    text-align:center;
                                    background-color:{self.OS_RED};
                                    }}
                                    QPushButton:Hover{{background-color:{self.ON_HOVER_OS_RED};}}"""

            self.btnstyle = f"""QPushButton{{
                                    background-color:{self.PANEL_COLOR};
                                    font-weight: bold;
                                    font-family:Arial;
                                    border: 1px solid {self.BORDER_COLOR};
                                    border-left:0;
                                    border:0;
                                    color:{self.FONT_COLOR};
                                    font-size:18px;
                                    text-align:left;}}
                                    QPushButton:hover{{
                                    background-color:{self.BORDER_COLOR};
                                    }}"""
            
            self.clicked_btnstyle = f"""QPushButton{{
                                    background-color:{self.OS_RED};
                                    font-weight: bold;
                                    font-family:Arial;
                                    border: 1px solid {self.BORDER_COLOR};
                                    border-left:0;
                                    border:0;
                                    color:white;
                                    font-size:18px;
                                    text-align:left;}}
                                    QPushButton:hover{{
                                    background-color:{self.ON_HOVER_OS_RED};
                                    }}"""
            
            self.combobox_style = f"""QComboBox{{
                                                    border: 1px solid {self.BORDER_COLOR}; 
                                                    background-color:{self.PANEL_COLOR};
                                                    border-radius:5px; 
                                                    color:{self.FONT_COLOR}}}

                                                    QComboBox QAbstractItemView {{
                                                    border: 1px solid {self.BORDER_COLOR};
                                                    border-radius:5px;
                                                    background-color:{self.WIN_COLOR};
                                                    color:{self.FONT_COLOR};}}

                                                    QComboBox::drop-down:button{{
                                                    border-left: 1px solid {self.BORDER_COLOR};
                                                    border-right: 1px solid {self.BORDER_COLOR};
                                                    border-bottom-right-radius:2px;
                                                    border-top-right-radius:2px;
                                                    background-color:{self.WIN_COLOR};}}

                                                    QComboBox::drop-down:hover{{
                                                    background-color:{self.ON_HOVER_OS_RED};
                                                    }}
                                                    QScrollBar:vertical {{
                                                            width: 3px;                 /* Kaydırma çubuğunun genişliği */
                                                            margin: 0px 0px 0px 0px; 
                                                            border: 0;
                                                            background-color:white;
                                                        }}

                                                        QScrollBar::handle:vertical {{
                                                            background-color: {self.OS_RED};         /* Kaydırıcı (handle) rengi */
                                                            min-height: 20px;            /* Kaydırıcının minimum yüksekliği */
                                                            border: 0 ;
                                                        }}
                                                        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                                                            background: none;            /* Ok işaretlerinin görünmemesi için */
                                                        }}

                                                        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                                                            background: none;            /* Ok işaretlerinin görünmemesi için */
                                                        }}

                                                    """
            if self.user_perm in ("Admin","Müdür"):
                admin_menu = QPushButton(" Admin Menü")
                admin_menu.setStyleSheet(self.btnstyle)
                admin_menu.setFixedSize(MenuPanel.width()-5,50)
                admin_menu.setObjectName("1")
                admin_menu.clicked.connect(self.left_menu_click) 

                preports = QPushButton(" Personel Raporları")
                preports.setStyleSheet(self.btnstyle)
                preports.setFixedSize(MenuPanel.width()-5,50)
                preports.setObjectName("2")
                preports.clicked.connect(self.left_menu_click) 

            reports = QPushButton(" Kişisel Raporlar")
            reports.setStyleSheet(self.btnstyle)
            reports.setFixedSize(MenuPanel.width()-5,50)
            reports.setObjectName("3")
            reports.clicked.connect(self.left_menu_click) 

            todos = QPushButton(" Toplantılarım")
            todos.setStyleSheet(self.btnstyle)
            todos.setFixedSize(MenuPanel.width()-5,50)
            todos.setObjectName("4")
            todos.clicked.connect(self.left_menu_click) 

            ayarlar = QPushButton(" Ayarlar")
            ayarlar.setStyleSheet(self.btnstyle)
            ayarlar.setFixedSize(MenuPanel.width()-5,50)
            ayarlar.setObjectName("9")
            # self.ayarlar.clicked.connect(self.ayarlar_click) 

            
            if self.user_perm in("Admin","Müdür") :
                self.Menu_layout.addWidget(admin_menu)
                self.Menu_layout.addWidget(preports)
            self.Menu_layout.addWidget(todos)
            self.Menu_layout.addWidget(reports)
            self.Menu_layout.addWidget(ayarlar,0,Qt.AlignBottom)

            spacer = QSpacerItem(1, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)  # Yatay, Dikey
            self.Menu_layout.addItem(spacer) 
            self.layout.addWidget(MenuPanel,0,QtCore.Qt.AlignLeft)
        else:
            MenuPanel = QFrame()
            MenuPanel.setFixedSize(350, 150)
            MenuPanel.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius:25px")

            massagelbl = QLabel()
            massagelbl.setText("Giriş Yetkiniz\nBulunmamaktadır.")
            massagelbl.setStyleSheet(f"border:0 ; background-color:{self.WIN_COLOR}; font-weight: bold;font-family:Arial;font-size: 18px;color:{self.FONT_COLOR}")
            massagelbl.setAlignment(QtCore.Qt.AlignCenter)

            perm_denied_layout = QVBoxLayout(MenuPanel)
            perm_denied_layout.addWidget(massagelbl,0,Qt.AlignCenter)
            self.layout.addWidget(MenuPanel,0,QtCore.Qt.AlignCenter)
            QTimer.singleShot(5000, self.close)


# ---------------------------------------------------------------------- Ortak Fonksiyonlar -----------------------------------------------------------------------------------------
    def reset_buttons(self):
        for item in range(self.Menu_layout.count()):
            widget = self.Menu_layout.itemAt(item).widget()
            if isinstance(widget,QPushButton):
                widget.setStyleSheet(self.btnstyle)
    
    def left_menu_click(self): # Sol Panel UI
        self.reset_buttons()
        buton_id = int(self.sender().objectName())
        self.sender().setStyleSheet(self.clicked_btnstyle)
        
        if self.contentpanel is not None:
            for child in self.contentpanel.findChildren(QWidget):
                child.deleteLater()
            self.contentpanel.deleteLater()

        self.contentpanel = QFrame()
        frame_x = self.frameGeometry().width()-205
        frame_y = self.frameGeometry().height()-60

        self.contentpanel.setFixedSize(frame_x,frame_y)
        self.contentpanel.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius:25px;border-bottom-right-radius:0px;border-top-right-radius:0px")
        
        self.content_child_frame = QFrame(self.contentpanel)
        self.content_child_frame.setFixedSize(frame_x,frame_y-39)
        self.content_child_frame.setStyleSheet(f"border-radius:0; border-bottom-left-radius:25px;")
        self.content_child_frame.move(0,39)
        self.content_child_frame.show()
        
            
        
        if buton_id == 1:#Admin Paneli
            btn_menu = Content_Button_Menu(self.contentpanel,self)
            btn_menu.new_btn("Workspaces",self.workspace_list_panel)
            btn_menu.new_btn("Yetkiler",self.list_users_panel)
            btn_menu.new_btn("Firmalar",self.frm_list_panel)
            btn_menu.new_btn("Kişiler",self.frm_prsn_list_panel)
            btn_menu.new_btn("Tara",self.scan_locale_user_data)
        elif buton_id == 2:#Personel Raporları
            btn_menu = Content_Button_Menu(self.contentpanel,self)
            btn_menu.new_btn("Firma Bazlı",lambda:self.frm_based_report_panel(2))
            btn_menu.new_btn("Personel Bazlı",lambda:self.person_based_report_panel(2))
        elif buton_id == 3:#Kişisel Raporlar
            btn_menu = Content_Button_Menu(self.contentpanel,self)
            btn_menu.new_btn("Firma Bazlı",self.frm_based_report_panel)
            btn_menu.new_btn("Kiş Bazlı",self.person_based_report_panel)
        elif buton_id == 4:#Toplantılarım
            btn_menu = Content_Button_Menu(self.contentpanel,self)
            btn_menu.new_btn("Liste",self.my_meets)
            btn_menu.new_btn("Yaklaşan",self.upcoming_meets)
            btn_menu.new_btn("Yapılacak",self.self_todos)
        Menu_layout = QVBoxLayout(self.contentpanel)
        Menu_layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.contentpanel,0,QtCore.Qt.AlignRight)
    
    def bildirim(self,text):
        notification.notify(
                    title='Admin Panel Bildirim',
                    message=text,
                    app_name='OS_VPanel',
                )

    def Style_Editable_Text(self,width:int,height:int,load_screen):
        dikey_layout= QVBoxLayout()

        yatay_layout_3 = QHBoxLayout()
        normal_btn = f"""QPushButton{{
                                  border: 1px solid {self.BORDER_COLOR};
                                  border-radius:0;
                                  color:{self.FONT_COLOR};
                                  font-size:13px;
                                  font-family: Arial;
                                  text-align:center;
                                  background-color:{self.PANEL_COLOR};
                                  }}
                                  QPushButton:Hover{{background-color:{self.BORDER_COLOR};}}"""
        font_size_list=["8","9","10","11","12","14","16","18","20","22","24","26","28","36","48","72"]
        font_size = QComboBox()
        font_size.setObjectName("Font-Size")
        font_size.setStyleSheet(self.combobox_style)
        font_size.setFixedSize(40,30)
        font_size.addItems(font_size_list)
        font_size.currentTextChanged.connect(self.MeetTextStyleFunction)
        
        bold_button = QPushButton("𝗞")
        bold_button.setObjectName("Kalın")
        bold_button.setStyleSheet(normal_btn)
        bold_button.setFixedSize(30,30)
        bold_button.clicked.connect(self.MeetTextStyleFunction)

        italic_button = QPushButton("𝙏")
        italic_button.setObjectName("Italic")
        italic_button.setStyleSheet(normal_btn)
        italic_button.setFixedSize(30,30)
        italic_button.clicked.connect(self.MeetTextStyleFunction)

        underline_button = QPushButton("A̲")
        underline_button.setObjectName("underline")
        underline_button.setStyleSheet(normal_btn)
        underline_button.setFixedSize(30,30)
        underline_button.clicked.connect(self.MeetTextStyleFunction)

        bg_color_picker_frame = QFrame()
        bg_color_picker_frame.setFixedSize(40,30)
        bg_color_picker_frame.setStyleSheet(f"""QFrame{{
                                  border: 1px solid {self.BORDER_COLOR};
                                  border-radius:0;
                                  color:{self.FONT_COLOR};
                                  background-color:{self.PANEL_COLOR};
                                  }}
                                  QFrame:Hover{{background-color:{self.BORDER_COLOR};}}""")   
        bg_color_picker_frame_layout = QHBoxLayout()
        bg_color_picker_frame_layout.setContentsMargins(0,0,0,0)
        
        #---------------------------------------------- Yazı arka plan rengi Belirleme--------------------------------------------------------------------

        bg_color_picker_frame_dikey_layout_1 = QVBoxLayout()

        bg_color_picker_frame_label_1 = QPushButton("🖊️")
        bg_color_picker_frame_label_1.setStyleSheet(f"""QPushButton{{border:0;border-radius:0;background-color:{self.PANEL_COLOR};font-weight: bold;}}QPushButton:Hover{{background-color:{self.BORDER_COLOR};}}""")
        bg_color_picker_frame_label_1.setObjectName("FontBackground")
        bg_color_picker_frame_label_1.clicked.connect(self.MeetTextStyleFunction)

        bg_color_picker_frame_label_2 = QLabel()
        bg_color_picker_frame_label_2.setFixedHeight(8)
        bg_color_picker_frame_label_2.setStyleSheet(f"border:0;border-radius:0;background-color:'yellow';margin:1px;")
        bg_color_picker_frame_label_2.setObjectName("ColorLabel")
        
        bg_color_picker_frame_dikey_layout_1.addWidget(bg_color_picker_frame_label_1)
        bg_color_picker_frame_dikey_layout_1.addWidget(bg_color_picker_frame_label_2)

        bg_color_picker_frame_dikey_layout_2 = QVBoxLayout()

        bg_color_picker_frame_button_1 = QPushButton("▼")
        bg_color_picker_frame_button_1.setStyleSheet(f"""QPushButton{{
                                                    border:0;
                                                    border-left: 1px solid {self.BORDER_COLOR};
                                  border-radius:0;
                                  color:{self.FONT_COLOR};
                                  background-color:{self.PANEL_COLOR};
                                  }}
                                  QPushButton:Hover{{background-color:{self.BORDER_COLOR};}}""")
        bg_color_picker_frame_button_1.setFixedSize(10,27)
        bg_color_picker_frame_button_1.setObjectName("ColorPicker")
        bg_color_picker_frame_button_1.clicked.connect(self.MeetTextStyleFunction)

        bg_color_picker_frame_dikey_layout_2.addWidget(bg_color_picker_frame_button_1)

        bg_color_picker_frame_layout.addLayout(bg_color_picker_frame_dikey_layout_1)
        bg_color_picker_frame_layout.addLayout(bg_color_picker_frame_dikey_layout_2)

        bg_color_picker_frame_layout.setSpacing(0)
        bg_color_picker_frame.setLayout(bg_color_picker_frame_layout)

        #---------------------------------------------- Yazı Rengi Belirleme--------------------------------------------------------------------
        font_color_picker_frame = QFrame()
        font_color_picker_frame.setFixedSize(40,30)
        font_color_picker_frame.setStyleSheet(f"""QFrame{{
                                  border: 1px solid {self.BORDER_COLOR};
                                  border-radius:0;
                                  color:{self.FONT_COLOR};
                                  background-color:{self.PANEL_COLOR};
                                  }}
                                  QFrame:Hover{{background-color:{self.BORDER_COLOR};}}""")   
        font_color_picker_frame_layout = QHBoxLayout()
        font_color_picker_frame_layout.setContentsMargins(0,0,0,0)
        

        font_color_picker_frame_dikey_layout_1 = QVBoxLayout()

        font_color_picker_frame_label_1 = QPushButton("A")
        font_color_picker_frame_label_1.setStyleSheet(f"""QPushButton{{border:0;border-radius:0;background-color:{self.PANEL_COLOR};color:{self.FONT_COLOR}}}QPushButton:Hover{{background-color:{self.BORDER_COLOR};}}""")
        font_color_picker_frame_label_1.setObjectName("FontColor")
        font_color_picker_frame_label_1.clicked.connect(self.MeetTextStyleFunction)

        font_color_picker_frame_label_2 = QLabel()
        font_color_picker_frame_label_2.setFixedHeight(8)
        font_color_picker_frame_label_2.setStyleSheet(f"border:0;border-radius:0;background-color:{self.FONT_COLOR};margin:1px;")
        font_color_picker_frame_label_2.setObjectName("ColorLabel2")
        
        font_color_picker_frame_dikey_layout_1.addWidget(font_color_picker_frame_label_1)
        font_color_picker_frame_dikey_layout_1.addWidget(font_color_picker_frame_label_2)

        font_color_picker_frame_dikey_layout_2 = QVBoxLayout()

        font_color_picker_frame_button_1 = QPushButton("▼")
        font_color_picker_frame_button_1.setStyleSheet(f"""QPushButton{{
                                                    border:0;
                                                    border-left: 1px solid {self.BORDER_COLOR};
                                  border-radius:0;
                                  color:{self.FONT_COLOR};
                                  background-color:{self.PANEL_COLOR};
                                  }}
                                  QPushButton:Hover{{background-color:{self.BORDER_COLOR};}}""")
        font_color_picker_frame_button_1.setFixedSize(10,27)
        font_color_picker_frame_button_1.setObjectName("ColorPickerFont")
        font_color_picker_frame_button_1.clicked.connect(self.MeetTextStyleFunction)

        font_color_picker_frame_dikey_layout_2.addWidget(font_color_picker_frame_button_1)

        font_color_picker_frame_layout.addLayout(font_color_picker_frame_dikey_layout_1)
        font_color_picker_frame_layout.addLayout(font_color_picker_frame_dikey_layout_2)

        font_color_picker_frame_layout.setSpacing(0)
        font_color_picker_frame.setLayout(font_color_picker_frame_layout)
        #-----------------------------------------------------------------------------------------------------------------------------------------

        create_note_btn = QPushButton("Kaydet")
        create_note_btn.setStyleSheet(self.normal_button) 
        create_note_btn.setFixedSize(50,30)
        create_note_btn.setObjectName(load_screen)
        create_note_btn.clicked.connect(self.new_meet)


        yatay_layout_3.setSpacing(2)
        # yatay_layout_3.setAlignment(Qt.AlignLeft)
        yatay_layout_3.addWidget(font_size)
        yatay_layout_3.addWidget(bold_button)
        yatay_layout_3.addWidget(italic_button)
        yatay_layout_3.addWidget(underline_button)
        yatay_layout_3.addWidget(bg_color_picker_frame)
        yatay_layout_3.addWidget(font_color_picker_frame,0,Qt.AlignLeft)
        yatay_layout_3.addWidget(create_note_btn,0,Qt.AlignRight)

        yatay_layout_4 = QHBoxLayout()
        yatay_layout_4.setObjectName("TexboxArea")
        meet_text_area = QTextEdit()
        meet_text_area.setObjectName("MeetTextArea")
        meet_text_area.setStyleSheet(f"border:1px solid {self.BORDER_COLOR};color:{self.FONT_COLOR};font-family: Arial;background-color:{self.PANEL_COLOR};border-radius:0;")
        meet_text_area.setFixedSize(width,height-150)
        yatay_layout_4.addWidget(meet_text_area)

        dikey_layout.addLayout(yatay_layout_3)
        dikey_layout.addLayout(yatay_layout_4)
        # ----------------------------------------------------------------------- TO DO -------------------------------------------
        dikey_scroll_area=QScrollArea()
        dikey_scroll_area.setStyleSheet(f"""QScrollBar:vertical {{
                                    width: 5px;                 /* Kaydırma çubuğunun genişliği */
                                    margin: 0px 0px 0px 0px; 
                                    border: 1;
                                    background-color:white;
                                }}

                                QScrollBar::handle:vertical {{
                                    background-color: {self.OS_RED};         /* Kaydırıcı (handle) rengi */
                                    min-height: 20px;            /* Kaydırıcının minimum yüksekliği */
                                    border: 0 ;
                                }}
                                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                                    background: none;            /* Ok işaretlerinin görünmemesi için */
                                }}

                                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                                    background: none;            /* Ok işaretlerinin görünmemesi için */
                                }}
                                QScrollBar:horizontal {{
                                    height: 0;                 /* Kaydırma çubuğunun genişliği */
                                    margin: 0px 0px 0px 0px; 
                                    border: 0;
                                    background-color:white;
                                }}
                                QScrollArea{{border:0;}}""")
        dikey_scroll_area.setFixedSize(width,150)
        dikey_scroll_area.setWidgetResizable(True)
        todo_area = QWidget()
        todo_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        todo_area.setStyleSheet("border:0;")
        todo_area.setFixedWidth(width-5)
        todo_area_layout = QVBoxLayout(todo_area)
        meet = self.findChildren(QFrame,"editmeet")
        if meet:
            meet = meet[0]
            meet = meet.property("meet_id")
            for todolist in self.todos.find({"meet_id":meet}):
                todo_area_layout.addWidget(self.to_do_template(todolist["item_state"],todolist["item_text"],todolist["reminder_date"],"add_to_do",todolist["_id"]))

        todo_area_layout.addWidget(self.to_do_template(False,"",datetime.today(),"new_to_do",0))
        
        dikey_scroll_area.setWidget(todo_area)
        dikey_layout.addWidget(dikey_scroll_area)
        
        return dikey_layout
    
    def to_do_template(self,checked:bool,text:str,date:datetime,widget_name:str,obj_id:int):

        todo_area =QWidget()
        todo_area.setFixedHeight(45)
        todo_area.setObjectName(widget_name)
        todo_area.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};border-radius:0;")

        yatay_layout =QHBoxLayout()
        chech_box =QCheckBox()
        if checked:
            chech_box.setCheckState(Qt.Checked)
        else:
            chech_box.setCheckState(Qt.Unchecked)  
        chech_box.setFixedSize(26,26)
        chech_box.setStyleSheet(f"""
            QCheckBox {{
                border: 1px solid {self.BORDER_COLOR};
                background-color: {self.PANEL_COLOR};
                width: 26px;
                height: 26px;
                border-radius: 13px;  /* Yuvarlak yapma */
                padding: 0px;
                outline: none;
            }}
            QCheckBox:checked {{
                background-color: {self.GREEN};  /* Tıklanmış durumda yeşil arka plan */
            }}
            QCheckBox:indicator {{
                width: 100%;
                height: 100%;
                border-radius: 50%;
            }}
        """)
        
        todo_textbox = self.common_items(QLineEdit,"new_to_do","Enter To Do Text..(Optional)",200,25)
        if widget_name == "new_to_do":
            todo_textbox.returnPressed.connect(self.add_to_do)
        todo_textbox.setText(text)
        
        date_picker = QDateEdit()
        
        date_picker.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.PANEL_COLOR};border-radius: 5px;color:{self.FONT_COLOR};")
        date_picker.setFixedSize(100,25)
        if widget_name == "new_to_do":
            date_picker.setDate(QDate.currentDate())
        elif widget_name == "add_to_do":
            date_picker.setDate(date)
        else:
            date_picker.setDate(QDate(date.year, date.month, date.day))

        
        yatay_layout.addWidget(chech_box)
        yatay_layout.addWidget(todo_textbox,0,Qt.AlignLeft)
        yatay_layout.addWidget(date_picker,0,Qt.AlignRight)

        if widget_name != "new_to_do":
            meet = self.findChildren(QFrame,"editmeet")
            delete_btn =QPushButton("X")
            delete_btn.setStyleSheet(f""" QPushButton{{ border:0;font-size:13px;font-weight:bold;background-color:{self.WIN_COLOR};color:{self.FONT_COLOR}}}QPushButton:hover{{background-color:{self.PANEL_COLOR};border:1px solid {self.BORDER_COLOR}}}""")
            delete_btn.setFixedSize(25,25)
            if meet: 
                delete_btn.setProperty("_id",obj_id)
                meet = meet[0]
                meet = meet.property("meet_id")
                delete_btn.clicked.connect(self.delete_todo)     
                user_control = self.conversations.find_one({"_id":meet})
                if self.user_id == user_control["user_id"]:
                    yatay_layout.addWidget(delete_btn)
            else:
                delete_btn.clicked.connect(lambda:delete_btn.parent().deleteLater())
                yatay_layout.addWidget(delete_btn)
        todo_area.setLayout(yatay_layout)
        return(todo_area)

    def delete_todo (self):
        button = self.sender()
        todo_id = button.property("_id")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Maddeyi Silmek İstediğinize Emin Misiniz?")
        msg.setWindowTitle("Bilgi Mesajı")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)       
        resp = msg.exec()
        if resp == 1024:
            self.todos.delete_one({"_id":todo_id})
            button.parent().deleteLater()

    def add_to_do(self):
        if self.sender().parent().objectName() == "new_to_do":
            check_state = self.sender().parent().findChildren(QCheckBox)[0].checkState()
            todo_text = self.sender().parent().findChildren(QLineEdit)[0].text()
            reminder_date_text = self.sender().parent().findChildren(QDateEdit)[0].date()
            is_checked = check_state == Qt.Checked
            meet = self.findChildren(QFrame,"editmeet")
            if meet:
                meet = meet[0]
                meet = meet.property("meet_id")
                data_id = self.todos.find().sort({"_id": -1}).limit(1).to_list()
                if data_id:
                    data_id = int(data_id[0]['_id'])+1
                else:
                    data_id = 1
                is_checked = check_state == Qt.Checked
                self.todos.insert_one({"_id":data_id,"meet_id":meet,"item_text":todo_text,"item_state":is_checked,"reminder_date":datetime(reminder_date_text.year(),reminder_date_text.month(),reminder_date_text.day())})
                todo_area = self.to_do_template(is_checked,todo_text,reminder_date_text,"add_to_do",data_id)
            else:
                todo_area = self.to_do_template(is_checked,todo_text,reminder_date_text,"add_to_do",0)
            parent_layout = self.sender().parent().parent().layout()
            parent_layout.addWidget(todo_area)
            self.sender().parent().deleteLater()
            parent_layout.addWidget(self.to_do_template(False,"",datetime.today(),"new_to_do",0))
            
    def common_items(self,widget:QWidget,widget_name:str,widget_text:str,widget_width:int,widget_height:int):#Panelde Tanımladığımız standart widgetları sürekli aynı kodları yazamamak için oluşturuldu
        if widget == QLineEdit:
            textbox = QLineEdit()
            textbox.setFixedSize(widget_width,widget_height)
            textbox.setObjectName(widget_name)
            textbox.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.PANEL_COLOR};border-radius: 5px;color:{self.FONT_COLOR};")
            textbox.setPlaceholderText(widget_text)
            return textbox
        elif widget == QComboBox:
            combobox = QComboBox()
            combobox.setStyleSheet(self.combobox_style)
            combobox.setFixedSize(widget_width, widget_height)
            combobox.setObjectName(widget_name)
            combobox.insertItem(0,widget_text,userData=0)
            combobox.setCurrentIndex(0)
            return combobox
        elif widget == QPushButton:
            btn = QPushButton(widget_text)
            btn.setObjectName(widget_name)
            btn.setStyleSheet(self.normal_button)
            btn.setFixedSize(widget_width,widget_height)
            return btn
    
    def Create_Table_Set_Items(self,widget:QWidget,widget_text,widget_width:int,widget_height:int,parent,set_bg=None):
        if widget == QTableWidget:
            tablo = CustomTableWidget(1,len(widget_text)-1,parent)
            tablo_style = f"""QTableWidget{{
                                border-radius:0;
                                color:{self.FONT_COLOR};
                                background-color: {self.PANEL_COLOR};
                                }}
                                QScrollBar:horizontal {{
                                    height: 5px;                 /* Kaydırma çubuğunun genişliği */
                                    margin: 0px 0px 0px 0px; 
                                    border: 1;
                                    background-color:white;
                                }}

                                QScrollBar::handle:horizontal {{
                                    background-color: {self.OS_RED};         /* Kaydırıcı (handle) rengi */
                                    min-height: 20px;            /* Kaydırıcının minimum yüksekliği */
                                    border: 0 ;
                                }}
                                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                                    background: none;            /* Ok işaretlerinin görünmemesi için */
                                }}

                                QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {{
                                    background: none;            /* Ok işaretlerinin görünmemesi için */
                                }}
                                QScrollBar:vertical {{
                                    width: 5px;                 /* Kaydırma çubuğunun genişliği */
                                    margin: 0px 0px 0px 0px; 
                                    border: 1;
                                    background-color:white;
                                }}

                                QScrollBar::handle:vertical {{
                                    background-color: {self.OS_RED};         /* Kaydırıcı (handle) rengi */
                                    min-height: 20px;            /* Kaydırıcının minimum yüksekliği */
                                    border: 0 ;
                                }}
                                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                                    background: none;            /* Ok işaretlerinin görünmemesi için */
                                }}

                                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                                    background: none;            /* Ok işaretlerinin görünmemesi için */
                                }}
                                QHeaderView {{
                                    background-color: {self.WIN_COLOR};
                                    border-radius:0;
                                }}
                                QHeaderView::section {{
                                background-color: {self.BORDER_COLOR}; 
                                color: {self.FONT_COLOR};                           
                                font-weight: bold;          
                                border: 1px solid black;
                                border-top:0;
                                border-radius:0;   
                                text-align: center;          
                            }}"""
            tablo.setStyleSheet(tablo_style)
            tablo.horizontalHeader().setVisible(False)
            # tablo.verticalHeader().setVisible(False)
            tablo.setFixedSize(widget_width,widget_height)
            tablo.move(0,0)
            if parent is not None:
                tablo.show()
            return tablo
        elif widget == QTableWidgetItem:
            item = QTableWidgetItem(widget_text)
            item.setTextAlignment(Qt.AlignCenter) 
            if widget_width == 0 or set_bg:
                item.setBackground(QColor(self.BORDER_COLOR))
            item.setFlags(QtCore.Qt.ItemIsEnabled) 
            parent.setItem(widget_width,widget_height,item) 
            
    def custom_color_common_items(self,widget:QWidget,widget_name:str,widget_text:str,widget_width:int,widget_height:int,color1:str,color2:str):# Buda Aynı widgetların hover renklerini değiştirdiğimiz versyonları
        if widget == QPushButton:
            style = f"""QPushButton{{
                                    border:0;
                                    border-right: 1px solid {self.BORDER_COLOR};
                                    border-radius:0;
                                    color:{self.FONT_COLOR};
                                    font-weight: bold;
                                    font-family: Arial;
                                    text-align:center;
                                    background-color:{color1};
                                    }}
                                    QPushButton:Hover{{background-color:{color2};}}"""
            btn = QPushButton(widget_text)
            btn.setObjectName(widget_name)
            btn.setStyleSheet(style)
            btn.setFixedSize(widget_width,widget_height)
            return btn

    def set_combobox_items(self,set_combobox:QComboBox,process:str,self_combobox:QComboBox):#Bu adındanda analaşıalcağı gibi comboboboxlara sürekli tanımladığımız itemler için kullanılıyor ve combo değişince diğer combo itemlerini değiştirmede de kullanılıyor
        match process:
            case "Ws_Parent_Set": # Ana Çalışma Alanlarını Listeler
                set_combobox.clear()
                set_combobox.addItem("Select Any Workspace",userData = -1)
                set_combobox.addItem("Main Workspace",userData = 0)
                for item in self.workspacedb.find({'parent':0}):
                    set_combobox.addItem(item['name'],userData = item['_id'])
            case "Self_Ws_Child": # Kişinin Tanımlı olduğu çalışma alanının alt gruplarını listeler
                set_combobox.clear()
                set_combobox.addItem("Select Any Workspace",userData = -1)
                for item in self.workspacedb.aggregate([{"$match":{"$or":[{'parent':self.user_workspace_id},{"_id":self.user_workspace_id}]}}]):
                    set_combobox.addItem(item['name'],userData = item['_id'])
            case "Select_Ws_Set_Ws": # seçilen üst çalışma alanına göre alt çalışma alanını listeler
                set_combobox.clear()
                ws_parent = self_combobox.itemData(self_combobox.currentIndex())
                set_combobox.addItem("Select Any Workspace",userData = -1)
                for item in self.workspacedb.find({"parent":ws_parent}):
                    set_combobox.addItem(item["name"],userData = item['_id'])
            case "Select_Ws_Set_Frm":#Seçilen çalışma alanına göre firmaları listeler
                set_combobox.clear()
                ws = self_combobox.itemData(self_combobox.currentIndex())
                set_combobox.addItem("Select Any Workspace",userData = 0)
                for item in self.frmdb.find({"workspace_id":ws}):
                    set_combobox.addItem(item["name"],userData = item['_id'])
            case "Self_Firm": # kişinin tanımlı olduğu çalışma alanına ait firmaları listeler alt alandaysa üst kısmı üst çalışma alanındaysa alt alanları listeler
                set_combobox.clear()
                set_combobox.addItem("Select Any Firm",userData = 0)
                parent_ws = self.workspacedb.find_one({"_id":self.user_workspace_id})
                if parent_ws["parent"] == 0:
                    ws_ids = []
                    for child_ws in self.workspacedb.find({"parent":self.user_workspace_id}):
                        ws_ids.append(child_ws["_id"])
                    ws_ids.append(self.user_workspace_id)
                    for item in self.frmdb.find({"workspace_id": {"$in": ws_ids}}):
                        set_combobox.addItem(item["name"],userData = item['_id'])
                else:
                    for item in self.frmdb.aggregate([{"$match":{"$or":[{"workspace_id":self.user_workspace_id},{"workspace_id":parent_ws["parent"]}]}}]):
                        set_combobox.addItem(item["name"],userData = item['_id'])
            case "Select_Frm_Set_Person": # Seçilen Firmaya ait kişileri listeler
                set_combobox.clear()
                set_combobox.addItem("Select Any Person",userData = 0)
                Frm_id = self_combobox.itemData(self_combobox.currentIndex())
                for item in self.prsdb.find({"frm_id":Frm_id}):
                    set_combobox.addItem(item["fullname"] +" - "+item["mail"],userData = item['_id'])

    def Data_Control_Func(self,item:QWidget,process:str): # Kullanıcıdan gelen veri kontrol ettirme fonksiyonu
        match process:
            case "Space":
                if item.count(" ") != len(item) and item[0] != " ":
                    return True
                else:
                    return False
            case "Mail":
                if item.count(" ") == 0 and item.count("@") ==1 and item.count(".") > 0 :
                    return True
                else:
                    return False

# ---------------------------------------------------------------------- Ortak Fonksiyonlar -----------------------------------------------------------------------------------------

# ---------------------------------------------------------------------- TO DO PANEL ----------------------------------------------------------------------------------
    def change_state_todos(self):
        checkbox = self.sender()
        doc_id = checkbox.property("_id")
        is_checked = checkbox.checkState() == Qt.Checked
        self.todos.update_one({"_id":doc_id},{"$set":{"item_state":is_checked}})
    
    def self_todos(self):
        if self.content_child_frame is not None:
            for child in self.content_child_frame.findChildren(QWidget):
                child.deleteLater()
        if self.content_child_frame.layout():
            QWidget().setLayout(self.content_child_frame.layout())

        VFuncLayout = QVBoxLayout()
        dikey_scroll_area=QScrollArea()
        dikey_scroll_area.setStyleSheet(f"""QScrollBar:vertical {{
                                    width: 5px;                 /* Kaydırma çubuğunun genişliği */
                                    margin: 0px 0px 0px 0px; 
                                    border: 1;
                                    background-color:white;
                                }}

                                QScrollBar::handle:vertical {{
                                    background-color: {self.OS_RED};         /* Kaydırıcı (handle) rengi */
                                    min-height: 20px;            /* Kaydırıcının minimum yüksekliği */
                                    border: 0 ;
                                }}
                                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                                    background: none;            /* Ok işaretlerinin görünmemesi için */
                                }}

                                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                                    background: none;            /* Ok işaretlerinin görünmemesi için */
                                }}
                                QScrollBar:horizontal {{
                                    height: 0;                 /* Kaydırma çubuğunun genişliği */
                                    margin: 0px 0px 0px 0px; 
                                    border: 0;
                                    background-color:white;
                                }}
                                QScrollArea{{border:0;}}""")
        dikey_scroll_area.setFixedSize(self.content_child_frame.width()-12,self.content_child_frame.height()-20)
        dikey_scroll_area.setWidgetResizable(True)
        todo_area = QWidget()
        todo_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        todo_area.setStyleSheet("border:0;")
        todo_area_layout = QVBoxLayout(todo_area)
        todo_area_layout.setContentsMargins(0,0,0,0)
        sql =[ {
                    '$lookup':{
                        'from':'conversations',
                        'localField':'meet_id',
                        'foreignField': '_id',
                        'as':'meet'
                    }
                },
                {
                    '$unwind':{
                        'path':'$meet',
                        'preserveNullAndEmptyArrays':True
                    }
                },
                {'$project':{
                    '_id':1,
                    'meet_id':1,
                    'item_text':1,
                    'item_state':1,
                    'date':{"$dateToString":{"format":"%Y-%m-%d","date":"$reminder_date"}},
                    'user_id':'$meet.user_id',
                    'meet_date':{"$dateToString":{"format":"%Y-%m-%d","date":'$meet.create_date'}},
                    'meet_header':'$meet.cst_header'
                }},
                {'$match':{'user_id':self.user_id,'item_state':False}}]
        for i in self.todos.aggregate(sql):
            todo_item = TodoItem(i, parent=self)  # Her bir item için TodoItem widget'ı oluşturuyoruz
            todo_area_layout.addWidget(todo_item)
        dikey_scroll_area.setWidget(todo_area)
        VFuncLayout.addWidget(dikey_scroll_area)
        VFuncLayout.addSpacing(20)
        self.content_child_frame.setLayout(VFuncLayout)
# ---------------------------------------------------------------------- TO DO PANEL ----------------------------------------------------------------------------------
# ---------------------------------------------------------------------------- NEW MEET ---------------------------------------------------------------------------------------------
    def New_Meet_Menu(self):
        Frame = self.content_child_frame.findChildren(QFrame,"new_meet_menu")
        if Frame:
            Frame= Frame[0]
            Frame.deleteLater()     
        Frame = QFrame(self.content_child_frame)
        Frame.setFixedSize(self.content_child_frame.width(),self.content_child_frame.height())   
        Frame.setObjectName("new_meet_menu")
        dikey_layout = QVBoxLayout()
        
        btn_menu_layout =QHBoxLayout()
        btn_menu_layout.setContentsMargins(0,0,0,0)
        btn_menu_layout.setSpacing(0)

        back_btn = self.custom_color_common_items(QPushButton,"back_btn","<",35,34,self.WIN_COLOR,self.PANEL_COLOR)
        back_btn.clicked.connect(lambda:Frame.deleteLater())
        btn_menu_layout.addWidget(back_btn,0,Qt.AlignLeft)
        yatay_layout_1 = QHBoxLayout()
        frame_x = (self.contentpanel.width()-20)/2

        frm_list = self.common_items(QComboBox,"frm_list","Select Any Firm",frame_x,25)
        person_list = self.common_items(QComboBox,"person_list","First Select Workspace",frame_x,25)

        self.set_combobox_items(frm_list,"Self_Firm",frm_list)
        frm_list.currentIndexChanged.connect(lambda :self.set_combobox_items(person_list,"Select_Frm_Set_Person",frm_list))

        yatay_layout_1.addWidget(frm_list)
        yatay_layout_1.addWidget(person_list)

        frm_list.move(0,0)

        yatay_layout_2 = QHBoxLayout()

        meet_header = self.common_items(QLineEdit,"meet_header","Enter Meet Header..",frame_x+100,25)

        date_picker = QDateEdit()
        date_picker.setDate(QDate.currentDate())
        date_picker.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.PANEL_COLOR};border-radius: 5px;color:{self.FONT_COLOR};")
        date_picker.setObjectName("Date_Picker")
        date_picker.setFixedHeight(25)

        yatay_layout_2.addWidget(meet_header)
        yatay_layout_2.addWidget(date_picker)

        yatay_layout_3= self.Style_Editable_Text(self.contentpanel.width()-20,550,"New_Meet")
        dikey_layout.addLayout(btn_menu_layout)
        dikey_layout.addLayout(yatay_layout_1)
        dikey_layout.addLayout(yatay_layout_2)
        dikey_layout.addLayout(yatay_layout_3)
        Frame.setLayout(dikey_layout)

        Frame.show()
    
    def new_meet(self):# Toplantıyı veritabanına kaydeder
        button_name = self.sender().objectName()
        if button_name == "New_Meet":
                textbox = self.content_child_frame.findChildren(QTextEdit,"MeetTextArea")[0]
                person_id = self.content_child_frame.findChildren(QComboBox,"person_list")[0]
                meet_header = self.content_child_frame.findChildren(QLineEdit,"meet_header")[0].text()
                person_id = person_id.itemData(person_id.currentIndex())
                date_picker = self.content_child_frame.findChildren(QDateEdit,"Date_Picker")[0]

                if person_id > 0:
                    if meet_header.count(" ") == len(meet_header) or meet_header[0] == " ":
                        self.bildirim("Toplantı başlığı boş olamaz veya boşluk ile başlayamaz!!")
                    else:
                        data = {"_id":None,"user_id":None,"person_id":None,"cst_header":None,"file_data":None,"create_date":None,"file_create_date":None}
                        data_id = self.conversations.find().sort({"_id": -1}).limit(1).to_list()
                        if data_id:
                            data_id = int(data_id[0]['_id'])+1
                        else:
                            data_id = 1
                        meet_date = date_picker.date()
                        meet_date_obj = datetime(meet_date.year(),meet_date.month(),meet_date.day())
                        data["_id"]=data_id
                        data["user_id"] = self.user_id
                        data["person_id"]=person_id
                        data["cst_header"]=meet_header
                        data["file_data"]= textbox.toHtml()
                        data["create_date"]=meet_date_obj
                        data["file_create_date"]=datetime.now()
                        self.conversations.insert_one(data)
                        meet = self.findChildren(QWidget,"add_to_do")
                        if meet:
                            for item in meet:
                                data = {"_id":None,"meet_id":None,"item_text":None,"item_state":None,"reminder_date":None}
                                todoid = self.todos.find().sort({"_id": -1}).limit(1).to_list()
                                if todoid:
                                    todoid = int(todoid[0]['_id'])+1
                                else:
                                    todoid = 1
                                data["_id"]=todoid
                                data["meet_id"] = data_id
                                for item_child in item.children():
                                    if isinstance(item_child, QCheckBox):
                                        is_checked = item_child.checkState() == Qt.Checked
                                        data["item_state"] = is_checked
                                    elif isinstance(item_child, QLineEdit):
                                        data["item_text"] = item_child.text()
                                    elif isinstance(item_child, QDateEdit):
                                        date = item_child.date()
                                        data["reminder_date"] = datetime(date.year(),date.month(),date.day())
                                self.todos.insert_one(data)

                        self.bildirim("Toplantı Oluşturulmuştur!!")
                        self.my_meets()
                        
                else:
                    self.bildirim("Lütfen Bir Kişi seçiniz")
        elif button_name == "Edit_Text":     
            textbox = self.findChildren(QTextEdit,"MeetTextArea")[0]
            meet_id = self.findChildren(QFrame,"editmeet")[0]
            meet_id = meet_id.property("meet_id") 
            textbox = textbox.toHtml()
            self.conversations.update_one({"_id":meet_id},{"$set":{"file_data":textbox}})
            meet = self.findChildren(QWidget,"add_to_do")
            if meet:
                for item in meet:
                    data ={"_id":None,"item_text":None,"item_state":None,"reminder_date":None}
                    for item_child in item.children():
                        if isinstance(item_child, QCheckBox):
                            is_checked = item_child.checkState() == Qt.Checked
                            data["item_state"] = is_checked
                        elif isinstance(item_child, QLineEdit):
                            data["item_text"] = item_child.text()
                        elif isinstance(item_child, QDateEdit):
                            date = item_child.date()
                            data["reminder_date"] = datetime(date.year(),date.month(),date.day())
                        elif isinstance(item_child, QPushButton):
                            todoid = item_child.property("_id")
                            data["_id"] = todoid
                    self.todos.update_one({"_id":data["_id"]},{"$set":{"item_text":data["item_text"],"item_state":data["item_state"],"reminder_date":data["reminder_date"]}})
            self.bildirim("Toplantı Notu Güncellendi!!")
        
    def MeetTextStyleFunction(self):#Seçilen still işlemini uygulayan fonksiyon
        process = self.sender().objectName()

        textbox = self.findChildren(QTextEdit,"MeetTextArea")[0]
        cursor = textbox.textCursor()
        fmt = QTextCharFormat()
        normal_btn = f"""QPushButton{{
                                  border: 1px solid {self.BORDER_COLOR};
                                  border-radius:0;
                                  color:{self.FONT_COLOR};
                                  font-family: Arial;
                                  font-size:13px;
                                  text-align:center;
                                  background-color:{self.PANEL_COLOR};
                                  }}
                                  QPushButton:Hover{{background-color:{self.BORDER_COLOR};}}"""
        clicked_btn = f"""
                        border: 1px solid {self.BORDER_COLOR};
                        border-radius:0;
                        color:{self.FONT_COLOR};
                        font-family: Arial;
                        font-size:13px;
                        text-align:center;
                        background-color:{self.BORDER_COLOR};
                                  """
        match process:
            case "Kalın":
                if cursor.charFormat().fontWeight() == QFont.Bold:
                    fmt.setFontWeight(QFont.Normal)
                    self.sender().setStyleSheet(normal_btn)
                else:
                    fmt.setFontWeight(QFont.Bold)
                    self.sender().setStyleSheet(clicked_btn)
            case "Italic":
                if cursor.charFormat().fontItalic():
                    self.sender().setStyleSheet(normal_btn)
                else:
                    self.sender().setStyleSheet(clicked_btn)
                fmt.setFontItalic(not cursor.charFormat().fontItalic())
            case "underline":
                if cursor.charFormat().fontUnderline():
                    self.sender().setStyleSheet(normal_btn)
                else:
                    self.sender().setStyleSheet(clicked_btn)
                fmt.setFontUnderline(not cursor.charFormat().fontUnderline())
            case "ColorPicker":
                color = QtWidgets.QColorDialog.getColor()
                if color.isValid():
                    color_area = self.findChildren(QLabel,"ColorLabel")[0]
                    color_area.setStyleSheet(f"border:0;border-radius:0;background-color:{color.name()};margin:1px;")
                    fmt.setBackground(QColor(color.name()))
                    button = self.findChildren(QPushButton,"FontBackground")[0]
                    button.setStyleSheet(f"border:0;border-radius:0;background-color:{self.BORDER_COLOR};font-weight: bold;")
            case "FontBackground":
                current_format = cursor.charFormat()
                brush = current_format.background()
                color_area = self.findChildren(QLabel,"ColorLabel")[0]
                button = self.sender()
                if  brush.style() == Qt.NoBrush or brush.color() == Qt.transparent:
                    color = color_area.palette().color(QPalette.Window).name()
                    fmt.setBackground(QColor(color))
                    button.setStyleSheet(f"border:0;border-radius:0;background-color:{self.BORDER_COLOR};font-weight: bold;")
                else:
                    color = color_area.palette().color(QPalette.Window).name()
                    fmt.setBackground(QBrush(Qt.transparent))
                    button.setStyleSheet(f"""QPushButton{{border:0;border-radius:0;background-color:{self.PANEL_COLOR};font-weight: bold;}}QPushButton:Hover{{background-color:{self.BORDER_COLOR};}}""")
            case "ColorPickerFont":
                color = QtWidgets.QColorDialog.getColor()
                if color.isValid():
                    color_area = self.findChildren(QLabel,"ColorLabel2")[0]
                    color_area.setStyleSheet(f"border:0;border-radius:0;background-color:{color.name()};margin:1px;")
                    fmt.setForeground(QColor(color.name()))
            case "FontColor":
                color_area = self.findChildren(QLabel,"ColorLabel2")[0]
                color = color_area.palette().color(QPalette.Window).name()
                fmt.setForeground(QColor(color))
            case "Font-Size":
                font = fmt.font()
                font.setPointSize(int(self.sender().currentText()))
                fmt.setFont(font)
        cursor.mergeCharFormat(fmt)
        textbox.setTextCursor(cursor)
# ---------------------------------------------------------------------------- NEW MEET ---------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------  MEET ---------------------------------------------------------------------------------------------
    def my_meets(self):
        tablo = self.content_child_frame.findChildren(QTableWidget,"My_Meets")
        if tablo:
            tablo= tablo[0]
            tablo.deleteLater()

        frame_x = self.contentpanel.width()
        frame_y = self.contentpanel.height()
        header = ['Kişi Adı','Mail','Firma','Toplantı Başlığı','Toplantı Tarihi','Toplantı Oluşturma Tarihi','']
        tablo =self.Create_Table_Set_Items(QTableWidget,header,frame_x,frame_y-60,self.content_child_frame)
        tablo.setObjectName("My_Meets")
        tablo.move(0,0)
        for col in range(len(header)):
            if col == 0:
                item = QTableWidgetItem(header[col])
                item.setTextAlignment(Qt.AlignCenter) 
                tablo.setVerticalHeaderItem(0,item)
            else:
                self.Create_Table_Set_Items(QTableWidgetItem,header[col],0,col-1,tablo)
        add_btn = self.custom_color_common_items(QPushButton,"add","Yeni",75,29,self.GREEN,self.ON_HOVER_GREEN)
        add_btn.clicked.connect(self.New_Meet_Menu)
        tablo.setCellWidget(0,5,add_btn)
        sql = [
            {
                '$lookup':{
                    'from':'person_list',
                    'localField':'person_id',
                    'foreignField': '_id',
                    'as':'person_inf'
                }
            },
            {
                '$unwind':{
                    'path':'$person_inf',
                    'preserveNullAndEmptyArrays':True
                }
            },
            {
                '$project': {
                    "_id": 1,
                    "user_id":1,
                    "person_id":1,
                    "cst_header": 1,
                    "create_date": 1,
                    "file_create_date":1,
                    "person_name": "$person_inf.fullname",
                    "person_mail": "$person_inf.mail",
                    "person_frm_id":"$person_inf.frm_id",
                    }
            },
            {
                '$lookup':{
                    'from':'frm_list',
                    'localField':'person_frm_id',
                    'foreignField': '_id',
                    'as':'frm_inf'
                }
            },
            {
                '$unwind':{
                    'path':'$frm_inf',
                    'preserveNullAndEmptyArrays':True
                }
            },
            {
                '$project': {
                    "_id": 1,
                    "user_id":1,
                    "person_id":1,
                    "cst_header": 1,
                    "create_date": {"$dateToString":{"format":"%Y-%m-%d","date":"$create_date"}},
                    "file_create_date":{"$dateToString":{"format":"%Y-%m-%d","date":"$file_create_date"}},
                    "person_name": 1,
                    "person_mail": 1,
                    "person_frm_id":1,
                    "frm_name":"$frm_inf.name"
                    }
            },
            {'$match':{"user_id":int(self.user_id)}}]
        for db_item in self.conversations.aggregate(sql):
            row = tablo.rowCount()
            tablo.insertRow(row)
            item = QTableWidgetItem(db_item["person_name"])
            item.setTextAlignment(Qt.AlignCenter) 
            tablo.setVerticalHeaderItem(row,item)
            self.Create_Table_Set_Items(QTableWidgetItem,db_item["person_mail"],row,0,tablo)
            self.Create_Table_Set_Items(QTableWidgetItem,db_item["frm_name"],row,1,tablo)
            self.Create_Table_Set_Items(QTableWidgetItem,db_item["cst_header"],row,2,tablo)
            self.Create_Table_Set_Items(QTableWidgetItem,db_item["create_date"],row,3,tablo)
            self.Create_Table_Set_Items(QTableWidgetItem,db_item["file_create_date"],row,4,tablo)
            update_btn = self.common_items(QPushButton,"update","Güncelle",75,29)
            update_btn.setProperty("_id",db_item["_id"])
            update_btn.clicked.connect(self.Meet_Details)
            tablo.setCellWidget(row,5,update_btn)
        tablo.resizeColumnsToContents()
        header=None
    
    def upcoming_meets(self):
        if self.content_child_frame is not None:
            for child in self.content_child_frame.findChildren(QWidget):
                child.deleteLater()
        if self.content_child_frame.layout():
            QWidget().setLayout(self.content_child_frame.layout())

        VFuncLayout = QVBoxLayout()
        dikey_scroll_area=QScrollArea()
        dikey_scroll_area.setStyleSheet(f"""QScrollBar:vertical {{
                                    width: 5px;                 /* Kaydırma çubuğunun genişliği */
                                    margin: 0px 0px 0px 0px; 
                                    border: 1;
                                    background-color:white;
                                }}

                                QScrollBar::handle:vertical {{
                                    background-color: {self.OS_RED};         /* Kaydırıcı (handle) rengi */
                                    min-height: 20px;            /* Kaydırıcının minimum yüksekliği */
                                    border: 0 ;
                                }}
                                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                                    background: none;            /* Ok işaretlerinin görünmemesi için */
                                }}

                                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                                    background: none;            /* Ok işaretlerinin görünmemesi için */
                                }}
                                QScrollBar:horizontal {{
                                    height: 0;                 /* Kaydırma çubuğunun genişliği */
                                    margin: 0px 0px 0px 0px; 
                                    border: 0;
                                    background-color:white;
                                }}
                                QScrollArea{{border:0;}}""")
        dikey_scroll_area.setFixedSize(self.content_child_frame.width()-12,self.content_child_frame.height()-20)
        dikey_scroll_area.setWidgetResizable(True)
        box_area = QWidget()
        box_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        box_area.setStyleSheet("border:0;")
        box_area_layout = QVBoxLayout(box_area)
        box_area_layout.setContentsMargins(0,0,0,0)
        yesterday_date = datetime.today() - timedelta(days=1)  # 1 gün geriye git
        yesterday_date = datetime(yesterday_date.year, yesterday_date.month, yesterday_date.day)
        sql = [
            {
                '$lookup':{
                    'from':'person_list',
                    'localField':'person_id',
                    'foreignField': '_id',
                    'as':'person_inf'
                }
            },
            {
                '$unwind':{
                    'path':'$person_inf',
                    'preserveNullAndEmptyArrays':True
                }
            },
            {
                '$project': {
                    "_id": 1,
                    "user_id":1,
                    "person_id":1,
                    "cst_header": 1,
                    "create_date": 1,
                    "file_create_date":1,
                    "person_name": "$person_inf.fullname",
                    "person_mail": "$person_inf.mail",
                    "person_frm_id":"$person_inf.frm_id",
                    }
            },
            {
                '$lookup':{
                    'from':'frm_list',
                    'localField':'person_frm_id',
                    'foreignField': '_id',
                    'as':'frm_inf'
                }
            },
            {
                '$unwind':{
                    'path':'$frm_inf',
                    'preserveNullAndEmptyArrays':True
                }
            },
            {
                '$project': {
                    "_id": 1,
                    "user_id":1,
                    "cst_header": 1,
                    "create_date": {"$dateToString":{"format":"%Y-%m-%d","date":"$create_date"}},
                    "person_name": 1,
                    "frm_name":"$frm_inf.name"
                    }
            },
            {
                '$match':{
                    "user_id":int(self.user_id),
                    'create_date':{'$gt': yesterday_date.strftime("%Y-%m-%d")}
                    }
            },
            {
                '$sort': {
                    'create_date': 1 
                }
            }]
        for i in self.conversations.aggregate(sql):
            meet_item = Upcome_Meets_Item(i, parent=self)  
            box_area_layout.addWidget(meet_item)
        dikey_scroll_area.setWidget(box_area)
        VFuncLayout.addWidget(dikey_scroll_area)
        VFuncLayout.addSpacing(20)
        self.content_child_frame.setLayout(VFuncLayout)
# ----------------------------------------------------------------------------  MEET ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------- Raporlar ---------------------------------------------------------------------------------------------
    def person_based_report_panel(self,menu_id = None):
        if self.content_child_frame is not None:
            for child in self.content_child_frame.findChildren(QWidget):
                child.deleteLater()
        if self.content_child_frame.layout():
            QWidget().setLayout(self.content_child_frame.layout()) 

        dikey_layout = QVBoxLayout(self.content_child_frame)
        yatay_layout = QHBoxLayout()
        yatay_layout.setAlignment(Qt.AlignTop)
        frame_x = (self.contentpanel.width()-20)/2

        if menu_id is None:
            frm_list = self.common_items(QComboBox,"frm_list","Select Any Firm",frame_x,25)
            self.set_combobox_items(frm_list,"Self_Firm",frm_list)
            frm_list.currentIndexChanged.connect(self.person_based_report)
            yatay_layout.addWidget(frm_list)

        else:
            main_ws  = self.common_items(QComboBox,"ws_list","Select Any Staff",frame_x,25)
            self.set_combobox_items(main_ws,"Ws_Parent_Set",main_ws)
            main_ws.removeItem(1)
            main_ws.currentIndexChanged.connect(self.staff_based_report)
            yatay_layout.addWidget(main_ws)


        date_db = self.common_items(QComboBox,"date","Select Any Date",frame_x,25)
        date_db.clear()
        sql=[{
            "$project":{
                "year":{"$year":"$create_date"}
                }
            },
            {
                "$group":{
                    "_id":None,
                    "min_year":{"$min":"$year"},
                    "max_year":{"$max":"$year"}
                    }
            }]
        min_year=0
        max_year=0
        for i in self.conversations.aggregate(sql):
            min_year=i["min_year"]
            max_year=i["max_year"]
        
        if min_year == 0 or max_year == 0:
            date_db.addItem("Rapor Verileri Bulunmamaktadır.",userData=0)
        else:
            if min_year == max_year:
                date_db.addItem(str(min_year),userData=int(min_year))
            else:
                date_db.addItem("Tüm Zamanlar",userData=1)
                for i in range(min_year,max_year+1):
                    date_db.addItem(str(i),userData=int(i)) 
                if menu_id is None:
                    date_db.currentIndexChanged.connect(self.person_based_report)
                else:
                    date_db.currentIndexChanged.connect(self.staff_based_report)
        
        date_db.setFixedWidth(frame_x)
        yatay_layout.addWidget(date_db)
        dikey_layout.addLayout(yatay_layout)
        dikey_layout.addSpacerItem(QSpacerItem(self.contentpanel.width(), self.contentpanel.height()-100, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.content_child_frame.setLayout(dikey_layout)
    
    def person_based_report(self):
        tablo = self.content_child_frame.findChildren(QTableWidget,"person_based")
        if tablo:
            tablo= tablo[0]
            tablo.deleteLater()
        
        frm_id = self.content_child_frame.findChildren(QComboBox,"frm_list")[0]
        frm_id = frm_id.itemData(frm_id.currentIndex())
        date = self.content_child_frame.findChildren(QComboBox,"date")[0]
        date = date.itemData(date.currentIndex())
        if frm_id > 0 and date > 0: 
            sql = [
                    {
                        '$lookup':{
                            'from':'person_list',
                            'localField':'person_id',
                            'foreignField': '_id',
                            'as':'person_name'
                        }
                    },
                    {
                        '$unwind':{
                            'path':'$person_name',
                            'preserveNullAndEmptyArrays':True
                        }
                    },
                    {
                        "$match":{
                            "user_id":int(self.user_id)
                            }
                    },
                    {
                        "$project": {
                            "person_id": 1, 
                            "year":{"$year":"$create_date"},
                            "month":{"$month":"$create_date"},
                            "person_name":"$person_name.fullname",
                            "person_mail":"$person_name.mail",
                            "person_frm_id":"$person_name.frm_id"
                        }
                    },
                    {
                        "$match":{
                            "person_frm_id":int(frm_id)
                            }
                    },
                    {
                        "$group":{
                            "_id":{"person_id":"$person_id","year":"$year","month":"$month","person_name":"$person_name","person_mail":"$person_mail"},
                            "visit_count":{"$sum":1}
                        }
                    },
                    {
                        "$project":{
                            "person_id":"$_id.person_id",
                            "person_name":"$_id.person_name",
                            "person_mail":"$_id.person_mail",
                            "year":"$_id.year",
                            "month":"$_id.month",
                            "visit_count":1,
                            "_id":0
                        }
                    },{"$sort":{"person_id":1}}]
            if date > 1:
                    sql.append({"$match":{"year":int(date)}})   
            header = ['Tam Adı',"Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]
            tablo = self.Create_Table_Set_Items(QTableWidget,header,self.contentpanel.width(),self.contentpanel.height()-110,self.content_child_frame)
            tablo.setObjectName("person_based")
            for i in range(tablo.columnCount()):
                tablo.setColumnWidth(i, 75)
            tablo.setEditTriggers(QTableWidget.NoEditTriggers)
            tablo.move(0,45)
            for col in range(len(header)):
                if col == 0:
                    item = QTableWidgetItem(header[col])
                    item.setTextAlignment(Qt.AlignCenter) 
                    tablo.setVerticalHeaderItem(0,item)
                else:
                    self.Create_Table_Set_Items(QTableWidgetItem,header[col],0,col-1,tablo)
            search_id = None
            for db_item in self.conversations.aggregate(sql):
                if search_id != db_item["person_id"]:
                    row = tablo.rowCount()
                    tablo.insertRow(row)
                    item = QTableWidgetItem(db_item["person_name"])
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setData(Qt.UserRole, db_item["person_id"])
                    tablo.setVerticalHeaderItem(row,item)
                    search_id = db_item["person_id"] 
                past_item = tablo.item(row,db_item['month']-1)
                if past_item is not None:
                    visit_num = int(past_item.text()) + db_item['visit_count']
                    self.Create_Table_Set_Items(QTableWidgetItem,str(visit_num),row,db_item["month"]-1,tablo,True)
                else:
                    self.Create_Table_Set_Items(QTableWidgetItem,str(db_item["visit_count"]),row,db_item["month"]-1,tablo,True)
            rp = Frm_Based_Report_Detail(date,tablo,1,self)
            tablo.verticalHeader().sectionDoubleClicked.connect(rp.click_vheader)
            tablo.cellDoubleClicked.connect(rp.click_table)

    def staff_based_report(self):
        tablo = self.content_child_frame.findChildren(QTableWidget,"staff_based")
        if tablo:
            tablo= tablo[0]
            tablo.deleteLater()
        ws_id = self.content_child_frame.findChildren(QComboBox,"ws_list")[0]
        ws_id = ws_id.itemData(ws_id.currentIndex())
        date = self.content_child_frame.findChildren(QComboBox,"date")[0]
        date = date.itemData(date.currentIndex())
        if ws_id > 0 and date > 0: 
            sql =[
                    {
                        '$lookup':{
                            'from':'users_data',
                            'localField':'user_id',
                            'foreignField': '_id',
                            'as':'user_inf'
                        }
                    },
                    {
                        '$unwind':{
                            'path':'$user_inf',
                            'preserveNullAndEmptyArrays':True
                        }
                    },
                    {
                        '$project':{
                            'user_id':1,
                            'user_name':'$user_inf.real_name',
                            'user_ws_id':'$user_inf.workspace_id',
                            "year":{"$year":"$create_date"},
                            "month":{"$month":"$create_date"},
                        }
                    },
                    {
                        '$lookup':{
                            'from':'workspace_list',
                            'localField':'user_ws_id',
                            'foreignField': '_id',
                            'as':'ws_inf'
                        }
                    },
                    {
                        '$unwind':{
                            'path':'$ws_inf',
                            'preserveNullAndEmptyArrays':True
                        }
                    },
                    {
                        '$project':{
                            'user_id':1,
                            'user_name':1,
                            'user_ws_id':1,
                            "year":1,
                            "month":1,
                            "user_ws_parent":"$ws_inf.parent"
                        }
                    },
                    {
                        "$match":{"$or":[
                            {"user_ws_id":ws_id},
                            {"user_ws_parent":ws_id}]
                            }
                    },
                    {
                        "$group":{
                            "_id":{"user_id":"$user_id","year":"$year","month":"$month","user_name":"$user_name"},
                            "visit_count":{"$sum":1}
                        }
                    },
                    {
                        "$project":{
                            "user_id":"$_id.user_id",
                            "user_name":"$_id.user_name",
                            "year":"$_id.year",
                            "month":"$_id.month",
                            "visit_count":1,
                            "_id":0
                        }
                    },{"$sort":{"user_id":1}}]
            if date > 1:
                    sql.append({"$match":{"year":int(date)}})     
            header = ['Tam Adı',"Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]
            tablo = self.Create_Table_Set_Items(QTableWidget,header,self.contentpanel.width(),self.contentpanel.height()-110,self.content_child_frame)
            tablo.setObjectName("staff_based")
            for i in range(tablo.columnCount()):
                tablo.setColumnWidth(i, 75)
            tablo.setEditTriggers(QTableWidget.NoEditTriggers)
            tablo.move(0,45)
            for col in range(len(header)):
                if col == 0:
                    item = QTableWidgetItem(header[col])
                    item.setTextAlignment(Qt.AlignCenter) 
                    tablo.setVerticalHeaderItem(0,item)
                else:
                    self.Create_Table_Set_Items(QTableWidgetItem,header[col],0,col-1,tablo)
            search_id = None
            for db_item in self.conversations.aggregate(sql):
                if search_id != db_item["user_id"]:
                    row = tablo.rowCount()
                    tablo.insertRow(row)
                    item = QTableWidgetItem(db_item["user_name"])
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setData(Qt.UserRole, db_item["user_id"])
                    tablo.setVerticalHeaderItem(row,item)
                    search_id = db_item["user_id"] 
                past_item = tablo.item(row,db_item['month']-1)
                if past_item is not None:
                    visit_num = int(past_item.text()) + db_item['visit_count']
                    self.Create_Table_Set_Items(QTableWidgetItem,str(visit_num),row,db_item["month"]-1,tablo,True)
                else:
                    self.Create_Table_Set_Items(QTableWidgetItem,str(db_item["visit_count"]),row,db_item["month"]-1,tablo,True)
            rp = Frm_Based_Report_Detail(date,tablo,3,self)
            tablo.verticalHeader().sectionDoubleClicked.connect(rp.click_vheader)
            tablo.cellDoubleClicked.connect(rp.click_table)
    
    def ReportDetailsTable(self,data,menu_id=None):
        MenuPanel = QFrame(self)
        MenuPanel.setFixedSize(self.width(),self.height()-50)
        MenuPanel.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius:0;border-left:0;border-bottom:0;")
        MenuPanel_lay = QVBoxLayout()
        MenuPanel_lay.setContentsMargins(0,0,0,0)
        MenuPanel_lay.setSpacing(0)
        btn_menu_lay = QHBoxLayout()
        back_btn = self.custom_color_common_items(QPushButton,"back_btn"," < ",35,35,self.WIN_COLOR,self.OS_RED)
        back_btn.clicked.connect(lambda:MenuPanel.deleteLater())
        btn_menu_lay.setAlignment(Qt.AlignTop)
        table_menu_lay = QHBoxLayout()
        header = ['Personel Adı','Çalışma Alanı','Firma Adı','Kişi Adı','Kişi Maili','Toplantı Başlığı','Toplantı Tarihi','Detay']
        if menu_id is None or menu_id == 1:
            for i in range(2):
                header.pop(0)

        tablo =self.Create_Table_Set_Items(QTableWidget,header,self.width(),MenuPanel.height()-35,None)
        
        for col in range(len(header)):
            if col == 0:
                item = QTableWidgetItem(header[col])
                item.setTextAlignment(Qt.AlignCenter) 
                tablo.setVerticalHeaderItem(0,item)
            else:
                self.Create_Table_Set_Items(QTableWidgetItem,header[col],0,col-1,tablo)
        sql_header=["real_name","ws_name",'frm_name',"person_name","person_mail","cst_header","year-month",""]
        if menu_id is None or menu_id == 1:
            for i in range(2):
                sql_header.pop(0)
        for db_item in self.conversations.aggregate(data):
                row = tablo.rowCount()
                tablo.insertRow(row)
               
                for header_item in range(len(sql_header)):
                    if header_item == 0:
                        item = QTableWidgetItem(db_item[sql_header[header_item]])
                        item.setTextAlignment(Qt.AlignCenter) 
                        tablo.setVerticalHeaderItem(row,item)
                    elif header_item == len(sql_header)-1:
                        detail_btn = self.common_items(QPushButton,"detail_btn","Detay",75,29)
                        detail_btn.setProperty("_id",db_item["_id"])
                        detail_btn.clicked.connect(self.Meet_Details)
                        tablo.setCellWidget(row,header_item-1,detail_btn)
                    else:
                        self.Create_Table_Set_Items(QTableWidgetItem,db_item[sql_header[header_item]],row,header_item-1,tablo)
        tablo.setEditTriggers(QTableWidget.NoEditTriggers)        
        tablo.resizeColumnsToContents()
        
        table_menu_lay.addWidget(tablo)
        btn_menu_lay.addWidget(back_btn,0,Qt.AlignLeft)
        MenuPanel_lay.addLayout(btn_menu_lay)
        MenuPanel_lay.addLayout(table_menu_lay)
        MenuPanel_lay.addSpacing(50)
        MenuPanel.setLayout(MenuPanel_lay)
        MenuPanel.move(0,37)
        MenuPanel.show()

    def Meet_Details(self,meet_id=None):
        MenuPanel = QFrame(self)
        MenuPanel.setFixedSize(self.width(),763)
        MenuPanel.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius:10px;border-top-left-radius:0px;border-top-right-radius:0px;border-top:0;")

        back_btn = QPushButton(" < ",MenuPanel)
        back_btn.setStyleSheet(f"""QPushButton{{
                                  border: 1px solid {self.BORDER_COLOR};
                                  border-bottom:0;
                                  border-top:0;
                                  border-radius:0;
                                  color:{self.FONT_COLOR};
                                  font-weight: bold;
                                  font-family: Arial;
                                  font-size:15px;
                                  text-align:center;
                                  background-color:{self.WIN_COLOR};
                                  }}
                                  QPushButton:Hover{{background-color:{self.OS_RED};}}""")
        back_btn.move(0,0)
        back_btn.setFixedSize(35,35)
        back_btn.show()
        back_btn.clicked.connect(lambda:back_btn.parentWidget().deleteLater())

        Content_Panel = QFrame(MenuPanel)
        Content_Panel.setFixedSize(MenuPanel.width(),MenuPanel.height()-35)
        Content_Panel.setObjectName("editmeet")
        
        Content_Panel.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius:10px;border-top-left-radius:0px;border-top-right-radius:0px;")
        Content_Panel.show()
        Content_Panel.move(0,35)
        if meet_id is False:
            button = self.sender()
            button_id = button.property("_id")  
        else:
            button_id = meet_id
        Content_Panel.setProperty("meet_id",button_id)
        conversation_text = self.conversations.find_one({"_id":button_id})
        if conversation_text['user_id'] == self.user_id:
            layout = self.Style_Editable_Text(Content_Panel.width()-20,Content_Panel.height()-100,"Edit_Text")
            Content_Panel.setLayout(layout)
            TextBox = Content_Panel.findChildren(QTextEdit,"MeetTextArea")[0]
            TextBox.setHtml(conversation_text["file_data"])
        else:
            meet_text_area = QTextEdit(Content_Panel)
            meet_text_area.setObjectName("MeetTextArea")
            meet_text_area.setStyleSheet(f"border:1px solid {self.BORDER_COLOR};color:{self.FONT_COLOR};font-family: Arial;background-color:{self.PANEL_COLOR};border-radius:0;")
            meet_text_area.setFixedSize(Content_Panel.width(),550)
            meet_text_area.show()
            meet_text_area.setReadOnly(True)
            meet_text_area.setHtml(conversation_text["file_data"])
            dikey_scroll_area=QScrollArea(Content_Panel)
            dikey_scroll_area.setStyleSheet(f"""QScrollBar:vertical {{
                                    width: 5px;                 /* Kaydırma çubuğunun genişliği */
                                    margin: 0px 0px 0px 0px; 
                                    border: 1;
                                    background-color:white;
                                }}

                                QScrollBar::handle:vertical {{
                                    background-color: {self.OS_RED};         /* Kaydırıcı (handle) rengi */
                                    min-height: 20px;            /* Kaydırıcının minimum yüksekliği */
                                    border: 0 ;
                                }}
                                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                                    background: none;            /* Ok işaretlerinin görünmemesi için */
                                }}

                                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                                    background: none;            /* Ok işaretlerinin görünmemesi için */
                                }}
                                QScrollBar:horizontal {{
                                    height: 0;                 /* Kaydırma çubuğunun genişliği */
                                    margin: 0px 0px 0px 0px; 
                                    border: 0;
                                    background-color:white;
                                }}
                                QScrollArea{{border:0;}}""")
            dikey_scroll_area.setFixedSize(Content_Panel.width(),150)
            dikey_scroll_area.setWidgetResizable(True)
            todo_area = QWidget(Content_Panel)
            todo_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            todo_area.setStyleSheet("border:0;")
            todo_area.setFixedWidth(Content_Panel.width()-10)
            todo_area_layout = QVBoxLayout(todo_area)
            for todolist in self.todos.find({"meet_id":button_id}):
                todo_area_layout.addWidget(self.to_do_template(todolist["item_state"],todolist["item_text"],todolist["reminder_date"],"add_to_do",todolist["_id"]))
            dikey_scroll_area.setWidget(todo_area)
            dikey_scroll_area.show()
            dikey_scroll_area.move(0,550)
        conversation_text=None
        
        MenuPanel.move(0,37)
        MenuPanel.show()

    def frm_based_report_panel(self,menu_id=None):
        if self.content_child_frame is not None:
            for child in self.content_child_frame.findChildren(QWidget):
                child.deleteLater()
        if self.content_child_frame.layout():
            QWidget().setLayout(self.content_child_frame.layout()) 

        dikey_layout = QVBoxLayout(self.content_child_frame)
        yatay_layout = QHBoxLayout()
        frame_x = (self.contentpanel.width()-20)/2

        date_db = self.common_items(QComboBox,"date","Select Any Date",frame_x,25)
        date_db.clear()
        sql=[{
            "$project":{
                "year":{"$year":"$create_date"}
                }
            },
            {
                "$group":{
                    "_id":None,
                    "min_year":{"$min":"$year"},
                    "max_year":{"$max":"$year"}
                    }
            }]
        min_year=0
        max_year=0
        for i in self.conversations.aggregate(sql):
            min_year=i["min_year"]
            max_year=i["max_year"]
        
        if min_year == 0 or max_year == 0:
            date_db.addItem("Rapor Verileri Bulunmamaktadır.",userData=0)
        else:
            if min_year == max_year:
                date_db.addItem("Select Any Date",userData=0)
                date_db.addItem(str(min_year),userData=int(min_year))
            else:
                date_db.addItem("Select Any Date",userData=0)
                date_db.addItem("Tüm Zamanlar",userData=1)
                for i in range(min_year,max_year+1):
                    date_db.addItem(str(i),userData=int(i)) 

        date_db.currentIndexChanged.connect(lambda:self.frm_based_report(menu_id))
        yatay_layout.setAlignment(Qt.AlignTop)
        yatay_layout.addWidget(date_db,0,Qt.AlignCenter)
        dikey_layout.addLayout(yatay_layout)
        dikey_layout.addSpacerItem(QSpacerItem(self.contentpanel.width(), self.contentpanel.height()-100, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.content_child_frame.setLayout(dikey_layout)

    def frm_based_report(self,menu_id=None):
        tablo = self.content_child_frame.findChildren(QTableWidget,"frm_based")
        frame_x = self.contentpanel.width()
        frame_y = self.contentpanel.height()
        if tablo:
            tablo= tablo[0]
            tablo.deleteLater()
        date = self.content_child_frame.findChildren(QComboBox,"date")[0]
        date = date.itemData(date.currentIndex())
        if date != 0:
            sql = [
                    {
                        '$lookup':{
                            'from':'person_list',
                            'localField':'person_id',
                            'foreignField': '_id',
                            'as':'person_name'
                        }
                    },
                    {
                        '$unwind':{
                            'path':'$person_name',
                            'preserveNullAndEmptyArrays':True
                        }
                    },
                    {
                        "$project": {
                            "person_id": 1, 
                            "year":{"$year":"$create_date"},
                            "month":{"$month":"$create_date"},
                            "person_frm_id":"$person_name.frm_id"
                        }
                    },
                    {
                        '$lookup':{
                            'from':'frm_list',
                            'localField':'person_frm_id',
                            'foreignField': '_id',
                            'as':'frm'
                        }
                    },
                    {
                        '$unwind':{
                            'path':'$frm',
                            'preserveNullAndEmptyArrays':True
                        }
                    },
                    {
                        "$project": {
                            "year":1,
                            "month":1,
                            "person_frm_id":1,
                            "frm_name":"$frm.name",
                            "ws_id":"$frm.workspace_id"
                        }
                    },
                    {
                        '$lookup':{
                            'from':'workspace_list',
                            'localField':'ws_id',
                            'foreignField': '_id',
                            'as':'ws_inf'
                        }
                    },
                    {
                        '$unwind':{
                            'path':'$ws_inf',
                            'preserveNullAndEmptyArrays':True
                        }
                    },
                    {
                        "$project": {
                            "year":1,
                            "month":1,
                            "person_frm_id":1,
                            "frm_name":1,
                            "ws_id":1,
                            "ws_parent":"$ws_inf.parent"
                        }
                    },
                    {
                        "$group":{
                            "_id":{"year":"$year","month":"$month","person_frm_id":"$person_frm_id","frm_name":"$frm_name","ws_id":"$ws_id","ws_parent":"$ws_parent"},
                            "visit_count":{"$sum":1}
                        }
                    },
                    {
                        "$project":{
                            "frm_id":"$_id.person_frm_id",
                            "frm_name":"$_id.frm_name",
                            "year":"$_id.year",
                            "month":"$_id.month",
                            "visit_count":1,
                            "ws_id":"$_id.ws_id",
                            "ws_parent":"$_id.ws_parent",
                            "_id":0
                        }
                    },{"$sort":{"frm_id":1}}]
            if menu_id is None:
                sql.insert(0,{"$match":{"user_id":self.user_id}})
            if date > 1 :
                sql.append({"$match":{"year":int(date)}})
            if self.user_perm == "Müdür":
                sql.append({"$match":{"$or":[{"ws_id":self.user_workspace_id},{"ws_parent":self.user_workspace_id}]}})
            header = ['Firma Adı',"Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]
            tablo =self.Create_Table_Set_Items(QTableWidget,header,frame_x,frame_y-100,self.content_child_frame)
            tablo.setEditTriggers(QTableWidget.NoEditTriggers) 
            tablo.setObjectName("frm_based")
            tablo.move(0,40)
            for col in range(tablo.columnCount()):
                tablo.setColumnWidth(col, 75)
            for col in range(len(header)):
                if col == 0:
                    item = QTableWidgetItem(header[col])
                    item.setTextAlignment(Qt.AlignCenter) 
                    tablo.setVerticalHeaderItem(0,item)
                else:
                    self.Create_Table_Set_Items(QTableWidgetItem,header[col],0,col-1,tablo)
            table_frm_id = None
            row = tablo.rowCount()
            for sql_item in self.conversations.aggregate(sql): 
                if sql_item["frm_id"] != table_frm_id:
                    row = tablo.rowCount()
                    tablo.insertRow(row)
                    item = QTableWidgetItem(sql_item["frm_name"])
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setData(Qt.UserRole, sql_item["frm_id"])
                    tablo.setVerticalHeaderItem(row,item)
                    table_frm_id = sql_item["frm_id"] 
                past_item = tablo.item(row,sql_item['month']-1)
                if past_item is not None:
                    visit_num = int(past_item.text()) + sql_item['visit_count']
                    self.Create_Table_Set_Items(QTableWidgetItem,str(visit_num),row,sql_item["month"]-1,tablo,True)
                else:
                    self.Create_Table_Set_Items(QTableWidgetItem,str(sql_item["visit_count"]),row,sql_item["month"]-1,tablo,True)
            rp = Frm_Based_Report_Detail(date,tablo,menu_id,self)
            tablo.verticalHeader().sectionDoubleClicked.connect(rp.click_vheader)
            tablo.cellDoubleClicked.connect(rp.click_table)

# ---------------------------------------------------------------------------- Raporlar ---------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------ Kişiler Paneli -------------------------------------------------------------------------------------------
    def to_lower_case(self):
        textbox = self.sender()
        text = textbox.text()
        textbox.setText(text.lower())

    def frm_prsn_list_panel(self):
        if self.content_child_frame is not None:
            for child in self.content_child_frame.findChildren(QWidget):
                child.deleteLater()
        if self.content_child_frame.layout():
            QWidget().setLayout(self.content_child_frame.layout()) 

        yatay_layout = QHBoxLayout(self.content_child_frame)
        yatay_layout.setAlignment(Qt.AlignTop)

        if self.user_perm == "Admin":
            frame_x = int((self.contentpanel.width()-30)/3)
            workspace_lister = self.common_items(QComboBox,"item1","Main Workspace",frame_x,25)
            self.set_combobox_items(workspace_lister,"Ws_Parent_Set",workspace_lister)
            ws_list = self.common_items(QComboBox,"workspace_list","Select Top Workspaces",frame_x,25)
            workspace_lister.currentIndexChanged.connect(lambda :self.set_combobox_items(ws_list,"Select_Ws_Set_Ws",workspace_lister))
            yatay_layout.addWidget(workspace_lister,0,Qt.AlignCenter)
        else:
            frame_x = int((self.contentpanel.width()-20)/2)
            ws_list = self.common_items(QComboBox,"workspace_list","Select Any Workspace",frame_x,25)
            for items in self.workspacedb.aggregate([{"$match":{"$or":[{"_id":self.user_workspace_id},{"parent":self.user_workspace_id}]}}]):
                ws_list.addItem(items['name'],userData = items['_id'])
        yatay_layout.addWidget(ws_list,0,Qt.AlignCenter)

        frm_list = self.common_items(QComboBox,"frm_list","First Select Workspace",frame_x,25)
        ws_list.currentIndexChanged.connect(lambda :self.set_combobox_items(frm_list,"Select_Ws_Set_Frm",ws_list))
        yatay_layout.addWidget(frm_list,0,Qt.AlignCenter)
        frm_list.currentIndexChanged.connect(self.frm_prsn_list)

    def frm_prsn_list(self,index):
        tablo = self.content_child_frame.findChildren(QTableWidget,"Person_List")
        if tablo:
            tablo= tablo[0]
            tablo.deleteLater()

        frame_x = self.contentpanel.width()
        frame_y = self.contentpanel.height()
        header = ['Tam Adı','Mail','Firma','Çalışma Alanı','']
        tablo =self.Create_Table_Set_Items(QTableWidget,header,frame_x,frame_y-100,self.content_child_frame)
        tablo.setObjectName("Person_List")
        tablo.move(1,40)
        for col in range(len(header)):
            if col == 0:
                item = QTableWidgetItem(header[col])
                item.setTextAlignment(Qt.AlignCenter) 
                tablo.setVerticalHeaderItem(0,item)
            else:
                self.Create_Table_Set_Items(QTableWidgetItem,header[col],0,col-1,tablo)
        if index > 0:
            add_btn = self.custom_color_common_items(QPushButton,"add","Yeni",75,29,self.GREEN,self.ON_HOVER_GREEN)
            add_btn.clicked.connect(self.frm_prsn_item_panel)
            tablo.setCellWidget(0,3,add_btn)
            sql = [
                {
                    '$lookup':{
                        'from':'frm_list',
                        'localField':'frm_id',
                        'foreignField': '_id',
                        'as':'frm'
                    }
                },
                {
                    '$unwind':{
                        'path':'$frm',
                        'preserveNullAndEmptyArrays':True
                    }
                },
                {
                    '$lookup':{
                        'from':'workspace_list',
                        'localField':'frm.workspace_id',
                        'foreignField': '_id',
                        'as':'ws'
                    }
                },
                {
                    '$unwind':{
                        'path':'$ws',
                        'preserveNullAndEmptyArrays':True
                    }
                },
                {
                    '$project': {
                        "_id": 1,
                        "fullname": 1,
                        "mail": 1,
                        "frm_id":1,
                        "frm_name": "$frm.name",
                        "ws_name": "$ws.name"
                        }
                }]
            for db_item in self.prsdb.aggregate(sql):
                row = tablo.rowCount()
                tablo.insertRow(row)
                item = QTableWidgetItem(db_item["fullname"])
                item.setTextAlignment(Qt.AlignCenter) 
                tablo.setVerticalHeaderItem(row,item)
                self.Create_Table_Set_Items(QTableWidgetItem,db_item["mail"],row,0,tablo)
                self.Create_Table_Set_Items(QTableWidgetItem,db_item["frm_name"],row,1,tablo)
                self.Create_Table_Set_Items(QTableWidgetItem,db_item["ws_name"],row,2,tablo)
                update_btn = self.common_items(QPushButton,"update","Güncelle",75,29)
                update_btn.setProperty("_id",db_item["_id"])
                update_btn.clicked.connect(self.frm_prsn_item_panel)
                tablo.setCellWidget(row,3,update_btn)
        tablo.resizeColumnsToContents()
        min_widths = [200, 150, 150,75]

        for col in range(tablo.columnCount()):
            column_width = tablo.columnWidth(col)
            if column_width < min_widths[col]:
                tablo.setColumnWidth(col, min_widths[col])
        min_widths = None
        header=None

    def frm_prsn_item_panel(self):
        button = self.sender()
        button_name = button.objectName()
        Frame = self.content_child_frame.findChildren(QFrame,"frm_prs_item")
        if Frame:
            Frame= Frame[0]
            Frame.deleteLater()     
        parent_width = self.content_child_frame.width()
        parent_height = self.content_child_frame.height()
        Frame = QFrame(self.content_child_frame)
        Frame.setFixedSize(parent_width,parent_height)   
        Frame.setObjectName("frm_prs_item")
        Frame_layout = QVBoxLayout()
        Frame_layout.setContentsMargins(0,0,0,0)
        Frame_layout.setSpacing(0)    
        Frame_layout1 = QHBoxLayout()
        Frame_layout1.setAlignment(Qt.AlignTop)
        Frame_layout1.setContentsMargins(0,0,0,0)
        Frame_layout1.setSpacing(0)
        btn_menu = QFrame()
        btn_menu.setFixedSize(parent_width-2,35)
        btn_menu.setStyleSheet(f"border:0;border-bottom:1px solid {self.BORDER_COLOR};border-radius:0;")
        
        btn_menu_layout =QHBoxLayout()
        btn_menu_layout.setContentsMargins(0,0,0,0)
        btn_menu_layout.setSpacing(0)

        back_btn = self.custom_color_common_items(QPushButton,"back_btn","<",35,34,self.WIN_COLOR,self.PANEL_COLOR)
        back_btn.clicked.connect(lambda:Frame.deleteLater())
        btn_menu_layout.addWidget(back_btn,0,Qt.AlignLeft)

        if button_name == "update":
            doc_id = button.property("_id")
            del_btn = self.common_items(QPushButton,"del_btn","Sil",50,30)
            del_btn.setProperty("_id",doc_id)
            del_btn.clicked.connect(self.frm_prsn_process)
            btn_menu_layout.addWidget(del_btn,0,Qt.AlignRight)
        btn_menu.setLayout(btn_menu_layout)
        Frame_layout1.addWidget(btn_menu)
        Frame_layout2 = QVBoxLayout()
        Frame_layout2.setAlignment(Qt.AlignCenter)
        Frame_layout2.setSpacing(5)

        if self.user_perm == "Admin":
            workspace_lister = self.common_items(QComboBox,"item2","Main Workspace",parent_width-200,25)
            self.set_combobox_items(workspace_lister,"Ws_Parent_Set",workspace_lister)
            ws_list = self.common_items(QComboBox,"workspace_list","Select Top Workspaces",parent_width-200,25)
            Frame_layout2.addWidget(workspace_lister)
            
        else:
            ws_list = self.common_items(QComboBox,"item_workspace_list","Select Any Workspace",parent_width-200,25)
            for items in self.workspacedb.aggregate([{"$match":{"$or":[{"_id":self.user_workspace_id},{"parent":self.user_workspace_id}]}}]):
                ws_list.addItem(items['name'],userData = items['_id'])
        Frame_layout2.addWidget(ws_list,0,Qt.AlignCenter)

        frm_list = self.common_items(QComboBox,"item_frm_list","First Select Workspace",parent_width-200,25)
        workspace_lister.currentIndexChanged.connect(lambda :self.set_combobox_items(ws_list,"Select_Ws_Set_Ws",workspace_lister))
        ws_list.currentIndexChanged.connect(lambda :self.set_combobox_items(frm_list,"Select_Ws_Set_Frm",ws_list))
        Frame_layout2.addWidget(frm_list,0,Qt.AlignCenter)
        prs_name = self.common_items(QLineEdit,"prs_name","Enter Person Name!",parent_width-200,25)
        prs_mail = self.common_items(QLineEdit,"prs_mail","Enter Person Mail!",parent_width-200,25)
        prs_mail.textChanged.connect(self.to_lower_case)
        Frame_layout2.addWidget(prs_name,0,Qt.AlignCenter)
        Frame_layout2.addWidget(prs_mail,0,Qt.AlignCenter)
        
        if button_name == "update":
            doc = self.prsdb.find_one({"_id":button.property("_id")})
            prs_name.setText(doc["fullname"])
            prs_mail.setText(doc["mail"])
            frm_id = doc["frm_id"]
            ws = self.frmdb.find_one({"_id":frm_id})
            ws = self.workspacedb.find_one({"_id":ws["workspace_id"]})
            ws_id = ws["_id"]
            if self.user_perm == "Admin":
                
                ws_parent = ws["parent"]
                for i in range(workspace_lister.count()):
                    item = workspace_lister.itemData(i)
                    if item == ws_parent:
                        workspace_lister.setCurrentIndex(i)
                        break
            for i in range(ws_list.count()):
                item = ws_list.itemData(i)
                if item == ws_id:
                    ws_list.setCurrentIndex(i)
                    break
            for i in range(frm_list.count()):
                item = frm_list.itemData(i)
                if item == frm_id:
                    frm_list.setCurrentIndex(i)
                    break
            update_btn = self.common_items(QPushButton,"update_btn","Güncelle",100,30)
            update_btn.setProperty("_id",doc_id)
            update_btn.clicked.connect(self.frm_prsn_process)
            Frame_layout2.addWidget(update_btn,0,Qt.AlignCenter)
            
        elif button_name == "add":
            add_btn = self.common_items(QPushButton,"add_btn","Ekle",100,30)
            add_btn.clicked.connect(self.frm_prsn_process)
            Frame_layout2.addWidget(add_btn,0,Qt.AlignCenter) 


        Frame_layout.addLayout(Frame_layout1)
        Frame_layout.addLayout(Frame_layout2)
        Frame_layout.addSpacing(400)
        Frame.setLayout(Frame_layout)
        Frame.show()
    
    def frm_prsn_process (self):
        button = self.sender()
        button_name = button.objectName()
        
        if button_name in ("add_btn","update_btn"):
            prs_name = self.content_child_frame.findChildren(QLineEdit,"prs_name")[0].text()
            prs_mail = self.content_child_frame.findChildren(QLineEdit,"prs_mail")[0].text()
            frm_id = self.content_child_frame.findChildren(QComboBox,"item_frm_list")[0]
            frm_id = frm_id.itemData(frm_id.currentIndex())
            if frm_id > 0:
                if self.Data_Control_Func(prs_mail,"Mail"):
                    if self.Data_Control_Func(prs_name,"Space"):
                        if button_name == "add_btn":
                            data = {"_id":"","fullname":"","mail":"","frm_id":""}
                            data_id = self.prsdb.find().sort({"_id": -1}).limit(1).to_list()
                            if data_id:
                                data_id = int(data_id[0]['_id'])+1
                            else:
                                data_id = 1
                            data['_id'] = data_id
                            data['fullname'] = prs_name
                            data['mail'] = prs_mail
                            data['frm_id'] = frm_id
                            self.prsdb.insert_one(data)
                            self.bildirim(f'{prs_name} adlı kişi Eklenmiştir.')
                        else:
                            self.prsdb.update_one({'_id':button.property("_id")},{'$set':{'fullname':prs_name,'mail':prs_mail,"frm_id":frm_id}})
                            self.bildirim('Kişi Güncellenmiştir')   
                        Frame = self.content_child_frame.findChildren(QFrame,"frm_prs_item")
                        if Frame:
                            Frame= Frame[0]
                            Frame.deleteLater()
                        self.frm_prsn_list_panel()
                    else:
                        self.bildirim("Kişi Adı boşluk olamaz veya boşlukla başlayamaz!")
                else:
                    self.bildirim("Geçerli bir e-posta giriniz!")
            else:
                self.bildirim("Geçerli bir firma seçiniz!")

        else:
            doc_id = button.property("_id")
            meet_count = self.conversations.count_documents({'person_id':doc_id})
            if meet_count > 0:
                self.bildirim("Kişiye Tanımlı Toplantılar olduğundan kişi silinemez!")
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Kişiyi silmek istediğinize emin misiniz?")
                msg.setWindowTitle("Bilgi Mesajı")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)       
                resp = msg.exec()
                if resp == 1024:
                    self.prsdb.delete_one({"_id":doc_id})
                    Frame = self.content_child_frame.findChildren(QFrame,"frm_prs_item")
                    if Frame:
                        Frame= Frame[0]
                        Frame.deleteLater()
                    self.frm_prsn_list_panel()
        

# ------------------------------------------------------------------------ Kişiler Paneli -------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------- Firma Paneli --------------------------------------------------------------------------------------------
# Bir çalışma alanındaki firmaları oluşturma listeme ,güncelleme ve silme işlemleri burdan yapılmaktadır.
# Prensip olarak üst çalışma alanındaki firmalar tüm alt çalışma alanları tarafından kullanılmaktadır. Aynı şekilde tüm alt alanlardaki firmalar üst alanda da kullanılmaktadır.
# Fakat alt alanların birbirleri arasındaki firmlara erişimi yoktur. Bu müdür tarafından personellerin firmarlarına gereksiz tanımlamayı azaltır.
# Aynı şekilde ortak olması gerekenler üst alana tanımlanarak tüm alt alanlarda da kullanıma izin veriler gereksiz tanımlamalardan kaçınılır.
# Admin olan kişi tüm herşeyi listelerken müdür kendi çalışma alanındakileri listeler ve işlem yapabilir
  
    def frm_list_panel(self):# Firmları Filtreleyebilecek yetkiye göre comboboxlar oluşturur
        if self.content_child_frame is not None:
            for child in self.content_child_frame.findChildren(QWidget):
                child.deleteLater()
        if self.content_child_frame.layout():
            QWidget().setLayout(self.content_child_frame.layout()) 

        yatay_layout = QHBoxLayout(self.content_child_frame)
        yatay_layout.setAlignment(Qt.AlignTop)
        frame_x = (self.contentpanel.width()-20)/2

        if self.user_perm == "Admin":
            workspace_lister = self.common_items(QComboBox,"item1","Main Workspace",frame_x,25)
            ws_list = self.common_items(QComboBox,"ws_list","Select Top Workspaces",frame_x,25)
            self.set_combobox_items(workspace_lister,"Ws_Parent_Set",workspace_lister)
            workspace_lister.currentIndexChanged.connect(lambda :self.set_combobox_items(ws_list,"Select_Ws_Set_Ws",workspace_lister))
            yatay_layout.addWidget(workspace_lister)
            
        else:
            ws_list = self.common_items(QComboBox,"ws_list","Select Top Workspaces",frame_x,25)
            self.set_combobox_items(ws_list,"Self_Ws_Child",ws_list)
        
        ws_list.currentIndexChanged.connect(self.frm_list_table)
        yatay_layout.addWidget(ws_list,0,Qt.AlignCenter)
        self.content_child_frame.setLayout(yatay_layout)
    
    def frm_list_table(self,index):#Filtrelere göre ilgili firmaları listeleyen tabloyu oluşturur
        tablo = self.content_child_frame.findChildren(QTableWidget,"frm_list")
        frame_x = self.contentpanel.width()
        frame_y = self.contentpanel.height()
        if tablo:
            tablo= tablo[0]
            tablo.deleteLater()
        header = ['Firma Adı','Çalışma Alanı','']
        tablo = self.Create_Table_Set_Items(QTableWidget,header,frame_x,frame_y-100,self.content_child_frame)
        tablo.setObjectName("frm_list")
        tablo.move(0,40)

        for col in range(len(header)):
            if col == 0:
                item = QTableWidgetItem(header[col])
                item.setTextAlignment(Qt.AlignCenter) 
                tablo.setVerticalHeaderItem(0,item)
            else:
                self.Create_Table_Set_Items(QTableWidgetItem,header[col],0,col-1,tablo)

        if index > 0:
            add_btn = self.custom_color_common_items(QPushButton,"add","Yeni",75,29,self.GREEN,self.ON_HOVER_GREEN)
            add_btn.clicked.connect(self.frm_item_panel)
            tablo.setCellWidget(0,1,add_btn)
            sql = [
                {
                    '$lookup':{
                        'from':'workspace_list',
                        'localField':'workspace_id',
                        'foreignField': '_id',
                        'as':'ws_child'
                    }
                },
                {
                    '$unwind':{
                        'path':'$ws_child',
                        'preserveNullAndEmptyArrays':True
                    }
                },
                {
                    '$project': {
                        "_id": 1,
                        "name": 1,
                        "workspace_id": 1,
                        "ws_name": "$ws_child.name"
                        }
                },
                {
                    '$match':{'workspace_id':self.sender().itemData(index)}
                }]
            
            for item in self.frmdb.aggregate(sql):
                row = tablo.rowCount()
                tablo.insertRow(row)
                tablo_item = QTableWidgetItem(item["name"])
                tablo_item.setTextAlignment(Qt.AlignCenter) 
                tablo.setVerticalHeaderItem(row,tablo_item)
                self.Create_Table_Set_Items(QTableWidgetItem,item["ws_name"],row,0,tablo)
                
                update_btn = self.common_items(QPushButton,"update","Güncelle",75,29)
                update_btn.setProperty("_id",item["_id"])
                update_btn.clicked.connect(self.frm_item_panel)
                tablo.setCellWidget(row,1,update_btn)
            tablo.resizeColumnsToContents()
            tablo_max_width=frame_x-77-tablo.verticalHeader().width()
            min_widths = [tablo_max_width,75]

            for col in range(tablo.columnCount()):
                column_width = tablo.columnWidth(col)
                if column_width != min_widths[col]:
                    tablo.setColumnWidth(col, min_widths[col])
            min_widths = None
            header=None

    def frm_item_panel(self):# Güncelleme veya ekleme butonuna basıldığında o item için panel oluşturur eğer güncelleme paneli ise silme butonu da ekler
        button = self.sender()
        button_name = button.objectName()
        Frame = self.content_child_frame.findChildren(QFrame,"frm_item")
        if Frame:
            Frame= Frame[0]
            Frame.deleteLater()
        parent_width = self.content_child_frame.width()
        parent_height = self.content_child_frame.height()
        Frame = QFrame(self.content_child_frame)
        Frame.setObjectName("frm_item")
        Frame.setFixedSize(parent_width,parent_height)
        doc_id = None
        parent_id = None
        ws_parent = None

        Frame_layout = QVBoxLayout()
        Frame_layout.setContentsMargins(0,0,0,0)
        Frame_layout.setSpacing(0)

        Frame_layout1 = QHBoxLayout()

        btn_menu = QFrame()
        btn_menu.setFixedSize(parent_width-2,35)
        btn_menu.setStyleSheet(f"border:0;border-bottom:1px solid {self.BORDER_COLOR};border-radius:0;")
        
        btn_menu_layout =QHBoxLayout()
        btn_menu_layout.setContentsMargins(0,0,0,0)
        btn_menu_layout.setSpacing(0)

        back_btn = self.custom_color_common_items(QPushButton,"back_btn","<",35,34,self.WIN_COLOR,self.PANEL_COLOR)
        back_btn.clicked.connect(lambda:Frame.deleteLater())
        btn_menu_layout.addWidget(back_btn,0,Qt.AlignLeft)

        if button_name == "update":
            doc_id = button.property("_id")
            del_btn = self.common_items(QPushButton,"del_btn","Sil",50,30)
            del_btn.setProperty("_id",doc_id)
            del_btn.clicked.connect(self.frm_process)
            btn_menu_layout.addWidget(del_btn,0,Qt.AlignRight)

        
        btn_menu.setLayout(btn_menu_layout)
        Frame_layout1.addWidget(btn_menu)

        Frame_layout2 = QVBoxLayout()
        Frame_layout2.setAlignment(Qt.AlignCenter)
        Frame_layout2.setSpacing(5)

        frm_name = self.common_items(QLineEdit,"frm_name","Enter Firm Name!",parent_width-300,25)
        Frame_layout2.addWidget(frm_name)

        if button_name == "update":
            item = self.frmdb.find_one({"_id":doc_id})
            frm_name.setText(item['name'])
            parent_id = item["workspace_id"]
            ws_parent = self.workspacedb.find_one({"_id":parent_id})
            ws_parent=ws_parent["parent"]

        if self.user_perm == "Admin":
            ws_parent_list = self.common_items(QComboBox,"item1","",parent_width-300,25)
            self.set_combobox_items(ws_parent_list,"Ws_Parent_Set",ws_parent_list)
            ws_list = self.common_items(QComboBox,"ws_list","Select Top Workspaces",parent_width-300,25)
            ws_parent_list.currentIndexChanged.connect(lambda :self.set_combobox_items(ws_list,"Select_Ws_Set_Ws",ws_parent_list))
            
            if button_name == "update":
                if ws_parent == 0:
                    ws_parent_list.setCurrentIndex(1)
                    for i in range(ws_list.count()):
                        ws_id = ws_list.itemData(i)
                        if ws_id == parent_id:
                            ws_list.setCurrentIndex(i)
                            break
                else:
                    for i in range(ws_parent_list.count()):
                        ws_parent_id = ws_parent_list.itemData(i)
                        if ws_parent_id == ws_parent:
                            ws_parent_list.setCurrentIndex(i)
                            break
                    for i in range(ws_list.count()):
                        ws_id = ws_list.itemData(i)
                        if ws_id == parent_id:
                            ws_list.setCurrentIndex(i)
                            break
            else:
                combo_1_id = self.content_child_frame.findChildren(QComboBox,"item1")[0]
                combo_1_id = int(combo_1_id.itemData(combo_1_id.currentIndex()))

                for i in range(ws_parent_list.count()):
                    ws_parent_id = ws_parent_list.itemData(i)
                    if ws_parent_id == combo_1_id:
                        ws_parent_list.setCurrentIndex(i)
                        break

                combo_2_id = self.content_child_frame.findChildren(QComboBox,"ws_list")[0]
                combo_2_id = int(combo_2_id.itemData(combo_2_id.currentIndex()))

                for i in range(ws_list.count()):
                    ws_id = ws_list.itemData(i)
                    if ws_id == combo_2_id:
                        ws_list.setCurrentIndex(i)
                        break

            Frame_layout2.addWidget(ws_parent_list)
            Frame_layout2.addWidget(ws_list)
        else:
            ws_list = self.common_items(QComboBox,"ws_list","Select Any Workspace",parent_width-300,25)
            for items in self.workspacedb.aggregate([{"$match":{"$or":[{"_id":self.user_workspace_id},{"parent":self.user_workspace_id}]}}]):
                ws_list.addItem(items['name'],userData = items['_id'])
                if button_name == "update":
                    if parent_id == items["_id"]:
                        ws_list.setCurrentIndex(ws_list.count()-1)
            Frame_layout2.addWidget(ws_list)

        if button_name == "update":
            update_btn = self.common_items(QPushButton,"update_btn","Güncelle",100,30)
            update_btn.setProperty("_id",doc_id)
            update_btn.clicked.connect(self.frm_process)
            Frame_layout2.addWidget(update_btn,0,Qt.AlignCenter)
        else:
            add_btn = self.common_items(QPushButton,"add_btn","Ekle",100,30)
            add_btn.clicked.connect(self.frm_process)
            Frame_layout2.addWidget(add_btn,0,Qt.AlignCenter)

        Frame_layout.addLayout(Frame_layout1)
        Frame_layout.addLayout(Frame_layout2)
        Frame_layout.addSpacing(100)
        Frame.setLayout(Frame_layout)
        Frame.show()

    def frm_process(self):
        button = self.sender()
        button_name = button.objectName()
        if button_name in ("update_btn","add_btn"):
            frm_name = self.content_child_frame.findChildren(QLineEdit,"frm_name")[0].text()
            workspace_id = self.content_child_frame.findChildren(QComboBox,"ws_list")[0]
            workspace_id = int(workspace_id.itemData(workspace_id.currentIndex()))
        
        if button_name in ("update_btn","del_btn"):
            doc_id = button.property("_id")
            if button_name =="del_btn":
                prs_count = self.prsdb.count_documents({'frm_id':doc_id})
                if prs_count == 0 : # Firmaya Kişi Ekli değilse silsin
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Firmayı silmek istediğinize emin misiniz?")
                    msg.setWindowTitle("Bilgi Mesajı")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)       
                    resp = msg.exec()
                    if resp == 1024:
                        self.frmdb.delete_one({"_id":doc_id})
                        Frame = self.content_child_frame.findChildren(QFrame,"frm_item")
                        if Frame:
                            Frame= Frame[0]
                            Frame.deleteLater()
                        self.frm_list_panel()
                else:
                    self.bildirim(f"Bu çalışma alanı  {prs_count} tane kişi tanımlı olduğundan silinememektedir.")
            else:
                if self.Data_Control_Func(frm_name,"Space"):
                    if workspace_id != 0:
                        self.frmdb.update_one({'_id':doc_id},{'$set':{'name':frm_name,'workspace_id':workspace_id}})
                        self.bildirim("Firma Güncellenmiştir!!") 
                        Frame = self.content_child_frame.findChildren(QFrame,"frm_item")
                        if Frame:
                            Frame= Frame[0]
                            Frame.deleteLater()
                        self.frm_list_panel()
                    else:
                        self.bildirim("Lütfen Çalışma alanı seçiniz!!") 
                else:
                    self.bildirim("Firma Adı Boş olamaz veya boşluk ile başlayamaz!!")
        elif button_name == "add_btn":
            if self.Data_Control_Func(frm_name,"Space"):
                if workspace_id != 0:
                    data = {"_id":"","name":"",'workspace_id':''}
                    data_id = self.frmdb.find().sort({"_id": -1}).limit(1).to_list()
                    if data_id:
                        data_id = int(data_id[0]['_id'])+1
                    else:
                        data_id = 1
                    data['_id'] = data_id
                    data['name'] = frm_name
                    data['workspace_id'] = workspace_id
                    self.frmdb.insert_one(data)
                    self.bildirim(f'{frm_name} adlı firma Eklenmiştir.')
                    Frame = self.content_child_frame.findChildren(QFrame,"frm_item")
                    if Frame:
                        Frame= Frame[0]
                        Frame.deleteLater()
                    self.frm_list_panel()
                else:
                    self.bildirim('Çalışma Alanı Seçiniz!!')  
            else:
                self.bildirim('Firma Adı Boş olamaz veya boşluk ile başlayamaz!!')

# ------------------------------------------------------------------------- Firma Paneli --------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------- Yetki Paneli --------------------------------------------------------------------------------------------
    # Bu panel yerela ağdaki kullanıcıları tarar
    # Kişiye yetki tanımlatır güncelletir silme seçeneği veriler kaybolmaması için izin verilmememiştir.
    # Yetkiye göre kişiyi tanımlayacağı alan ve verebileceği yetkileri kontrol eder
    def scan_locale_user_data(self):# yerel ağdaki kullanıcıları tarıyor
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("Bu işlem yaklaşık 10 dk sürecektir. Devam etmek istiyor musunuz?")
        msg.setWindowTitle("Bilgi Mesajı")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            
        resp = msg.exec()

        if resp == 1024:
            Common_Class.get_user_accounts()     

    def list_users_panel(self):#Kullanıcıları listeleme alan tasarımı
        if self.content_child_frame is not None:
            for child in self.content_child_frame.findChildren(QWidget):
                child.deleteLater()
        if self.content_child_frame.layout():
            QWidget().setLayout(self.content_child_frame.layout()) 
        
        yatay_layout = QHBoxLayout(self.content_child_frame)
        yatay_layout.setAlignment(Qt.AlignTop)
        
        Perm_list=["Admin","Müdür","Personel","Yetkisiz","Gereksiz"]
        if self.user_perm == "Müdür":
            Perm_list.remove("Admin")
        
        perm_combo = self.common_items(QComboBox,"perm_list","Tüm Yetkiler",int(self.content_child_frame.width()/2),25)
        perm_combo.addItems(Perm_list)
        perm_combo.currentIndexChanged.connect(self.list_user_table)
        perm_combo.setCurrentIndex(1)
        perm_combo.setCurrentIndex(0)

        yatay_layout.addWidget(perm_combo,0,Qt.AlignCenter)
        self.content_child_frame.setLayout(yatay_layout)
    
    def list_user_table(self,index): # seçilen yetkiye göre tablo filtreleme
        tablo = self.content_child_frame.findChildren(QTableWidget,"user_list")
        if tablo:
            tablo= tablo[0]
            tablo.deleteLater()

        sql = [
                {
                    '$lookup':{
                        'from':'workspace_list',
                        'localField':'workspace_id',
                        'foreignField': '_id',
                        'as':'ws_name'
                    }
                },
                {
                    '$unwind':{
                        'path':'$ws_name',
                        'preserveNullAndEmptyArrays':True
                    }
                },
                {
                    '$project':{
                        "_id":1,
                        "SID":None,
                        "username":1,
                        "real_name":1,
                        "workspace_id":1,
                        "permission":1,
                        "ws_name":"$ws_name.name",
                        "ws_parent":"$ws_name.parent"
                    }
                }]
        if self.user_perm == "Müdür":
            sql.append({'$match':{"$or":[{"ws_parent":self.user_workspace_id},{"workspace_id":self.user_workspace_id}],'permission':{"$ne":"Admin"}}})

        if index != 0:
            sql.append({'$match':{'permission':self.sender().currentText(),"_id":{"$ne":self.user_id}}})
        else:
            sql.append({'$match':{'permission':{"$ne":"Gereksiz"},"_id":{"$ne":self.user_id}}})
        
        header = ['Tam Adı','Kullanıcı Adı','Yetki','Çalışma Alanı','']
        tablo = self.Create_Table_Set_Items(QTableWidget,header,self.contentpanel.width(),self.contentpanel.height()-100,self.content_child_frame)
        tablo.move(0,40)
        tablo.setObjectName("user_list")
        
        for col in range(len(header)):
            if col == 0:
                item = QTableWidgetItem(header[col])
                item.setTextAlignment(Qt.AlignCenter) 
                tablo.setVerticalHeaderItem(0,item)
            else:
                self.Create_Table_Set_Items(QTableWidgetItem,header[col],0,col-1,tablo)
        
        add_btn = self.custom_color_common_items(QPushButton,"add","Yeni",74,29,self.GREEN,self.ON_HOVER_GREEN)
        add_btn.clicked.connect(self.users_item_panel)
        tablo.setCellWidget(0,3,add_btn)

        for db_item in self.usersdatadb.aggregate(sql):
            row = tablo.rowCount()
            tablo.insertRow(row)
            item = QTableWidgetItem(db_item["real_name"])
            item.setTextAlignment(Qt.AlignCenter) 
            tablo.setVerticalHeaderItem(row,item)
            self.Create_Table_Set_Items(QTableWidgetItem,db_item["username"],row,0,tablo)
            self.Create_Table_Set_Items(QTableWidgetItem,db_item["permission"],row,1,tablo)
            self.Create_Table_Set_Items(QTableWidgetItem,db_item["ws_name"],row,2,tablo)

            update_btn = self.common_items(QPushButton,"update","Güncelle",74,29)
            update_btn.setProperty("_id",db_item["_id"])
            update_btn.clicked.connect(self.users_item_panel)
            tablo.setCellWidget(row,3,update_btn)
        tablo.resizeColumnsToContents()
        tablo_max_width=self.contentpanel.width()- tablo.verticalHeader().width()-202-tablo.columnWidth(0)
        min_widths = [120, tablo_max_width,75]

        for col in range(tablo.columnCount()-1):
            column_width = tablo.columnWidth(col+1)
            if column_width != min_widths[col]:
                tablo.setColumnWidth(col+1, min_widths[col])
        min_widths = None
        header=None

    def users_item_panel(self):
        button = self.sender()
        button_name = button.objectName() 
        Frame = self.content_child_frame.findChildren(QFrame,"users_item")
        if Frame:
            Frame= Frame[0]
            Frame.deleteLater()
        parent_width = self.content_child_frame.width()
        parent_height = self.content_child_frame.height()
        Frame = QFrame(self.content_child_frame)
        Frame.setFixedSize(parent_width,parent_height)
        Frame_layout = QVBoxLayout()
        Frame_layout.setContentsMargins(0,0,0,0)
        Frame_layout.setSpacing(0)

        Frame_layout1 = QHBoxLayout()

        btn_menu = QFrame()
        btn_menu.setFixedSize(parent_width-2,35)
        btn_menu.setStyleSheet(f"border:0;border-bottom:1px solid {self.BORDER_COLOR};border-radius:0;")
        
        btn_menu_layout =QHBoxLayout()
        btn_menu_layout.setContentsMargins(0,0,0,0)
        btn_menu_layout.setSpacing(0)

        back_btn = self.custom_color_common_items(QPushButton,"back_btn","<",35,34,self.WIN_COLOR,self.PANEL_COLOR)
        back_btn.clicked.connect(lambda:Frame.deleteLater())

        btn_menu_layout.addWidget(back_btn,0,Qt.AlignLeft)

        btn_menu.setLayout(btn_menu_layout)

        Frame_layout1.addWidget(btn_menu)
        Frame_layout2 = QVBoxLayout()
        Frame_layout2.setAlignment(Qt.AlignCenter)
        Frame_layout2.setSpacing(5)
        
        user_fullname = self.common_items(QLineEdit,"user_fullname","Enter User Real Name",parent_width-200,25)
        mail = self.common_items(QLineEdit,"user_item_mail","Enter User Mail..(Optional)",parent_width-200,25)
        mail.textChanged.connect(self.to_lower_case)
        Frame_layout2.addWidget(user_fullname) 
        Frame_layout2.addWidget(mail) 
        perms = ["Admin","Müdür","Personel","Yetkisiz","Gereksiz"]    
        perm_combo = self.common_items(QComboBox,"item_panel_perm_list","Select User Permission",parent_width-200,25)

        if self.user_perm == "Admin":
            workspace_lister = self.common_items(QComboBox,"item1","Main Workspace",parent_width-200,25)
            self.set_combobox_items(workspace_lister,"Ws_Parent_Set",workspace_lister)
            ws_list = self.common_items(QComboBox,"workspace_list","Select Top Workspaces",parent_width-200,25)
            workspace_lister.currentIndexChanged.connect(lambda :self.set_combobox_items(ws_list,"Select_Ws_Set_Ws",workspace_lister))
            Frame_layout2.addWidget(workspace_lister)
        else:
            perms.remove("Admin")
            perms.remove("Müdür")
            ws_list = self.common_items(QComboBox,"workspace_list","Select Any Workspace",parent_width-200,25)
            for items in self.workspacedb.aggregate([{"$match":{"$or":[{"_id":self.user_workspace_id},{"parent":self.user_workspace_id}]}}]):
                ws_list.addItem(items['name'],userData = items['_id'])
        Frame_layout2.addWidget(ws_list)
        perm_combo.addItems(perms)
        Frame_layout2.addWidget(perm_combo)
        if button_name == "add":
            user_combo = self.common_items(QComboBox,"user_list","Select Any New User!",parent_width-200,25)
            if os.path.isfile("LocaleUsersData.json") == True:
                with open('LocaleUsersData.json', 'r') as file:
                    data = json.load(file)
                for i in self.usersdatadb.find():
                    SID = self.cp.decript(i['SID'])
                    data =list(filter(lambda item: item['SID'] != SID,data))

                for i in data:
                    user_combo.addItem(i['name']+" - "+i['fullname'],userData=i['SID'])
            else:
                user_combo.addItem("Please Scan Local User !!",userData=0)
            Frame_layout2.insertWidget(0,user_combo)
        elif button_name == "update":
            doc_id = button.property("_id")
            self_item = self.usersdatadb.find_one({"_id":doc_id})
            user_fullname.setText(self_item["real_name"])
            mail.setText(self_item["mail"])
            if self.user_perm == "Admin":
                ws_parent =self.workspacedb.find_one({"_id":self_item["workspace_id"]})
                for i in range(workspace_lister.count()):
                    item = workspace_lister.itemData(i)
                    if item == ws_parent["parent"]:
                        workspace_lister.setCurrentIndex(i)
                        break
            for i in range(ws_list.count()):
                item = ws_list.itemData(i)
                if item == self_item["workspace_id"]:
                    ws_list.setCurrentIndex(i)
                    break
        
            for i in range(perm_combo.count()):
                item = perm_combo.itemText(i)
                if self_item["permission"] == item:
                    perm_combo.setCurrentIndex(i)
                    break
        
        item_button_text = "Ekle" if button_name == "add" else "Güncelle"
        item_button_objname = "add" if button_name == "add" else "update"
        item_button = self.common_items(QPushButton,item_button_objname,item_button_text,75,30)
        if button_name == "update":
            item_button.setProperty("_id",button.property("_id"))
        item_button.clicked.connect(self.users_process)
        Frame_layout2.addWidget(item_button,0,Qt.AlignCenter)

        Frame_layout.addLayout(Frame_layout1)
        Frame_layout.addLayout(Frame_layout2)
        Frame.setLayout(Frame_layout)
        Frame.show()
    
    def users_process(self):
        button = self.sender()
        button_name = button.objectName()  
        user_fullname = self.content_child_frame.findChildren(QLineEdit,"user_fullname")[0].text()
        workspace_id = self.content_child_frame.findChildren(QComboBox,"workspace_list")[0]
        workspace_id = int(workspace_id.itemData(workspace_id.currentIndex()))  
        perm = self.content_child_frame.findChildren(QComboBox,"item_panel_perm_list")[0].currentText()
        user_mail = self.content_child_frame.findChildren(QLineEdit,"user_item_mail")[0].text()
        mail_state=True
        if user_mail != "":
            mail_state = self.Data_Control_Func(user_mail,"Mail")
            if mail_state == False:
                self.bildirim("Lütfen geçerli bir mail adresini giriniz!")
        if self.Data_Control_Func(user_fullname,"Space") and mail_state:
            if workspace_id != 0:
                if perm in ["Admin","Müdür","Personel","Gereksiz","Yetkisiz"]:
                    if button_name == "update":
                        self.usersdatadb.update_one({'_id':button.property("_id")},{'$set':{'real_name':user_fullname,'workspace_id':workspace_id,'permission':perm,'mail':user_mail}})
                        self.bildirim("Kullanıcı Güncellenmiştir!!") 
                        Frame = self.content_child_frame.findChildren(QFrame,"users_item")
                        if Frame:
                            Frame= Frame[0]
                            Frame.deleteLater()
                        self.list_users_panel()
                    else:
                        user_sid = self.content_child_frame.findChildren(QComboBox,"user_list")[0]
                        user_sid = user_sid.itemData(user_sid.currentIndex())
                        if user_sid != 0:
                            data = {"_id":"","SID":"",'username':'','real_name':"",'workspace_id':"","permission":""}
                            data_id = self.usersdatadb.find().sort({"_id": -1}).limit(1).to_list()
                            if data_id:
                                data_id = int(data_id[0]['_id'])+1
                            else:
                                data_id = 1
                            if os.path.isfile("LocaleUsersData.json") == True:
                                with open('LocaleUsersData.json', 'r') as file:
                                    json_data = json.load(file)
                            json_data =list(filter(lambda item: item['SID'] == user_sid,json_data))
                            data['_id'] = data_id
                            data['SID'] = self.cp.cript(user_sid)
                            data['username'] = json_data[0]['name']
                            data['real_name'] = user_fullname
                            data['workspace_id'] = workspace_id
                            data['permission'] = perm
                            data["mail"] = user_mail
                            self.usersdatadb.insert_one(data)
                            self.bildirim(f"{user_fullname} adlı kişi yetkilendirilmiştir.")
                            Frame = self.content_child_frame.findChildren(QFrame,"users_item")
                            if Frame:
                                Frame= Frame[0]
                                Frame.deleteLater()
                            self.list_users_panel()
                        else:
                            self.bildirim("Düzgün bir kullanıcı seçiniz!! Kullanıcı yoksa lütfen yerel ağdaki kullanıcıları taratınız!")   
                else:
                    self.bildirim("Düzgün bir yetki seçiniz!!")
            else:
                self.bildirim("Düzgün bir çalışma alanı seçiniz!!")
        else:
            self.bildirim("Kişinin Adı Boş olamaz veya boşluk ile başlayamaz!!")
        
# ------------------------------------------------------------------------- Yetki Paneli --------------------------------------------------------------------------------------------

# ----------------------------------------------------------------- WorkSpace ------------------------------------------------------------------------------------
# Workspace List Kişinin yetkisine göre çalışma alanlarını listeleliyor 
# Tıklanan Güncelle veya ekleme butonu workspace_item_panel yönlendiriyor ve butonun adına bakıyor böylelikle ekleme mi güncelleme mi onu anlıyoruz.
# Aynı zamanda kullanıcının yetkisine bakarak güncellemedeki üst çalışma alanını listeliyor

    def workspace_list_panel (self):# Çalışma Alanlarını Adminse hepsini müdürse kendi çalışma alanlarını listeliyor
        if self.content_child_frame is not None:
            for child in self.content_child_frame.findChildren(QWidget):
                child.deleteLater()

        frame_x = self.contentpanel.width()
        frame_y = self.frameGeometry().height()-60

        sql = [
                {
                    '$lookup':{
                        'from':'workspace_list',
                        'localField':'parent',
                        'foreignField': '_id',
                        'as':'parent_name'
                    }
                },
                {
                    '$unwind':{
                        'path':'$parent_name',
                        'preserveNullAndEmptyArrays':True
                    }
                },
                {
                    '$project':{
                        "_id":1,
                        "name":1,
                        "parent":1,
                        "parent_name":"$parent_name.name"
                    }
                }]
        if self.user_perm == "Müdür":
            sql.append({"$match":{"parent":self.user_workspace_id}})

        header = ['isim','Bağlı Olduğu Alan','']
        tablo = self.Create_Table_Set_Items(QTableWidget,header,frame_x,frame_y-60,self.content_child_frame)
        
        for col in range(len(header)):
            if col == 0:
                item = QTableWidgetItem(header[col])
                item.setTextAlignment(Qt.AlignCenter) 
                tablo.setVerticalHeaderItem(0,item)
            else:
                self.Create_Table_Set_Items(QTableWidgetItem,header[col],0,col-1,tablo)
        
        add_btn = self.custom_color_common_items(QPushButton,"add","Yeni",74,29,self.GREEN,self.ON_HOVER_GREEN)
        add_btn.clicked.connect(self.workspace_item_panel)#self.del_workspace_btn_click
        tablo.setCellWidget(0,1,add_btn)

        for db_items in self.workspacedb.aggregate(sql):
            row = tablo.rowCount()
            tablo.insertRow(row)
            item = QTableWidgetItem(db_items["name"])
            item.setTextAlignment(Qt.AlignCenter) 
            tablo.setVerticalHeaderItem(row,item)

            widget_text = db_items["parent_name"] if db_items["parent"] != 0 else "Main Workspace"
            self.Create_Table_Set_Items(QTableWidgetItem,widget_text,row,0,tablo)

            update_btn = self.common_items(QPushButton,"update","Güncelle",74,29)
            update_btn.setProperty("_id",db_items["_id"])
            update_btn.clicked.connect(self.workspace_item_panel)#self.del_workspace_btn_click
            tablo.setCellWidget(row,1,update_btn)
        tablo.resizeColumnsToContents()
        tablo_max_width=frame_x - tablo.verticalHeader().width()-77
        min_widths=[tablo_max_width,75]
        for col in range(tablo.columnCount()):
            column_width = tablo.columnWidth(col)
            if column_width != min_widths[col]:
                tablo.setColumnWidth(col, min_widths[col])
        min_widths = None
        header=None
        self.content_child_frame.show()
    
    def workspace_item_panel(self):# Seçilen işlem sonucu güncelleme veya ekleme paneli oluşturur eğer güncelle seçilirse silme butonu da oluşturulur
        button = self.sender()
        button_name = button.objectName()
        Frame = self.content_child_frame.findChildren(QFrame,"ws_item")
        if Frame:
            Frame= Frame[0]
            Frame.deleteLater()
        parent_width = self.content_child_frame.width()
        parent_height = self.content_child_frame.height()
        Frame = QFrame(self.content_child_frame)
        Frame.setFixedSize(parent_width,parent_height)

        Frame_layout = QVBoxLayout()
        Frame_layout.setContentsMargins(0,0,0,0)
        Frame_layout.setSpacing(0)
        Frame_layout1 = QHBoxLayout()

        btn_menu = QFrame()
        btn_menu.setFixedSize(parent_width-2,35)
        btn_menu.setStyleSheet(f"border:0;border-bottom:1px solid {self.BORDER_COLOR};border-radius:0;")
        
        btn_menu_layout =QHBoxLayout()
        btn_menu_layout.setContentsMargins(0,0,0,0)
        btn_menu_layout.setSpacing(0)

        back_btn = self.custom_color_common_items(QPushButton,"back_btn","<",35,34,self.WIN_COLOR,self.PANEL_COLOR)
        back_btn.clicked.connect(lambda:Frame.deleteLater())

        btn_menu_layout.addWidget(back_btn,0,Qt.AlignLeft)

        btn_menu.setLayout(btn_menu_layout)

        Frame_layout1.addWidget(btn_menu)
        Frame_layout2 = QVBoxLayout()

        ws_name = self.common_items(QLineEdit,"ws_name","Please Enter New Name!!",parent_width-300,25)
        

        parent_combo =self.common_items(QComboBox,"ws_parent","Main Workspace",parent_width-300,25)
        cursor = self.workspacedb.find({"parent":0}) if self.user_perm == "Admin" else self.workspacedb.find({"_id":self.user_workspace_id})
        if button_name =="update":
            doc_id = button.property("_id")
            item = self.workspacedb.find_one({"_id":doc_id})
            item_name=item["name"]
            parent_id = item["parent"]

            ws_name.setText(item_name)

            del_btn = self.common_items(QPushButton,"del_btn","Sil",50,30)
            del_btn.setProperty("_id",doc_id)
            del_btn.clicked.connect(self.workspace_process)
            btn_menu_layout.addWidget(del_btn,0,Qt.AlignRight)

        if self.user_perm == "Müdür":
            parent_combo.clear()

        for items in cursor:
            parent_combo.addItem(items['name'],userData = items['_id'])
            if button_name == "update":
                if parent_id == items["_id"]:
                    parent_combo.setCurrentIndex(parent_combo.count()-1)

        Frame_layout2.setAlignment(Qt.AlignCenter)
        Frame_layout2.setSpacing(5)
        Frame_layout2.addWidget(ws_name,0,Qt.AlignCenter)
        Frame_layout2.addWidget(parent_combo)
        if button_name == "update":
            update_btn = self.common_items(QPushButton,"update_btn","Güncelle",100,30)
            update_btn.setProperty("_id",doc_id)
            update_btn.clicked.connect(self.workspace_process)
            Frame_layout2.addWidget(update_btn,0,Qt.AlignCenter)
        else:
            add_btn = self.common_items(QPushButton,"add_btn","Ekle",100,30)
            add_btn.clicked.connect(self.workspace_process)
            Frame_layout2.addWidget(add_btn,0,Qt.AlignCenter)
        
        Frame_layout2.addSpacing(100)
        Frame_layout.addLayout(Frame_layout1)
        Frame_layout.addLayout(Frame_layout2)
        Frame.setLayout(Frame_layout)
        Frame.show()

    def workspace_process(self):# Yapılan işleme bakar ve işler
        button = self.sender()
        button_name = button.objectName()#Butonlara isim verdik buna göre işlemi ayırt edebiliyoruz
        if button_name in ("update_btn","add_btn"): # eğer işlem ekleme ve güncelleme ise ortak olan bilgileri tanımlıyor
            workspace_name = self.content_child_frame.findChildren(QLineEdit,"ws_name")[0].text()
            new_parent = self.content_child_frame.findChildren(QComboBox,"ws_parent")[0]
            new_parent_id = int(new_parent.itemData(new_parent.currentIndex()))
        if button_name in ("update_btn","del_btn"): # eğer işlem güncelleme ve silme ise bunların ortak olan verisini tanımlıyor ve işlemi yapıyor
            doc_id = button.property("_id")
            if button_name == "update_btn":
                if self.Data_Control_Func(workspace_name,"Space"):
                    if self.user_perm == "Admin" or (self.user_perm == "Müdür" and new_parent_id != 0):
                        self.workspacedb.update_one({'_id':doc_id},{'$set':{'name':workspace_name,'parent':new_parent_id}})
                        self.bildirim("Çalılşma Alanı Güncellenmiştir")
                        Frame = self.content_child_frame.findChildren(QFrame,"ws_item")
                        if Frame:
                            Frame= Frame[0]
                            Frame.deleteLater()
                        self.workspace_list_panel()
                    else:
                        self.bildirim('Lütfen Üst Çalışma Alanını Düzgün seçiniz!!')
                else:
                    self.bildirim('Çalışma Alanı adı boş olamaz veya boşluk ile başlayamaz !!')
            else: # Çalışma alanının altında kişi ,firma veya başka çalışma alanı eklimi kontrolü yapıyor 
                user_workspace = self.usersdatadb.count_documents({'workspace_id':doc_id})
                parent = self.workspacedb.count_documents({'parent':doc_id})
                frm_count = self.frmdb.count_documents({'workspace_id':doc_id})  
                if user_workspace == 0 and parent == 0 and frm_count == 0:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Çalışma alanını silmek istediğinize emin misiniz?")
                    msg.setWindowTitle("Bilgi Mesajı")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    resp = msg.exec()
                    if resp == 1024:
                        self.workspacedb.delete_one({"_id":doc_id})
                        Frame = self.content_child_frame.findChildren(QFrame,"ws_item")
                        if Frame:
                            Frame= Frame[0]
                            Frame.deleteLater()
                        self.workspace_list_panel()
                    else:
                        self.bildirim(f"Bu çalışma alanı {user_workspace} tane çalışan, {frm_count} tane firma ve {parent} tane çalışma alanı tanımlı olduğundan silinememektedir.")
        elif button_name == "add_btn":
            if self.Data_Control_Func(workspace_name,"Space"):
                data_id = self.workspacedb.find().sort({"_id": -1}).limit(1).to_list()
                if data_id:
                    data_id = int(data_id[0]['_id'])+1
                else:
                    data_id = 1
                data = {'_id':None,'name':None,"parent":None} 
                data['_id'] = data_id
                data['name'] = str(workspace_name)
                data['parent'] = new_parent_id
                self.workspacedb.insert_one(data)
                
                self.bildirim("Çalışma Alanı Oluşturulmuştur.")
                Frame = self.content_child_frame.findChildren(QFrame,"ws_item")
                if Frame:
                    Frame= Frame[0]
                    Frame.deleteLater()
                self.workspace_list_panel()
            else:
                self.bildirim(f'Çalışma Alanı adı boş olamaz veya boşluk ile başlayamaz !!')
# ----------------------------------------------------------------- WorkSpace ------------------------------------------------------------------------------------        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # THEME_ID = 0
    # if os.path.exists("user_config.cfg"):
    #     config = configparser.ConfigParser()
    #     config.read('user_config.cfg')
    #     THEME_ID = config['DEFAULT'].getint('user_theme')
    # else:
    #     with open("user_config.cfg", 'w') as file:
    #         config = configparser.ConfigParser()
    #         lines_to_write = [{"user_theme":0}]
    #         config['DEFAULT'] = lines_to_write[0]
    #         with open('user_config.cfg', 'w') as configfile:
    #             config.write(configfile)
    # user= str(getpass.getuser())  

    # result = subprocess.run(
    #         ['wmic', 'useraccount', 'where', f'name ="{user}"', 'get', 'sid'],
    #         capture_output=True,
    #         text=True,
    #         encoding='utf-8',
    #         errors='ignore'  # Hatalı karakterleri atlar
    #     )

    # sid_raw_data = result.stdout.strip().split("\n")
    # sid=None

    # for raw_sid_item in sid_raw_data[1:]:
    #         if raw_sid_item.strip():
    #             sid = raw_sid_item

    # cp = Cipher()

    # perm =None
    # user_id = None
    # user_name = None
    # ws_id = None
    # window = None

    # if sid == None:
    #     window = SuperAdminMenu(THEME_ID,user,0,0,"Yetkisiz")
    # else:
    #     load_dotenv(dotenv_path='db_inf.env')
    #     uri = os.getenv('SERVER_URI')
    #     client = MongoClient(uri, tlsCAFile=certifi.where())
    #     database = client["VisitPanelDB"]
    #     userdb = database["users_data"]

    #     for user_list in userdb.find({"username":user}):
    #         SID = cp.decript(user_list["SID"])
    #         if sid == SID:
    #             perm = user_list['permission']
    #             user_id=user_list["_id"]
    #             user_name=user_list["username"]
    #             ws_id=user_list["workspace_id"]
    #             break
        
    #     if user_id != None:
    #         window = SuperAdminMenu(THEME_ID=THEME_ID,user=user_name,user_id=user_id,ws_id=ws_id,perm=perm)
    #     else:
    #         window = SuperAdminMenu(THEME_ID,user,0,0,"Yetkisiz")
    
    window = SuperAdminMenu(0,"sistemdestek",1,1,"Admin")
    window.show()
    sys.exit(app.exec())