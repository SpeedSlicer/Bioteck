from flask import Flask, render_template, render_template_string, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/time')
def get_time():
    now = datetime.now()
    time_string = now.strftime('%I:%M %p')
    return jsonify({'time': time_string})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)