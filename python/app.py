from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
return "<h1>Hello, Cyber Security Club! This is a VULNERABLE app.</h1>"

@app.route('/secret')
def secret():
return f"<h1>The secret is: {os.environ.get('MY_SECRET', 'No secret found')}</h1>"

if __name__ == '__main__':
app.run(host='0.0.0.0', port=5000)
