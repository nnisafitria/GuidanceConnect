from flask import Flask, redirect, url_for, jsonify, render_template, request, session
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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

@app.route('/blog/<id>', methods=['GET'])
def blog(id):
    blog = db.blogs.find_one({'_id': ObjectId(id)})
    return render_template('blog.html', blog=blog)

@app.route('/alumni_mahasiswa')
def alumni_mahasiswa():
    return render_template('mahasiswa_alumni.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Cari pengguna berdasarkan username
        user = db.users.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            # Jika username dan password cocok, set session
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))  # Ganti 'dashboard' dengan halaman setelah login
        else:
            # Jika tidak cocok, tampilkan pesan error
            error_msg = 'Invalid username or password. Please try again.'
            return render_template('login.html', error_msg=error_msg)

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin_mahasiswa', methods=['GET'])
def admin_mahasiswa():
    students = list(db.students.find({}))
    return render_template('admin_mahasiswa.html', students=students)

@app.route('/tambah_mahasiswa', methods=['GET', 'POST'])
def tambah_mahasiswa():
    if request.method == 'POST':
        nim = request.form.get('nim')
        nama = request.form.get('nama')
        
        if nim and nama:
            db.students.insert_one({'nim': nim, 'nama': nama})
        
        return redirect(url_for('admin_mahasiswa'))
    
    return render_template('tambah_mahasiswa.html')

@app.route('/edit_mahasiswa/<student_id>', methods=['GET', 'POST'])
def edit_mahasiswa(student_id):
    student = db.students.find_one({'_id': ObjectId(student_id)})
    
    if request.method == 'POST':
        nim = request.form.get('nim')
        nama = request.form.get('nama')
        
        if nim and nama:
            db.students.update_one({'_id': ObjectId(student_id)}, {'$set': {'nim': nim, 'nama': nama}})
            return redirect(url_for('admin_mahasiswa'))
    
    return render_template('edit_mahasiswa.html', student=student)

@app.route('/delete_mahasiswa/<student_id>', methods=['GET'])
def delete_mahasiswa(student_id):
    db.students.delete_one({'_id': ObjectId(student_id)})
    return redirect(url_for('admin_mahasiswa'))

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
            file_path = os.path.join('GuidanceConnect/static/img/blog', filename)
            gambar.save(file_path)
        else:
            filename = None

        waktu_sekarang = datetime.now()
        waktu_format = waktu_sekarang.strftime('%Y-%m-%d')

        doc = {
            'nama':judul,
            'gambar':filename,
            'deskripsi':deskripsi,
            'time': waktu_format
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
            file_path = os.path.join('GuidanceConnect/static/img/blog', filename)
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
        namabeasiswa= request.form.get('namabeasiswa')
        deskripsidanpersyaratan = request.form.get('deskripsidanpersyaratan')
        gambarbeasiswa = request.files.get('gambarbeasiswa')

        if gambarbeasiswa:
            filename = secure_filename(gambarbeasiswa.filename)
            file_path = os.path.join('GuidanceConnect/static/img/beasiswa', filename)
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

@app.route('/tambah_beasiswa', methods=['GET', 'POST'])

@app.route('/edit_info/<id>', methods=['GET', 'POST'])
def edit_info(id):
    if request.method == 'POST':
        namabeasiswa = request.form.get('namabeasiswa')
        deskripsidanpersyaratan = request.form.get('deskripsidanpersyaratan')
        gambarbeasiswa = request.files.get('gambarbeasiswa')
        
        doc = {
            'namabeasiswa':namabeasiswa,
            'deskripsidanpersyaratan':deskripsidanpersyaratan
        }

        if gambarbeasiswa:
            filename = (gambarbeasiswa.filename)
            file_path = os.path.join('GuidanceConnect/static/img/beasiswa', filename)
            gambarbeasiswa.save(file_path)
            doc['gambarbeasiswa'] = filename

        db.infos.update_one({'_id': ObjectId(id)}, {"$set": doc})
        return redirect(url_for("admin_infobeasiswa"))
    
    info = db.infos.find_one({'_id': ObjectId(id)})
    return render_template('edit_info.html', info=info)

@app.route('/delete_info/<id>', methods=['POST'])
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

if __name__ == '__main__':
    app.run(port=5000,debug=True)