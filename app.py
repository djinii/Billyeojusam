from flask import Flask, render_template, jsonify, request,redirect,url_for
import jwt
import hashlib
from datetime import datetime,timedelta
app = Flask(__name__)
SECRET_KEY = 'REDSEVEN'

from pymongo import MongoClient
client = MongoClient('mongodb://test:test@13.124.146.75',27017)
db = client.dbjungle


## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('log_in.html')

@app.route('/sign')
def login():
    return render_template('sign.html')

@app.route('/mypage')
def signup():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256']) # token디코딩합니다.
        userinfo = db.users.find_one({'id': payload['id']}, {'_id': 0})

        dry=db.users.find_one({'id': payload['id']}, {'_id': False, 'id': False,'pw': False,'name_give': False, 'phone': False, 'curlingiron': False,'detergent': False, 'fever': False, 'hanger': False,'painkiller': False,'index': False})
        curl=db.users.find_one({'id': payload['id']}, )
        dete=db.users.find_one({'id': payload['id']}, {'_id': False, 'id': False,'pw': False,'name_give': False, 'phone': False, 'dryingrack': False,'curlingiron': False, 'fever': False, 'hanger': False,'painkiller': False,'index': False})
        fever=db.users.find_one({'id': payload['id']}, {'_id': False, 'id': False,'pw': False,'name_give': False, 'phone': False, 'dryingrack': False,'curlingiron': False,'detergent': False, 'hanger': False,'painkiller': False,'index': False})
        hanger=db.users.find_one({'id': payload['id']}, {'_id': False, 'id': False,'pw': False,'name_give': False, 'phone': False, 'dryingrack': False,'curlingiron': False,'detergent': False, 'fever': False,'painkiller': False,'index': False})
        pain=db.users.find_one({'id': payload['id']}, {'_id': False, 'id': False,'pw': False,'name_give': False, 'phone': False, 'dryingrack': False,'curlingiron': False,'detergent': False, 'fever': False, 'hanger': False,'index': False})

        dry = dry.get('dryingrack')
        curl = curl.get('curlingiron')
        dete = dete.get('detergent')
        fever = fever.get('fever')
        hanger = hanger.get('hanger')
        pain = pain.get('painkiller')

        if dry =='1':
            d_check="checked"
            d_Ncheck=""
        elif dry=='0':
            d_check=""
            d_Ncheck="checked" 
        
        if curl =='1':
            c_check="checked"
            c_Ncheck=""
        elif curl =='0':
            c_check="" 
            c_Ncheck="checked"
            
        if dete=='1':
            de_check="checked"
            de_Ncheck=""
        elif dete =='0':
            de_check=""
            de_Ncheck="checked"
            
        if fever=='1':
            f_check="checked"
            f_Ncheck="" 
        elif fever =='0':
            f_check=""
            f_Ncheck="checked"
            
        if hanger=='1':
            h_check="checked"
            h_Ncheck="" 
        elif hanger =='0':
            h_check=""
            h_Ncheck="checked"
                    
        if pain=='1':
            p_check="checked"
            p_Ncheck="" 
        elif pain =='0':
            p_check=""
            p_Ncheck="checked"
            
        return render_template("mypage.html", user_info=userinfo, d_check=d_check, d_Ncheck=d_Ncheck, c_check=c_check, c_Ncheck=c_Ncheck, 
                               de_check=de_check, de_Ncheck=de_Ncheck, f_check=f_check, f_Ncheck=f_Ncheck, h_check=h_check, h_Ncheck=h_Ncheck, 
                               p_check=p_check, p_Ncheck=p_Ncheck)
    except jwt.ExpiredSignatureError:
        return redirect("/")
    except jwt.exceptions.DecodeError:
        return redirect("/")

@app.route('/find')
def find():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256']) # token디코딩합니다.
        userinfo = db.users.find_one({'id': payload['id']}, {'_id': 0})
        return render_template("Main.html", user_info=userinfo)
    
    except jwt.ExpiredSignatureError:
        return redirect("/")
    except jwt.exceptions.DecodeError:
        return redirect("/")

@app.route('/login', methods=['POST'])
def api_login():
    id_recieve = request.form['id_give']
    pw_recieve = request.form['pw_give']
     
    result = db.users.find_one({'id': id_recieve, 'pw': pw_recieve}) # id, 암호화된pw을 가지고 해당 유저를 찾습니다.

     # JWT 토큰 발급
    if result is not None:
         # JWT 토큰 생성
        payload = {
            'id': id_recieve,
            'exp': datetime.utcnow() + timedelta(seconds=20)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
    
# 회원가입
@app.route("/sign", methods=["POST"])
def join():
   # 사용자 정보 받아오기
   id_recieve = request.form["id_give"]
   name_recieve = request.form["name_give"]
   pw_recieve = request.form["pw_give"]
   phone_recieve = request.form["phone_give"]

   dryingrack_recieve = request.form["dryingrack_give"]
   curlingiron_recieve = request.form["curlingiron_give"]
   detergent_recieve = request.form["detergent_give"]
   fever_recieve = request.form["fever_give"]
   hanger_recieve = request.form["hanger_give"]
   painkiller_recieve = request.form["painkiller_give"]

   result = db.users.find_one({'id': id_recieve})
   
   if result is not None:
        return jsonify({'result': 'fail', 'msg': 'ID 중복확인을 해주세요'})
   else:
        db.users.insert_one({'id': id_recieve, 'pw': pw_recieve, 'name_give': name_recieve, "phone":phone_recieve, 
           "dryingrack":dryingrack_recieve, "curlingiron":curlingiron_recieve, "detergent":detergent_recieve, 
           "fever":fever_recieve, "hanger":hanger_recieve, "painkiller":painkiller_recieve,"canuse":'O'})
        return jsonify({'result': 'success'})


@app.route("/sign/check", methods=["POST"])
def checkID():
   id_recieve = request.form["id_give"]
   result = db.users.find_one({'id': id_recieve})
   if result is not None:
        return jsonify({'result': 'fail', 'msg': '이미 존재하는 ID입니다!'})
   else:
        return jsonify({'result': 'success'})


@app.route('/find/dryingrack', methods=['GET'])
def read_dryingrack():
    dryingrack_result = list(db.users.find({"dryingrack": "1"}, {'_id': False}))
    return jsonify({'result': 'success', 'articles': dryingrack_result})


@app.route('/find/curlingiron', methods=['GET'])
def read_curlingiron():
    curlingiron_result = list(db.users.find({"curlingiron": "1"}, {'_id': False}))
    return jsonify({'result': 'success', 'articles': curlingiron_result})

@app.route('/find/detergent', methods=['GET'])
def read_detergent():
    detergent_result = list(db.users.find({"detergent": "1"}, {'_id': False}))
    return jsonify({'result': 'success', 'articles': detergent_result})

@app.route('/find/fever', methods=['GET'])
def read_fever():
    fever_result = list(db.users.find({"fever": "1"}, {'_id': False}))
    return jsonify({'result': 'success', 'articles': fever_result})

@app.route('/find/hanger', methods=['GET'])
def read_hanger():
    hanger_result = list(db.users.find({"hanger": "1"}, {'_id': False}))
    return jsonify({'result': 'success', 'articles': hanger_result})

@app.route('/find/painkiller', methods=['GET'])
def read_painkiller():
    painkiller_result = list(db.users.find({"painkiller": "1"}, {'_id': False}))
    return jsonify({'result': 'success', 'articles': painkiller_result})


#회원탈퇴
@app.route('/mypage/delete', methods=['POST'])
def delete():
    token_receive = request.cookies.get('mytoken')    
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    db.users.delete_one({"id":payload["id"]})
    return jsonify({"result":"success"})

@app.route('/mypage/edit', methods=['POST'])
def modify():
    token_receive = request.cookies.get('mytoken')    
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    
    pw_recieve=request.form['pw_give']
    num_recieve=request.form['num_give']
    
    dryingrack_recieve = request.form["dryingrack_give"]
    curlingiron_recieve = request.form["curlingiron_give"]
    detergent_recieve = request.form["detergent_give"]
    fever_recieve = request.form["fever_give"]
    hanger_recieve = request.form["hanger_give"]
    painkiller_recieve = request.form["painkiller_give"]
    
    db.users.update_many({"id":payload["id"]},{'$set':{'pw':pw_recieve, 'phone':num_recieve}})
    db.users.update_many({"id":payload["id"]},{'$set':{'dryingrack':dryingrack_recieve, 'curlingiron':curlingiron_recieve, 'detergent':detergent_recieve, 'fever':fever_recieve, 'hanger':hanger_recieve, 'painkiller':painkiller_recieve}})
    
    return jsonify({"result": "success", "msg":"회원정보가 수정되었습니다."})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)