import os
from pathlib import Path

PRODUCT_NAME = 'qiitacli'
ACCESSTOKEN_PATH = os.environ.get(
    "QIITACLI_ACCESSTOKEN_PATH",
    os.path.join(Path.home(), ".{}.secret".format(PRODUCT_NAME)))

__version__ = '0.1.0'
__name__ = PRODUCT_NAME
