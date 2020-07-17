from selenium import webdriver
from pyquery import PyQuery as pq
import pandas as pd
import numpy as np
import time
import re
import math

browser = webdriver.Chrome()
browser.maximize_window()
record_list = pd.read_csv('./record_id.csv')
record_list = list(record_list['id'])


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


def CaseDetail(record_list):
    # 登录
    login()

    # 根据案例号爬取案例相关信息
    case_url = "https://www.itslaw.com/api/judgements/detail?_timer=" + str(int(time.time())) + "&judgementId="
    # 被告人计数
    total = 0
    fail = 0
    # 记录爬取结果的DataFrame
    col_name = ['被告人姓名', '性别', '民族', '出生日期', '籍贯', '居住地', '文化程度', '职业', '案例名称', '案例编号', '审理法院', '罪名', '刑期', '罚金']
    result = pd.DataFrame(columns=col_name)

    for i in range(0, len(record_list)):
        try:
            browser.get(case_url + record_list[i])
            html = browser.page_source
            case = str(pq(html))
            title_rule = '"title":"(.*?)"'
            title = str(re.findall(title_rule, case)[0])
            case_num_rule = '"caseNumber":"(.*?)"'
            case_num = str(re.findall(case_num_rule, case)[0])
            court_rule = '","name":"(.*?)","type":"court"}'
            court = str(re.findall(court_rule, case, re.S)[0])

            # 提取被告人信息段落
            defendant_rule = '"当事人信息(.*?)审理经过'
            defendant = str(re.findall(defendant_rule, case, re.S)[0])
            # 提取被告人信息
            defendant_rule = '被告人(.*?)。'
            defendant = re.findall(defendant_rule, defendant, re.S)
            d_total = len(defendant)

            # 提取判决信息段落
            judge_rule = '裁判结果(.*?)审判人员'
            judge = str(re.findall(judge_rule, case, re.S)[0])
            # 提取判决信息
            judge_rule = '被告人(.*?)元'
            judge = re.findall(judge_rule, judge, re.S)
            j_total = len(judge)

            # if j_total < d_total:
            #     for m in range(0, len(judge)):
            #         judge[m] = '被告人' + judge[m]
            #     judge = str(judge)
            #     judge_rule = '被告人(.*?)；'
            #     judge = re.findall(judge_rule, judge, re.S)

            for j in range(0, len(defendant)):
                lst_d = defendant[j].split("，")
                lst_j = judge[j].split("，")
                # 记录被告人信息
                for k in range(0, len(lst_d)):
                    if k == 0:
                        result.loc[total, '被告人姓名'] = lst_d[k]
                    elif '曾用名' in lst_d[k]:
                        pass
                    elif lst_d[k] == '男' or lst_d[k] == '女':
                        result.loc[total, '性别'] = lst_d[k]
                    elif ('省' in lst_d[k] or '市' in lst_d[k] or '县' in lst_d[k]) and ('人' in lst_d[k]):
                        result.loc[total, '籍贯'] = lst_d[k].split('人')[0]
                    elif '出生地' in lst_d[k]:
                        result.loc[total, '籍贯'] = lst_d[k].split('地')[1]
                    elif '户籍住址' in lst_d[k]:
                        result.loc[total, '籍贯'] = lst_d[k].split('住址')[1]
                    elif '户籍地' in lst_d[k]:
                        result.loc[total, '籍贯'] = lst_d[k].split('地')[1]
                    elif '户籍' in lst_d[k]:
                        result.loc[total, '籍贯'] = lst_d[k].split('户籍')[1]
                    elif '文化' in lst_d[k]:
                        result.loc[total, '文化程度'] = lst_d[k].split('文化')[0]
                    elif '住' in lst_d[k]:
                        result.loc[total, '居住地'] = lst_d[k].split('住')[1]

                    elif '年' in lst_d[k] and '月' in lst_d[k] and '日' in lst_d[k] and '生' in lst_d[k]:
                        if '出生于' in lst_d[k]:
                            lst1 = lst_d[k].split('出生于')
                            result.loc[total, '出生日期'] = lst1[0]
                            result.loc[total, '籍贯'] = lst1[1]
                        else:
                            result.loc[total, '出生日期'] = lst_d[k].split('出生')[0]
                    elif '族' in lst_d[k]:
                        result.loc[total, '民族'] = lst_d[k]
                    elif '逮捕' in lst_d[k] or '拘留' in lst_d[k] or '拘捕' in lst_d[k] or '看守' in lst_d[k] or '羁押' in lst_d[
                        k]:
                        pass
                    else:
                        result.loc[total, '职业'] = lst_d[k]

                # 记录案件信息
                result.loc[total, '案例名称'] = title
                result.loc[total, '案例编号'] = case_num
                result.loc[total, '审理法院'] = court

                # 记录判决信息
                for k in range(0, len(lst_j)):
                    if '犯' in lst_j[k]:
                        name = result.loc[total, '被告人姓名']
                        result.loc[total, '罪名'] = lst_j[k].split(name)[1]
                    elif '处罚金' in lst_j[k]:
                        result.loc[total, '罚金'] = lst_j[k].split('处罚金')[1] + '元'
                    elif '判处' in lst_j[k]:
                        result.loc[total, '刑期'] = lst_j[k].split('判处')[1]

                    else:
                        pass

                total += 1
            print('第' + str(i + 1) + '个案例爬取成功。')
        except:
            print('第' + str(i + 1) + '个案例爬取失败。')
            fail += 1

    print('爬取结束，成功{0}条，失败{1}条，共记录{2}条被告人信息。'.format(1000 - fail, fail, len(result)))
    browser.quit()
    return result


result = CaseDetail(record_list)
result.to_csv("./result2.csv", encoding='utf_8_sig', index=None)
