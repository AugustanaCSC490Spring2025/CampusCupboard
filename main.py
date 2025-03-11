import os
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inventory')
def inventory():
    return "Inventory Feed Page" # Placeholder for inventory implementation

@app.route('/volunteer')
def volunteer():
    return "Volunteer Page" # Placeholder for volunteer implementation

@app.route('/about')
def about():
    return "About Us Page" # Placeholder for about page implementation

@app.route('/admin')
def admin():
    return "Admin Page" # Placeholder for admin page implementation

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)