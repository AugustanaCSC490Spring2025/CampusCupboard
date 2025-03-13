import os
from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# In-memory storage for messages (for demonstration purposes)
messages = []

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
    return "Volunteer Page" # Placeholder for volunteer implementation

@app.route('/aboutus')
def about():
    return render_template('aboutus.html') # Placeholder for about page implementation

@app.route('/admin')
def admin():
    return "Admin Page" # Placeholder for admin page implementation

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)