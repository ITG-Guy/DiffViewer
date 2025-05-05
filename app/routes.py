# Routing Protocols are dealed in this scripts
from flask import render_template, request, redirect, url_for, flash, send_from_directory  
from flask_login import login_user, login_required, logout_user,current_user
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from . import app, mongo
from .models import User
from .constants import *

@app.route('/json_diff_viewer')
def json_diff_viewer():
    json1 = {
        "layer1": {
            "layer2": {
                "key3": {
                    "layer4": {
                        "key1": [1, 2, 3],
                        "key2": {"subkey1": "value1", "subkey2": "value2"},
                        "key3": "original_value",
                        "key4": [
                            {"id": 1, "name": "item1"},
                            {"id": 2, "name": "item2"}
                        ]
                    }
                }
            }
        }
    }

    json2 = {
        "layer1": {
            "layer2": {
                "key3": {
                    "layer4": {
                        "key1": [1, 2, 4],
                        "key2": {"subkey1": "value1"},
                        "key3": "edited_value",
                        "key4": [
                            {"id": 1, "name": "item1"},
                            {"id": 3, "name": "item3"}
                        ],
                        "key5": [
                            {"id": 4, "details": {"info": "extra"}},
                            {"id": 5, "details": {"info": "additional"}}
                        ]
                    },
                    "new_key": "new_value"
                }
            }
        }
    }

    # Pass the JSON objects and their differences to the template
    return render_template('json_diff_viewer.html', json1=json1, json2=json2)

@app.route('/')
# @login_required
def home():
    # Example how to get the data from DB and deliver it to model template.
    # # project_name_list = [x['project_name'] for x in mongo.db['Main_Table'].find({}, {'project_name': 1, '_id': 0})]
    # query = {'project_type': PROJECT_TYPE.FLAGSHIP.value}
    # flagship_project_list = [x for x in mongo.db['Main_Table'].find(query, {'project_name': 1, '_id': 1, 'ect_version': 1 , 'author': 1, 'date_created' : 1, 'merged_status': 1})] 

    # grouped_flagship_projects = group_projects_by_name(flagship_project_list)
    
    # return render_template('home.html',flagship_project_list=flagship_project_list, 
    #                        volume_project_list=volume_project_list, 
    #                        wearable_project_list=wearable_project_list,
    #                        grouped_flagship_projects = grouped_flagship_projects,
    #                        grouped_volume_projects = grouped_volume_projects,
    #                        grouped_wearable_projects = grouped_wearable_projects,
    #                        grouped_etc_projects = grouped_etc_projects)
    return render_template('index.html')

@app.route('/users_profile')
@login_required
def users_profile():
    return render_template('users-profile.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Search user with a username
        # (MongoDB에서 사용자 조회)
        user_data = mongo.db.users.find_one({'username': username})
        if user_data and User.validate_login(user_data['password_hash'], password):
            # Make a User instance including _id
            # (_id를 포함하여 User 객체 생성)
            user = User(user_data['username'], user_data['email'], user_data['password_hash'], user_data['_id'])
            # With a 'login_user' function, login operation is done.
            # (Flask-Login의 `login_user` 함수를 사용하여 사용자 로그인 처리)
            login_user(user, remember=True)  # `remember=True`is optional.
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    
    return render_template('pages-login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        existing_user = mongo.db.users.find_one({'username': username})
        if existing_user is None:
            password_hash = generate_password_hash(password)
            mongo.db.users.insert_one({'username': username, 'email': email, 'password_hash': password_hash})
            return redirect(url_for('login'))
        else:
            flash('Username already exists')
    
    return render_template('pages-register.html')

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if new_password != confirm_password:
        flash('Passwords do not match!', 'error')
        return redirect(url_for('users_profile'))

    current_user.set_password(new_password)
    current_user.save()
    flash('Password successfully updated!', 'success')
    return redirect(url_for('users_profile'))


@app.route('/static/<path:path>')
def serve_static(path):  # 추가된 부분
    return send_from_directory('static', path)

# 404 에러 페이지 라우트 설정
@app.errorhandler(404)
def page_not_found(error):
    return render_template('pages-error-404.html'), 404
