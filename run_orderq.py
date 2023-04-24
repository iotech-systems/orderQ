#!/usr/bin/env python3

import flask as _f, setproctitle
import configparser as _cp


ROOT_DIR = "/opt/iotech/orderQ"
TMPLS_DIR = f"{ROOT_DIR}/tmpls"
STATIC_DIR = f"{ROOT_DIR}/static"

FLASK_PORT: int = 8022

APP_NAME = "orderQ"
app = _f.Flask(APP_NAME, static_url_path=""
   , static_folder=STATIC_DIR, template_folder=TMPLS_DIR)

@app.route("/info", methods=["GET"])
def info():
   remote_ip = _f.request.remote_addr
   return _f.render_template("info.html", remote_ip=remote_ip)


# == == == == == == == == == == == == == == == == == == == == == == == == == ==
# -- -- [ start app here ] -- --
if __name__ == "__main__":
   setproctitle.setproctitle(APP_NAME)
   app.run(host="0.0.0.0", port=FLASK_PORT, debug=False)
# == == == == == == == == == == == == == == == == == == == == == == == == == ==
