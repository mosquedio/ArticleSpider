# -*- coding: utf-8 -*-
# @Time    : 19-4-15 下午12:22
# @Author  : turing_lee
# @Email   : 13500502420@163.com
# @File    : zhihu.py

import scrapy
import time
import pyautogui
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from mouse import move,click

class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']

    def start_requests(self):
        login_success = False
        chrome_option = Options()
        chrome_option.add_argument("--disable-extensions")
        chrome_option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")          #在/usr/bin文件夹下运行命令  google-chrome --remote-debugging-port=9222
        browser = webdriver.Chrome(executable_path="/home/hadoop/pylearn/chromedriver", chrome_options=chrome_option)
        try:
            browser.maximize_window()
        except:
            pass
        browser.get("https://www.zhihu.com/signin")
        browser.find_element_by_css_selector(".SignFlow-accountInputContainer input").send_keys(Keys.CONTROL+"a")
        browser.find_element_by_css_selector(".SignFlow-accountInputContainer input").send_keys("18516987161")
        # browser.find_element_by_css_selector(".SignFlow-accountInput input").send_keys(Keys.CONTROL+"a")
        # browser.find_element_by_css_selector(".SignFlow-accountInput input").send_keys("18516987161")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL+"a")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys("zhihu18516")
        # pyautogui.click(1000,700)
        browser.find_element_by_css_selector(".SignFlow-submitButton").click()
        time.sleep(2)

        try:
            notify_ele = browser.find_element_by_class_name("Zi--Bell")
            login_success = True
        except:
            pass

        # if login_success:
        #     cookies = browser.get_cookies()
        #
        #     pickle.dump(cookies, open("/home/hadoop/.virtualenvs/ArticleSpider/cookies/zhihu.cookie", "wb"))
        #     cookie_dict = {}  # 注意将setting中的cookie设置打开
        #     for cookie in cookies:
        #         cookie_dict[cookie["name"]] = cookie["value"]
        #
        #     return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]


        #这里执行验证码登录
        while not login_success:
            browser.find_element_by_css_selector(".SignFlow-submitButton").click
            # pyautogui.click(1000,700)
            time.sleep(2)

            try:
                english_captcha_element = browser.find_element_by_class_name("Captcha-englishImg")
            except:
                english_captcha_element = None

            try:
                chinese_captcha_element = browser.find_element_by_class_name("Captcha-chineseImg")
            except:
                chinese_captcha_element = None

            if chinese_captcha_element:
                # ele_position = chinese_captcha_element.location
                # x_relative = ele_position["x"]
                # y_relative = ele_position["y"]
                # browser可以执行js
                # browser_navigation_panel_height = browser.execute_script("return window.outerHeight - window.innerHeight;")
                x_relative = 888
                y_relative = 613
                browser_navigation_panel_height = 0
                base64_text = chinese_captcha_element.get_attribute("src")
                import base64
                text = base64_text.replace("data:image/jpg;base64,","").replace("%0A","")
                fh = open("yzm_cn.jpeg","wb")
                fh.write(base64.b64decode(text))
                fh.close()

                from zheye import zheye
                z = zheye()
                positions = z.Recognize("yzm_cn.jpeg")
                last_position = []
                if len(positions) == 2:
                    if positions[0][1] > positions[1][1]:
                        last_position.append([positions[1][1], positions[1][0]])
                        last_position.append([positions[0][1], positions[0][0]])
                    else:
                        last_position.append([positions[0][1], positions[0][0]])
                        last_position.append([positions[1][1], positions[1][0]])
                    first_position = [int(last_position[0][0] / 2), int(last_position[0][1] / 2)]
                    second_position = [int(last_position[1][0] / 2), int(last_position[1][1] / 2)]
                    pyautogui.moveTo(x_relative+first_position[0],y_relative+browser_navigation_panel_height+first_position[1])
                    pyautogui.click()
                    time.sleep(1)
                    pyautogui.moveTo(x_relative + second_position[0], y_relative + browser_navigation_panel_height + second_position[1])
                    pyautogui.click()
                    time.sleep(1)
                else:
                    last_position.append([positions[0][1], positions[0][0]])
                    first_position = [int(last_position[0][0] / 2), int(last_position[0][1] / 2)]
                    pyautogui.moveTo(x_relative + first_position[0], y_relative + browser_navigation_panel_height + first_position[1])
                    pyautogui.click()
                    time.sleep(1)
                browser.find_element_by_css_selector(".SignFlow-accountInput input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-accountInput input").send_keys("18516987161")
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys("zhihu18516")
                # browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
                pyautogui.moveTo(1010, 746)
                pyautogui.click()


            if english_captcha_element:
                base64_text = english_captcha_element.get_attribute("src")
                import base64
                text = base64_text.replace("data:image/jpg;base64,","").replace("%0A", "")
                fh = open("yzm_en.jpeg", "wb")
                fh.write(base64.b64decode(text))
                fh.close()
                from tools.yundama_requests import YDMHttp
                yundama = YDMHttp("turing","liwen123456789",7439,"77efce0791d6ebb1e1aeedefba40757b")
                code = ""
                while True:
                    if code == "":
                        code = yundama.decode("yzm_en.jpeg", 5000, 60)
                    else:
                        break
                browser.find_element_by_css_selector(".SignFlow-captchaContainer > div > div > div.Input-wrapper > input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-captchaContainer > div > div > div.Input-wrapper > input").send_keys(code)
                # root > div > main > div > div > div > div.SignContainer-inner > div.Login-content > form > div.Captcha.SignFlow-captchaContainer > div > div > div.Input-wrapper > input
                    # '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[3]/div/div/div[1]/input').send_keys(Keys.CONTROL + "a")
                    # '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[3]/div/div/div[1]/input').send_keys(code)
                browser.find_element_by_css_selector(".SignFlow-accountInput input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-accountInput input").send_keys("18516987161")
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
                browser.find_element_by_css_selector(".SignFlow-password input").send_keys("zhihu18516")
                # browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
                pyautogui.moveTo(1010, 725)
                pyautogui.click()

                try:
                    notify_ele = browser.find_element_by_class_name("Zi--Bell")
                    login_success = True
                except:
                    pass

        # browser.get("https://www.zhihu.com/")
        cookies = browser.get_cookies()
        pickle.dump(cookies,open("/home/hadoop/.virtualenvs/ArticleSpider/cookies/zhihu.cookie","wb"))
        cookie_dict={}              #注意将setting中的cookie设置打开
        for cookie in cookies:
            cookie_dict[cookie["name"]] = cookie["value"]

        for i in range(3):
            # '''三次下拉操作，这是javascript的知识     execute_script是用来执行js代码的'''
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            time.sleep(3)

        return [scrapy.Request(url=self.start_urls[0],dont_filter=True,cookies=cookie_dict)]

        # time.sleep(160)
    # def start_requests(self):
    #     chrome_option = Options()
    #     chrome_option.add_argument("--disable-extensions")
    #     chrome_option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")          #在/usr/bin文件夹下运行命令  google-chrome --remote-debugging-port=9222
    #     browser = webdriver.Chrome(executable_path="/home/hadoop/pylearn/chromedriver", chrome_options=chrome_option)
    #     browser.get("https://www.zhihu.com/signin")
    #     time.sleep(2)
    #     browser.find_element_by_css_selector(".SignFlow-accountInput input").send_keys(Keys.CONTROL+"a")
    #     browser.find_element_by_css_selector(".SignFlow-accountInput input").send_keys("18516987161")
    #     browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL+"a")
    #     browser.find_element_by_css_selector(".SignFlow-password input").send_keys("zhihu18516")
    #     time.sleep(2)
    #     pyautogui.moveTo(984,692)
    #     pyautogui.click()
    #     # move(984, 692)             #获取屏幕坐标的工具xdotool-getmouselocation,不过需要再经过自己的计算
    #     # click()
    #     # browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
    #     time.sleep(2)
    #
    #     browser.get("https://www.zhihu.com/")
    #     cookies = browser.get_cookies()
    #
    #     pickle.dump(cookies,open("/home/hadoop/.virtualenvs/ArticleSpider/cookies/zhihu.cookie","wb"))
    #     cookie_dict={}              #注意将setting中的cookie设置打开
    #     for cookie in cookies:
    #         cookie_dict[cookie["name"]] = cookie["value"]
    #
    #     return [scrapy.Request(url=self.start_urls[0],dont_filter=True,cookies=cookie_dict)]


    def parse(self, response):

        pass
