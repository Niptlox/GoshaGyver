from flask import Flask, jsonify, request, abort, make_response, render_template

app = Flask(__name__)

STATE_WET = "wet"
STATE_DRY = "dry"

data = [
    {"id": 0, "title": "Ванная", "enabled": True, "state": STATE_WET},
    {"id": 1, "title": "Подвал", "enabled": False, "state": STATE_DRY}
]


@app.route('/update_data', methods=['POST'])
def update_data():
    print(request.json)
    if not request.json:
        abort(400)
    if "set_enabled" in request.json:
        if not isinstance(request.json["set_enabled"], list):
            request.json["set_enabled"] = [request.json["set_enabled"]]
        for d in request.json["set_enabled"]:
            data[d["id"]]["enabled"] = d["enabled"]
            print("UPDATE", data)
    return jsonify({'result': True})


@app.route('/get_data', methods=['GET'])
def get_tasks():
    return jsonify({'data': data})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")


if __name__ == '__main__':
    app.run(debug=True)
