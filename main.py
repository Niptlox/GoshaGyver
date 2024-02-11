import os

from flask import Flask, jsonify, request, abort, make_response, render_template, send_from_directory

app = Flask(__name__, root_path=os.getcwd())
app.config['UPLOAD_FOLDER'] = "uploads"
LOG_FILENAME = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], "logs.txt")

VIEW_CARD = 1
VIEW_CHOICE = 2

STATE_WET = "wet"
STATE_DRY = "dry"

MODE_AUTO = 0
MODE_HAND = 1
with open(LOG_FILENAME, "r") as f:
    logging_text = "".join(f.readlines()[-20:])

data = {"home": [
    {"id": 0, "title": "Ванная", "enabled": True, "state": STATE_WET, "view_type": VIEW_CARD},
    {"id": 1, "title": "Подвал", "enabled": False, "state": STATE_DRY, "view_type": VIEW_CARD}
],
    "settings": {
        "work_mode": MODE_AUTO,
        "testing_text": "TESTING....",
        "logging_text": logging_text,
        "tap_state": 0
    }
}


def logf(*s):
    st = " ".join(map(str, s))+"\n"
    with open(LOG_FILENAME, "a") as f:
        f.write(st)
    data["settings"]["logging_text"] = st + data["settings"]["logging_text"]


@app.route('/update_data', methods=['POST'])
def update_data():
    print(request.json)
    if not request.json:
        abort(400)
    category = "home"
    if "set_enabled" in request.json:
        # if not isinstance(request.json["set_enabled"], list):
        #     request.json["set_enabled"] = [request.json["set_enabled"]]
        for d in request.json["set_enabled"]:
            data[category][d["id"]]["enabled"] = d["enabled"]
            print("UPDATE E", data)
    # if "set_mode" in request.json:
    #     for d in request.json["set_mode"]:
    #         data[category][d["id"]]["mode"] = d["mode"]
    #         print("UPDATE M", data)
    return jsonify({'result': True})


@app.route('/update_settings', methods=['POST'])
def set_settings():
    print(request.json)
    if not request.json:
        abort(400)
    name = request.json.get("name", "work_mode")
    value = request.json.get("value")
    data["settings"][name] = value
    return jsonify({'result': True})


@app.route('/get_data', methods=['GET'])
def get_tasks():
    return jsonify({'data': data["home"]})


@app.route('/get_settings', methods=['GET'])
def get_settings():
    print("r", data["settings"])
    return jsonify({'data': data["settings"]})


@app.route('/start_testing', methods=['GET'])
def testing():
    data["settings"]["testing_text"] += "\n START ttttt) 10% <br>"
    logf("start testing!")
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(uploads, filename)


@app.route('/download_logs', methods=['GET', 'POST'])
def download_logs():
    return send_from_directory(LOG_FILENAME, "")


if __name__ == '__main__':
    app.run()
