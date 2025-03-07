from flask import request, Blueprint
import logging
from flask import jsonify
import requests

from src.utils.server_interface import create_http_server
from src.utils.dns_interface import GetIP
from src.utils.http_interface import GetPage

logger = logging.getLogger(__name__)

agent_apis = Blueprint('api', __name__)

@agent_apis.route('/run-task/get_ip_dns', methods=["POST"])
def get_ip():
    params = request.json
    domain = params.get("domain")

    response = GetIP(domain).get_ip()
    if response:
        return jsonify(response), 200
    else:
        return jsonify({"Error": "Can't retrieve IP from the domain"}), 500


@agent_apis.route('/run-task/get_page', methods=["POST"])
def get_page():
    params = request.json
    uri = params.get("uri")
    port = params.get("port")
    domain = params.get("domain")

    response = GetPage(domain, port, uri).get_page()

    if response:
        logger.info("Page successfully received")
        return jsonify(response), 200
    else:
        logger.error("Page was not received")
        return jsonify({"Error": "Can't open page"}), 500


@agent_apis.route('/run-task/server_status/<task_id>', methods=["GET"])
def server_status(task_id):
    result = create_http_server.AsyncResult(task_id)
    if requests.get(f"http://127.0.0.1:{result.info['port']}{result.info['uri']}").ok:
        return jsonify({"task_id": task_id, "result": "CREATED"})
    return jsonify({"task_id": task_id, "status": "Pending"})


@agent_apis.route('/run-task/start_server', methods=["POST"])
def start_server():
    params = request.json
    user = request.headers.get('user')
    port = params.get("port")
    uri = params.get("uri")
    data_to_return = params.get("data_to_return")

    result = create_http_server.delay(port, uri, data_to_return, user)
    logger.info(f"Creating server: {result.id} requested by {user}")
    return jsonify({"task_id": result.id, "status": "Task started", "server_url": "http://localhost:"f"{port}{uri}"})
