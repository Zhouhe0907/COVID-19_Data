# @Time    : 2020/6/3 1:06 上午
# @Author  : Zhouhe
# @FileName: AutoUpdateInWeb.py
# @Software: PyCharm

import urllib
from urllib import request
from urllib.parse import urlencode
# 跳过SSL验证证书
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# BeautifulSoup分析网页代码
from bs4 import BeautifulSoup as bs
# 数据库连接
import pymysql
import re
# 格式化时间
import datetime

'''----连接数据库---'''
HOST = '127.0.0.1'
PORT = 3306
USER = 'root'
PASSWORD = 'hao1018113'
DATABASE = 'Data'
TABLENAME = 'COVID_19' # 进行操作的表名
connect = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE,charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor，用以对数据库进行操作
cursor = connect.cursor()

'''------function:检测表是否存在------'''
def table_exist(table_name):
    sql = "show tables;"
    cursor.execute(sql)
    tables = [cursor.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        return 1  # 存在返回1
    else:
        return 0  # 不存在返回0

if table_exist(TABLENAME) == 0:
    print("表 \'",TABLENAME,"\' 不存在，即将创建。")
    createTableSql = "create table IF NOT EXISTS " + TABLENAME + "" \
                                                                 "(Admin varchar(255)," \
                                                                 " Province_State varchar(255), " \
                                                                 " Country_Region varchar(255)," \
                                                                 " Confirmed INT," \
                                                                 " Deaths INT," \
                                                                 " Recovered INT," \
                                                                 " Active INT," \
                                                                 " LastUpdate date," \
                                                                 " primary key(Admin,Province_State,Country_Region,LastUpdate));"
    cursor.execute(createTableSql)
    print("表已成功创建，请重启程序以进行插入数据！")
    connect.commit()
    connect.close()
else:
    print("表已存在，等待插入数据...") # 表存在时进入

    '''----爬取网页部分----'''
    # 伪造向目标地址提交请求的头部
    headers = { 'User-Agent': 'mozilla/5.0 (windows nt 6.1; wow64) applewebkit/537.36 (khtml, like gecko) chrome/27.0.1453.94 safari/537.36'}
    url_01 = "https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports"# 主网页地址
    # 向目标地址发送请求
    request_01 = request.Request(url=url_01, headers=headers) #命名格式：request:发送请求 01：主网页
    # 得到服务器回应
    response_01 = request.urlopen(request_01) # reponse: 得到网页回应 01:主网页
    # 从回应中获得代码
    html_01 = response_01.read().decode('utf-8') # html_01：主网页的回应
    soup_01 = bs(html_01, 'html.parser') # soup_01 主网页分析
    tbody_01 = soup_01.find('tbody') # tbody tr td a 等皆为网页结构
    # 在网页响应获得的代码中找到子网页链接
    tr_01 = tbody_01.find_all('tr', class_='js-navigation-item')

    '''
    格式化当前时间,用来找到GitHub内最新更新文件
    例如今天是2020年6月3日，dayInWeb = 06-03-2020，与网站上子网页名字对应
    '''
    currentDay = datetime.date.today()
    delta = datetime.timedelta(days = 2)
    currentDay = currentDay - delta
    dayInWeb = currentDay.strftime('%m-%d-%Y')

    '''----记录数据库及网页更新状态----'''
    fileInWebUpdated = 0 # 用以判断网页文件是否更新，0为未更新，1为已更新
    latestDatabase = 1 # 数据库是否为最新数据，1为最新数据
    totalList = [] #盛放待向数据库中批量插入的数据

    for t in tr_01:
        td_01 = t.find('td', class_='content')
        span_01 = td_01.find('span', class_='css-truncate css-truncate-target')
        href_01 = span_01.find('a')
        csv_01 = str(href_01.get('href'))
        if csv_01[-14:-4] != dayInWeb: #进入最近日期的子网页
            continue
        if csv_01[-3:] == 'csv': #判断是否为csv文件

            fileInWebUpdated = 1 #网页更新状态：已更新

            '''------判断进入子网页的条件-----'''
            csv_01 = 'https://github.com' + csv_01
            webUrl_02 = csv_01
            requestTo_webUrl_02 = request.Request(url=webUrl_02, headers=headers)
            responseFrom_webUrl_02 = request.urlopen(requestTo_webUrl_02)
            html_02 = responseFrom_webUrl_02.read().decode('utf-8')
            soup_02 = bs(html_02, 'html.parser')
            table_02 = soup_02.find('table', class_='js-csv-data csv-data js-file-line-container')
            tbody_02 = table_02.find('tbody')
            tr_02 = tbody_02.find_all('tr', class_='js-file-line')

            '''------进入子网页-----'''
            for tr in tr_02: #按行顺序进入csv表格
                countryDict = {}  #用字典来盛放当前行数据
                td_02_details = tr.find_all('td')
                index = 0 # index：当前列
                for tds in td_02_details:
                    tds = str(tds.string)
                    if index == 2:
                        countryDict['Admin'] = tds if tds != 'None' else '#NULL'
                    if index == 3:
                        countryDict['Province_State'] = tds if tds != 'None' else '#NULL'
                    if index == 4:
                        countryDict['Country_Region'] = tds if tds != 'None' else '#NULL'
                        if countryDict['Country_Region'] == "Mainland China":
                            countryDict['Country_Region'] = "China"
                    if index == 5:
                        '''----------判断是否需要格式化时间--------'''
                        if len((tds).split('/', 2)) == 3:  # 时间格式形如 5/9/20时进入
                            formatTime = '2020-0' + tds.split('/', 2)[0] + '-'  # 时间改为2020-05-
                            if int(tds.split('/', 2)[1]) > 9:  # '日'大于于10时进入
                                formatTime = formatTime + tds.split('/', 2)[1]
                            else:
                                formatTime = formatTime + '0' + tds.split('/', 2)[1]  # 否则'日'前补'0'

                            formatTime = formatTime + " "  # 日期与时间的空格符
                            if int(tds.split(' ', 1)[1].split(':', 1)[0]) < 10:  # 小时小于10时进入
                                formatTime = formatTime + '0' + tds.split(' ', 1)[1]  # 小时前补0
                            else:
                                formatTime = formatTime + tds.split(' ', 1)[1]  # 否则直接拷贝时间
                        else:
                            formatTime = tds.replace("T", " ")  # 时间为中带有'T'时将'T'转为' '
                        countryDict['LastUpdate'] = formatTime[0:10]

                    if index == 8:
                        countryDict['Confirmed'] = int(tds) if tds != 'None' else 0
                    if index == 9:
                        countryDict['Deaths'] = int(tds) if tds != 'None' else 0
                    if index == 10:
                        countryDict['Recovered'] = int(tds) if tds != 'None' else 0
                    if index == 11:
                        countryDict['Active'] = int(tds) if tds != 'None' else 0

                        '''当前行数据提取完毕
                           开始查询数据库库表中是否是当前得到的日期地区的的最新记录
                        '''
                        values = []
                        querySql = "select * from " + TABLENAME + " where Admin = %s and Province_State = %s and Country_Region = %s and LastUpdate = %s;"
                        values.append(countryDict['Admin'])
                        values.append(countryDict['Province_State'])
                        values.append(countryDict['Country_Region'])
                        values.append(countryDict['LastUpdate'])
                        exist = cursor.execute(querySql, values)
                        if exist > 0: #如果表中存在相同日期地区的相同记录
                            record = cursor.fetchone() # 获取数据库中相同的记录
                            if record : # 当此记录不为空即存在时进入
                                if record[3] < countryDict['Confirmed']: # 数据库中不是最新数据时进入
                                    values = [countryDict['Confirmed'], countryDict['Deaths'], countryDict['Recovered'], countryDict['Active']] + values
                                    updateSql = "update " + TABLENAME + " set Confirmed = %s, Deaths = %s, Recovered = %s, Active = %s where Admin = %s and Province_State = %s and Country_Region = %s and LastUpdate = %s;"
                                    cursor.execute(updateSql,values)
                                    print("Update one record：",countryDict)
                                    connect.commit()
                                    break
                                else:
                                    break
                            break
                        else:  # 当数据库中不存在相同记录时进入
                            currentData = (countryDict['Admin'],
                                           countryDict['Province_State'],
                                           countryDict['Country_Region'],
                                           countryDict['Confirmed'],
                                           countryDict['Deaths'],
                                           countryDict['Recovered'],
                                           countryDict['Active'],
                                           countryDict['LastUpdate'])
                            totalList.append(currentData) # 向待批量添加的数据表中添加元组
                            latestDatabase = 0
                            break
                    index += 1
    if fileInWebUpdated == 1: # 当网页文件已更新时进入
        print("Data in web has already been updated！")
        if latestDatabase == 0:
            insertSql = "INSERT IGNORE INTO " + TABLENAME + " VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
            cursor.executemany(insertSql,totalList)
            print("数据插入成功,今日共更新",len(totalList),'条数据，多余数据将在格式化步骤被清理。')
            '''--------格式化数据--------'''
            # 判断是否为网页中用来做计算的数据
            change = "UPDATE " + TABLENAME + " SET Admin = '#RDForCalculate' WHERE Active < 0 and Confirmed = 0 AND Admin != '#RDForCalculate';"
            # 数据量为负数的相应操作
            abs = "UPDATE " + TABLENAME + " SET Confirmed = Confirmed + ABS(Active) WHERE Active < 0 and Confirmed > 0;"
            # 计算当前Active人数
            active = "UPDATE " + TABLENAME + " SET Active = Confirmed - Deaths - Recovered WHERE Country_Region != Admin and Country_Region != Province_State;"
            # 插入国家级数据信息
            insert =  "INSERT IGNORE INTO " + TABLENAME + " SELECT * FROM (SELECT Country_Region AS Admin, Country_Region AS Province_State, Country_Region, SUM(Confirmed) AS Confirmed,SUM(Deaths) AS Deaths, SUM(Recovered) AS Recovered, SUM(Active) AS Active, LastUpdate FROM " + TABLENAME + " WHERE Country_Region != Province_State AND Country_Region != Admin GROUP BY LastUpdate, Country_Region) newTable;"
            # 去除只有国家的数据
            deleteExtra1 = "DELETE FROM " + TABLENAME + " WHERE Admin = '#NULL' AND Province_State = '#NULL';"
            # 去除重复数据
            deleteExtra2 = "DELETE FROM " + TABLENAME + " WHERE Admin != '#RDForCalculate' AND Active < 0 AND Confirmed = 0;"
            # 添加世界数据
            addWorld = "INSERT IGNORE INTO " + TABLENAME + " SELECT * FROM(SELECT \"World\" As Admin, \"World\" As Province_State, \"World\" As Country_Region, SUM(Confirmed) AS Confirmed,SUM(Deaths) AS Deaths, SUM(Recovered) AS Recovered, SUM(Active) AS Active, LastUpdate FROM " + TABLENAME + " WHERE Country_Region = Province_State AND Country_Region = Admin AND Admin != 'World' GROUP BY LastUpdate) newTable;"
            cursor.execute(change)
            cursor.execute(abs)
            cursor.execute(active)
            cursor.execute(insert)
            cursor.execute(deleteExtra1)
            cursor.execute(deleteExtra2)
            cursor.execute(addWorld)
            print("成功格式化数据库！")
            connect.commit()
        else:
            print("--- 插入失败，因为数据库已是最新 ---")
    else:
        print("网页数据未更新！")

'---关闭资源---'
cursor.close()
connect.close()