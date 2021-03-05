# 导入所需要的库
import pandas as pd
import numpy  as np
import calendar
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# 创建Chrome控制窗口
browser = webdriver.Chrome(executable_path="C:/Program Files (x86)/Google/Chrome/chromedriver.exe")

# 打开所要爬取的网站
browser.get('https://www.zq12369.com/environment.php?city=%E7%9F%B3%E5%AE%B6%E5%BA%84&tab=city')

# 初始化类别按钮,由于网站使用了ajax控件,以及数据存放在svg标签中;元素定位使用CSS选择器（XPath不能定位部分数据）
l_cat=[
'div[class="btngroup"]>div[id="btn-group1"]>button[value ="AQI"]',
'div[class="btngroup"]>div[id="btn-group1"]>button[value ="PM2.5"]',
'div[class="btngroup"]>div[id="btn-group1"]>button[value ="PM10"]',
'div[class="btngroup"]>div[id="btn-group1"]>button[value ="SO2"]',
'div[class="btngroup"]>div[id="btn-group1"]>button[value ="NO2"]',
'div[class="btngroup"]>div[id="btn-group1"]>button[value ="CO"]',
'div[class="btngroup"]>div[id="btn-group1"]>button[value ="O3"]',
]

#存储爬取的数据
all_date =[]


# 初始化所要爬取的年份（由于只是爬取一年多数据，没有在年份上使用循环）
ye=2018

# 爬虫的主循环程序
for mo in range(1,13):                  # 月份控制
    temp_mo = calendar.monthcalendar(ye,mo)
    for row in temp_mo:
        for col in row:                 # 日控制
            if col!=0:
                da =[ye,mo,col]
                date = date_str%(da[0],da[1]-1,da[2])
                browser.execute_script(date)
                sleep(2)
                temp_l_date = []
                for cat in l_cat:       # 爬取数据的类别控制
                    cat_click = browser.find_element_by_css_selector(cat)
                    cat_click_test=cat_click.text
                    cat_click.click()
                    temp_d_value = {}
                    sleep(2)
                    tag = 'div[id="pointchart"]>div>svg>g[class="highcharts-axis-labels highcharts-xaxis-labels"]'
                    temp_l_name= browser.find_element_by_css_selector(tag).text.split()
                    for index in range(1,52):     # 逐个提取数据
                        try: 
                            text = "//*[name()='svg'] /*[name()='g'][6]/*[name()='g'][%d]/*[name()='text'] "%index
                    #         temp_d_value.append([temp_l_name[index-1],browser.find_element_by_xpath(text).text ])
                            temp_d_value[temp_l_name[index-1]] = browser.find_element_by_xpath(text).text
                        except:
                            pass
    
                    for cov  in alal:             # 空数据填充  
                        if cov not in temp_d_value:
                            temp_d_value[cov] = np.nan
                    
                    # 格式化数据
                    DD = "%d-%d-%d"%(da[0],da[1],da[2])
                    temp_l_D = [DD,cat_click_test,temp_d_value['鹿泉一中'],temp_d_value['封龙山'],temp_d_value['人民会堂'],temp_d_value['元氏县气象局'],temp_d_value['元氏住建局'],temp_d_value['22中南校区'],
                    temp_d_value['井陉县3502生活区'],temp_d_value['赞皇中学'],temp_d_value['西北水源'],temp_d_value['职工医院'],temp_d_value['西南高教'],temp_d_value['井陉县气象局']
                    ,temp_d_value['世纪公园'],temp_d_value['栾城区环保局'],temp_d_value['井陉矿区南寨小学'],temp_d_value['鹿泉住建局'],temp_d_value['栾城六中'],temp_d_value['赵县文广新局']
                    ,temp_d_value['平山县县政府'],temp_d_value['井陉矿区区委大楼'],temp_d_value['高新区'],temp_d_value['赵县环保局'],temp_d_value['高邑镇政府'],temp_d_value['赞皇县政府']
                    ,temp_d_value['赵县县政府'],temp_d_value['正定县公安消防大队'],temp_d_value['平山冶河'],temp_d_value['鹿泉区环保局'],temp_d_value['辛集城管大队'],temp_d_value['栾城通讯公司']
                    ,temp_d_value['正定县党校'],temp_d_value['新乐市委东楼'],temp_d_value['新乐市卫生局'],temp_d_value['藁城实验学校'],temp_d_value['新乐实验学校'],temp_d_value['高邑县政府']
                    ,temp_d_value['正定联通公司'],temp_d_value['辛集市政府'],temp_d_value['灵寿县市场管理局'],temp_d_value['灵寿供水'],temp_d_value['藁城市环保局'],temp_d_value['无极环保局']
                    ,temp_d_value['藁城八中'],temp_d_value['晋州市人民政府'],temp_d_value['无极卫计局'],temp_d_value['辛集采油五厂'],temp_d_value['行唐启明中学'],temp_d_value['行唐县委办公楼']
                    ,temp_d_value['晋州老干部局'],temp_d_value['深泽华丽大楼'],temp_d_value['深泽供电局']]
                    
                    # 将数据添加到字典
                    all_date.append(temp_l_D)
                    

# 将列表数据转化为pandas的DataFrame格式
df = pd.DataFrame(all_date)

# 添加列名
df.columns=["日期","指标",'鹿泉一中','封龙山','人民会堂','元氏县气象局','元氏住建局','22中南校区',
 '井陉县3502生活区','赞皇中学','西北水源','职工医院','西南高教','井陉县气象局'
,'世纪公园','栾城区环保局','井陉矿区南寨小学','鹿泉住建局','栾城六中','赵县文广新局'
 ,'平山县县政府','井陉矿区区委大楼','高新区','赵县环保局','高邑镇政府','赞皇县政府'
 ,'赵县县政府','正定县公安消防大队','平山冶河','鹿泉区环保局','辛集城管大队','栾城通讯公司'
,'正定县党校','新乐市委东楼','新乐市卫生局','藁城实验学校','新乐实验学校','高邑县政府'
,'正定联通公司','辛集市政府','灵寿县市场管理局','灵寿供水','藁城市环保局','无极环保局'
 ,'藁城八中','晋州市人民政府','无极卫计局','辛集采油五厂','行唐启明中学','行唐县委办公楼'
 ,'晋州老干部局','深泽华丽大楼','深泽供电局']
 

# 输出爬取的数据
df.sort_values("日期").to_excel("./全部年各地区各指标数据.xlsx",index=False)



# 所有监测点名称，方便格式化使用 
alal =['人民会堂',
 '22中南校区',
 '高新区',
 '西北水源',
 '封龙山',
 '栾城区环保局',
 '辛集城管大队',
 '藁城八中',
 '栾城六中',
 '无极卫计局',
 '藁城实验学校',
 '正定县公安消防大队',
 '井陉县3502生活区',
 '赵县文广新局',
 '世纪公园',
 '新乐市委东楼',
 '行唐启明中学',
 '无极环保局',
 '高邑镇政府',
 '正定县党校',
 '赵县环保局',
 '深泽华丽大楼',
 '深泽供电局',
 '辛集市政府',
 '元氏县气象局',
 '晋州市人民政府',
 '元氏住建局',
 '井陉县气象局',
 '赵县县政府',
 '新乐实验学校',
 '正定联通公司',
 '辛集采油五厂',
 '鹿泉住建局',
 '栾城通讯公司',
 '新乐市卫生局',
 '行唐县委办公楼',
 '职工医院',
 '赞皇中学',
 '藁城市环保局',
 '井陉矿区南寨小学',
 '西南高教',
 '赞皇县政府',
 '高邑县政府',
 '灵寿供水',
 '平山县县政府',
 '井陉矿区区委大楼',
 '灵寿县市场管理局',
 '鹿泉区环保局',
 '鹿泉一中',
 '平山冶河',
 '晋州老干部局']



# 由于在爬取数据的过程中需要与服务器进行交互，但是传输的数据是加密的，由于我不是很熟悉JS的代码，
# 因此将负责参数传递和接收数据,以及后期渲染函数进行修改后，直接通过JS模块执行实现数据的交互
date_str = """

var st= new Date()

st.setFullYear(%d)
st.setMonth(%d)
st.setDate(%d)

var et= st

var startTime = st.pattern('yyyy-MM-dd');
var endTime = et.pattern('yyyy-MM-dd');

  method = "GETCITYPOINTAVG";
  var city_param = encode_param("石家庄");
  startTime = startTime.substr(0,10);
  endTime = endTime.substr(0,10);
	$.ajax({
      url: 'api/zhenqiapi.php',
      data:{'appId': appId,
           'method': encode_param(method),
           'city': city_param,
           'startTime': encode_param(startTime),
           'endTime': encode_param(endTime),
           'secret': encode_secret(method,city_param,startTime,endTime)},
      type: "post",
      success: function (data) {
        data = eval('(' + decode_result(data) + ')');
        if(data.total>0)
			  {
				  categoryPoint.splice(0, categoryPoint.length);
			    dataPointAQI.splice(0, dataPointAQI.length);
			    dataPointPM25.splice(0, dataPointPM25.length);
			    dataPointPM10.splice(0, dataPointPM10.length);
			    dataPointSO2.splice(0, dataPointSO2.length);
			    dataPointNO2.splice(0, dataPointNO2.length);
			    dataPointO3.splice(0, dataPointO3.length);
			    dataPointCO.splice(0, dataPointCO.length);
			    minaqi=500,maxaqi=0;
			    minpm25=10000,maxpm25=0;
			    minpm10=10000,maxpm10=0;
			    minso2=10000,maxso2=0;
			    minno2=10000,maxno2=0;
			    mino3=10000,maxo3=0;
			    minco=10000,maxco=0;
				for(i=0;i<data.total;i++)
				{

					point = data.rows[i].pointname;
					categoryPoint.push(point);

					aqi = parseInt(data.rows[i].aqi);
				    aqiIndex = getAQILevelIndex(aqi);
				    dataPointAQI.push({
				      	name:point,
				      	y:aqi,
				      	color: getColorByIndex(aqiIndex)
				    });

				    pm25 = parseInt(data.rows[i].pm2_5);
				    pm25Index = getPM25LevelIndex(pm25);
				    dataPointPM25.push({
				      	name:point,
				      	y:pm25,
				      	color: getColorByIndex(pm25Index)
				    });

				    pm10 = parseInt(data.rows[i].pm10);
				    pm10Index = getPM10LevelIndex(pm10);
				    dataPointPM10.push({
				      	name:point,
				      	y:pm10,
				      	color: getColorByIndex(pm10Index)
				    });

				    so2 = parseInt(data.rows[i].so2);
				    so2Index = getSO2LevelIndex(so2);
				    dataPointSO2.push({
				      	name:point,
				      	y:so2,
				      	color: getColorByIndex(so2Index)
				    });

				    no2 = parseInt(data.rows[i].no2);
				    no2Index = getNO2LevelIndex(no2);
				    dataPointNO2.push({
				      	name:point,
				      	y:no2,
				      	color: getColorByIndex(no2Index)
				    });

				    o3 = parseInt(data.rows[i].o3);
				    o3Index = getO3LevelIndex(pm25);
				    dataPointO3.push({
				      	name:point,
				      	y:o3,
				      	color: getColorByIndex(o3Index)
				    });

				    co = parseFloat(parseFloat(data.rows[i].co).toFixed(3));
				    coIndex = getCOLevelIndex(co);
				    dataPointCO.push({
				      	name:point,
				      	y:co,
				      	color: getColorByIndex(coIndex)
				    });


				    if(aqi>maxaqi)
				    {
				    	maxaqi = aqi;
				    	worstpointaqi = point
				    }
				    if(aqi<minaqi)
				    {
				    	minaqi = aqi;
				    	bestpointaqi = point;
				    }

				    if(pm25>maxpm25)
				    {
				    	maxpm25 = pm25;
				    	worstpointpm25 = point
				    }
				    if(pm25<minpm25 && pm25>0)
				    {
				    	minpm25 = pm25;
				    	bestpointpm25 = point;
				    }

				    if(pm10>maxpm10)
				    {
				    	maxpm10 = pm10;
				    	worstpointpm10 = point
				    }
				    if(pm10<minpm10 && pm10>10)
				    {
				    	minpm10 = pm10;
				    	bestpointpm10 = point;
				    }

				    if(so2>maxso2)
				    {
				    	maxso2 = so2;
				    	worstpointso2 = point
				    }
				    if(so2<minso2 && so2>0)
				    {
				    	minso2 = so2;
				    	bestpointso2 = point;
				    }

				     if(no2>maxno2)
				    {
				    	maxno2 = no2;
				    	worstpointno2 = point
				    }
				    if(no2<minno2 && no2>0)
				    {
				    	minno2 = no2;
				    	bestpointno2 = point;
				    }

				    if(o3>maxo3)
				    {
				    	maxo3 = o3;
				    	worstpointo3 = point
				    }
				    if(o3<mino3 && o3>0)
				    {
				    	mino3 = o3;
				    	bestpointo3 = point;
				    }

				    if(co>maxco)
				    {
				    	maxco = co;
				    	worstpointco = point
				    }
				    if(co<minco && co>0)
				    {
				    	minco = co;
				    	bestpointco = point;
				    }
				}

				showPointChartByItem();
			}

		}
	});



"""

