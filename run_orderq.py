#!/usr/bin/env python3

import json, os
import flask as _f, setproctitle
import configparser as _cp


# -- -- -- --
ROOT_DIR = "/opt/iotech/orderQ"
if os.uname()[1] == "3cpo":
   ROOT_DIR = "/home/erik/__github__/orderq"
# -- -- -- --
TMPLS_DIR = f"{ROOT_DIR}/tmpls"
STATIC_DIR = f"{ROOT_DIR}/static"
INI_FILE = f"{ROOT_DIR}/conf/site.ini"
if not os.path.exists(INI_FILE):
   raise FileExistsError(INI_FILE)

INI: _cp.ConfigParser = _cp.ConfigParser()
if len(INI.read(INI_FILE)) != 1:
   raise Exception("IniLoadingError")


FLASK_PORT: int = INI.getint("FLASK", "PORT")
APP_NAME: str = INI.get("FLASK", "APP_NAME")
app = _f.Flask(APP_NAME, static_url_path=""
   , static_folder=STATIC_DIR, template_folder=TMPLS_DIR)


@app.route("/info", methods=["GET"])
def info():
   remote_ip = _f.request.remote_addr
   return _f.render_template("info.html", remote_ip=remote_ip)

@app.route("/get/called-orders/<shopid>", methods=["GET"])
def get_called_orders(shopid):
   from core.shopOps import shopOps
   ops: shopOps = shopOps(INI, shopid)
   d: {} = ops.get_called_orders()
   resp: _f.Response = _f.make_response(json.dumps(d))
   resp.status_code = 200
   resp.content_type = "application/json"
   return resp

@app.route("/set/called-orders/<shopid>", methods=["POST"])
def set_called_orders(shopid):
   from core.shopOps import shopOps
   numbers = _f.request.args.get("n", type=str)
   ops: shopOps = shopOps(INI, shopid)
   ops.update_called_orders(shopid, numbers)
   return "OK", 200, {"content-type": "text/plain"}


# == == == == == == == == == == == == == == == == == == == == == == ==
# -- -- [ start app here ] -- --
if __name__ == "__main__":
   setproctitle.setproctitle(APP_NAME)
   app.run(host="0.0.0.0", port=FLASK_PORT, debug=False)
# == == == == == == == == == == == == == == == == == == == == == == ==
