#!/usr/bin/env python
# coding: utf-8

# lawInquire, legalSupportFoundationInterface, legalSupportFoundation, classicCaseInterface, classicCase, recommendlabel, preDetection  
# 

# In[2]:


import psycopg2
conn = psycopg2.connect(
    database="d4c82p6fm9a96j",
    user="bmxysyqnocrlty",
    password="8f1dde080259f7cb36fafdab8678ffaf245ff772211f10f343ffa13e5c7d5300",
    host="ec2-107-22-160-102.compute-1.amazonaws.com",
    port="5432"
    )


# # 查詢法條

# lawList   
# index INT UNIQUE //法條條目  
# law TEXT //法條內容  

# In[ ]:


def lawInquire(index):
    cursor = conn.cursor()
    quere = "SELECT law FROM lawList WHERE index = \'" + str(index) + "\';"
    cursor.execute(quere)
    results = cursor.fetchall()
    conn.commit()
    return results[0][0]


# # 法律扶助基金會

# In[3]:


def legalSupportFoundationInterface():
    context = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": "請選擇想要的地區",
                "align": "center"
                }
            ]
        },
        
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
            {
                "type": "button",
                "style": "primary",
                "action": {
                    "type": "postback",
                    "label":"北部",
                    "data":"法律扶助基金會北部"
                }
            },
            
            {
                "type": "button",
                "style": "primary",
                "action": {
                    "type": "postback",
                    "label":"中部",
                    "data":"法律扶助基金會中部"
                }
            },
               
            {
                "type": "button",
                "style": "primary",
                "action": {
                    "type": "postback",
                    "label":"南部",
                    "data":"法律扶助基金會南部"
                }
            },
            
            {
                "type": "button",
                "style": "primary",
                "action": {
                    "type": "postback",
                    "label":"東部",
                    "data":"法律扶助基金會東部"
                }
            },
            
            {
                "type": "button",
                "style": "primary",
                "action": {
                    "type": "postback",
                    "label":"離島",
                    "data":"法律扶助基金會離島"
                }
            }
            ]
        }
    }
    
    return context


# legalSupportFoundation  
# area TEXT //地區  
# club TEXT //分會別  
# phone TEXT //電話  
# fax TEXT //傳真  
# email TEXT //email  
# address TEXT //地址  
# https TEXT //網址  

# In[4]:


def legalSupportFoundation(input):
    cursor = conn.cursor()
    quere = "SELECT club,phone,fax,email,address,https FROM legalSupportFoundation WHERE area = \'" + str(input) + "\';"
    cursor.execute(quere)
    results = cursor.fetchall()
    conn.commit()
    
    action = []
    for i in range(len(results)):
        temp = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": results[i][0],
                "weight": "bold",
                "size": "xl"
                },
                {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                    {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                    {
                    "type": "text",
                    "text": "電話",
                    "flex": 2
                    },
                    {
                        "type": "text",
                        "text": results[i][1],
                        "wrap": True,
                        "flex": 4
                    }
                ]
                },
                {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                    {
                    "type": "text",
                    "text": "傳真",
                    "flex": 2
                    },
                    {
                    "type": "text",
                    "text": results[i][2],
                    "wrap": True,
                    "flex": 4
                    }
                ]
                },
                {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                    {
                    "type": "text",
                    "text": "電子信箱",
                    "flex": 2
                    },
                    {
                    "type": "text",
                    "text": results[i][3],
                    "wrap": True,
                    "flex": 4
                    }
                ]
                },
                {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                    {
                    "type": "text",
                    "text": "地址",
                    "flex": 2
                    },
                    {
                    "type": "text",
                    "text": results[i][4],
                    "wrap": True,
                    "flex": 4
                    }
                ]
                }
                ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
            {
                "type": "button",
                "style": "primary",
                "action": {
                    "type": "uri",
                    "label": "詳細資訊",
                    "uri": results[i][5]
                }
            }
            ]
        }
        }
        action.append(temp)

    context = {
    "type": "carousel",
    "contents": action
    }
    
    return context


# # 經典案例

# classicCaseInterface  
# category TEXT //類別  
# classicCaseName TEXT //案例名稱  
# classicCase TEXT //案例  

# In[5]:


def classicCaseInterface():
    cursor = conn.cursor()
    quere = "SELECT category,classicCaseName from classicCaseInterface;"
    cursor.execute(quere)
    results = cursor.fetchall()
    conn.commit()
    
    #判別不相同的有幾類
    category = []
    for i in range(len(results)):
        if(results[i][0] not in category):
            category.append(results[i][0])
    
    button = []
    action = []
    
    for i in range(len(category)):
        tmp = []
        for j in range(len(results)):
            if(results[j][0] == category[i]):
                temp = {"type": "button","style": "primary","action": {"type": "postback","label":results[j][1],"data":"經典案例" + results[j][1]}}
                tmp.append(temp)      
        button.append(tmp)
        
        temp = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": category[i],
                "weight": "bold",
                "size": "xl"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": button[i]
        }
        }
        action.append(temp)
        
    context = {
    "type": "carousel",
    "contents": action
    }

    return context


# In[6]:


def classicCase(input):
    cursor = conn.cursor()
    quere = "SELECT classicCase from classicCaseInterface where classicCaseName = \'"+str(input)+"\';"
    cursor.execute(quere)
    results = cursor.fetchall()
    conn.commit()
    
    context = {
        "type": "bubble",
        "size": "giga",
        "styles": {
            "body": {
                "separator": True
            }
        },
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": str(input),
                "size": "xl",
                "weight": "bold"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": results[0][0],
                "size": "lg",
                "wrap":True
                }
            ]
        }
    }
    return context


# # 前預測

# 先判斷是否有其他相似案例

# In[ ]:


def preDetection(input):
    cursor = conn.cursor()
    quere = "SELECT category from classicCaseInterface where classicCaseName = \'"+str(input)+"\';"
    cursor.execute(quere)
    results = cursor.fetchall()
    
    quere = "SELECT classicCaseName from classicCaseInterface where category = \'"+ results[0][0] +"\';"
    cursor.execute(quere)
    results = cursor.fetchall()
    conn.commit()
    
    context = [results[i][0] for i in range(len(results)) if results[i][0] != input]
    return context


# # 相似案例推薦

# In[7]:


def recommendlabel(case):
    action = []
    for i in range(len(case)):
        temp = {"action": {"data": case[i][0], "label": case[i][0], "type": "postback"}, "type": "action"}
        action.append(temp)
    context = {"items": action}
    return context

