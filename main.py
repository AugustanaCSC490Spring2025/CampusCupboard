import os
from flask import Flask, redirect, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

messages = []  # List to store messages

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres: yIf7EOylTW2vKJK5@nobly-intrigued-dassie.data-1.use1.tembo.io:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CENTRAL_TZ = ZoneInfo("America/Chicago")
UTC_TZ = ZoneInfo("UTC")

#reminder to take out IDSwipe class and keep StudentInput
class IDSwipe(db.Model):
    __tablename__ = 'id_swipes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scanned_id = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC_TZ))  

#class to make table for id swipe
class StudentInput(db.Model):
    __tablename__ = 'student_inputs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String, nullable=False)
    pounds_taken = db.Column(db.Float, nullable=False) 
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC_TZ))

class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    shift = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC_TZ))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'POST':
        message = request.form['message']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        messages.append({'text': message, 'timestamp': timestamp})
        return redirect(url_for('inventory'))
    return render_template('inventoryFeed.html', messages=messages)

@app.route('/add_message', methods=['POST'])
def add_message():
    message = request.form['message']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    messages.append({'text': message, 'timestamp': timestamp})
    return redirect(url_for('inventory'))

@app.route('/volunteer')
def volunteer():
    return render_template('volunteer.html')  # Render the volunteer page

@app.route('/aboutus')
def about():
    return render_template('aboutus.html') # Placeholder for about page implementation

@app.route('/admin')
def admin():
    return render_template('admin_page.html') # Placeholder for admin page implementation

@app.route('/IDscan', methods=['GET', 'POST'])
def IDscan():
    if request.method == 'POST':
        scanned_id = request.form.get('inputBox', '').strip()[3:-6]
        if scanned_id:
            new_swipe = IDSwipe(scanned_id=scanned_id)
            db.session.add(new_swipe)
            db.session.commit()

    return render_template('id_scan.html')

@app.route('/student_input', methods=['GET', 'POST'])
def student_input():
    if request.method == 'POST':
        student_id = request.form.get('studentID')
        pounds_taken = request.form.get('poundsTaken')
        pounds_taken = float(pounds_taken)
        
        new_input = StudentInput(student_id=student_id, pounds_taken=pounds_taken)
        db.session.add(new_input)
        db.session.commit()
        
        return redirect(url_for('student_input'))
    return render_template('student_input.html')  

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/volunteer_signup', methods=['GET', 'POST'])
def volunteer_signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        shift = request.form.get('shift')
        
        new_volunteer = Volunteer(name=name, email=email, shift=shift)
        db.session.add(new_volunteer)
        db.session.commit()
        
        return redirect(url_for('volunteer_signup'))
    return render_template('volunteer_signup.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)