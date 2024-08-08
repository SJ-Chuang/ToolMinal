from flask import Flask, render_template, request, redirect
from urllib.parse import urlparse
from datetime import datetime
import settings
import logging
import apps
import sys
import os

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

url_patterns = {
    "/app/ytdownload": apps.ytdownload,
}

for prefix, module in url_patterns.items():
    app.register_blueprint(module.blueprint, url_prefix=prefix)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", **dict(
        hostname=urlparse(request.base_url).hostname,
        version=settings.VERSION
    ))

@app.route("/brucechuang", methods=["GET"])
def brucechuang():
    return render_template("brucechuang.html")

if __name__ == "__main__":
    app.run(debug=True, port=8880, host="0.0.0.0")