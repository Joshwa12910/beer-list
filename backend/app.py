from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('beers.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS beers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            brewery TEXT,
            abv REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()


@app.route('/beers', methods=['GET'])
def get_beers():
    conn = sqlite3.connect('beers.db')
    c = conn.cursor()
    c.execute("SELECT id, name, brewery, abv FROM beers")
    rows = c.fetchall()
    conn.close()

    beers = []
    for row in rows:
        beers.append({
            "id": row[0],
            "name": row[1],
            "brewery": row[2],
            "abv": row[3]
        })

    return jsonify(beers)


@app.route('/beers', methods=['POST'])
def add_beer():
    data = request.json

    name = data.get("name")
    brewery = data.get("brewery")
    abv = data.get("abv")

    if not name or len(name) > 100:
        return jsonify({"error": "Invalid name"}), 400

    if not brewery or len(brewery) > 100:
        return jsonify({"error": "Invalid brewery"}), 400

    try:
        abv = float(abv)
        if abv < 0 or abv > 100:
            return jsonify({"error": "Invalid ABV"}), 400
    except:
        return jsonify({"error": "ABV must be a number"}), 400

    conn = sqlite3.connect('beers.db')
    c = conn.cursor()
    c.execute("INSERT INTO beers (name, brewery, abv) VALUES (?, ?, ?)",
              (name, brewery, abv))
    conn.commit()
    conn.close()

    return jsonify({"message": "Beer added"}), 201


@app.route('/beers/<int:id>', methods=['DELETE'])
def delete_beer(id):
    conn = sqlite3.connect('beers.db')
    c = conn.cursor()
    c.execute("DELETE FROM beers WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted"})


if __name__ == '__main__':
    app.run(port=5001, debug=True)