from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/update', methods=["POST"])
def update():
    payload = request.get_json(force=True)
    humidity = payload['humidity']
    temperature = payload['temperature']
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('INSERT INTO records(humidity, temperature) VALUES(?,?)', (humidity,temperature))
    conn.commit()
    conn.close()
    resp = {'status':'OK'}
    return jsonify(resp)
    
@app.route('/query', methods=["GET"])
def query():
    # name = request.args.get('name')
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('SELECT * FROM records')
    records = c.fetchall()
    results = []
    for r in records:
        results.append({'timestamp':r[1], 'humidity':r[2], 'temperature':r[3]})
    conn.commit()
    conn.close()
    resp = {'status':'OK', 'results':results}
    return jsonify(resp)

if __name__ == '__main__':
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS records
             (_id INTEGER PRIMARY KEY AUTOINCREMENT,
             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
             humidity TEXT NOT NULL,
             temperature TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    app.run(debug=True)
