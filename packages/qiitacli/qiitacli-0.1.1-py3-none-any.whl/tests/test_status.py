from click.testing import CliRunner

from qiitacli.client import cmd

from . import load_accesstoken, remove_accesstoken, write_accesstoken


def test_status():
    token = load_accesstoken()
    write_accesstoken(token)
    runner = CliRunner()
    result = runner.invoke(cmd, ['status'])
    print(result.output)
    assert result.exit_code == 0
    remove_accesstoken()


def test_status_bad_accesstoken():
    write_accesstoken('bud access token')
    runner = CliRunner()
    result = runner.invoke(cmd, ['status'])
    print(result.output)
    assert result.exit_code == 1
    remove_accesstoken()
