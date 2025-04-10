import os
from flask import Flask, redirect, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo
from werkzeug.utils import secure_filename

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images')

app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

messages = []  # List to store messages
uploaded_images = []  # List to store dictionaries with 'filename' and 'description'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CENTRAL_TZ = ZoneInfo("America/Chicago")
UTC_TZ = ZoneInfo("UTC")
 
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

#homepage route
@app.route('/')
def index():
    return render_template('index.html')

#inventory feed route
@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'POST':
        # Handle message submission
        message = request.form.get('message')
        if message:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            messages.append({'text': message, 'timestamp': timestamp})
        # Redirect to the same page to prevent form resubmission
        return redirect(url_for('inventory'))

    # Pass both messages and uploaded images to the template
    return render_template('inventoryFeed.html', messages=messages, uploaded_images=uploaded_images)

ALLOWED_EXTENSIONS = {'png', 'heic', 'jpg', 'jpeg'}
 
def allowed_file(filename):
     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return redirect(url_for('inventory'))

    file = request.files['image']
    description = request.form.get('description')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Add the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Prepend the new image to the list
        uploaded_images.insert(0, {'filename': filename, 'description': description, 'timestamp': timestamp})

    return redirect(url_for('inventory'))


@app.route('/volunteer')
def volunteer():
    return render_template('volunteer.html')

#about us page route
@app.route('/aboutus')
def about():
    return render_template('aboutus.html') # Placeholder for about page implementation

#admin page route
#   needs a login page page with username and pass at somepoint
@app.route('/admin')
def admin():
    return render_template('admin_page.html') # Placeholder for admin page implementation

#student swipe page route inside admin page
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

@app.route('/data_dashboard', methods=['GET', 'POST']) 
def data_dashboard():
    # all swiped inputs
    student_inputs = StudentInput.query.all()
    
    #convert data to dictionaries
    swipe_data = [{'student_id': input.student_id, 'pounds_taken': input.pounds_taken, 'timestamp': input.timestamp} for input in student_inputs]
    
    #distinct student ID count
    distinct_student_count = db.session.query(StudentInput.student_id).distinct().count()
    total_student_count = db.session.query(StudentInput.student_id).count()
    
    #user ID's
    distinct_user_ids = db.session.query(StudentInput.student_id).distinct().all()
    user_ids = [user_id[0] for user_id in distinct_user_ids]

    #total # of pounds taken
    total_pounds_taken = db.session.query(db.func.sum(StudentInput.pounds_taken)).scalar()

    return render_template('data_dashboard.html', data=swipe_data, total_student_count=total_student_count, distinct_user_count=distinct_student_count, total_lbs_taken=total_pounds_taken)


#calendar page route
@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

#volunteer page signup route
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

