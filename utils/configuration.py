from SmartDjango import NetPacker

from Config.models import Config, CI
from utils.spider.economist import EconomistSpider

DEV_MODE = True

NetPacker.set_mode(debug=DEV_MODE)
# NetPacker.customize_http_code(fixed_http_code=200)

SECRET_KEY = Config.get_value_by_key(CI.PROJECT_SECRET_KEY)
JWT_ENCODE_ALGO = Config.get_value_by_key(CI.JWT_ENCODE_ALGO)

SPIDER = EconomistSpider()
