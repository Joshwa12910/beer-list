from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage
beers = []

@app.route('/')
def index():
    return render_template('index.html', beers=beers)

if __name__ == '__main__':
    app.run(debug=True)