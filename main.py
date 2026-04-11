from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/time')
def get_time():
    now = datetime.now()
    return jsonify({'time': now.strftime('%I:%M %p')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)