from selenium import webdriver
from selenium.webdriver.common.by import By

from logs.log import log1
from selenium.common.exceptions import NoSuchElementException
import get_cwd
import os
import time
import configparser

path = get_cwd.get_cwd()
config_path = os.path.join(path, 'config/config.ini')


class BasePage:
    """测试基类"""

    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def is_displayed(element):
        """元素是否存在"""
        value = element.is_displayed()
        return value

    @staticmethod
    def my_sleep(seconds):
        """强制等待"""
        time.sleep(seconds)
        log1.info('暂停%d秒' % seconds)

    def get_img(self):
        """截图"""
        screenshots_path = os.path.join(get_cwd.get_cwd(), 'screenshots/')  # 拼接截图保存路径
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))  # 按格式获取当前时间
        screen_name = screenshots_path + rq + '.png'  # 拼接截图文件名
        # noinspection PyBroadException
        try:
            self.driver.get_screenshot_as_file(screen_name)
            log1.info("截图保存成功")
        except BaseException:
            log1.error("截图失败", exc_info=1)

    def find_element(self, selector):
        """定位元素"""
        by = selector[0]
        value = selector[1]
        element = None
        if by in ['id', 'name', 'class', 'tag', 'link', 'plink', 'css', 'xpath']:
            # noinspection PyBroadException
            try:
                if by == 'id':
                    element = self.driver.find_element(By.ID, value)
                elif by == 'name':
                    element = self.driver.find_element(By.NAME, value)
                elif by == 'class':
                    element = self.driver.find_element(By.CLASS_NAME, value)
                elif by == 'tag':
                    element = self.driver.find_element(By.TAG_NAME, value)
                elif by == 'link':
                    element = self.driver.find_element(By.LINK_TEXT, value)
                elif by == 'plink':
                    element = self.driver.find_element(By.PARTIAL_LINK_TEXT, value)
                elif by == 'css':
                    element = self.driver.find_element(By.CSS_SELECTOR, value)
                elif by == 'xpath':
                    element = self.driver.find_element(By.XPATH, value)
                else:
                    log1.error('没有找到元素')
                log1.info('元素定位成功。定位方式：%s，使用的值%s：' % (by, value))
                return element
            except NoSuchElementException:
                log1.error("报错信息：", exc_info=1)
                self.get_img()  # 调用截图
        else:
            log1.error('输入的元素定位方式错误')

    def type(self, selector, value):
        """输入内容"""
        time.sleep(1)
        element = self.find_element(selector)
        time.sleep(1)
        element.clear()
        log1.info('清空输入内容')
        # noinspection PyBroadException
        try:
            element.send_keys(value)
            log1.info('输入的内容：%s' % value)
        except BaseException:
            log1.error('内容输入报错', exc_info=1)
            self.get_img()

    def click(self, selector):
        """点击元素"""
        element = self.find_element(selector)
        # noinspection PyBroadException
        try:
            element.click()
            log1.info('点击元素成功')
        except BaseException:
            display = self.is_displayed(element)
            if display is True:
                self.my_sleep(3)
                element.click()
                log1.info('点击元素成功')
            else:
                self.get_img()
                log1.error('点击元素报错', exc_info=1)

    def use_js(self, js):
        """调用js"""
        # noinspection PyBroadException
        try:
            self.driver.execute_script(js)
            log1.info('js执行成功，js内容为：%s' % js)
        except BaseException:
            log1.error('js执行报错', exc_info=1)

    def switch_menu(self, parent_element, second_element, target_element):
        """三级菜单切换"""
        self.my_sleep(3)
        # noinspection PyBroadException
        try:
            self.driver.switch_to_default_content()
            self.click(parent_element)
            log1.info('成功点击一级菜单：%s' % parent_element)
            self.click(second_element)
            log1.info('成功点击二级菜单：%s' % second_element)
            self.click(target_element)
            log1.info('成功点击三级菜单：%s' % target_element)
        except BaseException:
            log1.error('切换菜单报错', exc_info=1)

    def switch_iframe(self, selector):
        """切换farm"""
        element = self.find_element(selector)
        # noinspection PyBroadException
        try:
            self.driver.switch_to.frame(element)
            log1.info('切换frame成功')
        except BaseException:
            log1.error('切换frame报错', exc_info=1)

    def get_title(self):
        """获取title"""
        title = self.driver.title
        log1.info('当前窗口的title是:%s' % title)
        return title

    def my_quit(self):
        """关闭浏览器"""
        self.driver.quit()
        log1.info('关闭浏览器')

    def config_get(self, key, section=None):
        """读取配置文件字段的值并返回"""
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8-sig")
        switch = config.get('environment', 'switch')
        if section is None and switch == str(0):
            section = 'test'
        elif section is None and switch == str(1):
            section = 'prod'
        config_get = config.get(section, key)
        return config_get

    def config_write(self, key=None, value=None, section=None):
        """往配置文件写入键值"""
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8-sig")
        switch = config.get('environment', 'switch')
        if section is None and switch == str(0):
            section = 'test'
        elif section is None and switch == str(1):
            section = 'prod'
        if key is not None and value is not None:
            config.set(section, key, value)
            log1.info('在section:%s下写入%s=%s' % (section, key, value))
            with open(config_path, 'w', encoding='utf-8')as f:
                config.write(f)
        else:
            config.add_section(section)
            log1.info('新增section：%s' % section)
            with open(config_path, 'w', encoding='utf-8')as f:
                config.write(f)

    def config_delete(self, key=None, section=None):
        """删除配置文件字段"""
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8-sig")
        switch = config.get('environment', 'switch')
        if section is None and switch == str(0):
            section = 'test'
        elif section is None and switch == str(1):
            section = 'prod'
        if key is not None:
            config.remove_option(section, key)
            log1.info('删除section:%s下key为：%s的记录' % (section, key))
            with open(config_path, 'w', encoding='utf-8') as f:
                config.write(f)
        else:
            config.remove_section(section)
            log1.info('删除section:%s' % section)
            with open(config_path, 'w', encoding='utf-8') as f:
                config.write(f)

    def open_browser(self):
        browser = self.config_get('browser', 'environment')
        log1.info('读取浏览器配置')
        url = self.config_get('url')
        log1.info('读取url：%s' % url)
        try:
            if browser == str(0):
                self.driver = webdriver.Chrome()
                log1.info('打开的浏览器为chrome')
            elif browser == str(1):
                self.driver = webdriver.Firefox()
                log1.info('打开的浏览器为Firefox')
            self.driver.get(url)
            self.driver.maximize_window()
            log1.info('浏览器最大化')
            self.driver.implicitly_wait(10)
            log1.info('设置静态等待时间10秒')
            return self.driver
        except BaseException:
            log1.error('浏览器打开报错')

    def config_options(self, section):
        """读取配置文件某section下所有键"""
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8-sig")
        username = config.options(section)
        return username

    def get_addkey(self, user):
        """遍历获得配置文件收件人email"""
        total = 0
        receiver = []
        for i in user:
            if total < len(user):
                emails = self.config_get(i, 'addressed')
                receiver.append(emails)
                total += 1
        return receiver
