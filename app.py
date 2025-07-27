from  flask import Flask,render_template,redirect,request,url_for,session,flash

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
# ...existing code...
app =Flask(__name__)
app.secret_key = '515151' 


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(email='admin@example.com').first():
        from werkzeug.security import generate_password_hash
        admin = User(email='admin@example.com', password=generate_password_hash('admin123'))
        db.session.add(admin)
        db.session.commit()
@app.route('/')
def home():
    return redirect(url_for('login'))
# ...existing code...


@app.route('/login' , methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user'] = user.email
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.')
            return redirect(url_for('login'))



    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))
# ...existing code...

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404 - Page Not Found</h1>", 404

if __name__ == '__main__':
    app.run(debug=1)

