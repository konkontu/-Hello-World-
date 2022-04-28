#!/usr/bin/env python
"""
Command-line utility for administrative tasks.

# For more information about this file, visit
# https://docs.djangoproject.com/en/2.1/ref/django-admin/
"""

import os
import sys

if __name__ == '__main__':
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'chet.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    from flask import Flask, request, jsonify
import json
import datetime
from enum import Enum
import sqlite3


app = Flask(__name__)



class Discrimination(Enum):
    Today_Meal = 1
    Tomorrow_Meal = 2
    Selected_Date = 3


def Meal(discrimination, date):

    try:

        conn = sqlite3.connect("C:\\Users\\yju08\OneDrive\\����ȭ����\\����������\\��������б� Hello World ��\\datebase.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM meal_data WHERE meal_data.date = {}".format(date))

        breakfast = "�ش��ϴ� �޽��� �����ϴ�"
        lunch = "�ش��ϴ� �޽��� �����ϴ�"
        dinner = "�ش��ϴ� �޽��� �����ϴ�"

        for data in cur.fetchall():
            if data[2] == "����":
                breakfast = data[3]
            elif data[2] == "�߽�":
                lunch = data[3]
            elif data[2] == "����":
                dinner = data[3]

        month = date[4:6]
        day = date[6:]

        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "{}�� {}�� [����]".format(month,day)+"\n"+breakfast+"\n\n"+ "{}�� {}�� [�߽�]".format(month,day)+"\n"+lunch+"\n\n"+"{}�� {}�� [����]".format(month,day)+"\n"+dinner
                        }
                    }
                ],
                "quickReplies": [
                    {
                        "label":"Ȩ����",
                        "action":"block",
                        "blockId" : "5ea7fc9c8b6993000177b6fe",

                    },
                ]
            }
        }

        if discrimination == Discrimination.Today_Meal:
            res["template"]["quickReplies"].append({"label":"���ϱ޽���?", "action":"block", "blockId" : "5ea7ff16cdbc3a00015a1c7d",})
            res["template"]["quickReplies"].append({"label": "��¥����","action":"block","blockId" : "5ea7ff204ab83b0001681c89",})

        elif discrimination==Discrimination.Tomorrow_Meal:
            res["template"]["quickReplies"].append({"label":"���ñ޽���?", "action":"block", "blockId" : "5ea7cb4a73e9c100015b01dd",})
            res["template"]["quickReplies"].append({"label": "��¥����","action":"block","blockId" : "5ea7ff204ab83b0001681c89",})

        elif discrimination==Discrimination.Selected_Date:
            res["template"]["quickReplies"].append({"label":"���ñ޽���?", "action":"block", "blockId" : "5ea7cb4a73e9c100015b01dd",})
            res["template"]["quickReplies"].append({"label":"���ϱ޽���?", "action":"block", "blockId" : "5ea7ff16cdbc3a00015a1c7d",})
            res["template"]["quickReplies"].append({"label": "��¥����","action":"block","blockId" : "5ea7ff204ab83b0001681c89",})

        
        


    except Exception as e:

        res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "���װ� �߻��߽��ϴ�.\n�����ڴԲ� ���׸� �����ҰԿ�"
                    }
                }
            ],
            "quickReplies": [
                {
                    "label":"Ȩ����",
                    "action":"block",
                    "blockId" : "5ea7fc9c8b6993000177b6fe",

                    },
                ]
            }
        }
   
        print("\n\n���ܰ� �߻��߽��ϴ� : {}".format(e))
        

    finally:
        conn.close()
        return res



@app.route('/TodayMeal', methods=['POST'])
def TodayMeal():

    now = datetime.datetime.now()
    
    return jsonify(Meal(Discrimination.Today_Meal, now.strftime('%Y%m%d')))


@app.route('/TomorrowMeal', methods=['POST'])
def TomorrowMeal():

    today = datetime.datetime.today()
    tomorrow = today + datetime.timedelta( days=1)

    return jsonify(Meal(Discrimination.Tomorrow_Meal, tomorrow.strftime("%Y%m%d")))


@app.route('/SelectDate', methods=['POST'])
def SelectDate():
    req = request.get_json()
    date = json.loads(req["action"]["detailParams"]["date"]["value"])["value"]

    return jsonify(Meal(Discrimination.Selected_Date, date.replace("-","")))




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, threaded=True)