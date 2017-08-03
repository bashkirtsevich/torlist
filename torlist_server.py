from flask import Flask, jsonify, url_for
from flask_redis import FlaskRedis

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost:6379/1"

redis_store = FlaskRedis(app)


@app.route("/")
def index():
    routes = []
    for rule in app.url_map.iter_rules():
        options = {arg: "[{0}]".format(arg) for arg in rule.arguments}
        url = url_for(rule.endpoint, **options)
        methods = ",".join(rule.methods)
        routes.append({"url": url, "endpoint": rule.endpoint, "methods": methods})

    return jsonify({"greet": "Torlist demo server",
                    "routes": routes})


@app.route("/get_last_update")
def get_last_update():
    value = redis_store.get("last_list_update")
    if value:
        result = value.decode("utf-8")
        return jsonify({"result": result})
    else:
        return jsonify({"result": {"error": "Server is not ready yet"}})


@app.route("/is_contains_ip/<ip_address>")
def is_contains_ip(ip_address):
    return jsonify({"result": redis_store.exists(ip_address)})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
