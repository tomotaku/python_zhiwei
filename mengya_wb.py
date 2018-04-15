# -*- coding: utf-8 -*-
"""
如果不好使的话 重新获取一下cookie

"""
import re
import requests
import pandas as pd
rua=[]
num = 1
total=74
while num<total:
    url ="http://www.weiboreach.com/servlet/QueryHistory?page="+str(num)
    cookies=dict(cookies_my='Hm_lvt_97858ba3a880d943a557dd8b64ba7852=1523583303,1523597534; Hm_lpvt_97858ba3a880d943a557dd8b64ba7852=1523597680; JSESSIONID=C56889BE818EB42FFF63556527A3E53C')
    r = requests.get(url,cookies=cookies)
    page = r.text
    (total,events) = page.split(',',1)
    total = int(re.sub("\D", "", total))
    events = events.split('[',1)[1].rsplit(']',1)[0]
    events_list = list(eval(events))
    for i in range(5):
        val=events_list[i]['ckurl']
        event_url='http://www.weiboreach.com/servlet/GetZl?type=zl&val='+val
        events_list[i]['analyze'] = requests.get(event_url,cookies=cookies).text
    rua+=events_list
    num+=1

raw_data = pd.read_excel('D:\\m.xlsx')
raw_data[['analyze']]
new_column=['本消息曝光量','本消息情感值','本消息内容评价','本消息用户总评','行业标准曝光量','行业标准情感值','行业标准内容评价','行业标准用户总评','曝光量','情感值','内容评价','用户质量','用户活跃度','加v比例','参与用户数','水军','短链点击数','综合得分']  
for i in raw_data.index:
    raw_data.loc[i][0] = re.sub(r'\[|\]|\"','',raw_data.loc[i][0])
    data_fin = pd.concat([raw_data,raw_data['analyze'].str.split(r',',expand=True)],axis=1)
    data_fin.rename(columns=dict(zip(range(18),new_column)), inplace=True)

data=pd.read_excel('123.xls')
data['曝光量/万'] = data['曝光量/万'].apply(lambda x :int(x.split('万')[0]))