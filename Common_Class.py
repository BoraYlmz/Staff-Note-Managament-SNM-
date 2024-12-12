import sys
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton,QFrame,QSizePolicy
from PySide6.QtCore import Qt
import hashlib
from cryptography.fernet import Fernet
import base64
import subprocess
import json
import getpass

# Buradaki Classlar İleride Ayrı menüler veya arayüzler geliştirilmesinde kullanılabilecek classlardır. Duruma göre ana panelden buraya eklemeler yapılabilir.

class theme_color():
    WIN_COLOR = None
    PANEL_COLOR = None
    BORDER_COLOR = None
    OS_RED = "#a60c26"
    GREEN = "#25be71"
    ON_HOVER_GREEN = "#1a854f"
    ORANGE = "#fd9637"
    ON_HOVER_OS_RED = "#850a1e"
    FONT_COLOR =None

    def __init__(self,theme_id:int):
        self.theme_id = theme_id

    def set_color(self):
        if self.theme_id == 1: #Dark_Mode
            theme_color.WIN_COLOR = "#181818"
            theme_color.PANEL_COLOR = "#1f1f1f"
            theme_color.BORDER_COLOR = "#353535"
            theme_color.FONT_COLOR ="white"
        else: #Light_Mode
            theme_color.WIN_COLOR = "#ffffff"
            theme_color.PANEL_COLOR = "#e6e6e6"
            theme_color.BORDER_COLOR = "#cccccc"
            theme_color.FONT_COLOR ="black"
    
    def get_color(self):
        
        return theme_color.WIN_COLOR,theme_color.PANEL_COLOR,theme_color.BORDER_COLOR,theme_color.OS_RED,theme_color.ON_HOVER_OS_RED,theme_color.GREEN,theme_color.ON_HOVER_GREEN,theme_color.ORANGE,theme_color.FONT_COLOR

class CustomTitleBar(QWidget):
    def __init__(self,bar_color:str,font_color:str,border_color:str,hover_btn:str, parent=None,):
        super().__init__(parent)
        # self.setStyleSheet(f"border-left: 1px solid {border_color};border-right: 1px solid {border_color};border-bottom: none;border-top:1px solid {border_color}")


        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)

        frame = QFrame()
        frame.setStyleSheet(f"border-left: 1px solid {border_color};border-right: none;border-bottom: none;border-top:1px solid {border_color};border-bottom-right-radius:0px;border-bottom-left-radius:0px;")
        frame_layout = QHBoxLayout(frame)
        frame_layout.setContentsMargins(0,0,0,0)
        frame_layout.setSpacing(0)
        frame_layout.addStretch()
        # Kapatma butonu
        close_button = QPushButton("X")
        close_button.setObjectName("closebtn")
        close_button.setStyleSheet(f"""QPushButton#closebtn{{
                                        color: {font_color};
                                        font-weight:bold; 
                                        border-left:1px solid {border_color};
                                        border-top:none;
                                        border-right:1px solid {border_color};
                                        border-bottom:none;border-radius:0px;
                                        border-top-right-radius:5px;
                                    }}
                                    QPushButton#closebtn:hover {{
                                        background-color:{hover_btn};
                                        color:white
                                   }}""")

        close_button.setFixedSize(35,35)
        close_button.clicked.connect(self.close_window)

        # Küçültme butonu
        minimize_button = QPushButton("_")
        minimize_button.setObjectName("minibtn")
        minimize_button.setStyleSheet(f"""QPushButton#minibtn{{
                                            color: {font_color};
                                            font-weight:bold; 
                                            border-left:1px solid {border_color};
                                            border-top:none;border-right:none;
                                            border-bottom:none;
                                            border-radius:0px
                                      }}
                                      QPushButton#minibtn:hover{{
                                            background-color:{hover_btn};
                                            color:white
                                      }}""")
        minimize_button.setFixedSize(35,35)
        minimize_button.clicked.connect(self.minimize_window)
        
        frame_layout.addWidget(minimize_button)
        frame_layout.addWidget(close_button)
        
        
        main_layout.addWidget(frame)
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.startPos = None  # Sürükleme başlangıç pozisyonu

    def close_window(self):
        self.parent().close()

    def minimize_window(self):
        self.parent().showMinimized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.globalPosition().toPoint()  # Sürükleme başlangıç noktası

    def mouseMoveEvent(self, event):
        if self.startPos is not None:
            # Pencereyi sürükle
            delta = event.globalPosition().toPoint() - self.startPos
            self.parent().move(self.parent().pos() + delta)  # QPoint kullanarak
            self.startPos = event.globalPosition().toPoint()  # Güncelle

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = None  # Sürükleme durduruldu

class Cipher:
    def __init__(self):
        # Sabit anahtar
        base_key = "iylQyqqkLkPP8ewJLkUC0z-IAmmNxetCjhTQGKQWJJ4"
        self.base_cipher = Fernet(self.create_fernet_key(base_key))

    def create_fernet_key(self, KEY):
        # Anahtar oluşturma
        key_hash = hashlib.sha256(KEY.encode()).digest()
        key_bytes = base64.urlsafe_b64encode(key_hash)
        return key_bytes

    def cript(self, data):

        encrypted_data = self.base_cipher.encrypt(data.encode())

        return base64.urlsafe_b64encode(encrypted_data).decode()

    def decript(self, data):
        # Padding ekleme
        padding_needed = len(data) % 4
        if padding_needed:
            data += '=' * (4 - padding_needed)
        
        decoded_data = base64.urlsafe_b64decode(data)

        dec_data = self.base_cipher.decrypt(decoded_data).decode()
        
        return dec_data
    
def get_user_accounts():
    try:
        # WMIC komutunu çalıştır
        result = subprocess.run(
            ['wmic', 'useraccount', 'get', 'name,fullname,sid'],
            capture_output=True
        )
        # İlk olarak UTF-8 ile çözümle
        try:
            raw_output = result.stdout.decode('windows-1254', errors='replace')  
        except UnicodeDecodeError:
            raw_output = result.stdout.decode('utf-8', errors='replace')
        data = []
        # Çıktıyı işleme
        if raw_output:  # stdout'un None olmadığını kontrol et
            users = raw_output.strip().split("\n")
            for user in users[1:]:  # İlk satır başlık olduğu için atla
                if user.strip():  # Boş satırları atla
                    text = user.strip()
                    text = text.replace("™","Ö").replace("”","ö").replace("�","ı").replace("‡","ç").replace("§","ğ").replace("€","Ç").replace("Ÿ","ş").replace("˜","İ").replace("š","Ü")
                    parts = text.split()  # Kullanıcı bilgilerini ayır
                    if len(parts) >= 3:  # Eğer yeterli bilgi varsa
                        user_info = {
                            "fullname": " ".join(parts[:-2]),  # Tam adı birleştir
                            "name": parts[-2],  # Kullanıcı adını al
                            "SID": parts[-1] 
                        }
                        data.append(user_info)
            # print(data)
            # for i in data:
            #     user = str(getpass.getuser())
            #     cp = cripto.Cipher(user)
            #     i["fullname"] = cp.cript(i["fullname"],"")
            #     i["name"] = cp.cript(i["name"],"")
            #     i["SID"] = cp.cript(i["SID"],"")
            filename = "LocaleUsersData.json"
            try:
                with open(filename, 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, ensure_ascii=False, indent=4)  # ensure_ascii=False, Türkçe karakterleri doğru yazmak için
                    print(f"{filename} dosyası oluşturuldu.")
            except Exception as e:
                print(f"Hata: {e}")
        else:
            print("Hata: Çıktı alınamadı.")

        # Hata çıktısını kontrol et
        if result.stderr:
            print("Hata:", result.stderr.strip())

    except Exception as e:
        print(f"Hata: {e}")
