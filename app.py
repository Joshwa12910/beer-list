from flask import Flask, render_template, request, redirect, url_for
from flask import flash

app = Flask(__name__)
app.secret_key = "beerkey"  
beers = []


@app.route('/')
def index():
    return render_template('index.html', beers=beers)


@app.route('/add', methods=['POST'])
def add_beer():
    name = request.form.get('name', '')
    brewery = request.form.get('brewery', '')
    abv = request.form.get('abv', '')

    if len(name) == 0 or len(name) > 100:
        flash("Invalid beer name! What are ya crazy?")
        return redirect(url_for('index'))

    if len(brewery) == 0 or len(brewery) > 100:
        flash("Invalid brewery name! Quit horsing around!")
        return redirect(url_for('index'))

    try:
        abv = float(abv)
        if abv < 0 or abv > 100:
            flash("ABV must be between 0 and 100, durrr")
            return redirect(url_for('index'))
    except:
        flash("ABV must be a number")
        return redirect(url_for('index'))

    beers.append({
        "name": name,
        "brewery": brewery,
        "abv": abv
    })

    return redirect(url_for('index'))


@app.route('/delete/<int:index>')
def delete(index):
    if 0 <= index < len(beers):
        beers.pop(index)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)