@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    brewery = request.form.get('brewery')
    abv = request.form.get('abv')

    # Validation
    if not name or len(name) > 100:
        return "Invalid beer name"

    if not brewery or len(brewery) > 100:
        return "Invalid brewery"

    try:
        abv = float(abv)
        if abv < 0 or abv > 100:
            return "Invalid ABV"
    except:
        return "ABV must be a number"

    beers.append({
        'name': name,
        'brewery': brewery,
        'abv': abv
    })

    return redirect(url_for('index'))