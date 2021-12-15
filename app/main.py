#https://ianlondon.github.io/blog/deploy-flask-docker-nginx
import psycopg2
from flask import Flask, jsonify, request, render_template
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage


UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'jpg'}

app = Flask(__name__,template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_files():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

@app.route('/')
@app.route('/index')
def show_index():
    
    name='4-01'
    print(name)
    name = name +'.jpg'
    print(name)
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], name)
    return render_template("showimg.html", user_image = full_filename)

#get all name of video API 
#http://127.0.0.1:5000/get-all-name
@app.route('/get-all-name')
def get_all_name():
    host = "video-api.postgres.database.azure.com"
    dbname = "video"
    user = "admin_ad@video-api"
    password = "vajajava+25%"
    sslmode = "require"
    # Construct connection string
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    conn = psycopg2.connect(conn_string) 
    print("Connection established")
    cursor = conn.cursor()
    # Fetch all rows from table
    cursor.execute("select video_name from videos;")
    rows = cursor.fetchall()
    
    # Print all rows
    i=0
    valid={}
    for row in rows:
        valid[i] ={
            "name":str(row[0]),
            }
        i=i+1
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(valid)

#get all name of video API 
#http://127.0.0.1:5000/get-all-epsode/<video_name>
#Ex.1
#form1
#http://127.0.0.1:5000/get-all-episode/The trap
#form2
#http://127.0.0.1:5000/get-all-episode/The%20trap
@app.route('/get-all-episode/<video_name>')
def get_all_episode(video_name):
    #uname = request.args.get('username')
    #upsw = request.args.get('password')
    host = "video-api.postgres.database.azure.com"
    dbname = "video"
    user = "admin_ad@video-api"
    password = "vajajava+25%"
    sslmode = "require"
    # Construct connection string
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    conn = psycopg2.connect(conn_string) 
    print("Connection established")
    cursor = conn.cursor()
    # Fetch all rows from table
    cursor.execute("select subvideo_id from subvideos inner join videos on subvideos.video_id=videos.video_id "+" where videos.video_name="+ "'" +video_name+"';")
    rows = cursor.fetchall()
    
    # Print all rows
    i=0
    valid={}
    for row in rows:
        valid[i] ={
            "episode":str(row[0]),
            }
        i=i+1
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(valid)


#Play video API
#http://127.0.0.1:5000/subvideo_id
#http://127.0.0.1:5000/1
@app.route('/directurl/<subvideo_id>')
def directurl(subvideo_id):
    host = "video-api.postgres.database.azure.com"
    dbname = "video"
    user = "admin_ad@video-api"
    password = "vajajava+25%"
    sslmode = "require"
    # Construct connection string
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    conn = psycopg2.connect(conn_string) 
    print("Connection established")
    cursor = conn.cursor()
    # Fetch all rows from table
    cursor.execute("SELECT subvideo_hls FROM subvideos where "+"subvideo_id = "+"'"+subvideo_id+"';")
    rows = cursor.fetchall()
    i=0
    valid={}
    url=''
    for row in rows:
        url = str(row[0])
        valid[i] ={
            "url":str(row[0]),       
            }
        i=i+1
    print(url)
    conn.commit()
    cursor.close()
    conn.close()
    
    return render_template('index.html', url=url)



# Login API
#http://127.0.0.1:5000/login/username/password
#http://127.0.0.1:5000/login/markza007/12344321
@app.route('/login/<username>/<pswd>')
def login(username, pswd):
    #uname = request.args.get('username')
    #upsw = request.args.get('password')
    host = "video-api.postgres.database.azure.com"
    dbname = "video"
    user = "admin_ad@video-api"
    password = "vajajava+25%"
    sslmode = "require"
    # Construct connection string
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    conn = psycopg2.connect(conn_string) 
    print("Connection established")
    cursor = conn.cursor()
    # Fetch all rows from table
    cursor.execute("SELECT * FROM members where "+"member_username = "+"'"+username+"' AND member_password = "+"'"+pswd+"'"+";")
    rows = cursor.fetchall()
    
    # Print all rows
    i=0
    valid={}
    for row in rows:
        valid[i] ={
            "role":str(row[1]),
            "fname":str(row[2]),
            "lname":str(row[3]),
            "expire":str(row[7]),
            }
        i=i+1
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(valid)

# Register API
# http://localhost:5000/register/member_id/member_type/member_fname/member_lname/member_username/member_password/member_expire/member_email
# http://localhost:5000/register/10003/admin/zala/santacluas/xwxxw_a/bhh1100/12-12-2100/adminsss@gmail.com

@app.route('/register/<member_id>/<member_type>/<member_fname>/<member_lname>/<member_username>/<member_password>/<member_expire>/<member_email>')
def register(member_id, member_type,member_fname,member_lname,member_username,member_password,member_expire,member_email):
    host = "video-api.postgres.database.azure.com"
    dbname = "video"
    user = "admin_ad@video-api"
    password = "vajajava+25%"
    sslmode = "require"
    # Construct connection string
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)


    #Insert
    #############################
    conn = psycopg2.connect(conn_string) 
    print("Connection established")
    cursor = conn.cursor()
    # Fetch all rows from table
    cursor.execute("insert into members(member_id, member_type, member_fname, member_lname, member_username, member_password, member_expire, member_email)"+" values("+ "'"+member_id+"', " + "'"+member_type+"', "+ "'"+member_fname+"', " + "'"+member_lname+"', " +"'"+member_username+"', " +"'"+member_password+"', "+ "'"+member_expire+"', "+ "'"+member_email+"'" ");")
    conn.commit()
    cursor.close()
    conn.close()
    #Insert
    ##############################
    #View
    conn = psycopg2.connect(conn_string) 
    print("Connection established")
    cursor = conn.cursor()
    # Fetch all rows from table
    cursor.execute("SELECT * FROM members where "+"member_id = "+"'"+member_id+"'" + ";")
    rows = cursor.fetchall() 
    # Print all rows
    i=0
    valid={}
    for row in rows:
        valid[i] ={
            "role":str(row[1]),
            "fname":str(row[2]),
            "lname":str(row[3]),
            "expire":str(row[7]),
            }
        i=i+1
    conn.commit()
    cursor.close()
    conn.close()
    #View
    return jsonify(valid)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=80)
    #app.run(debug=True)


# get sub video id
# select subvideo_id from subvideos inner join videos on subvideos.video_id=videos.video_id where videos.video_name='The trap';

# get all movies name
# select video_name from videos;