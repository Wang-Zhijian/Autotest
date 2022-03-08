import testsuites.test_baidu
import testsuites.test_baidu_news
import unittest
import get_cwd
import os
import HTMLTestRunnerCN
from framework.my_email import mail

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(testsuites.test_baidu.TestBaidu('test_baidu'))
    suite.addTest(testsuites.test_baidu_news.TestBaiduNews('test_news'))
    path = get_cwd.get_cwd()
    file_path = os.path.join(path, 'report/测试报告.html')
    fp = open(file_path, 'wb')
    runner = HTMLTestRunnerCN.HTMLTestReportCN(
        stream=fp,
        title='测试报告',
        description='报告中描述部分',
        tester='测试者'
    )
    runner.run(suite)
    fp.close()
    mail()
