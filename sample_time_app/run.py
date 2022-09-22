from flask import Flask
app = Flask(__name__)

from datetime import datetime
import pytz


@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/time')
def curr_time():
    return str(datetime.now(pytz.timezone('US/Eastern')).time())

app.run(host='0.0.0.0',
        port=8080,
        debug=True)
