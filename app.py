from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
import csv
import time
import random
import email.message
import smtplib
import pymysql

question = 100

app = Flask(__name__ ,static_folder = "static" ,static_url_path = "/")

def vocabulary(name):
    db = pymysql.connect(host='localhost', port=3306, user='Vocabulary', passwd='0492932899', charset='utf8', db='Vocabulary')
    sql = "SELECT * FROM `用戶端` WHERE `姓名` = '" + name + "'"

    with db.cursor() as cursor:
        # 執行 SQL 指令
        cursor.execute(sql)
        
        # 取出全部資料
        data = cursor.fetchone()

    print("資料庫中資料: " ,data)

    return data

@app.route("/README")
def README():
    return render_template("README.html")

@app.route("/Search")
def Search():
    return render_template("資料查詢網.html")

@app.route("/Search/Index")
def Search_Index():
    return render_template("查詢入口.html")

@app.route("/Search/Vocabulary")
def Vocabulary():
    return render_template("Vocabulary查詢入口.html")

@app.route("/Search/Vocabulary/Search" ,methods = ["POST"])
def Vo_User_chack_data():
    Search_user_name = request.form["name"]
    Search_user_name = str(Search_user_name)

    print("使用者資料查詢名稱: ",Search_user_name)

    try:
        data = vocabulary(Search_user_name)
        return render_template("Vocabulary學生資料查詢結果.html" ,Class =  data[0] ,class_en = data[1] ,teacher_en = data[2] ,no = data[3] ,id = data[4] ,name = data[5])

    except:
        print("無資料")
        return render_template("Vocabulary學生資料查詢結果.html" ,Class =  "無資料" ,class_en = "無資料" ,teacher_en = "無資料" ,no = "無資料" ,id = "無資料" ,name = "無資料")

class User_Login():
    def Datahub(name ,id):
        data = []
        try:
            db = pymysql.connect(host='localhost', port=3306, user='Vocabulary', passwd='0492932899', charset='utf8', db='Vocabulary')
            sql = """SELECT * FROM `用戶端` WHERE `姓名` LIKE '""" + name + "'"

            with db.cursor() as cursor:
                
                # 執行 SQL 指令
                cursor.execute(sql)
                
                # 取出全部資料
                data = cursor.fetchone()

            dn = data[5]
            di = data[4]

            return User_Login.Datachack(name ,id ,dn ,di)
        
        except:
            return None
    
    def Datachack(name ,id ,dn ,di):
        if(name == dn and id == di):
            return True

        else:
            return None

class Login():
    def verify_user():
        global user_id
        global user_name
        print("執行登入驗證")
        print("****變數內容****")
        print("    user_name :" ,user_name)
        print("    user_id :" ,user_id)
        print("登入狀態: ",end="")
        if(user_name == "" or user_id == ""):
            print("使用者跳過登入步驟")
            return None
        
        else:
            print("正常")
            return 0

class MAIN():
    def word_file(file_path):
        word = []
        with open(file_path ,mode='r' ,encoding="utf-8") as csvfile1:
            content = csv.reader(csvfile1)
            for i in content:
                word.append(i)
        return word
    
    def examination(name ,file_path ,web_path):
        global times
        global answer
        global chinese_word
        global english_word
        global question

        word = MAIN.word_file(file_path)

        for i in range(question):
            times += 1
            r = len(word)
            print("本題庫總題數: " ,r)
            s = random.randint(0 ,r)
            print("本題目編號: " ,(s + 1))
            print("本題中英文: " ,word[s])
            chinese_word = word[s][1]
            english_word = word[s][0]
            return render_template("單字王測驗.html" ,no = times ,chinese = chinese_word ,path = web_path ,ans = english_word)

    def tof(path ,answer):
        global time_end
        global times
        global question
        global time_system_end
        global time_system_start
        global time_system_total
        global english_word

        if(times == question):
            time_system_end = time.time()
            time_system_total = time_system_end - time_system_start
            
            time_end = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

        global english_word
        global chinese_word
        global scores

        global error_word
        scores = int(scores)
        print("使用者答案: ",answer)
        print("答題狀況: " ,end="")
        if answer == english_word:
            scores += 1
            print("正確")
            s = "True"

        else:
            error_word.append(chinese_word)
            error_word.append(english_word)
            print("錯誤")
            s = "False"

        if(times != question):
            return render_template("單字王測驗答案.html" ,no = times ,chinese = chinese_word ,english = english_word ,answer = s ,path = path)

        else:
            time_system_total = time_system_end - time_system_start

            return render_template("單字王測驗答案_終.html" ,no = times ,chinese = chinese_word ,english = english_word ,answer = s)

class send_mail():
    def mail_setting():
        global user_id
        user_id = str(user_id)
        user_id += "@goog.ptsh.ntct.edu.tw"
        print("使用者信箱: ",user_id)

    def auto():
        send_mail.set()
        send_mail.admin()
        send_mail.student()
        #send_mail.teacher()


    def set():
        global send_mail_set

        global error_m
        global true_m
        global error_word

        global time_system_total

        error_m = 0
        true_m = 0

        error_m = int(int(len(error_word)) / 2)
        true_m = 100 - error_m
        
        error_m = str(error_m)
        true_m = str(true_m)
        
        time_system_total = "{:.2f}".format(time_system_total)
        time_system_total = str(time_system_total)

        send_mail_set = ""
        set = ""

        for k in range(len(error_word)):
            if(k == 0 or k %2 == 0):
                send_mail_set += error_word[k]
                send_mail_set += "："

            else:
                set = error_word[k] + "\n"
                send_mail_set += set

    def admin():
        global time_start
        global time_end
        global time_system_total
        global scores
        global user_name
        global total
        global user_id
        global send_mail_set
        global error_m
        global true_m
        global level_choose

        scores = str(scores)

        msg = email.message.EmailMessage()
        msg["From"] = "pt.albertism@gmail.com"
        msg["To"] = "910041@goog.ptsh.ntct.edu.tw"
        msg["Subject"] = "單字王測驗成績單(系統端)　姓名：" + user_name + "　等級：" + str(level_choose)

        msg.set_content("--------------------學生資料--------------------" + "\n"
        + "姓名：" + user_name + "　成績：" + str(scores) + "　等級：" + level_choose + "\n" 
        + "學生帳號：" + user_id + "\n"
        + "作答開始時間：" + str(time_start) + "\n" 
        + "作答結束時間：" + str(time_end) + "\n"
        + "正確題數：" + str(true_m) + "\n"
        + "錯誤題數：" + str(error_m) + "\n"
        + "總作答時間：" + str(time_system_total) + "秒" + "\n"
        + "--------------------錯誤內容--------------------" + "\n"
        + send_mail_set)

        server = smtplib.SMTP_SSL("smtp.gmail.com" ,465)
        server.login("pt.albertism@gmail.com" ,"ivyjsvgxdmhlnghu")
        server.send_message(msg)
        server.close()
        print(user_name, "成績已寄送至系統端")
        time.sleep(1)
    
    def student():
        global time_start
        global time_end
        global time_system_total
        global scores
        global user_name
        global user_id
        global total
        global send_mail_set
        global error_m
        global true_m
        global level_choose

        scores = str(scores)

        msg = email.message.EmailMessage()
        msg["From"] = "pt.albertism@gmail.com"
        msg["To"] = str(user_id)
        msg["Subject"] = "單字王測驗成績單(學生端)　姓名：" + str(user_name) + "　等級：" + str(level_choose)

        msg.set_content("--------------------學生資料--------------------" + "\n"
        +"姓名：" + str(user_name) + "　成績：" + str(scores) + "　等級：" + str(level_choose) + "\n" 
        + "學生帳號：" + str(user_id) + "\n"
        + "作答開始時間：" + str(time_start) + "\n" 
        + "作答結束時間：" + str(time_end) + "\n"
        + "正確題數：" + str(true_m) + "\n"
        + "錯誤題數：" + str(error_m) + "\n"
        + "總作答時間：" + str(time_system_total) + "秒" + "\n"
        + "--------------------錯誤內容--------------------" + "\n"
        + send_mail_set)

        server = smtplib.SMTP_SSL("smtp.gmail.com" ,465)
        server.login("pt.albertism@gmail.com" ,"ivyjsvgxdmhlnghu")
        server.send_message(msg)
        server.close()
        print(user_name ,"成績已寄送至學生端")
        time.sleep(1)
    
    def teacher():
        global time_start
        global time_end
        global time_system_total
        global scores
        global user_name
        global user_id
        global total
        global send_mail_set
        global error_m
        global true_m
        global level_choose

        scores = str(scores)

        msg = email.message.EmailMessage()
        msg["From"] = "pt.albertism@gmail.com"
        msg["To"] = "t2011019@goog.ptsh.ntct.edu.tw"
        msg["Subject"] = "單字王測驗成績單(教師端)　姓名：" + str(user_name) + "　等級：" + str(level_choose)

        msg.set_content("--------------------學生資料--------------------" + "\n"
        +"姓名：" + str(user_name) + "　成績：" + str(scores) + "　等級：" + str(level_choose) + "\n" 
        + "學生帳號：" + str(user_id) + "\n"
        + "作答開始時間：" + str(time_start) + "\n" 
        + "作答結束時間：" + str(time_end) + "\n"
        + "正確題數：" + str(true_m) + "\n"
        + "錯誤題數：" + str(error_m) + "\n"
        + "總作答時間：" + str(time_system_total) + "秒" + "\n")

        server = smtplib.SMTP_SSL("smtp.gmail.com" ,465)
        server.login("pt.albertism@gmail.com" ,"ivyjsvgxdmhlnghu")
        server.send_message(msg)
        server.close()
        print(user_name ,"成績已寄送至教師端")
        time.sleep(1)

    def log_in_system(user_name ,user_id ,time_online):
        msg = email.message.EmailMessage()
        msg["From"] = "pt.albertism@gmail.com"
        msg["To"] = "910041@goog.ptsh.ntct.edu.tw"
        msg["Subject"] = "單字王測驗網上線報告(系統端)　姓名：" + user_name + "　上線報告"

        msg.set_content("姓名：" + user_name + "\n" 
        + "學生帳號：" + user_id + "\n"
        + "上線時間：" + time_online)

        server = smtplib.SMTP_SSL("smtp.gmail.com" ,465)
        server.login("pt.albertism@gmail.com" ,"ivyjsvgxdmhlnghu")
        server.send_message(msg)
        server.close()
        print(user_name ,"上線紀錄已傳送至系統端")
        time.sleep(1)
        send_mail.mail_setting()
        
    def text_start_teacher(user_name ,user_id ,time_now):
        pass

        msg = email.message.EmailMessage()
        msg["From"] = "pt.albertism@gmail.com"
        msg["To"] = "t2011019@goog.ptsh.ntct.edu.tw"
        msg["Subject"] = "單字王測驗網測驗開始通知(教師端)　姓名：" + user_name + "　測驗開始"

        msg.set_content("姓名：" + user_name + "\n" 
        + "學生帳號：" + user_id + "\n"
        + "開始時間：" + time_now)

        server = smtplib.SMTP_SSL("smtp.gmail.com" ,465)
        server.login("pt.albertism@gmail.com" ,"ivyjsvgxdmhlnghu")
        server.send_message(msg)
        server.close()
        print(user_name ,"測驗開始紀錄已傳送至教師端")
        time.sleep(1)

    def text_start_system(user_name ,user_id ,time_now):
        msg = email.message.EmailMessage()
        msg["From"] = "pt.albertism@gmail.com"
        msg["To"] = "910041@goog.ptsh.ntct.edu.tw"
        msg["Subject"] = "單字王測驗網測驗開始通知(系統端)　姓名：" + user_name + "　測驗開始"

        msg.set_content("姓名：" + user_name + "\n" 
        + "學生帳號：" + user_id + "\n"
        + "開始時間：" + time_now)

        server = smtplib.SMTP_SSL("smtp.gmail.com" ,465)
        server.login("pt.albertism@gmail.com" ,"ivyjsvgxdmhlnghu")
        server.send_message(msg)
        server.close()
        print(user_name ,"測驗開始記錄已傳送至系統端")
        time.sleep(1)   

    def problem(name ,id ,problem):
        msg = email.message.EmailMessage()
        msg["From"] = "pt.albertism@gmail.com"
        msg["To"] = "910041@goog.ptsh.ntct.edu.tw"
        msg["Subject"] = "單字王測驗使用者回報(系統端)　姓名：" + name

        msg.set_content("姓名：" + name + "　學號：" + id + "\n" 
        + "回報內容：" + problem + "\n")

        server = smtplib.SMTP_SSL("smtp.gmail.com" ,465)
        server.login("pt.albertism@gmail.com" ,"ivyjsvgxdmhlnghu")
        server.send_message(msg)
        server.close()
        print(name ,"使用者回報記錄已傳送至系統端")
        time.sleep(1)

@app.route("/")
def Loading():
    return render_template("單字王測驗網.html")

@app.route("/Entrance")
def Entrance():
    return render_template("入口.html")

@app.route("/Global/Error/Return") 
def Global_error_return(): 
    return render_template("錯誤回報_登入.html" ,path = reqp)

@app.route("/Global/Error/Return/Request" ,methods = ["POST"]) 
def Global_error_return_request():
    name = request.form["name"]
    id = request.form["id"]
    problem = request.form["problem"]

    global pro_name
    global pro_id
    global pro_problem

    pro_name = name
    pro_id = id
    pro_problem  = problem

    print("錯誤回報使用者(登入):　" ,pro_name)
    print("錯誤回報使用者信箱(登入):　" ,pro_id)
    print("錯誤回報內容(登入):　" ,pro_problem)

    return render_template("錯誤回報上傳_登入.html")

@app.route("/Global/Error/Return/Request/Show") 
def Global_error_return_request_show():
    global pro_name
    global pro_id
    global pro_problem

    send_mail.problem(pro_name ,pro_id ,pro_problem)

    return render_template("錯誤回報完成_登入.html")

@app.route("/Global/Privacy") 
def Global_Privacy():
    return render_template("隱私權保護政策.html")

@app.route("/Global/Copyright")
def Global_copyright():
    return render_template("著作權宣告.html")

@app.route("/Vocabulary/User/Login")
def User_login():
    global user_name
    global user_id
    user_name = ""
    user_id = ""
    return render_template("單字王使用者登入.html")

@app.route("/Vocabulary/User/Login/Chack" ,methods = ["POST"])
def User_chack_data():
    global user_name
    global user_id
    global reqp
    user_name = request.form["user_name"]
    user_id = request.form["user_id"]
    user_name = str(user_name)
    user_id = str(user_id)
    datahub = User_Login.Datahub(user_name ,user_id)

    print("登入使用者姓名:　" ,user_name)
    print("登入使用者學號:　" ,user_id)

    if(datahub == None):
        reqp = '"/Vocabulary/User/Login"'
        print(user_name ,"登入失敗")
        return render_template("單字王使用者登入錯誤.html")

    elif(datahub == True):
        return render_template("單字王使用者資料確認.html" ,user_name = user_name ,user_id = user_id)
    
    else:
        reqp = '"/Vocabulary/User/Login"'
        return render_template("單字王使用者登入錯誤.html")

@app.route("/Vocabulary/User/Login/Online/Show")
def User_online_show():
    return render_template("單字王使用者登入通知.html")

@app.route("/Vocabulary/User/Login/Online")
def User_online():
    global time_online
    time_online = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    send_mail.log_in_system(user_name ,user_id ,time_online)
    print(time_online ,user_name ,"登入")
    return redirect("/Vocabulary/User/Index")

@app.route("/Vocabulary/User/Login/Error/Return") 
def User_error_return(): 
    return render_template("單字王錯誤回報_帳號.html" ,path = reqp)

@app.route("/Vocabulary/User/Login/Error/Return/Request" ,methods = ["POST"]) 
def User_error_return_request():
    name = request.form["name"]
    id = request.form["id"]
    problem = request.form["problem"]

    global pro_name
    global pro_id
    global pro_problem

    pro_name = name
    pro_id = id
    pro_problem  = problem

    print("錯誤回報使用者(帳號):　" ,pro_name)
    print("錯誤回報使用者信箱(帳號):　" ,pro_id)
    print("錯誤回報內容(帳號):　" ,pro_problem)

    return render_template("單字王錯誤回報上傳_帳號.html")

@app.route("/Vocabulary/User/Login/Error/Return/Request/Show") 
def User_error_return_request_show():
    global pro_name
    global pro_id
    global pro_problem

    send_mail.problem(pro_name ,pro_id ,pro_problem)

    return render_template("單字王錯誤回報完成_帳號.html")

@app.route("/Vocabulary/User/Index")
def User_index():
    if(Login.verify_user() == None):
        return redirect("/Vocabulary/User/Login")
    global user_name
    global user_id
    return render_template("單字王使用者介面.html" ,user_name = user_name ,user_id = user_id)

@app.route("/Vocabulary/User/Index/Error/Return") 
def User_index_error_return(): 
    return render_template("單字王錯誤回報_主頁.html" ,path = reqp)

@app.route("/Vocabulary/User/Index/Error/Return/Request" ,methods = ["POST"]) 
def User_index_error_return_request():
    name = request.form["name"]
    id = request.form["id"]
    problem = request.form["problem"]

    global pro_name
    global pro_id
    global pro_problem

    pro_name = name
    pro_id = id
    pro_problem  = problem

    print("錯誤回報使用者(主頁):　" ,pro_name)
    print("錯誤回報使用者信箱(主頁):　" ,pro_id)
    print("錯誤回報內容(主頁):　" ,pro_problem)

    return render_template("單字王錯誤回報上傳_主頁.html")

@app.route("/Vocabulary/User/Index/Error/Return/Request/Show") 
def User_index_error_return_request_show():
    global pro_name
    global pro_id
    global pro_problem

    send_mail.problem(pro_name ,pro_id ,pro_problem)

    return render_template("單字王錯誤回報完成_主頁.html")

@app.route("/Vocabulary/User/Test/Level_1_3/Setting")
def User_Level_1_3_setting():
    global times
    global english_word
    global chinese_word
    global scores
    global error_word

    times = 0
    english_word = ""
    chinese_word = ""
    scores = 0
    error_word = []

    path = "/Vocabulary/User/Test/Level_1_3/Setting/Send_mail_show"

    print(user_name ,"測驗等級: Level 1~3 開始準備")

    return render_template("單字王測驗準備.html" ,path = path)

@app.route("/Vocabulary/User/Test/Level_1_3/Setting/Send_mail_show")
def User_Level_1_3_serring_send_mail_show():
    path = "/Vocabulary/User/Test/Level_1_3/Setting/Send_mail"
    return render_template("單字王測驗開始通知.html" ,path = path)

@app.route("/Vocabulary/User/Test/Level_1_3/Setting/Send_mail")
def User_Level_1_3_serring_send_mail():
    global user_name
    global user_id
    
    time_now = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    path = "/Vocabulary/User/Test/Level_1_3"
    
    print(time_now ,"使用者: " ,user_name ,"開始測驗")

    send_mail.text_start_teacher(user_name ,user_id ,time_now)
    send_mail.text_start_system(user_name ,user_id ,time_now)

    return redirect(path)

@app.route("/Vocabulary/User/Test/Level_1_3")
def User_Level_1_3():
    global time_system_start
    global time_system_end
    
    global time_start
    global time_end
    global level_choose
    global path
    global times


    path = "/Vocabulary/User/Test/Level_1_3"
    level_choose = "Level 1~3"

    if(times == 1):
        time_system_start = time.time()
        time_start = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    if(times == 100):
        time_system_end = time.time()
        time_end = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    return MAIN.examination("level 1-3" ,"Vocabulary/level 1-3.csv" ,"/Vocabulary/User/Test/Answer")

@app.route("/Vocabulary/User/Test/Level_4/Setting")
def User_Level_4_setting():
    global times
    global english_word
    global chinese_word
    global scores
    global error_word

    times = 0
    english_word = ""
    chinese_word = ""
    scores = 0
    error_word = []

    path = "/Vocabulary/User/Test/Level_4/Setting/Send_mail_show"

    print(user_name ,"測驗等級: Level 4 開始準備")

    return render_template("單字王測驗準備.html" ,path = path)

@app.route("/Vocabulary/User/Test/Level_4/Setting/Send_mail_show")
def User_Level_4_serring_send_mail_show():
    path = "/Vocabulary/User/Test/Level_4/Setting/Send_mail"
    return render_template("單字王測驗開始通知.html" ,path = path)

@app.route("/Vocabulary/User/Test/Level_4/Setting/Send_mail")
def User_Level_4_serring_send_mail():
    global user_name
    global user_id
    
    time_now = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    path = "/Vocabulary/User/Test/Level_4"
    
    print(time_now ,"使用者: " ,user_name ,"開始測驗")

    send_mail.text_start_teacher(user_name ,user_id ,time_now)
    send_mail.text_start_system(user_name ,user_id ,time_now)

    return redirect(path)

@app.route("/Vocabulary/User/Test/Level_4")
def User_Level_4():
    global time_system_start
    global time_system_end

    global time_start
    global time_end
    global level_choose
    global path
    global times

    path = "/Vocabulary/User/Test/Level_4"
    level_choose = "Level 4"

    if(times == 1):
        time_system_start = time.time()
        time_start = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    if(times == 100):
        time_system_end = time.time()
        time_end = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    return MAIN.examination("level 4" ,"Vocabulary/level 4.csv" ,"/Vocabulary/User/Test/Answer")

@app.route("/Vocabulary/User/Test/Level_5/Setting")
def User_Level_5_setting():
    global times
    global english_word
    global chinese_word
    global scores
    global error_word

    times = 0
    english_word = ""
    chinese_word = ""
    scores = 0
    error_word = []

    path = "/Vocabulary/User/Test/Level_5/Setting/Send_mail_show"

    print(user_name ,"測驗等級: Level 5 開始準備")

    return render_template("單字王測驗準備.html" ,path = path)

@app.route("/Vocabulary/User/Test/Level_5/Setting/Send_mail_show")
def User_Level_5_serring_send_mail_show():
    path = "/Vocabulary/User/Test/Level_5/Setting/Send_mail"
    return render_template("單字王測驗開始通知.html" ,path = path)

@app.route("/Vocabulary/User/Test/Level_5/Setting/Send_mail")
def User_Level_5_serring_send_mail():
    global user_name
    global user_id
    
    time_now = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    path = "/Vocabulary/User/Test/Level_5"
    
    print(time_now ,"使用者: " ,user_name ,"開始測驗")

    send_mail.text_start_teacher(user_name ,user_id ,time_now)
    send_mail.text_start_system(user_name ,user_id ,time_now)

    return redirect(path)

@app.route("/Vocabulary/User/Test/Level_5")
def User_Level_5():
    global time_system_start
    global time_system_end

    global time_start
    global time_end
    global level_choose
    global path
    global times

    path = "/Vocabulary/User/Test/Level_5"
    level_choose = "Level 5"

    if(times == 1):
        time_system_start = time.time()
        time_start = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    if(times == 100):
        time_system_end = time.time()
        time_end = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    return MAIN.examination("level 5" ,"Vocabulary/level 5.csv" ,"/Vocabulary/User/Test/Answer")

@app.route("/Vocabulary/User/Test/Level_6/Setting")
def User_Level_6_setting():
    global times
    global english_word
    global chinese_word
    global scores
    global error_word

    times = 0
    english_word = ""
    chinese_word = ""
    scores = 0
    error_word = []

    path = "/Vocabulary/User/Test/Level_6/Setting/Send_mail_show"

    print(user_name ,"測驗等級: Level 6 開始準備")

    return render_template("單字王測驗準備.html" ,path = path)

@app.route("/Vocabulary/User/Test/Level_6/Setting/Send_mail_show")
def User_Level_6_serring_send_mail_show():
    path = "/Vocabulary/User/Test/Level_6/Setting/Send_mail"
    return render_template("單字王測驗開始通知.html" ,path = path)

@app.route("/Vocabulary/User/Test/Level_6/Setting/Send_mail")
def User_Level_6_serring_send_mail():
    global user_name
    global user_id
    
    time_now = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    path = "/Vocabulary/User/Test/Level_6"
    
    print(time_now ,"使用者: " ,user_name ,"開始測驗")

    send_mail.text_start_teacher(user_name ,user_id ,time_now)
    send_mail.text_start_system(user_name ,user_id ,time_now)

    return redirect(path)

@app.route("/Vocabulary/User/Test/Level_6")
def User_Level_6():
    global time_system_start
    global time_system_end
        
    global time_start
    global time_end
    global level_choose
    global path
    global times

    path = "/Vocabulary/User/Test/Level_6"
    level_choose = "Level 6"

    if(times == 1):
        time_system_start = time.time()
        time_start = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    if(times == 100):
        time_system_end = time.time()
        time_end = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    return MAIN.examination("level 6" ,"Vocabulary/level 6.csv" ,"/Vocabulary/User/Test/Answer")

@app.route("/Vocabulary/User/Test/Level_4_6/Setting")
def User_Level_4_6_setting():
    global times
    global english_word
    global chinese_word
    global scores
    global error_word

    times = 0
    english_word = ""
    chinese_word = ""
    scores = 0
    error_word = []

    path = "/Vocabulary/User/Test/Level_4_6/Setting/Send_mail_show"

    print(user_name ,"測驗等級: Level 4~6 開始準備")

    return render_template("單字王測驗準備.html" ,path = path)

@app.route("/Vocabulary/User/Test/Level_4_6/Setting/Send_mail_show")
def User_Level_4_6_serring_send_mail_show():
    path = "/Vocabulary/User/Test/Level_4_6/Setting/Send_mail"
    return render_template("單字王測驗開始通知.html" ,path = path)

@app.route("/Vocabulary/User/Test/Level_4_6/Setting/Send_mail")
def User_Level_4_6_serring_send_mail():
    global user_name
    global user_id
    
    time_now = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    path = "/Vocabulary/User/Test/Level_4_6"
    
    print(time_now ,"使用者: " ,user_name ,"開始測驗")

    send_mail.text_start_teacher(user_name ,user_id ,time_now)
    send_mail.text_start_system(user_name ,user_id ,time_now)
    return redirect(path)

@app.route("/Vocabulary/User/Test/Level_4_6")
def User_Level_4_6():
    global time_system_start
    global time_system_end
        
    global time_start
    global time_end
    global level_choose
    global path
    global times
    
    level_choose = "Level 4~6"
    path = "/Vocabulary/User/Test/Level_4_6"

    if(times == 1):
        time_system_start = time.time()
        time_start = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    if(times == 100):
        time_system_end = time.time()
        time_end = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    return MAIN.examination("level 4-6" ,"Vocabulary/level 4-6.csv" ,"/Vocabulary/User/Test/Answer")

@app.route("/Vocabulary/User/Test/Answer")
def User_text_answer():
    global answer
    global path

    answer = request.args.get("ans")
    return MAIN.tof(path ,answer)
    
@app.route("/Vocabulary/User/Test/Score")
def User_score():
    global scores
    global time_start
    global time_end
    
    return render_template("單字王測驗成績.html" ,scores = scores ,star_time = time_start ,end_time = time_end)

@app.route("/Vocabulary/User/Test/Error/Return") 
def User_test_error_return(): 
    return render_template("單字王錯誤回報_測驗.html" ,path = reqp)

@app.route("/Vocabulary/User/Test/Error/Return/Request" ,methods = ["POST"]) 
def User_test_error_return_request():
    name = request.form["name"]
    id = request.form["id"]
    problem = request.form["problem"]

    global pro_name
    global pro_id
    global pro_problem

    pro_name = name
    pro_id = id
    pro_problem  = problem

    print("錯誤回報使用者(測驗):　" ,pro_name)
    print("錯誤回報使用者信箱(測驗):　" ,pro_id)
    print("錯誤回報內容(測驗):　" ,pro_problem)

    return render_template("單字王錯誤回報上傳_測驗.html")

@app.route("/Vocabulary/User/Test/Error/Return/Request/Show") 
def User_test_error_return_request_show():
    global pro_name
    global pro_id
    global pro_problem

    send_mail.problem(pro_name ,pro_id ,pro_problem)

    return render_template("單字王錯誤回報完成_測驗.html")

@app.route("/Vocabulary/User/Test/Send_mail")
def User_test_send_mail_sever():
    if(Login.verify_user() == None):
        return redirect("/Vocabulary/User/Login")
    
    send_mail.auto()
    
    return redirect("/Vocabulary/User/Test/Send_mail/Endding")

@app.route("/Vocabulary/User/Test/Send_mail/Endding")
def User_send_mail_sever_endding():
    if(Login.verify_user() == None):
        return redirect("/Vocabulary/User/Login")

    return render_template("單字王測驗成績寄送完畢.html")

@app.route("/Vocabulary/User/Test/Send_mail/Show")
def User_send_mail_show():
    if(Login.verify_user() == None):
        return redirect("/Vocabulary/User/Login")
    return render_template("單字王測驗成績寄送.html")

@app.route("/Vocabulary/User/Test/Error/Show")
def User_text_error_show():
    global error_word

    error_show = []

    for i in range(len(error_word)):
        error_show.append(error_word[i])

    if(len(error_word) / 2 < 100):
        for i in range(len(error_word) / 2 ,101 ,1):
            error_show.append("無資料")
    
    return render_template("單字王測驗錯題檢視.html"
    ,user = user_name
    
    ,chinese_001 = error_show[0]
    ,english_001 = error_show[1]

    ,chinese_002 = error_show[2]
    ,english_002 = error_show[3]

    ,chinese_003 = error_show[4]
    ,english_003 = error_show[5]

    ,chinese_004 = error_show[6]
    ,english_004 = error_show[7]

    ,chinese_005 = error_show[8]
    ,english_005 = error_show[9]

    ,chinese_006 = error_show[10]
    ,english_006 = error_show[11]

    ,chinese_007 = error_show[12]
    ,english_007 = error_show[13]

    ,chinese_008 = error_show[14]
    ,english_008 = error_show[15]

    ,chinese_009 = error_show[16]
    ,english_009 = error_show[17]

    ,chinese_010 = error_show[18]
    ,english_010 = error_show[19]

    ,chinese_011 = error_show[20]
    ,english_011 = error_show[21]

    ,chinese_012 = error_show[22]
    ,english_012 = error_show[23]

    ,chinese_013 = error_show[24]
    ,english_013 = error_show[25]

    ,chinese_014 = error_show[26]
    ,english_014 = error_show[27]

    ,chinese_015 = error_show[28]
    ,english_015 = error_show[29]

    ,chinese_016 = error_show[30]
    ,english_016 = error_show[31]

    ,chinese_017 = error_show[32]
    ,english_017 = error_show[33]

    ,chinese_018 = error_show[34]
    ,english_018 = error_show[35]

    ,chinese_019 = error_show[36]
    ,english_019 = error_show[37]

    ,chinese_020 = error_show[38]
    ,english_020 = error_show[39]

    ,chinese_021 = error_show[40]
    ,english_021 = error_show[41]

    ,chinese_022 = error_show[42]
    ,english_022 = error_show[43]

    ,chinese_023 = error_show[44]
    ,english_023 = error_show[45]
    
    ,chinese_024 = error_show[46]
    ,english_024 = error_show[47]

    ,chinese_025 = error_show[48]
    ,english_025 = error_show[49]

    ,chinese_026 = error_show[50]
    ,english_026 = error_show[51]

    ,chinese_027 = error_show[52]
    ,english_027 = error_show[53]

    ,chinese_028 = error_show[54]
    ,english_028 = error_show[55]

    ,chinese_029 = error_show[56]
    ,english_029 = error_show[57]

    ,chinese_030 = error_show[58]
    ,english_030 = error_show[59]

    ,chinese_031 = error_show[60]
    ,english_031 = error_show[61]

    ,chinese_032 = error_show[62]
    ,english_032 = error_show[63]

    ,chinese_033 = error_show[64]
    ,english_033 = error_show[65]

    ,chinese_034 = error_show[66]
    ,english_034 = error_show[67]

    ,chinese_035 = error_show[68]
    ,english_035 = error_show[69]

    ,chinese_036 = error_show[70]
    ,english_036 = error_show[71]

    ,chinese_037 = error_show[72]
    ,english_037 = error_show[73]

    ,chinese_038 = error_show[74]
    ,english_038 = error_show[75]

    ,chinese_039 = error_show[76]
    ,english_039 = error_show[77]

    ,chinese_040 = error_show[78]
    ,english_040 = error_show[79]

    ,chinese_041 = error_show[80]
    ,english_041 = error_show[81]

    ,chinese_042 = error_show[82]
    ,english_042 = error_show[83]

    ,chinese_043 = error_show[84]
    ,english_043 = error_show[85]

    ,chinese_044 = error_show[86]
    ,english_044 = error_show[87]

    ,chinese_045 = error_show[88]
    ,english_045 = error_show[89]

    ,chinese_046 = error_show[90]
    ,english_046 = error_show[91]

    ,chinese_047 = error_show[92]
    ,english_047 = error_show[93]

    ,chinese_048 = error_show[94]
    ,english_048 = error_show[95]

    ,chinese_049 = error_show[96]
    ,english_049 = error_show[97]

    ,chinese_050 = error_show[98]
    ,english_050 = error_show[99]

    ,chinese_051 = error_show[100]
    ,english_051 = error_show[101]

    ,chinese_052 = error_show[102]
    ,english_052 = error_show[103]

    ,chinese_053 = error_show[104]
    ,english_053 = error_show[105]

    ,chinese_054 = error_show[106]
    ,english_054 = error_show[107]

    ,chinese_055 = error_show[108]
    ,english_055 = error_show[109]

    ,chinese_056 = error_show[110]
    ,english_056 = error_show[111]

    ,chinese_057 = error_show[112]
    ,english_057 = error_show[113]

    ,chinese_058 = error_show[114]
    ,english_058 = error_show[115]

    ,chinese_059 = error_show[116]
    ,english_059 = error_show[117]

    ,chinese_060 = error_show[118]
    ,english_060 = error_show[119]

    ,chinese_061 = error_show[120]
    ,english_061 = error_show[121]

    ,chinese_062 = error_show[122]
    ,english_062 = error_show[123]

    ,chinese_063 = error_show[124]
    ,english_063 = error_show[125]

    ,chinese_064 = error_show[126]
    ,english_064 = error_show[127]

    ,chinese_065 = error_show[128]
    ,english_065 = error_show[129]

    ,chinese_066 = error_show[130]
    ,english_066 = error_show[131]

    ,chinese_067 = error_show[132]
    ,english_067 = error_show[133]

    ,chinese_068 = error_show[134]
    ,english_068 = error_show[135]

    ,chinese_069 = error_show[136]
    ,english_069 = error_show[137]

    ,chinese_070 = error_show[138]
    ,english_070 = error_show[139]

    ,chinese_071 = error_show[140]
    ,english_071 = error_show[141]

    ,chinese_072 = error_show[142]
    ,english_072 = error_show[143]

    ,chinese_073 = error_show[144]
    ,english_073 = error_show[145]

    ,chinese_074 = error_show[146]
    ,english_074 = error_show[147]

    ,chinese_075 = error_show[148]
    ,english_075 = error_show[149]

    ,chinese_076 = error_show[150]
    ,english_076 = error_show[151]

    ,chinese_077 = error_show[152]
    ,english_077 = error_show[153]

    ,chinese_078 = error_show[154]
    ,english_078 = error_show[155]

    ,chinese_079 = error_show[156]
    ,english_079 = error_show[157]

    ,chinese_080 = error_show[158]
    ,english_080 = error_show[159]

    ,chinese_081 = error_show[160]
    ,english_081 = error_show[161]

    ,chinese_082 = error_show[162]
    ,english_082 = error_show[163]

    ,chinese_083 = error_show[164]
    ,english_083 = error_show[165]

    ,chinese_084 = error_show[166]
    ,english_084 = error_show[167]

    ,chinese_085 = error_show[168]
    ,english_085 = error_show[169]

    ,chinese_086 = error_show[170]
    ,english_086 = error_show[171]

    ,chinese_087 = error_show[172]
    ,english_087 = error_show[173]

    ,chinese_088 = error_show[174]
    ,english_088 = error_show[175]

    ,chinese_089 = error_show[176]
    ,english_089 = error_show[177]

    ,chinese_090 = error_show[178]
    ,english_090 = error_show[179]
    
    ,chinese_091 = error_show[180]
    ,english_091 = error_show[181]

    ,chinese_092 = error_show[182]
    ,english_092 = error_show[183]

    ,chinese_093 = error_show[184]
    ,english_093 = error_show[185]

    ,chinese_094 = error_show[186]
    ,english_094 = error_show[187]

    ,chinese_095 = error_show[188]
    ,english_095 = error_show[189]

    ,chinese_096 = error_show[190]
    ,english_096 = error_show[191]

    ,chinese_097 = error_show[192]
    ,english_097 = error_show[193]

    ,chinese_098 = error_show[194]
    ,english_098 = error_show[195]

    ,chinese_099 = error_show[196]
    ,english_099 = error_show[197]

    ,chinese_100 = error_show[198]
    ,english_100 = error_show[199]
    )

@app.route("/Vocabulary/User/Logout")
def User_log_out():
    global user_name
    global user_id

    print(user_name ,"登出")

    user_name = ""
    user_id = ""

    return render_template("單字王使用者登出.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("網站錯誤404.html")

@app.errorhandler(500)
def server_error(e):
    return render_template("網站錯誤500.html")

if __name__ == '__main__':
    app.run()
