from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,QFrame,QHBoxLayout,QLineEdit,QPushButton,QComboBox,QSizePolicy,QSpacerItem,QTableWidget,QTableWidgetItem,QMessageBox,QDateEdit,QTextEdit
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
from datetime import datetime
import configparser
import getpass
import subprocess
from dotenv import load_dotenv
import ast

class Content_Button_Menu():
    def __init__(self,parent,BORDER_COLOR,WIN_COLOR,FONT_COLOR,PANEL_COLOR,OS_RED,ON_HOVER_OS_RED):
        self.BORDER_COLOR = BORDER_COLOR
        self.WIN_COLOR = WIN_COLOR
        self.FONT_COLOR = FONT_COLOR
        self.PANEL_COLOR = PANEL_COLOR
        self.OS_RED = OS_RED
        self.ON_HOVER_OS_RED = ON_HOVER_OS_RED

        btn_menu_frm = QFrame(parent)
        btn_menu_frm.setFixedSize(parent.width(),40)
        btn_menu_frm.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius:25px;border-bottom-right-radius:0px;border-top-right-radius:0px;border-bottom-left-radius:0px;")
        btn_menu_frm.move(0,0)

        self.btn_menu_h_layout = QHBoxLayout(btn_menu_frm)
        self.btn_menu_h_layout.setContentsMargins(0,0,0,0)
        self.btn_menu_h_layout.setSpacing(0)
        self.spacer = QSpacerItem(1,39,QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.btn_menu_h_layout.addItem(self.spacer)

        self.left_btn_sheet = f"""QPushButton {{color:{self.FONT_COLOR};background-color:{self.PANEL_COLOR};font-size:14px;border: 0;border-right:1px solid {self.BORDER_COLOR}; border-bottom:1px solid {self.BORDER_COLOR}; border-radius:0;border-top-left-radius:25px; font-weight:bold;}} QPushButton:hover{{background-color:{self.BORDER_COLOR};}} """
        self.left_btn_clicked_sheet = f"""QPushButton {{color:{self.FONT_COLOR};background-color:{self.OS_RED};font-size:14px;border: 0;border-right:1px solid {self.BORDER_COLOR}; border-bottom:1px solid {self.BORDER_COLOR}; border-radius:0;border-top-left-radius:25px; font-weight:bold;}} QPushButton:hover{{background-color:{self.ON_HOVER_OS_RED};}} """
        self.btn_sheet=f"""QPushButton {{color:{self.FONT_COLOR};background-color:{self.PANEL_COLOR};font-size:14px;border: 0;border-right:1px solid {self.BORDER_COLOR}; border-bottom:1px solid {self.BORDER_COLOR}; border-radius:0; font-weight:bold;}} QPushButton:hover{{background-color:{self.BORDER_COLOR};}} """
        self.btn_clicked_sheet = f"""QPushButton {{color:{self.FONT_COLOR};background-color:{self.OS_RED};font-size:14px;border: 0;border-right:1px solid {self.BORDER_COLOR}; border-bottom:1px solid {self.BORDER_COLOR}; border-radius:0; font-weight:bold;}} QPushButton:hover{{background-color:{self.ON_HOVER_OS_RED};}} """
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
                                    color:{self.FONT_COLOR};
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
                                    color:{self.FONT_COLOR};
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
                yetkipaneli_button = QPushButton(" Yetkilendirme")
                yetkipaneli_button.setStyleSheet(self.btnstyle)
                yetkipaneli_button.setObjectName("2")
                yetkipaneli_button.setFixedSize(MenuPanel.width()-5,50)
                yetkipaneli_button.clicked.connect(self.left_menu_click) 

                frmprs = QPushButton(" Kişiler")
                frmprs.setStyleSheet(self.btnstyle)
                frmprs.setFixedSize(MenuPanel.width()-5,50)
                frmprs.setObjectName("4")
                frmprs.clicked.connect(self.left_menu_click) 

            reports = QPushButton(" Kişisel Raporlar")
            reports.setStyleSheet(self.btnstyle)
            reports.setFixedSize(MenuPanel.width()-5,50)
            reports.setObjectName("5")
            reports.clicked.connect(self.left_menu_click) 

            new_meet = QPushButton(" Yeni Toplantı")
            new_meet.setStyleSheet(self.btnstyle)
            new_meet.setFixedSize(MenuPanel.width()-5,50)
            new_meet.setObjectName("6")
            new_meet.clicked.connect(self.left_menu_click) 

            new_desing = QPushButton(" Yeni Menü")
            new_desing.setStyleSheet(self.btnstyle)
            new_desing.setFixedSize(MenuPanel.width()-5,50)
            new_desing.setObjectName("8")
            new_desing.clicked.connect(self.left_menu_click) 

            ayarlar = QPushButton(" Ayarlar")
            ayarlar.setStyleSheet(self.btnstyle)
            ayarlar.setFixedSize(MenuPanel.width()-5,50)
            ayarlar.setObjectName("7")
            # self.ayarlar.clicked.connect(self.ayarlar_click) 
            if self.user_perm in("Admin","Müdür") :
                self.Menu_layout.addWidget(yetkipaneli_button)
                self.Menu_layout.addWidget(frmprs)
                self.Menu_layout.addWidget(new_desing)
            self.Menu_layout.addWidget(reports)
            self.Menu_layout.addWidget(new_meet,0,Qt.AlignTop)
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
        
        if buton_id == 2:#Permission Top Menü
            btn_menu = Content_Button_Menu(self.contentpanel,self.BORDER_COLOR,self.WIN_COLOR,self.FONT_COLOR,self.PANEL_COLOR,self.OS_RED,self.ON_HOVER_OS_RED)
            btn_menu.new_btn("Ekle",self.insert_perm_user_panel)
            btn_menu.new_btn("Güncelle",self.update_perm_user_panel)
            btn_menu.new_btn("Yetkililer",self.list_users)
            btn_menu.new_btn("Tara",self.scan_locale_user_data)
        elif buton_id == 4:#Kişiler Top Menü
            btn_menu = Content_Button_Menu(self.contentpanel,self.BORDER_COLOR,self.WIN_COLOR,self.FONT_COLOR,self.PANEL_COLOR,self.OS_RED,self.ON_HOVER_OS_RED)
            btn_menu.new_btn("Ekle",self.frm_prs_insert_panel)
            btn_menu.new_btn("Güncelle",self.frm_prs_update_panel)
            btn_menu.new_btn("Kişiler",self.prs_list_panel)
        elif buton_id == 5:#Kişisel Raporlar
            btn_menu = Content_Button_Menu(self.contentpanel,self.BORDER_COLOR,self.WIN_COLOR,self.FONT_COLOR,self.PANEL_COLOR,self.OS_RED,self.ON_HOVER_OS_RED)
            btn_menu.new_btn("Firma Bazlı",self.frm_based_report_panel)
            btn_menu.new_btn("Kiş Bazlı",self.person_based_report_panel)
        elif buton_id == 8:#Kişisel Raporlar
            btn_menu = Content_Button_Menu(self.contentpanel,self.BORDER_COLOR,self.WIN_COLOR,self.FONT_COLOR,self.PANEL_COLOR,self.OS_RED,self.ON_HOVER_OS_RED)
            btn_menu.new_btn("Workspaces",self.workspace_list_panel)
            btn_menu.new_btn("Yetkiler",None)
            btn_menu.new_btn("Firmalar",self.frm_list_panel)
            btn_menu.new_btn("Kişiler",None)
        elif buton_id == 6:#Kişiler Top Menü
            self.New_Meet_Menu()

        Menu_layout = QVBoxLayout(self.contentpanel)
        Menu_layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.contentpanel,0,QtCore.Qt.AlignRight)
    
    def bildirim(self,text):
        notification.notify(
                    title='Admin Panel Bildirim',
                    message=text,
                    app_name='OS_VPanel',
                )

    def workspace_combo_set_items(self,combobox,durum):#Çalışma alanı comboboxları için gereken güncelleme fonksiyonu
        combobox.clear()
        if durum == 1: # Sadece Ana Workspaceleri yazdırır
            for item in self.workspacedb.find({'parent':0}):
                combobox.addItem(item['name'],userData = item['_id'])
        elif durum == 2:# hepsini ebevenyni ile yazdırır
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
                }]
            for item in self.workspacedb.aggregate(sql):
                if item['parent'] == 0:
                    combobox.addItem("Main Workspace > "+item['name'],userData=item['_id'])
                else:
                    combobox.addItem(item["parent_name"]["name"]+" > "+item['name'],userData=item['_id'])
        elif durum == 3:
            sender = self.sender()
            print(sender)
            for item in self.workspacedb.find({'parent':sender.itemData(sender.currentIndex())}):
                combobox.addItem(item['name'],userData=item['_id'])    

    def change_combo_set_combo(self,combobox,durum,itemdata):# tasarım alanlarındaki comboboxları duruma göre yapılandırma
        match durum:
            case 1:# seçilen çalışma alanının altındakileri gösterir eğer seçilen item değilse resetler 
                if itemdata == -1:
                    combobox.clear()
                    combobox.insertItem(0,"Please Parent Select First..",userData=0)
                    combobox.setCurrentIndex(0)
                elif isinstance(itemdata,int):
                    combobox.clear()
                    combobox.insertItem(0,"Select Any Workspace.",userData=0)
                    combobox.setCurrentIndex(0)
                    for item in self.workspacedb.find({'parent':int(itemdata)}):
                        combobox.addItem(item['name'],userData=item['_id'])
            case 2:# Textboxları comboboxın yazısı ile eşleme (güncelleme ekranlarında isim girmekle uğraşılmasın diye)
                if itemdata == "reset":
                    combobox.setText("")
                    combobox.setPlaceholderText("Enter New Name..") 
                else:
                    combobox.setText(itemdata)
            case 3:#
                if itemdata == -1:
                    combobox.clear()
                    combobox.insertItem(0,"Please Workspace Select First..",userData=0)
                    combobox.setCurrentIndex(0)
                elif itemdata == 0:
                    combobox.clear()
                    sql = [
                            {
                                '$lookup':{
                                    'from':'workspace_list',
                                    'localField':'workspace_id',
                                    'foreignField': '_id',
                                    'as':'workspace_name'
                                }
                            },
                            {
                                '$unwind':{
                                    'path':'$workspace_name',
                                    'preserveNullAndEmptyArrays':True
                                }
                            }]
                    combobox.insertItem(0,"select any user!",userData=0)
                    for item in self.usersdatadb.aggregate(sql):
                        combobox.addItem(item['real_name']+" - "+item['username']+" - "+item['workspace_name']['name']+" - "+item['permission'] ,userData=item['_id'])
                elif isinstance(itemdata,int):
                    combobox.clear()
                    sql = [
                            {
                                '$lookup':{
                                    'from':'workspace_list',
                                    'localField':'workspace_id',
                                    'foreignField': '_id',
                                    'as':'workspace_name'
                                }
                            },
                            {
                                '$unwind':{
                                    'path':'$workspace_name',
                                    'preserveNullAndEmptyArrays':True
                                }
                            },
                            {
                                '$match':{
                                    'workspace_id':int(itemdata)
                                }
                            }]
                    combobox.insertItem(0,"select any user!",userData=0)
                    for item in self.usersdatadb.aggregate(sql):
                        combobox.addItem(item['real_name']+" - "+item['username']+" - "+item['workspace_name']['name']+" - "+item['permission'] ,userData=item['_id'])
            case 4:# seçime bağlı firmaları listeler
                if itemdata == 0:
                    combobox.clear()
                    combobox.insertItem(0,"Please Parent Select First..",userData=0)
                    combobox.setCurrentIndex(0)
                elif isinstance(itemdata,int):
                    combobox.clear()
                    combobox.insertItem(0,"Select any firm!",userData=0)
                    for item in self.frmdb.find({'workspace_id':itemdata}):
                        combobox.addItem(item['name'],userData=item['_id'])
            case 5:
                if itemdata == 0:
                    combobox.clear()
                    combobox.insertItem(0,"Please Parent Select First..",userData=0)
                    combobox.setCurrentIndex(0)
                elif isinstance(itemdata,int):
                    combobox.clear()
                    combobox.insertItem(0,"Select any person!",userData=0)
                    for item in self.prsdb.find({'frm_id':itemdata}):
                        combobox.addItem(item['fullname']+" - "+item['mail'],userData=item['_id'])

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
        meet_text_area.setFixedSize(width,height)
        yatay_layout_4.addWidget(meet_text_area)

        dikey_layout.addLayout(yatay_layout_3)
        dikey_layout.addLayout(yatay_layout_4)
        return dikey_layout
# ---------------------------------------------------------------------- Ortak Fonksiyonlar -----------------------------------------------------------------------------------------

# ------------------------------------------------------------------------ Ortak Widgetlar ------------------------------------------------------------------------------------------
    def common_elements(self,widget_name:str,name:str):
        frame_x = self.contentpanel.width()
        match widget_name:
            case "workspace_lister":
                combobox = QComboBox()
                combobox.setStyleSheet(self.combobox_style)
                combobox.setFixedSize(frame_x-200, 25)
                combobox.setObjectName(name)
                self.workspace_combo_set_items(combobox,1)
                combobox.insertItem(0,"Select Workspace Area..",userData=-1)
                combobox.insertItem(1,"Main Workspaces",userData=0)
                combobox.setCurrentIndex(0)
                return combobox
            case "clear_list_combo":
                combobox = QComboBox()
                combobox.setStyleSheet(self.combobox_style)
                combobox.setFixedSize(frame_x-200, 25)
                combobox.setObjectName(name)
                combobox.insertItem(0,"Please Parent Select First..",userData=0)
                combobox.setCurrentIndex(0)
                return combobox
            case "TextBox":
                textbox = QLineEdit()
                textbox.setFixedSize(frame_x-200,25)
                textbox.setObjectName(name)
                textbox.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.PANEL_COLOR};border-radius: 5px;color:{self.FONT_COLOR};")
                textbox.setPlaceholderText("Enter New Name..")
                return textbox
            case "button_add":
                btn = QPushButton("Ekle")
                btn.setStyleSheet(self.normal_button)
                btn.setFixedSize(100,30)
                return btn
            case "button_update":
                btn = QPushButton("Güncelle")
                btn.setStyleSheet(self.normal_button)
                btn.setFixedSize(100,30)
                return btn
            case "ws_list":
                combobox = QComboBox()
                combobox.setStyleSheet(self.combobox_style)
                combobox.setFixedSize(frame_x-200, 25)
                combobox.setObjectName(name)
                self.workspace_combo_set_items(combobox,1)
                combobox.insertItem(0,"Select Any Workspace..",userData=0)
                combobox.setCurrentIndex(0)
                return combobox
# ------------------------------------------------------------------------ Ortak Widgetlar ------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------- NEW MEET ---------------------------------------------------------------------------------------------
    def New_Meet_Menu(self):
        if self.content_child_frame is not None:
            for child in self.content_child_frame.findChildren(QWidget):
                child.deleteLater()
        if self.content_child_frame.layout():
            QWidget().setLayout(self.content_child_frame.layout())

        dikey_layout = QVBoxLayout(self.content_child_frame)
        yatay_layout_1 = QHBoxLayout()
        frame_x = (self.contentpanel.width()-20)/2

        frm_list = self.common_elements("clear_list_combo","frm_list")
        frm_list.setFixedWidth(frame_x)

        person_list = self.common_elements("clear_list_combo","person_list")
        person_list.setFixedWidth(frame_x)

        self.change_combo_set_combo(frm_list,4,self.user_workspace_id)
        frm_list.currentIndexChanged.connect(lambda index:self.change_combo_set_combo(person_list,5,frm_list.itemData(index)))

        yatay_layout_1.addWidget(frm_list)
        yatay_layout_1.addWidget(person_list)

        frm_list.move(0,0)

        yatay_layout_2 = QHBoxLayout()

        meet_header = self.common_elements("TextBox","meet_header")
        meet_header.setFixedWidth(frame_x+100)
        meet_header.setPlaceholderText("Enter Meet Header..")

        date_picker = QDateEdit()
        date_picker.setDate(QDate.currentDate())
        date_picker.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.PANEL_COLOR};border-radius: 5px;color:{self.FONT_COLOR};")
        date_picker.setObjectName("Date_Picker")
        date_picker.setFixedHeight(25)

        yatay_layout_2.addWidget(meet_header)
        yatay_layout_2.addWidget(date_picker)

        yatay_layout_3= self.Style_Editable_Text(self.contentpanel.width()-20,550,"New_Meet")

        dikey_layout.addLayout(yatay_layout_1)
        dikey_layout.addLayout(yatay_layout_2)
        dikey_layout.addLayout(yatay_layout_3)

        self.content_child_frame.setLayout(dikey_layout)
    
    def new_meet(self):
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
                        self.bildirim("Toplantı Oluşturulmuştur!!")
                        self.New_Meet_Menu()
                else:
                    self.bildirim("Lütfen Bir Kişi seçiniz")
        elif button_name == "Edit_Text":
            textbox = self.findChildren(QTextEdit,"MeetTextArea")[0]
            meet_id = self.findChildren(QFrame,"editmeet")[0]
            meet_id = meet_id.property("meet_id")  
            textbox = textbox.toHtml()
            self.conversations.update_one({"_id":meet_id},{"$set":{"file_data":textbox}})
            self.bildirim("Toplantı Notu Güncellendi!!")
        
    def MeetTextStyleFunction(self):
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

# ---------------------------------------------------------------------------- Raporlar ---------------------------------------------------------------------------------------------
    def person_based_report_panel(self):
        if self.content_child_frame is not None:
            for child in self.content_child_frame.findChildren(QWidget):
                child.deleteLater()
        if self.content_child_frame.layout():
            QWidget().setLayout(self.content_child_frame.layout()) 

        dikey_layout = QVBoxLayout(self.content_child_frame)
        yatay_layout = QHBoxLayout()
        frame_x = (self.contentpanel.width()-20)/2

        frm_list = self.common_elements("clear_list_combo","frm_list")
        frm_list.setFixedWidth(frame_x)

        self.change_combo_set_combo(frm_list,4,self.user_workspace_id)
        frm_list.currentIndexChanged.connect(self.person_based_report)

        yatay_layout.setAlignment(Qt.AlignTop)
        yatay_layout.addWidget(frm_list)

        date_db = self.common_elements("clear_list_combo","date")
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
                    date_db.currentIndexChanged.connect(self.person_based_report)
        
        

        date_db.setFixedWidth(frame_x)
        yatay_layout.addWidget(date_db)
        dikey_layout.addLayout(yatay_layout)
        dikey_layout.addSpacerItem(QSpacerItem(self.contentpanel.width(), self.contentpanel.height()-100, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.content_child_frame.setLayout(dikey_layout)
    
    def person_based_report(self,index):
        tablo = self.content_child_frame.findChildren(QTableWidget,"person_based")
        frame_x = self.contentpanel.width()
        frame_y = self.contentpanel.height()
        if tablo:
            tablo= tablo[0]
            tablo.deleteLater()
        
        frm_id = self.content_child_frame.findChildren(QComboBox,"frm_list")[0]
        frm_id = frm_id.itemData(frm_id.currentIndex())

        date = self.content_child_frame.findChildren(QComboBox,"date")[0]
        date = date.itemData(date.currentIndex())
        #,"year-month":{"$dateToString":{"format":"%Y-%m","date":"$create_date"}}
        if isinstance(frm_id,int):
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
                sorgu = self.conversations.aggregate(sql).to_list(None)
                person_ids = []
                for i in sorgu:
                    if i['person_id'] not in person_ids:
                        person_ids.append(int(i["person_id"]))
                row= len(person_ids)
                header = ['Tam Adı','Mail',"Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]
                tablo = CustomTableWidget(row+1,len(header),self.content_child_frame)
                tablo.setObjectName("person_based")
                tablo.setStyleSheet(f"""QTableWidget{{
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
                                    }}""")
                tablo.horizontalHeader().setVisible(False)
                tablo.verticalHeader().setVisible(False)
                tablo_max_width=int((frame_x-150)/3)-1
                tablo.setColumnWidth(0, 150)
                tablo.setColumnWidth(1, 200)
                for i in range(12):
                    tablo.setColumnWidth(i+2, 75)
                tablo.setFixedSize(frame_x,frame_y-110)
                tablo.move(0,45)
                tablo.setEditTriggers(QTableWidget.NoEditTriggers)
    
                for col in range(len(header)):
                    item = QTableWidgetItem(header[col])
                    item.setTextAlignment(Qt.AlignCenter) 
                    item.setBackground(QColor(self.BORDER_COLOR))
                    tablo.setItem(0,col,item) 
                    tablo.show()
                row_num=1
                sql_header = ['person_name','person_mail','month','visit_count']
                row_id = 0
                for item in sorgu:
                    if row_id == item["person_id"]:
                        row_num -= 1
                        table_item_kontrol= tablo.item(row_num,int(item[sql_header[2]])+1)
                        if table_item_kontrol != None:
                            visit_num = int(table_item_kontrol.text())+int(item[sql_header[3]])
                            table_item = QTableWidgetItem(str(visit_num))
                        else:
                            table_item = QTableWidgetItem(str(item[sql_header[3]]))
                        table_item.setTextAlignment(Qt.AlignCenter) 
                        table_item.setBackground(QColor(self.BORDER_COLOR))
                        tablo.setItem(row_num,int(item[sql_header[2]])+1,table_item)
                    else:
                        for i in range(len(sql_header)):
                            if i != 2:
                                table_item = QTableWidgetItem(str(item[sql_header[i]]))
                                table_item.setTextAlignment(Qt.AlignCenter) 
                                table_item.setBackground(QColor(self.BORDER_COLOR))
                                tablo.setItem(row_num,i,table_item)
                                if i == 0:
                                    tablo.item(row_num,i).setData(Qt.UserRole,item["person_id"])
                            else:
                                table_item = QTableWidgetItem(str(item[sql_header[i+1]]))
                                table_item.setTextAlignment(Qt.AlignCenter) 
                                table_item.setBackground(QColor(self.BORDER_COLOR))
                                tablo.setItem(row_num,int(item[sql_header[i]])+1,table_item)
                                break
                    row_num += 1
                    row_id = item["person_id"]
                tablo.cellDoubleClicked.connect(self.person_based_report_detail_click)
    
    def person_based_report_detail_click(self,row,col):
        tablo = self.content_child_frame.findChildren(QTableWidget,"person_based")[0]
        max_row = tablo.rowCount()
        date = self.content_child_frame.findChildren(QComboBox,"date")[0]
        date = date.itemData(date.currentIndex())
        if row == 0: # Başlık kısmına tıklandı ise
            if col > 1: #başlık kısmında aylardan birine tıklandı ise
                visit_count = False
                for i in range(1,max_row):
                    item = tablo.item(i,col)
                    if item != None:
                        visit_count = True
                        break
                if visit_count: # Eğer o ay içerisinde herhangi bir ziyaret varsa panelde detayları gösterecek
                    frm_id = self.content_child_frame.findChildren(QComboBox,"frm_list")[0]
                    frm_id = frm_id.itemData(frm_id.currentIndex())
                    sql =[{
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
                                "year-month":{"$dateToString":{"format":"%Y-%m-%d","date":"$create_date"}},
                                "create_date":1,
                                "person_name":"$person_name.fullname",
                                "person_mail":"$person_name.mail",
                                "person_frm_id":"$person_name.frm_id",
                                "cst_header":1
                            }
                        },
                        {
                            "$match":{
                                "person_frm_id":int(frm_id),
                                "$expr": {
                                 "$eq": [{ "$month": "$create_date" }, col-1]
                                 }
                                }
                        }
                        ]
                    if date > 1 :
                        sql.append({
                            "$match":{
                                "$expr": {
                                 "$eq": [{ "$year": "$create_date" }, date]
                                 }
                                }
                        })
                    data = self.conversations.aggregate(sql)
                    self.ReportDetailsTable(data)
        else:# kişi tablosuna tıklandıysa
            if col == 0:#Kişiye Tıklandıysa
                item = tablo.item(row,col)
                item = item.data(Qt.UserRole)
                sql =[{
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
                                "year-month":{"$dateToString":{"format":"%Y-%m-%d","date":"$create_date"}},
                                "create_date":1,
                                "person_name":"$person_name.fullname",
                                "person_mail":"$person_name.mail",
                                "person_frm_id":"$person_name.frm_id",
                                "cst_header":1
                            }
                        },
                        {
                            "$match":{
                                "person_id":int(item)
                                }
                        }
                        ]
                if date > 1 :
                        sql.append({
                            "$match":{
                                "$expr": {
                                 "$eq": [{ "$year": "$create_date" }, date]
                                 }
                                }
                        })
                data = self.conversations.aggregate(sql)
                self.ReportDetailsTable(data)#Kişiye ait visitleri detaylarını gösteren pencereyi açacak
            elif col > 1:# kişinin belli bir ayına tıklandıysa
                item =  tablo.item(row,col)
                if item != None:
                    person_id = tablo.item(row,0)
                    person_id = person_id.data(Qt.UserRole)
                    frm_id = self.content_child_frame.findChildren(QComboBox,"frm_list")[0]
                    frm_id = frm_id.itemData(frm_id.currentIndex())
                    sql =[{
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
                                "year-month":{"$dateToString":{"format":"%Y-%m-%d","date":"$create_date"}},
                                "create_date":1,
                                "person_name":"$person_name.fullname",
                                "person_mail":"$person_name.mail",
                                "person_frm_id":"$person_name.frm_id",
                                "cst_header":1
                            }
                        },
                        {
                            "$match":{
                                "person_frm_id":int(frm_id),
                                "person_id":person_id,
                                "$expr": {
                                 "$eq": [{ "$month": "$create_date" }, col-1]
                                 }
                                }
                        }
                        ]
                    if date > 1 :
                        sql.append({
                            "$match":{
                                "$expr": {
                                 "$eq": [{ "$year": "$create_date" }, date]
                                 }
                                }
                        })
                    data = self.conversations.aggregate(sql)
                    self.ReportDetailsTable(data)
                    
    def ReportDetailsTable(self,data):
        MenuPanel = QFrame(self)
        MenuPanel.setFixedSize(self.width(),763)
        MenuPanel.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius:10px;border-top-left-radius:0px;border-top-right-radius:0px;border-right:0;border-top:0;")

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

        sorgu = data.to_list(None)
        row= len(sorgu)
        header = ['Tam Adı','Mail','Toplantı Tarihi','Toplantı Başlığı','Detay']
        tablo = QTableWidget(row+1,len(header),MenuPanel)
        tablo.setStyleSheet(f"""QTableWidget{{
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
                            }}""")
        tablo.horizontalHeader().setVisible(False)
        tablo.verticalHeader().setVisible(False)
        tablo_max_width=int((MenuPanel.width()-375)/2)-1
        tablo.setColumnWidth(0, 200)
        tablo.setColumnWidth(1, tablo_max_width)
        tablo.setColumnWidth(2, 100)
        tablo.setColumnWidth(3, tablo_max_width)
        tablo.setColumnWidth(4, 75)
        tablo.setFixedSize(MenuPanel.width(),MenuPanel.height()-45)
        tablo.move(0,35)
        
        for col in range(len(header)):
            item = QTableWidgetItem(header[col])
            item.setTextAlignment(Qt.AlignCenter) 
            item.setBackground(QColor(self.BORDER_COLOR))
            item.setFlags(QtCore.Qt.ItemIsEnabled) 
            tablo.setItem(0,col,item) 
            tablo.show()
        row_num=1
        sql_header = ['person_name','person_mail','year-month','cst_header','_id']
        for item in sorgu:
            for i in range(len(sql_header)):
                if i == len(sql_header)-1:
                    detail_btn = QPushButton("Detay")
                    detail_btn.setStyleSheet(self.normal_button)
                    detail_btn.setProperty("_id",item[sql_header[i]])
                    detail_btn.clicked.connect(self.Meet_Details)
                    tablo.setCellWidget(row_num,i,detail_btn)
                else:
                    table_item = QTableWidgetItem(str(item[sql_header[i]]))
                    table_item.setTextAlignment(Qt.AlignCenter) 
                    table_item.setFlags(QtCore.Qt.ItemIsEnabled) 
                    tablo.setItem(row_num,i,table_item)
            row_num += 1

        MenuPanel.move(0,37)
        MenuPanel.show()

    def Meet_Details(self):
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

        button = self.sender()
        button_id = button.property("_id")  
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
        conversation_text=None
        
        MenuPanel.move(0,37)
        MenuPanel.show()

    def frm_based_report_panel(self):
        if self.content_child_frame is not None:
            for child in self.content_child_frame.findChildren(QWidget):
                child.deleteLater()
        if self.content_child_frame.layout():
            QWidget().setLayout(self.content_child_frame.layout()) 

        dikey_layout = QVBoxLayout(self.content_child_frame)
        yatay_layout = QHBoxLayout()
        frame_x = (self.contentpanel.width()-20)/2

        date_db = self.common_elements("clear_list_combo","date")
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
                date_db.addItem("Tüm Zamanlar",userData=1)
                for i in range(min_year,max_year+1):
                    date_db.addItem(str(i),userData=int(i)) 


        date_db.setFixedWidth(frame_x)
        date_db.currentIndexChanged.connect(self.frm_based_report)
        yatay_layout.setAlignment(Qt.AlignTop)
        yatay_layout.addWidget(date_db,0,Qt.AlignCenter)
        dikey_layout.addLayout(yatay_layout)
        dikey_layout.addSpacerItem(QSpacerItem(self.contentpanel.width(), self.contentpanel.height()-100, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.content_child_frame.setLayout(dikey_layout)

    def frm_based_report(self):
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
                        "$match":{
                            "user_id":int(self.user_id)
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
                            "frm_name":"$frm.name"
                        }
                    },
                    {
                        "$group":{
                            "_id":{"year":"$year","month":"$month","person_frm_id":"$person_frm_id","frm_name":"$frm_name"},
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
                            "_id":0
                        }
                    },{"$sort":{"frm_id":1}}]
            if date > 1 :
                sql.append({"$match":{"year":int(date)}})
            sorgu = self.conversations.aggregate(sql).to_list(None)
            frm_ids = []
            for i in sorgu:
                if i['frm_id'] not in frm_ids:
                    frm_ids.append(int(i["frm_id"]))
            row= len(frm_ids)+1
            header = ['Firma Adı',"Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]
            tablo = CustomTableWidget(row,len(header),self.content_child_frame)
            tablo.setObjectName("frm_based")
            tablo.setStyleSheet(f"""QTableWidget{{
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
                                }}""")
            tablo.horizontalHeader().setVisible(False)
            tablo.verticalHeader().setVisible(False)
            tablo.setColumnWidth(0, 200)
            for i in range(12):
                tablo.setColumnWidth(i+1, 75)
            tablo.setFixedSize(frame_x,frame_y-110)
            tablo.move(0,45)
            tablo.setEditTriggers(QTableWidget.NoEditTriggers)

            for col in range(len(header)):
                item = QTableWidgetItem(header[col])
                item.setTextAlignment(Qt.AlignCenter) 
                item.setBackground(QColor(self.BORDER_COLOR))
                tablo.setItem(0,col,item) 
                tablo.show()
            row_num=1
            row_id = 0
            for item in sorgu:
                if row_id == item["frm_id"]:
                    row_num -= 1
                    past_item = tablo.item(row_num,int(item['month']))
                    if past_item != None:
                        visit_num = int(past_item.text()) + int(item['visit_count'])
                        table_item = QTableWidgetItem(str(visit_num))
                    else:
                        table_item = QTableWidgetItem(str(item['visit_count']))
                    table_item.setTextAlignment(Qt.AlignCenter) 
                    table_item.setBackground(QColor(self.BORDER_COLOR))
                    tablo.setItem(row_num,int(item['month']),table_item)
                else:
                    table_item = QTableWidgetItem(str(item['frm_name']))
                    table_item.setTextAlignment(Qt.AlignCenter) 
                    table_item.setBackground(QColor(self.BORDER_COLOR))
                    tablo.setItem(row_num,0,table_item)
                    tablo.item(row_num,0).setData(Qt.UserRole,item["frm_id"])

                    table_item = QTableWidgetItem(str(item['visit_count']))
                    table_item.setTextAlignment(Qt.AlignCenter) 
                    table_item.setBackground(QColor(self.BORDER_COLOR))
                    tablo.setItem(row_num,int(item['month']),table_item)
                row_num += 1
                row_id = item["frm_id"]
            tablo.cellDoubleClicked.connect(self.frm_based_report_detail_click)
   
    def frm_based_report_detail_click(self,row,col):
        tablo = self.content_child_frame.findChildren(QTableWidget,"frm_based")[0]
        max_row = tablo.rowCount()
        date = self.content_child_frame.findChildren(QComboBox,"date")[0]
        date = date.itemData(date.currentIndex())
        if row == 0: # Başlık kısmına tıklandı ise    
            if col > 1: #başlık kısmında aylardan birine tıklandı ise
                visit_count = False
                for i in range(1,max_row):
                    item = tablo.item(i,col)
                    if item != None:
                        visit_count = True
                        break
                if visit_count: # Eğer o ay içerisinde herhangi bir ziyaret varsa panelde detayları gösterecek
                    date = self.content_child_frame.findChildren(QComboBox,"date")[0]
                    date = date.itemData(date.currentIndex())
                    sql =[{
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
                                "year-month":{"$dateToString":{"format":"%Y-%m-%d","date":"$create_date"}},
                                "create_date":1,
                                "person_name":"$person_name.fullname",
                                "person_mail":"$person_name.mail",
                                "person_frm_id":"$person_name.frm_id",
                                "cst_header":1
                            }
                        },
                        {
                            "$match":{
                                "$expr": {
                                 "$eq": [{ "$month": "$create_date" }, col]
                                 }
                                }
                        }
                        ]
                    if date > 1 :
                        sql.append({
                            "$match":{
                                "$expr": {
                                 "$eq": [{ "$year": "$create_date" }, date]
                                 }
                                }
                        })
                    data = self.conversations.aggregate(sql)
                    self.ReportDetailsTable(data)
        else:# Firma tablosuna tıklandıysa
            if col == 0:#Firmaya Tıklandıysa
                frm_id = tablo.item(row,col)
                frm_id = frm_id.data(Qt.UserRole)
                sql =[{
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
                                "year-month":{"$dateToString":{"format":"%Y-%m-%d","date":"$create_date"}},
                                "create_date":1,
                                "person_name":"$person_name.fullname",
                                "person_mail":"$person_name.mail",
                                "person_frm_id":"$person_name.frm_id",
                                "cst_header":1
                            }
                        },
                        {
                            "$match":{
                                "person_frm_id":int(frm_id)
                                }
                        }
                        ]
                if date > 1 :
                        sql.append({
                            "$match":{
                                "$expr": {
                                 "$eq": [{ "$year": "$create_date" }, date]
                                 }
                                }
                        })
                data = self.conversations.aggregate(sql)
                self.ReportDetailsTable(data)#Kişiye ait visitleri detaylarını gösteren pencereyi açacak
            elif col > 1:# Firmanın belli bir ayına tıklandıysa
                item =  tablo.item(row,col)
                if item != None:
                    frm_id = tablo.item(row,0)
                    frm_id = frm_id.data(Qt.UserRole)
                    sql =[{
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
                                "year-month":{"$dateToString":{"format":"%Y-%m-%d","date":"$create_date"}},
                                "create_date":1,
                                "person_name":"$person_name.fullname",
                                "person_mail":"$person_name.mail",
                                "person_frm_id":"$person_name.frm_id",
                                "cst_header":1
                            }
                        },
                        {
                            "$match":{
                                "person_frm_id":int(frm_id),
                                "$expr": {
                                 "$eq": [{ "$month": "$create_date" }, col]
                                 }
                                }
                        }
                        ]
                    if date > 1 :
                        sql.append({
                            "$match":{
                                "$expr": {
                                 "$eq": [{ "$year": "$create_date" }, date]
                                 }
                                }
                        })
                    data = self.conversations.aggregate(sql)
                    self.ReportDetailsTable(data)
# ---------------------------------------------------------------------------- Raporlar ---------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------ Kişiler Paneli -------------------------------------------------------------------------------------------
    def frm_prs_insert_panel(self):
        if self.content_child_frame is not None:
            for child in self.content_child_frame.findChildren(QWidget):
                child.deleteLater()

        if self.content_child_frame.layout():
            QWidget().setLayout(self.content_child_frame.layout()) 
 
        dikey_layout = QVBoxLayout(self.content_child_frame)

        workspace_lister = self.common_elements("workspace_lister","item1")
        ws_list = self.common_elements("clear_list_combo","item2")
        frm_list = self.common_elements("clear_list_combo","frm_list")
        prs_name = self.common_elements("TextBox","prs_name")
        prs_mail = self.common_elements("TextBox","prs_mail")
        btn = self.common_elements("button_add","btn")

        prs_mail.textChanged.connect(self.to_lower_case)
        workspace_lister.currentIndexChanged.connect(lambda index:self.change_combo_set_combo(ws_list,1,workspace_lister.itemData(index)))
        ws_list.currentIndexChanged.connect(lambda index:self.change_combo_set_combo(frm_list,4,ws_list.itemData(index)))
        prs_mail.setPlaceholderText("Enter person mail..")
        btn.clicked.connect(self.insert_person_btn_click)

        dikey_layout.setAlignment(Qt.AlignCenter)
        dikey_layout.addWidget(workspace_lister)
        dikey_layout.addWidget(ws_list)
        dikey_layout.addWidget(frm_list)
        dikey_layout.addWidget(prs_name)
        dikey_layout.addWidget(prs_mail)
        dikey_layout.addWidget(btn,0,Qt.AlignCenter)
        dikey_layout.addSpacing(150)

        self.content_child_frame.setLayout(dikey_layout)

    def to_lower_case(self):
        textbox = self.sender()
        text = textbox.text()
        textbox.setText(text.lower())

    def insert_person_btn_click(self):
        frm_id = self.content_child_frame.findChildren(QComboBox,"frm_list")[0]
        frm_id = frm_id.itemData(frm_id.currentIndex())
        prs_name = self.content_child_frame.findChildren(QLineEdit,"prs_name")[0].text()
        prs_mail = self.content_child_frame.findChildren(QLineEdit,"prs_mail")[0].text()
        if frm_id != 0:
            if prs_mail.count(" ") == 0 and prs_mail.count("@") ==1 and prs_mail.count(".") > 0 and prs_mail :
                if self.prsdb.count_documents({'mail':prs_mail,'frm_id':frm_id}) == 0:
                    if prs_name.count(" ") != len(prs_name) and prs_name[0] != " ":
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
                        self.frm_prs_insert_panel()
                    else:
                        self.bildirim("Kişi adı boşluk olamaz veya boşluk ile başlayamaz!!")
                else:
                    self.bildirim("Bu kullanıcı zaten ekli!!")
            else:
                self.bildirim("Uygun bir mail adresi giriniz.")
        else:
            self.bildirim("Önce Kişinin ekleneceği firmayı seçiniz!")
    
    def prs_list_panel(self):
        if self.content_child_frame is not None:
            for child in self.content_child_frame.findChildren(QWidget):
                child.deleteLater()
        if self.content_child_frame.layout():
            QWidget().setLayout(self.content_child_frame.layout()) 

        yatay_layout = QHBoxLayout(self.content_child_frame)
        frame_x = (self.contentpanel.width()-30)/3

        workspace_lister = self.common_elements("workspace_lister","item1")
        ws_list = self.common_elements("clear_list_combo","ws_list")
        frm_list = self.common_elements("clear_list_combo","frm_list")
        workspace_lister.setFixedWidth(frame_x)
        ws_list.setFixedWidth(frame_x)
        frm_list.setFixedWidth(frame_x)

        workspace_lister.currentIndexChanged.connect(lambda index:self.change_combo_set_combo(ws_list,1,workspace_lister.itemData(index)))
        ws_list.currentIndexChanged.connect(lambda index:self.change_combo_set_combo(frm_list,4,ws_list.itemData(index)))
        frm_list.currentIndexChanged.connect(self.prs_list_table)

        yatay_layout.setAlignment(Qt.AlignTop)
        yatay_layout.addWidget(workspace_lister)
        yatay_layout.addWidget(ws_list)
        yatay_layout.addWidget(frm_list)

        self.content_child_frame.setLayout(yatay_layout)
    
    def prs_list_table(self,index):
        tablo = self.content_child_frame.findChildren(QTableWidget,"person_list")
        frame_x = self.contentpanel.width()
        frame_y = self.contentpanel.height()
        if tablo:
            tablo= tablo[0]
            tablo.deleteLater()

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
        if index > 0:
            sql.append({'$match':{'frm_id':self.sender().itemData(index)}})
            sorgu = self.prsdb.aggregate(sql).to_list(None)
            row= len(sorgu)
            header = ['id','Tam Adı','Mail','Firma','Çalışma Alanı']
            tablo = QTableWidget(row+1,len(header),self.content_child_frame)
            tablo.setStyleSheet(f"""QTableWidget{{
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
                                }}""")
            tablo.horizontalHeader().setVisible(False)
            tablo.verticalHeader().setVisible(False)
            tablo_max_width=int((frame_x-150)/3)-1
            tablo.setColumnWidth(0, 50)
            tablo.setColumnWidth(1, 150)
            tablo.setColumnWidth(2, 200)
            tablo.setColumnWidth(3, 200)
            tablo.setColumnWidth(4, 200)
            tablo.setFixedSize(frame_x,frame_y-100)
            tablo.move(0,40)
            
            for col in range(len(header)):
                item = QTableWidgetItem(header[col])
                item.setTextAlignment(Qt.AlignCenter) 
                item.setBackground(QColor(self.BORDER_COLOR))
                item.setFlags(QtCore.Qt.ItemIsEnabled) 
                tablo.setItem(0,col,item) 
                tablo.show()
            row_num=1
            sql_header = ['_id','fullname','mail','frm_name','ws_name']
            for item in sorgu:
                for i in range(len(sql_header)):
                    table_item = QTableWidgetItem(str(item[sql_header[i]]))
                    table_item.setTextAlignment(Qt.AlignCenter) 
                    table_item.setFlags(QtCore.Qt.ItemIsEnabled) 
                    tablo.setItem(row_num,i,table_item)
                row_num += 1

    def frm_prs_update_panel(self):
        if self.content_child_frame is not None:
            for child in self.content_child_frame.findChildren(QWidget):
                child.deleteLater()

        if self.content_child_frame.layout():
            QWidget().setLayout(self.content_child_frame.layout()) 
 
        dikey_layout = QVBoxLayout(self.content_child_frame)

        workspace_lister = self.common_elements("workspace_lister","item1")
        ws_list = self.common_elements("clear_list_combo","item2")
        frm_list = self.common_elements("clear_list_combo","frm_id")
        prs_list = self.common_elements("clear_list_combo","prs_list")
        prs_name = self.common_elements("TextBox","prs_name")
        prs_mail = self.common_elements("TextBox","prs_mail")
        workspace_lister2 = self.common_elements("workspace_lister","item3")
        ws_list2 = self.common_elements("clear_list_combo","item4")
        new_frm_list = self.common_elements("clear_list_combo","new_frm_id")
        btn = self.common_elements("button_update","btn")

        prs_mail.textChanged.connect(self.to_lower_case)
        workspace_lister.currentIndexChanged.connect(lambda index:self.change_combo_set_combo(ws_list,1,workspace_lister.itemData(index)))
        ws_list.currentIndexChanged.connect(lambda index:self.change_combo_set_combo(frm_list,4,ws_list.itemData(index)))
        frm_list.currentIndexChanged.connect(lambda index:self.change_combo_set_combo(prs_list,5,frm_list.itemData(index)))
        prs_mail.setPlaceholderText("Enter person mail..")
        workspace_lister2.currentIndexChanged.connect(lambda index:self.change_combo_set_combo(ws_list2,1,workspace_lister2.itemData(index)))
        ws_list2.currentIndexChanged.connect(lambda index:self.change_combo_set_combo(new_frm_list,4,ws_list2.itemData(index)))
        btn.clicked.connect(self.frm_prs_update_btn_click)

        dikey_layout.setAlignment(Qt.AlignCenter)
        dikey_layout.addWidget(workspace_lister)
        dikey_layout.addWidget(ws_list)
        dikey_layout.addWidget(frm_list)
        dikey_layout.addSpacing(25)
        dikey_layout.addWidget(prs_list)
        dikey_layout.addWidget(prs_name)
        dikey_layout.addWidget(prs_mail)
        dikey_layout.addSpacing(25)
        dikey_layout.addWidget(workspace_lister2)
        dikey_layout.addWidget(ws_list2)
        dikey_layout.addWidget(new_frm_list)
        dikey_layout.addWidget(btn,0,Qt.AlignCenter)
        dikey_layout.addSpacing(25)

        self.content_child_frame.setLayout(dikey_layout)

    def frm_prs_update_btn_click(self):
        prs_id = self.content_child_frame.findChildren(QComboBox,"prs_list")[0]
        prs_id = prs_id.itemData(prs_id.currentIndex())
        prs_name = self.content_child_frame.findChildren(QLineEdit,"prs_name")[0].text()
        prs_mail = self.content_child_frame.findChildren(QLineEdit,"prs_mail")[0].text()
        new_frm_id = self.content_child_frame.findChildren(QComboBox,"new_frm_id")[0]
        new_frm_id = new_frm_id.itemData(new_frm_id.currentIndex())
        if prs_id != 0:
            if prs_mail.count(" ") == 0 and prs_mail.count("@") ==1 and prs_mail.count(".") > 0 and prs_mail :
                if prs_name.count(" ") != len(prs_name) and prs_name[0] != " ":
                    cursor = self.prsdb.find_one({'mail':prs_mail,'frm_id':new_frm_id})
                    if cursor["_id"] == prs_id:
                        self.prsdb.update_one({'_id':prs_id},{'$set':{'fullname':prs_name,'mail':prs_mail,"frm_id":new_frm_id}})
                        self.bildirim(f'{prs_name} adlı güncellenmiştir.')
                        self.frm_prs_update_panel()            
                    else:
                        self.bildirim("Kişi zaten ekli!!")
                else:
                    self.bildirim("Kişi adı boşluk olamaz veya boşluk ile başlayamaz!!")
            else:
                self.bildirim("Uygun bir mail adresi giriniz.")
        else:
            self.bildirim("Önce Kişinin ekleneceği firmayı seçiniz!")
# ------------------------------------------------------------------------ Kişiler Paneli -------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------- Firma Paneli --------------------------------------------------------------------------------------------
    
    def frm_list_panel(self):
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
    
    def frm_list_table(self,index):
        tablo = self.content_child_frame.findChildren(QTableWidget,"frm_list")
        frame_x = self.contentpanel.width()
        frame_y = self.contentpanel.height()
        if tablo:
            tablo= tablo[0]
            tablo.deleteLater()
        header = ['Firma Adı','Çalışma Alanı','']
        tablo = QTableWidget(1,len(header),self.content_child_frame)
        tablo.setObjectName("frm_list")
        tablo.setStyleSheet(f"border-radius:0;color:{self.FONT_COLOR};background-color: {self.PANEL_COLOR};")
        tablo.horizontalHeader().setVisible(False)
        tablo.verticalHeader().setVisible(False)
        tablo_max_width=int((frame_x-75)/2)-1
        tablo.setColumnWidth(0, tablo_max_width)
        tablo.setColumnWidth(1, tablo_max_width)
        tablo.setColumnWidth(2, 75)
        tablo.setFixedSize(frame_x,frame_y-100)
        tablo.move(0,40)

        for col in range(len(header)):
            item = QTableWidgetItem(header[col])
            item.setTextAlignment(Qt.AlignCenter) 
            item.setBackground(QColor(self.BORDER_COLOR))
            item.setFlags(QtCore.Qt.ItemIsEnabled) 
            tablo.setItem(0,col,item) 
        tablo.show()

        if index > 0:
            add_btn = self.custom_color_common_items(QPushButton,"add","Yeni",75,29,self.GREEN,self.ON_HOVER_GREEN)
            add_btn.clicked.connect(self.frm_item_panel)
            tablo.setCellWidget(0,2,add_btn)
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
            
            sql_header = ['name','ws_name']
            for item in self.frmdb.aggregate(sql):
                row = tablo.rowCount()
                tablo.insertRow(row)
                for i in range(len(sql_header)):
                    table_item = QTableWidgetItem(str(item[sql_header[i]]))
                    table_item.setTextAlignment(Qt.AlignCenter) 
                    table_item.setFlags(QtCore.Qt.ItemIsEnabled) 
                    tablo.setItem(row,i,table_item)
                
                update_btn = QPushButton("Güncelle")
                update_btn.setStyleSheet(self.normal_button)
                update_btn.setProperty("_id",item["_id"])
                update_btn.setObjectName("update")
                update_btn.clicked.connect(self.frm_item_panel)
                tablo.setCellWidget(row,2,update_btn)

    def frm_item_panel(self):
        button = self.sender()
        button_name = button.objectName()
        Frame = self.content_child_frame.findChildren(QFrame,"frm_item")
        if Frame:
            Frame= Frame[0]
            Frame.deleteLater()
        parent_width = self.content_child_frame.width()
        parent_height = self.content_child_frame.height()
        Frame = QFrame(self.content_child_frame)
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
            del_btn.clicked.connect(self.del_frm_btn_click)
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
            update_btn.clicked.connect(self.frm_update_btn_click)
            Frame_layout2.addWidget(update_btn,0,Qt.AlignCenter)
        else:
            add_btn = self.common_items(QPushButton,"add_btn","Ekle",100,30)
            add_btn.clicked.connect(self.insert_frm_btn_click)
            Frame_layout2.addWidget(add_btn,0,Qt.AlignCenter)

        Frame_layout.addLayout(Frame_layout1)
        Frame_layout.addLayout(Frame_layout2)
        Frame_layout.addSpacing(100)
        Frame.setLayout(Frame_layout)
        Frame.show()

    def del_frm_btn_click(self):
        button = self.sender()
        doc_id = button.property("_id")  
        prs_count = self.prsdb.count_documents({'frm_id':doc_id})
        if prs_count == 0 :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Firmayı istediğinize emin misiniz?")
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

    def frm_update_btn_click(self):
        frm_name = self.content_child_frame.findChildren(QLineEdit,"frm_name")[0].text()
        frm_id = self.sender()
        frm_id = frm_id.property("_id")
        workspace_id = self.content_child_frame.findChildren(QComboBox,"ws_list")[0]
        workspace_id = int(workspace_id.itemData(workspace_id.currentIndex()))

        if frm_id > 0:
            if frm_name.count(" ") != len(frm_name) and frm_name[0] != " ":
                if workspace_id != 0:
                    self.frmdb.update_one({'_id':frm_id},{'$set':{'name':frm_name,'workspace_id':workspace_id}})
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
        else:
            self.bildirim("Lütfen Firma Seçiniz!!")

    def insert_frm_btn_click(self):# Firma ekleme 
        frm_name = self.content_child_frame.findChildren(QLineEdit,"frm_name")[0].text()
        ws_id = self.content_child_frame.findChildren(QComboBox,"ws_list")[0]
        ws_id = ws_id.itemData(ws_id.currentIndex())
        if frm_name.count(" ") != len(frm_name) and frm_name[0] != " ":
            if ws_id != 0:
                data = {"_id":"","name":"",'workspace_id':''}
                data_id = self.frmdb.find().sort({"_id": -1}).limit(1).to_list()
                if data_id:
                    data_id = int(data_id[0]['_id'])+1
                else:
                    data_id = 1
                data['_id'] = data_id
                data['name'] = frm_name
                data['workspace_id'] = ws_id
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


    def common_items(self,widget:QWidget,widget_name:str,widget_text:str,widget_width:int,widget_height:int):
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

    def custom_color_common_items(self,widget:QWidget,widget_name:str,widget_text:str,widget_width:int,widget_height:int,color1:str,color2:str):
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

    def set_combobox_items(self,set_combobox:QComboBox,process:str,self_combobox:QComboBox):
        match process:
            case "Ws_Parent_Set":
                set_combobox.clear()
                set_combobox.addItem("Select Any Workspace",userData = -1)
                set_combobox.addItem("Main Workspace",userData = 0)
                for item in self.workspacedb.find({'parent':0}):
                    set_combobox.addItem(item['name'],userData = item['_id'])
            case "Self_Ws_Child":
                set_combobox.clear()
                set_combobox.addItem("Select Any Workspace",userData = -1)
                for item in self.workspacedb.aggregate([{"$match":{"$or":[{'parent':self.user_workspace_id},{"_id":self.user_workspace_id}]}}]):
                    set_combobox.addItem(item['name'],userData = item['_id'])
            case "Select_Ws_Set_Ws":
                set_combobox.clear()
                ws_parent = self_combobox.itemData(self_combobox.currentIndex())
                set_combobox.addItem("Select Any Workspace",userData = -1)
                for item in self.workspacedb.find({"parent":ws_parent}):
                    set_combobox.addItem(item["name"],userData = item['_id'])
# ------------------------------------------------------------------------- Firma Paneli --------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------- Yetki Paneli --------------------------------------------------------------------------------------------
    def scan_locale_user_data(self):# yerel ağdaki kullanıcıları tarıyor
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("Bu işlem yaklaşık 10 dk sürecektir. Devam etmek istiyor musunuz?")
        msg.setWindowTitle("Bilgi Mesajı")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            
        resp = msg.exec()

        if resp == 1024:
            Common_Class.get_user_accounts()     

    def update_perm_user_panel(self):#Kullanıcı yetki güncelleme alanı tasarımı
        if self.content_child_frame is not None:
            for child in self.content_child_frame.findChildren(QWidget):
                child.deleteLater()
        if self.content_child_frame.layout():
            QWidget().setLayout(self.content_child_frame.layout()) 
        
        dikey_layout = QVBoxLayout(self.content_child_frame)
        Perm_list=["Admin","Müdür","Personel","Yetkisiz","Gereksiz"]
        
        ws_list = self.common_elements("clear_list_combo","workspace_list")
        user_combo = self.common_elements("clear_list_combo","user_list")
        user_fullname = self.common_elements("TextBox","user_fullname")
        workspace_lister = self.common_elements("workspace_lister","item1")
        ws_list2 = self.common_elements("clear_list_combo","new_workspace_list")
        perm_combo = self.common_elements("clear_list_combo","perm_list")
        btn = self.common_elements("button_update","btn")
        
        
        
        perm_combo.addItems(Perm_list)
        ws_list.currentIndexChanged.connect(lambda index:self.change_combo_set_combo(user_combo,3,ws_list.itemData(index)))
        user_combo.currentIndexChanged.connect(lambda index:self.change_combo_set_combo(user_fullname,2,user_combo.currentText()[:user_combo.currentText().find("-")-1] if index != 0 else " " ))
        workspace_lister.currentIndexChanged.connect(lambda index:self.change_combo_set_combo(ws_list2,1,workspace_lister.itemData(index)))
        ws_list.clear()
        self.workspace_combo_set_items(ws_list,2)
        ws_list.insertItem(0,"Select Workspace !!",userData=-1)
        ws_list.insertItem(1,"Tüm Yetkililer",userData=0)
        ws_list.setCurrentIndex(0)
        btn.clicked.connect(self.update_perm_user_btn_click)
        
        dikey_layout.setAlignment(Qt.AlignCenter)
        dikey_layout.addWidget(ws_list)
        dikey_layout.addWidget(user_combo)
        dikey_layout.addWidget(user_fullname)
        dikey_layout.addWidget(workspace_lister)
        dikey_layout.addWidget(ws_list2)
        dikey_layout.addWidget(perm_combo)
        dikey_layout.addWidget(btn,0,Qt.AlignCenter)
        dikey_layout.addSpacing(150)

        self.content_child_frame.setLayout(dikey_layout)

    def update_perm_user_btn_click(self):#Kullanıcı yetki güncelleme 
        user_fullname = self.content_child_frame.findChildren(QLineEdit,"user_fullname")[0].text()
        user_id = self.content_child_frame.findChildren(QComboBox,"user_list")[0]
        user_id = user_id.itemData(user_id.currentIndex())
        workspace_id = self.content_child_frame.findChildren(QComboBox,"new_workspace_list")[0]
        workspace_id = int(workspace_id.itemData(workspace_id.currentIndex()))
        perm = self.content_child_frame.findChildren(QComboBox,"perm_list")[0].currentText()
        if isinstance(user_id,int):
            if user_fullname.count(" ") != len(user_fullname) and user_fullname[0] != " ":
                if workspace_id != 0:
                    self.usersdatadb.update_one({'_id':user_id},{'$set':{'real_name':user_fullname,'workspace_id':workspace_id,'permission':perm}})
                    self.bildirim("Kullanıcı Güncellenmiştir!!") 
                    self.update_perm_user_panel()
                else:
                   self.bildirim("Lütfen Çalışma alanı seçiniz!!") 
            else:
                self.bildirim("Kişinin Adı Boş olamaz veya boşluk ile başlayamaz!!")
        else:
            self.bildirim("Lütfen Kullanıcı Seçiniz!!")

    def insert_perm_user_panel(self):#Kullanıcıya yetki tanımlama alanının tasarımı
        if self.content_child_frame is not None:
            for child in self.content_child_frame.findChildren(QWidget):
                child.deleteLater()
        if self.content_child_frame.layout():
            QWidget().setLayout(self.content_child_frame.layout()) 
        
        dikey_layout = QVBoxLayout(self.content_child_frame)
        Perm_list=["Admin","Müdür","Personel","Yetkisiz","Gereksiz"]
        
        user_combo = self.common_elements("clear_list_combo","user_list")
        user_fullname = self.common_elements("TextBox","user_fullname")
        workspace_lister = self.common_elements("workspace_lister","item1")
        ws_list = self.common_elements("clear_list_combo","workspace_list")
        perm_combo = self.common_elements("clear_list_combo","perm_list")
        btn = self.common_elements("button_add","btn")
        
        perm_combo.addItems(Perm_list)
        workspace_lister.currentIndexChanged.connect(lambda index:self.change_combo_set_combo(ws_list,1,workspace_lister.itemData(index)))
        btn.clicked.connect(self.insert_perm_user_btn_click)
        
        dikey_layout.setAlignment(Qt.AlignCenter)
        dikey_layout.addWidget(user_combo)
        dikey_layout.addWidget(user_fullname)
        dikey_layout.addWidget(workspace_lister)
        dikey_layout.addWidget(ws_list)
        dikey_layout.addWidget(perm_combo)
        dikey_layout.addWidget(btn,0,Qt.AlignCenter)
        dikey_layout.addSpacing(150)

        self.content_child_frame.setLayout(dikey_layout)

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
    
    def insert_perm_user_btn_click(self):#Kullanıcıya yetki tanımlama
        user_fullname = self.content_child_frame.findChildren(QLineEdit,"user_fullname")[0].text()
        user_sid = self.content_child_frame.findChildren(QComboBox,"user_list")[0]
        user_sid = user_sid.itemData(user_sid.currentIndex())
        workspace_id = self.content_child_frame.findChildren(QComboBox,"workspace_list")[0]
        workspace_id = int(workspace_id.itemData(workspace_id.currentIndex()))
        perm = self.content_child_frame.findChildren(QComboBox,"perm_list")[0].currentText()
        if user_sid != 0:
            if user_fullname.count(" ") != len(user_fullname) and user_fullname[0] != " ":
                if workspace_id != 0:
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
                    self.usersdatadb.insert_one(data)
                    self.bildirim(f"{user_fullname} adlı kişi yetkilendirilmiştir.")
                    self.insert_perm_user_panel()
                else:
                    self.bildirim("Düzgün bir çalışma alanı seçiniz!!")
            else:
                self.bildirim("Kişinin Adı Boş olamaz veya boşluk ile başlayamaz!!")
        else:
            self.bildirim("Lütfen Tara Butonuna basarak lokal ağdaki kullanıcıları tarayınız!!")

    def list_users(self):#Kullanıcıları listeleme alan tasarımı
        if self.content_child_frame is not None:
            for child in self.content_child_frame.findChildren(QWidget):
                child.deleteLater()
        if self.content_child_frame.layout():
            QWidget().setLayout(self.content_child_frame.layout()) 

        frame_x = self.contentpanel.width()
        x_center = self.content_child_frame.width()/2
        
        Perm_list=["Tüm Yetkiler","Admin","Müdür","Personel","Yetkisiz","Gereksiz"]
        perm_combo = QComboBox(self.content_child_frame)
        perm_combo.setStyleSheet(self.combobox_style)
        perm_combo.setFixedSize(frame_x-200, 25)
        perm_combo.move(x_center-int((perm_combo.width()/2)),5)
        perm_combo.addItems(Perm_list)
        perm_combo.setObjectName("perm_list")
        perm_combo.show()
        perm_combo.setCurrentIndex(1)
        perm_combo.currentIndexChanged.connect(self.set_list_user_table)
        perm_combo.setCurrentIndex(0)
    
    def set_list_user_table(self,index): # seçilen yetkiye göre tablo filtreleme
        tablo = self.content_child_frame.findChildren(QTableWidget,"user_list")
        frame_x = self.contentpanel.width()
        frame_y = self.contentpanel.height()
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
                }]
        if index != 0:
            sql.append({'$match':{'permission':self.sender().currentText()}})
        
        sorgu = self.usersdatadb.aggregate(sql).to_list(None)
        row= len(sorgu)
        header = ['id','Tam Adı','Kullanıcı Adı','Yetki','Çalışma Alanı']
        tablo = QTableWidget(row+1,len(header),self.content_child_frame)
        tablo.setStyleSheet(f"border-radius:0;color:{self.FONT_COLOR};background-color: {self.PANEL_COLOR};")
        tablo.horizontalHeader().setVisible(False)
        tablo.verticalHeader().setVisible(False)
        tablo_max_width=int((frame_x-225)/2)-1
        tablo.setColumnWidth(0, 50)
        tablo.setColumnWidth(1, tablo_max_width)
        tablo.setColumnWidth(2, 100)
        tablo.setColumnWidth(3, 75)
        tablo.setColumnWidth(4, tablo_max_width)
        tablo.setFixedSize(frame_x,frame_y-95)
        tablo.move(0,35)
        
        for col in range(len(header)):
            item = QTableWidgetItem(header[col])
            item.setTextAlignment(Qt.AlignCenter) 
            item.setBackground(QColor(self.BORDER_COLOR))
            item.setFlags(QtCore.Qt.ItemIsEnabled) 
            tablo.setItem(0,col,item) 
            tablo.show()
        row_num=1
        sql_header = ['_id','real_name','username','permission','ws_name','name']
        for item in sorgu:
            for i in range(len(sql_header)):
                if i != 4 and i != 5:
                    table_item = QTableWidgetItem(str(item[sql_header[i]]))
                    table_item.setTextAlignment(Qt.AlignCenter) 
                    table_item.setFlags(QtCore.Qt.ItemIsEnabled) 
                    tablo.setItem(row_num,i,table_item)
                else:
                    table_item = QTableWidgetItem(str(item[sql_header[i]][sql_header[i+1]]))
                    table_item.setTextAlignment(Qt.AlignCenter) 
                    table_item.setFlags(QtCore.Qt.ItemIsEnabled) 
                    tablo.setItem(row_num,i,table_item)
                    break
            row_num += 1

    def common_items(self,widget:QWidget,widget_name:str,widget_text:str,widget_width:int,widget_height:int):
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

    def custom_color_common_items(self,widget:QWidget,widget_name:str,widget_text:str,widget_width:int,widget_height:int,color1:str,color2:str):
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

# ------------------------------------------------------------------------- Yetki Paneli --------------------------------------------------------------------------------------------

# ----------------------------------------------------------------- WorkSpace ------------------------------------------------------------------------------------
# Workspace List Kişinin yetkisine göre çalışma alanlarını listeleliyor 
# Tıklanan Güncelle veya ekleme butonu workspace_item_panel yönlendiriyor ve butonun adına bakıyor böylelikle ekleme mi güncelleme mi onu anlıyoruz.
# Aynı zamanda kullanıcının yetkisine bakarak güncellemedeki üst çalışma alanını listeliyor

    def workspace_list_panel (self):# Çalışma Alanı Listeleme
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
        workspace_items = self.workspacedb.aggregate(sql).to_list(None)

        header = ['isim','Bağlı Olduğu Alan','']
        tablo = QTableWidget(len(workspace_items)+1,len(header),self.content_child_frame)
        tablo.setStyleSheet(f"border-radius:0;color:{self.FONT_COLOR};background-color: {self.PANEL_COLOR};")
        tablo.horizontalHeader().setVisible(False)
        tablo.verticalHeader().setVisible(False)
        tablo_max_width=int((frame_x-75)/2)-1
        tablo.setColumnWidth(0, tablo_max_width)
        tablo.setColumnWidth(1, tablo_max_width)
        tablo.setColumnWidth(2, 75)
        tablo.setFixedSize(frame_x,frame_y-60)
        tablo.move(0,0)
        tablo.show()

        for col in range(len(header)):
            item = QTableWidgetItem(header[col])
            item.setTextAlignment(Qt.AlignCenter) 
            item.setBackground(QColor(self.BORDER_COLOR))
            item.setFlags(QtCore.Qt.ItemIsEnabled) 
            tablo.setItem(0,col,item) 
        
        add_btn = self.custom_color_common_items(QPushButton,"add","Yeni",74,29,self.GREEN,self.ON_HOVER_GREEN)
        add_btn.clicked.connect(self.workspace_item_panel)#self.del_workspace_btn_click
        tablo.setCellWidget(0,2,add_btn)

        if workspace_items:
            row_num=1
            for db_item in workspace_items:
                item = QTableWidgetItem(str(db_item['name']))
                item.setTextAlignment(Qt.AlignCenter) 
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                tablo.setItem(row_num,0,item)

                if db_item['parent'] != 0:
                    item = QTableWidgetItem(str(db_item['parent_name']))
                    item.setTextAlignment(Qt.AlignCenter) 
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    tablo.setItem(row_num,1,item)
                else:
                    item = QTableWidgetItem("Main Workspace")
                    item.setTextAlignment(Qt.AlignCenter) 
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    tablo.setItem(row_num,1,item)

                update_btn = QPushButton("Güncelle")
                update_btn.setStyleSheet(self.normal_button)
                update_btn.setProperty("_id",db_item["_id"])
                update_btn.setObjectName("update")
                update_btn.clicked.connect(self.workspace_item_panel)#self.del_workspace_btn_click
                tablo.setCellWidget(row_num,2,update_btn)
                row_num+=1

        self.content_child_frame.show()
    
    def del_workspace_btn_click(self):# Çalışma Alanınıdaki seçili satırı silme
        button = self.sender()
        doc_id = button.property("_id")  
        
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

    def workspace_item_panel(self):
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
            del_btn.clicked.connect(self.del_workspace_btn_click)
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
            update_btn.clicked.connect(self.update_workspace_btn_click)
            Frame_layout2.addWidget(update_btn,0,Qt.AlignCenter)
        else:
            add_btn = self.common_items(QPushButton,"add_btn","Ekle",100,30)
            add_btn.clicked.connect(self.insert_workspace_panel_btn_click)
            Frame_layout2.addWidget(add_btn,0,Qt.AlignCenter)
        
        Frame_layout2.addSpacing(100)
        Frame_layout.addLayout(Frame_layout1)
        Frame_layout.addLayout(Frame_layout2)
        Frame.setLayout(Frame_layout)
        Frame.show()

    def update_workspace_btn_click(self):# Çalışma Alanı Güncelleme
        button = self.sender()
        doc_id = button.property("_id")
        workspace_name = self.content_child_frame.findChildren(QLineEdit,"ws_name")[0].text()
        new_parent = self.content_child_frame.findChildren(QComboBox,"ws_parent")[0]
        new_parent_id = int(new_parent.itemData(new_parent.currentIndex()))
        
        if workspace_name.count(" ") != len(workspace_name) and workspace_name[0] != " ":
            if self.user_perm == "Admin":
                self.workspacedb.update_one({'_id':doc_id},{'$set':{'name':workspace_name,'parent':new_parent_id}})
                self.bildirim("Çalılşma Alanı Güncellenmiştir")
                Frame = self.content_child_frame.findChildren(QFrame,"ws_item")
                if Frame:
                    Frame= Frame[0]
                    Frame.deleteLater()
                self.workspace_list_panel()
            else:
                if new_parent_id != 0:
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
    
    def insert_workspace_panel_btn_click(self):#DataBase'e Çalışma Alanı Ekleme
        parent_combobox = self.content_child_frame.findChildren(QComboBox,"ws_parent")[0]
        workspace_name = self.content_child_frame.findChildren(QLineEdit,"ws_name")[0]
        parent_id = int(parent_combobox.itemData(parent_combobox.currentIndex()))
        if workspace_name.text().count(" ") != len(workspace_name.text()) and workspace_name.text()[0] != " ":
            data_id = self.workspacedb.find().sort({"_id": -1}).limit(1).to_list()
            if data_id:
                data_id = int(data_id[0]['_id'])+1
            else:
                data_id = 1
            data = {'_id':None,'name':None,"parent":None} 
            data['_id'] = data_id
            data['name'] = str(workspace_name.text())
            data['parent'] = parent_id
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
    #     uri = "mongodb+srv://RAW:OsR3aDAndWr1t3Us3r@osvpaneldb.kgluv.mongodb.net/"
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
    
    window = SuperAdminMenu(1,"sistemdestek",1,1,"Admin")
    window.show()
    sys.exit(app.exec())