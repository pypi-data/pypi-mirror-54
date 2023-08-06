import pytest
from click.testing import CliRunner

from qiitacli.client import cmd

from . import load_accesstoken, remove_accesstoken, write_accesstoken


def test_list():
    token = load_accesstoken()
    write_accesstoken(token)
    runner = CliRunner()
    result = runner.invoke(cmd, ['list'])
    print(result.output)
    assert result.exit_code == 0
    remove_accesstoken()


def test_list_bad_accesstoken():
    write_accesstoken('bad accesstoken')
    runner = CliRunner()
    result = runner.invoke(cmd, ['list'])
    print(result.output)
    assert result.exit_code == 1
    remove_accesstoken()


@pytest.mark.parametrize("option", [
    (['--id']),
    (['--date']),
    (['--tags']),
    (['--url']),
    (['--separator', ',']),
])
def test_list_with_option(option):
    token = load_accesstoken()
    write_accesstoken(token)
    runner = CliRunner()
    result = runner.invoke(cmd, ['list'] + option)
    print(result.output)
    assert result.exit_code == 0
    remove_accesstoken()
