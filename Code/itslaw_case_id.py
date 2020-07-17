from selenium import webdriver
from pyquery import PyQuery as pq
import pandas as pd
import time
import re

browser = webdriver.Chrome()
browser.maximize_window()

def login():
    url = r'https://www.itslaw.com'
    browser.get(url)
    # 处理弹窗 1
    try:
        browser.find_element_by_class_name("ant-notification-notice-close").click()
    except:
        print('No window,continue.')
    # 处理弹窗 2
    try:
        browser.find_element_by_class_name("ant-modal-close-x").click()
    except:
        print('No window,continue.')
    time.sleep(1)
    # 点击"登录"按钮
    browser.find_element_by_xpath('//*[@id="itslaw"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div/button[1]').click()
    time.sleep(0.5)
    # 输入用户名和密码，并点击登陆
    browser.find_element_by_class_name("ant-form-item-control").click()
    browser.find_element_by_id("phoneNum").send_keys("15099366759")
    # browser.find_element_by_class_name("ant-form-item-control").click()
    browser.find_element_by_id("password").send_keys("python12345")
    browser.find_element_by_xpath(
        "/html/body/div[5]/div/div[2]/div/div[2]/div[2]/form/div[3]/div/div/span/button").click()
    time.sleep(2)
    return None


def Initialization():
    """------------------关闭弹窗、登录网站、条件筛选、爬取案例ID号并返回List------------------"""
    # 登录
    login()

    # 输入关键字“电信网络诈骗”查询
    browser.find_element_by_xpath('//*[@id="itslaw"]/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[1]/input').send_keys(
        "电信网络诈骗")
    browser.find_element_by_xpath('//*[@id="itslaw"]/div[1]/div[2]/div[1]/div/div[2]/div[2]/button[1]').click()
    time.sleep(5)
    # 选择“一审”和年份“2018”
    # 先选择一审
    browser.find_element_by_xpath('//*[@id="itslaw"]/div[1]/div[4]/div[1]/div[6]/div[2]/div[1]/div/span').click()
    time.sleep(2)
    # 在选择年份
    try:
        browser.find_element_by_xpath('//*[@id="itslaw"]/div[1]/div[4]/div[1]/div[5]/div[2]/div[3]/div/span').click()
    except:
        print('选择年份失败！')
    time.sleep(2)

    # 开始爬取案例URL的ID号
    record_rule = 'judgementId=(.*?)"'
    while (1):
        html = browser.page_source
        data_case_id = str(pq(html))
        data_case_id = re.sub("[\n\t]", "", data_case_id)
        data_case_id = re.sub(" ", "", data_case_id)
        record_list = re.findall(record_rule, data_case_id, re.S)
        record = len(record_list)
        time.sleep(0.5)
        if record < 1000:
            # 以下两行：使用JS定位到页面的底部，然后将页面进行拉倒底部。
            js = "var q=document.documentElement.scrollTop=10000"
            browser.execute_script(js)
            # 点击加载更多
            browser.find_element_by_xpath('//*[@id="itslaw"]/div[1]/div[4]/div[2]/a').click()
            time.sleep(1)
            continue
        else:
            print("已爬取1000条案例ID")
            break
    browser.quit()
    return record_list


record_list = Initialization()
record_id = pd.DataFrame(columns=['id'])
record_id['id'] = record_list
record_id.to_csv("./record_id.csv", index=None)
