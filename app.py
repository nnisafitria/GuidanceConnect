from flask import Flask, redirect, url_for, jsonify, render_template, request, hashlib, jwt, datetime, timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

MONGODB_CONNECTION_STRING = "mongodb+srv://annisafitria821:sparta@cluster0.cjx4lrn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client.dbmypbb

@app.route('/')
def index():
    blogs = list(db.blogs.find({}))
    return render_template('index.html',blogs=blogs)

@app.route('/profil')
def profil():
    return render_template('profil.html')

@app.route('/alumni')
def alumni():
    return render_template('alumni.html')

@app.route('/forum')
def forum():
    return render_template('forum.html')

@app.route('/konseling')
def konseling():
    return render_template('konseling.html')

@app.route('/elibrary')
def elibrary():
    return render_template('elibrary.html')

@app.route('/advokasi')
def advokasi():
    return render_template('advokasi.html')

@app.route('/beasiswa')
def beasiswa():
    return render_template('informasiBeasiswa.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/alumni_mahasiswa')
def alumni_mahasiswa():
    return render_template('mahasiswa_alumni.html')

@app.route('/admin')
def admin():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin_mahasiswa')
def admin_mahasiswa():
    return render_template('admin_mahasiswa.html')

@app.route('/tambah_mahasiswa')
def tambah_mahasiswa():
    return render_template('tambah_mahasiswa.html')

@app.route('/admin_alumni')
def admin_alumni():
    return render_template('admin_alumni.html')

@app.route('/tambah_alumni')
def tambah_alumni():
    return render_template('tambah_alumni.html')

@app.route('/admin_blog')
def admin_blog():
    blogs = list(db.blogs.find({}))
    return render_template('admin_blog.html',blogs=blogs)

@app.route('/tambah_blog', methods=['GET', 'POST'])
def tambah_blog():
    if request.method == 'POST':
        judul = request.form.get('judul')
        deskripsi = request.form.get('deskripsi')
        gambar = request.files.get('gambar')

        if not judul or not gambar or not deskripsi:
            return jsonify({"msg": 'Semua field harus diisi'})

        if gambar:
            filename = secure_filename(gambar.filename)
            file_path = os.path.join('static/img/blog', filename)
            gambar.save(file_path)
        else:
            filename = None

        doc = {
            'nama':judul,
            'gambar':filename,
            'deskripsi':deskripsi
        }
        db.blogs.insert_one(doc)

        return redirect(url_for("admin_blog"))
    return render_template('tambah_blog.html')

@app.route('/edit_blog/<id>', methods=['GET', 'POST'])
def edit_blog(id):
    if request.method == 'POST':
        judul = request.form.get('judul')
        deskripsi = request.form.get('deskripsi')
        gambar = request.files.get('gambar')
        
        doc = {
            'nama':judul,
            'deskripsi':deskripsi
        }

        if gambar:
            filename = (gambar.filename)
            file_path = os.path.join('static/img/blog', filename)
            gambar.save(file_path)
            doc['gambar'] = filename

        db.blogs.update_one({'_id': ObjectId(id)}, {"$set": doc})
        return redirect(url_for("admin_blog"))
    
    blog = db.blogs.find_one({'_id': ObjectId(id)})
    return render_template('edit_blog.html', blog=blog)

@app.route('/delete/<id>', methods=['POST'])
def delete_blog(id):
    db.blogs.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('admin_blog'))

@app.route('/admin_infobeasiswa')
def admin_infobeasiswa():
    infos = list(db.infos.find({}))
    return render_template('admin_infobeasiswa.html',infos=infos)

@app.route('/tambah_beasiswa')
def tambah_beasiswa():
    if request.method == 'POST':
        namabeasiswa= request.form.get('nama beasiswa')
        deskripsidanpersyaratan = request.form.get('deskripsi dan persyaratan')
        gambarbeasiswa = request.files.get('gambar beasiswa')

        if not namabeasiswa or not gambarbeasiswa or not deskripsidanpersyaratan:
            return jsonify({"msg": 'Semua field harus diisi'})

        if gambarbeasiswa:
            filename = secure_filename(gambarbeasiswa.filename)
            file_path = os.path.join('static/img/info beasiswa', filename)
            gambarbeasiswa.save(file_path)
        else:
            filename = None

        doc = {
            'namabeasiswa':namabeasiswa,
            'gambarbeasiswa':filename,
            'deskripsidanpersyaratan':deskripsidanpersyaratan
        }
        db.infos.insert_one(doc)

        return redirect(url_for("admin_infobeasiswa"))
    return render_template('tambah_beasiswa.html')

@app.route('/edit_info/<id>', methods=['GET', 'POST'])
def edit_info(id):
    if request.method == 'POST':
        namabeasiswa = request.form.get('namabeasiswa')
        deskripsidanpersyaratan = request.form.get('deskripsidanpersyaratan')
        gambarbeasiswa = request.files.get('gambarbeasiswa')
        
        doc = {
            'nama':namabeasiswa,
            'deskripsi':deskripsidanpersyaratan
        }

        if gambarbeasiswa:
            filename = (gambarbeasiswa.filename)
            file_path = os.path.join('static/img/info beasiswa', filename)
            gambarbeasiswa.save(file_path)
            doc['gambarbeasiswa'] = filename

        db.infos.update_one({'_id': ObjectId(id)}, {"$set": doc})
        return redirect(url_for("admin_infobeasiswa"))
    
    info = db.infos.find_one({'_id': ObjectId(id)})
    return render_template('edit_blog.html', info=info)

@app.route('/delete/<id>', methods=['POST'])
def delete_info(id):
    db.infos.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('admin_infobeasiswa'))

@app.route('/semester1')
def semester1():
    return render_template('semester1.html')

@app.route('/semester2')
def semester2():
    return render_template('semester2.html')

@app.route('/semester3')
def semester3():
    return render_template('semester3.html')

@app.route('/semester4')
def semester4():
    return render_template('semester4.html')

@app.route('/semester5')
def semester5():
    return render_template('semester5.html')

@app.route('/semester6')
def semester6():
    return render_template('semester6.html')

@app.route('/', methods=['GET'])
def home():
        token_recieve = request.cookies.gey('mytoken')
        try:
            payload = jwt.decode(
            token_recieve, 
            SECRET_KEY, 
            algorithms=['HS256']
            )
            admin_info = db.admin.find_one({'id': payload['id']})
            return render_template('admin.html', nickname=admin_info['nick'])
        except jwt.ExpiredSignatureError:
            return redirect(url_for('login', msg="Token login anda telah kedaluwarsa"))
        except jwt.exceptions.DecodeError:
            return redirect(url_for(
            'login',
            msg="Ada masalah saat masuk"
        ))

@app.route('/admin', methods=['GET'])
def admin():
    msg = request.args.get('msg')
    return render_template('login.html', msg=msg)

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    id_recieve = request.form.get('id_give')
    pw_recieve = request.form.get('pw_give')
    nickname_recieve = request.form.get('nickname_give')
    
    pw_hash = hashlib.sha256(pw_recieve.encode('utf-8')).hexdigest()
    db.user.insert_one({
      'id': id_recieve,
      'pw': pw_hash,
      'nick': nickname_recieve, 
    })
    
    return jsonify({
        'result': 'success'})
    
@app.route('/api/login', methods=['POST'])
def api_login():
        id_recieve = request.form.get('id_give')
        pw_recieve = request.form.get('pw_give')
        pw_hash = hashlib.sha256(pw_recieve.encode('utf-8')).hexdigest()
        result = db.admin.find_one({
            'id': id_recieve,
            'pw': pw_recieve
        })
        if result:
            payload = {
                'id': id_recieve,
                'exp': datetime.utcnow() + timedelta(seconds=1)
            }
            token = jwt.encode(
                payload,
                SECRET_KEY,
                algorithms=['HS256']
            )
            return jsonify({
                'result': 'success',
                'token': token
            })
        else:
            return jsonify({
                'result': 'fail',
                'msg': 'Baik id atau kata sandi anda salah', 
            })
@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_recieve = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(
            token_recieve,
            SECRET_KEY,
            algorithms=['HS256']
        )
        print(payload)
        admin_info = db.admin.find_one({'id': payload.get('id')}, {'_id': 0})
        return jsonify({
            'result': 'success',
            'nickname': admin_info.get('nick')
        })
    except jwt.ExpiredSignatureError:
        msg = "Token login anda telah kedaluwarsa"
        return jsonify({'result': 'fail', 'msg': msg})
    except jwt.exceptions.DecodeError:
        msg="Ada masalah saat masuk"
        return jsonify({'result': 'fail', 'msg': msg})

if __name__ == '__main__':
    app.run(port=5000,debug=True)