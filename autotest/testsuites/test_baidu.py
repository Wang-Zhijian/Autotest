import unittest
from framework.base_page import BasePage
from pageobject.baidu_page import BaiduPage


class TestBaidu(unittest.TestCase):
    """百度首页"""

    def setUp(self):
        bro = BasePage(self)
        self.driver = bro.open_browser()

    def test_baidu(self):
        """测试百度搜索"""
        baidu = BaiduPage(self.driver)
        baidu.type_kw('selenium')
        baidu.click_su()
        baidu.get_title()
        baidu.my_quit()


if __name__ == '__main__':
    unittest.main()
