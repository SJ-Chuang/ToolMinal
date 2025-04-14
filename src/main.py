import importlib.util
from flask import Flask, render_template, request, redirect
from urllib.parse import urlparse
from datetime import datetime
import settings
import logging
import apps
import sys
import os
import importlib
import inspect
from apps.base import AppBase

LOG_DIR = f"{settings.BASE_DIR}/../../logs"

os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=datetime.today().strftime(f"{LOG_DIR}/%Y%m%d.log"),
    filemode="a"
)

console = logging.StreamHandler(sys.stdout)
console.setFormatter(logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"))
logging.getLogger().addHandler(console)

app = Flask(__name__, 
    template_folder=settings.TEMPLATE_FOLDER,
    static_url_path="/static", 
    static_folder=settings.STATIC_FOLDER
)

url_patterns = {}
for root, dirs, files in os.walk(os.path.join(settings.BASE_DIR, "apps")):
    for file in files:
        if file.endswith(".py") and not file.startswith("_"):
            module_name = os.path.splitext(file)[0]
            spec = importlib.util.spec_from_file_location(module_name, f"{root}/{file}")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for name, tmp in inspect.getmembers(module, inspect.isclass):
                if issubclass(tmp, AppBase) and tmp is not AppBase:
                    logging.info(f"Loading `{name}` from {file}")
                    obj = tmp()
                    url_patterns[obj.url_prefix] = {"title": obj.title, "description": obj.description}
                    app.register_blueprint(obj.blueprint)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", **dict(
        hostname=urlparse(request.base_url).hostname,
        url_patterns=url_patterns,
        version=settings.VERSION
    ))

@app.route("/brucechuang", methods=["GET"])
def brucechuang():
    return render_template("brucechuang.html")

if __name__ == "__main__":
    app.run(debug=True, port=8880, host="0.0.0.0")