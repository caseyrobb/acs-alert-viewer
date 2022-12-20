import redis
from redis.commands.json.path import Path
from flask import Flask, request, Response, jsonify, json, abort, render_template
from flask_caching import Cache
from flask_paginate import Pagination, get_page_args
from datetime import datetime

app = Flask(__name__)
cache = Cache(
    app, config={"CACHE_TYPE": "redis", "CACHE_REDIS_URL": "redis://redis:6379/0"}
)

# redis connection
r = redis.StrictRedis(host="redis", port=6379, decode_responses=True)
try:
    r.ping()
except (redis.exceptions.ConnectionError, ConnectionRefusedError):
    abort(503, {"Error": "Cannot connect to redis"})


@app.route("/api/v1/webhook", methods=["POST"])
def post_alert():
    webhook = request.get_json()
    r.json().set(f"alert:{webhook['alert']['id']}", Path.root_path(), webhook)
    if not r:
        return Response(status=503)
    return Response(status=200)


@app.template_filter("formatDate")
def formatDate(sdate):
    return datetime.strptime(sdate[:19], "%Y-%m-%dT%H:%M:%S")


# @app.route('/api/v1/alert/<id>', methods=['GET'])
def get_alert(id):
    alert = r.json().get(f"alert:{id}")
    if not alert:
        return jsonify(id=f"{id}", status="Not found")
    return alert


# @app.route('/api/v1/alerts', methods=['GET'])
@cache.cached(timeout=20)
def get_alerts():
    alerts = []
    keys = r.keys("alert:*")
    [alerts.append(r.json().get(k)) for k in keys]
    alerts.sort(key=lambda x: x["alert"]["time"], reverse=True)
    return jsonify(alerts)


def get_alerts_page(alerts, offset=0, per_page=10):
    return alerts[offset : offset + per_page]


@app.route("/")
def index():
    page, per_page, offset = get_page_args(
        page_parameter="page", per_page_parameter="per_page"
    )
    alerts = get_alerts().json
    total = len(alerts)
    pagination_alerts = get_alerts_page(alerts, offset=offset, per_page=per_page)
    pagination = Pagination(
        page=page, per_page=per_page, total=total, css_framework="foundation"
    )
    return render_template(
        "index.html",
        alerts=pagination_alerts,
        page=page,
        per_page=per_page,
        pagination=pagination,
    )


@app.route("/alert/<alertId>")
def alert(alertId):
    return render_template("alert.html", alerts=get_alert(alertId))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
