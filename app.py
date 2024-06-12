from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
    return render_template('admin_blog.html')

@app.route('/tambah_blog')
def tambah_blog():
    return render_template('tambah_blog.html')

@app.route('/admin_infobeasiswa')
def admin_infobeasiswa():
    return render_template('admin_infobeasiswa.html')

@app.route('/tambah_beasiswa')
def tambah_beasiswa():
    return render_template('tambah_beasiswa.html')

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