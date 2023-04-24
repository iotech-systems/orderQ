
import redis
import configparser as _cp


class shopOps(object):

   def __init__(self, ini: _cp.ConfigParser, shopid: int):
      self.ini: _cp.ConfigParser = ini
      self.shopid = shopid
      self.red: redis.Redis = None

   def __del__(self):
      try:
         if self.red is not None:
            self.red.close()
      except:
         pass

   def get_called_orders(self) -> []:
      self.__set_conn__()
      arr = []
      rval = self.red.hget(f"ORDER_CALL_TABLES", self.shopid)
      if "," in rval:
         arr = rval.split(",")
      return arr

   def update_called_orders(self, shopid, numbers):
      self.__set_conn__()
      rval = self.red.hset(f"ORDER_CALL_TABLES", key=shopid, value=numbers)
      return rval

   def __set_conn__(self):
      # -- -- -- --
      host = self.ini.get("REDIS", "HOST")
      port: int = self.ini.getint("REDIS", "PORT")
      pwd: str = self.ini.get("REDIS", "PWD")
      db: int = self.ini.getint("REDIS", "CALLED_NUMBERS_DB_IDX")
      # -- -- -- --
      self.red: redis.Redis = \
         redis.Redis(host=host, port=port, db=db, password=pwd, decode_responses=True)
      # -- -- -- --
