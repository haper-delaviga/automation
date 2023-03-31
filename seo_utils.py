from airtest.core.api import *
from airtest.aircv import *
from PIL import Image
import configparser
import random
import pytesseract

config = configparser.ConfigParser()
config.read('seo_domain.ini')
pytesseract.pytesseract.tesseract_cmd = config['path']['tesseract_cmd']

class AndroidPhone:

    def __init__(self, config_file):
        print("---安卓手機初始化---")
        # read config
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')
        self.test_pic_path = config.get('path', 'test_pic_path')
        self.username = config.get('user_params', 'username')
        self.password = config.get('user_params', 'password')

    def chrome_private_mode(self):
        touch(Template(r"tpl1680138401794.png", record_pos=(0.001, 0.764), resolution=(720, 1600)))
        sleep(1.0)
        touch(Template(r"tpl1680138840508.png", record_pos=(0.419, -0.94), resolution=(720, 1600)))
        touch(Template(r"tpl1680138501339.png", record_pos=(0.013, -0.678), resolution=(720, 1600)))

    def chrome_download(self, url):
        touch(Template(r"tpl1680138520707.png", record_pos=(-0.083, -0.947), resolution=(720, 1600)))
        text(url)
        touch(Template(r"tpl1680139197476.png", record_pos=(0.007, 0.671), resolution=(720, 1600)))
        sleep(1.0)
        touch(Template(r"tpl1680193769749.png", record_pos=(0.328, 0.257), resolution=(720, 1600)))
        sleep(3.0)
        touch(Template(r"tpl1680139217235.png", record_pos=(0.344, -0.792), resolution=(720, 1600)))
        sleep(4.0)
        touch(Template(r"tpl1680139621900.png", record_pos=(0.303, 0.121), resolution=(720, 1600)))
        sleep(10.0)
        touch(Template(r"tpl1680139261896.png", record_pos=(0.312, 0.126), resolution=(720, 1600)))

    def bty_login(self):
        
        """
        1. 判斷當前登入方式，使用帳密登入
        2. 輸入帳號密碼
        3. 點擊登入
        """
        
        log('執行B體育登入') # log步驟
        if exists(Template(r"tpl1669271160558.png", record_pos=(-0.371, -0.412), resolution=(720, 1600))):  
            touch(Template(r"tpl1669257103291.png", record_pos=(0.071, 0.201), resolution=(720, 1600))) # 切換為帳號密碼登入
        sleep(1.0)
        touch(Template(r"tpl1669257475045.png", record_pos=(-0.271, -0.414), resolution=(720, 1600)))    # 輸入焦點-帳號
        text(self.username)  # 輸入帳號
        sleep(1.0)
        touch(Template(r"tpl1669257483697.png", record_pos=(-0.272, -0.235), resolution=(720, 1600)))   # 輸入焦點-密碼
        text(self.password)  #  輸入密碼
        touch(Template(r"tpl1669257539555.png", record_pos=(0.003, 0.042), resolution=(720, 1600))) # 點擊登入

    def bty_get_domainname(self, url):
        
        """
        1. 點擊我的按鈕
        2. 點擊頭像信息
        3. 點擊用戶名
        4. toast 出現後對頁面進行截圖
        """
        
        log('執行截圖獲取域名')
        sleep(8.0) # 等待頁面加載
        touch(Template(r"tpl1680095835833.png", record_pos=(0.41, 0.89), resolution=(720, 1600)))
        touch(Template(r"tpl1680095854039.png", record_pos=(-0.381, -0.869), resolution=(720, 1600)))
        touch(Template(r"tpl1680139831622.png", record_pos=(-0.371, -0.792), resolution=(720, 1600)))
        sleep(1.0)   # 等待 toast 時間
        screen = G.DEVICE.snapshot()
        local = aircv.crop_image(screen,(0,1100,720,1600))
        snapshot(msg="寫死域名截圖.")
        # 保存局部截图到指定文件夹中
        filename = url.replace("https://", "https_").replace("/", "_") + ".png"
        pil_image = cv2_2_pil(local)
        # pil_image.save(self.test_pic_path, filename, quality=99, optimize=True)
        pil_image.save(os.path.join(self.test_pic_path, filename), quality=99, optimize=True)
        sleep(1.0)

    def kill_processes(self):
    
        """
        1. 點擊icon查看後台程式
        2. 點擊全部清除
        """
        
        log('殺死進程')
        touch(Template(r"tpl1669254667626.png", record_pos=(0.261, 1.044), resolution=(720, 1600)))
        sleep(1.0)
        touch(Template(r"tpl1669254700474.png", record_pos=(-0.006, 0.672), resolution=(720, 1600)))  

    def image_to_string(self, url, domain):

        """
        1. 將寫死域名截圖轉為字符串
        2. 判斷寫死域名是否符合預期
        """

        log('开始转换写死域名')
        filename = url.replace("https://", "https_").replace("/", "_") + ".png"
        domain_string = pytesseract.image_to_string(Image.open(os.path.join(self.test_pic_path, filename)), lang='eng')
        log(f"写死域名为： {domain_string}, 预期域名为： {domain}")
        if domain in domain_string:
            return True


def extract_to_be_test(config_file):
    # read config.ini
    config = configparser.ConfigParser()
    config.read(config_file)

    # read domain_mapping and test_num
    to_be_test = {}
    domain_mapping = {}
    for key, value in config.items('domain_mapping'):
        # turn landing page url into https
        if not key.startswith("http") or key.startswith("https"):
            key = "https://" + key
        domain_mapping.setdefault(value, []).append(key)

    test_num = int(config['random_items']['n'])

    if test_num == 0:
        for key, value in domain_mapping.items():
            to_be_test[key] = value
    else:
        # extract random items from domain_mapping
        for key, value in domain_mapping.items():
            if len(value) >= test_num:
                to_be_test[key] = random.sample(value, test_num)
            else:
                to_be_test[key] = value

    return to_be_test

