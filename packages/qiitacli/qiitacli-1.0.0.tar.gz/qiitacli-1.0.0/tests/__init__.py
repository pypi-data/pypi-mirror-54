import os
from pathlib import Path

BASE_DIR = os.path.abspath(__file__)
TEST_ACCESSTOKEN_PATH = os.path.join('tests', '.accesstoken.secret')
os.environ['QIITACLI_ACCESSTOKEN_PATH'] = TEST_ACCESSTOKEN_PATH


def load_accesstoken():
    token = os.environ.get("ACCESSTOKEN", None)  # for travis
    if token is not None:
        return token

    token_path = Path('etc/accesstoken.secret')  # for pytest
    if token_path.exists():
        with token_path.open("r") as f:
            token = f.readline()
            return token

    return 'accesstoken'  # :-(


def write_accesstoken(token):
    token_path = Path(TEST_ACCESSTOKEN_PATH)
    with token_path.open("w") as f:
        f.write(token)


def remove_accesstoken():
    os.remove(TEST_ACCESSTOKEN_PATH)
