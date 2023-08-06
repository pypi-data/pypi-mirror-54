import os
from pathlib import Path

import pytest

from qiitacli.accesstoken import (_read_accesstoken_from_stdin,
                                  get_accesstoken, set_accesstoken)
from qiitacli.exceptions import QiitaCliException

from . import TEST_ACCESSTOKEN_PATH


def test_read_accesstoken_from_stdin(monkeypatch):

    inputstr = "accesstoken"

    def mockreturn(args):
        return inputstr

    monkeypatch.setattr("builtins.input", mockreturn)

    token = _read_accesstoken_from_stdin()
    assert token == inputstr


def test_read_accesstoken_error(monkeypatch):

    def mockreturn(args):
        raise KeyboardInterrupt()

    monkeypatch.setattr("builtins.input", mockreturn)

    with pytest.raises(QiitaCliException):
        _read_accesstoken_from_stdin()

    def mockreturn(args):
        raise EOFError()

    monkeypatch.setattr("builtins.input", mockreturn)

    with pytest.raises(QiitaCliException):
        _read_accesstoken_from_stdin()


def test_set_accesstoken(monkeypatch):
    inputstr = "accesstoken"

    def mockreturn(args):
        return inputstr

    monkeypatch.setattr("builtins.input", mockreturn)
    monkeypatch.setattr("os.umask", mockreturn)

    token = set_accesstoken()
    assert token == inputstr
    os.remove(TEST_ACCESSTOKEN_PATH)

    token = set_accesstoken(inputstr)
    assert token == inputstr
    os.remove(TEST_ACCESSTOKEN_PATH)


def test_set_accesstoken_error(monkeypatch):
    inputstr = "accesstoken"

    def mockreturn(args):
        raise OSError()

    monkeypatch.setattr("os.umask", mockreturn)

    with pytest.raises(QiitaCliException):
        set_accesstoken(inputstr)


def test_get_accesstoken():
    inputstr = "accesstoken"

    p = Path(TEST_ACCESSTOKEN_PATH)
    with p.open("w") as f:
        f.write(inputstr)

    token = get_accesstoken()
    assert token == inputstr
    os.remove(TEST_ACCESSTOKEN_PATH)


def test_get_accesstoken_file_not_exist(monkeypatch):
    inputstr = "accesstoken"

    def mockreturn(args):
        return inputstr

    monkeypatch.setattr("builtins.input", mockreturn)
    monkeypatch.setattr("os.umask", mockreturn)

    token = get_accesstoken()
    assert token == inputstr
    os.remove(TEST_ACCESSTOKEN_PATH)


def test_get_accesstoken_error(monkeypatch):
    inputstr = "accesstoken"

    p = Path(TEST_ACCESSTOKEN_PATH)
    with p.open("w") as f:
        f.write(inputstr)

    def mockreturn(*args):
        raise OSError()

    monkeypatch.setattr("pathlib.Path.open", mockreturn)

    with pytest.raises(QiitaCliException):
        get_accesstoken()
    os.remove(TEST_ACCESSTOKEN_PATH)
