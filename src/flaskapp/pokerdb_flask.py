from flask import Flask, render_template
from pydb import dbconn
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('example_child.html')
    # return 'hey bb'

@app.route('/yiwen')
def yiwen():
    return render_template('example_child.html')

if __name__=='__main__':
    app.run(host='0.0.0.0')
