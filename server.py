from flask import Flask

from src.api_routes.apis import agent_apis
from src.utils.logger_interface import setup_logger

setup_logger("app_log.log", "INFO")


app = Flask(__name__)

app.register_blueprint(agent_apis, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True,
            host="0.0.0.0",
            port=5555)
