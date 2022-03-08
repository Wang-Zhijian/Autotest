import unittest
from framework.base_page import BasePage
from pageobject.baidu_news_page import NewPage
from pageobject.baidu_page import BaiduPage


class TestBaiduNews(unittest.TestCase):
    """百度新闻"""

    def setUp(self):
        bro = BasePage(self)
        self.driver = bro.open_browser()

    def test_news(self):
        """搜索selenium"""
        baidu = BaiduPage(self.driver)
        baidu.click_new()
        handles = self.driver.window_handles  # 获取所有窗口句柄
        self.driver.switch_to.window(handles[1])
        new = NewPage(self.driver)
        new.type_ww('selenium')
        new.click_wr()
        new.my_quit()


if __name__ == '__main__':
    unittest.main()
