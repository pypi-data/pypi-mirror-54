
from click.testing import CliRunner
from qiita_v2.exception import QiitaApiException

from qiitacli.client import cmd

from . import load_accesstoken, remove_accesstoken, write_accesstoken


def dammy_get_success(*args, **kwargs):
    class dammy_response:
        status = 200

        def to_json(self):
            return {'title': 'dammy article'}

    return dammy_response()


def dammy_delete_success(*args, **kwargs):
    class dammy_response:
        status = 200

        def to_json(self):
            return {'success': 'success'}

    return dammy_response()


def dammy_error(*args, **kwargs):
    raise QiitaApiException('error')


def test_delete(monkeypatch):

    monkeypatch.setattr(
        'qiita_v2.client.QiitaClient.get_item', dammy_get_success)
    monkeypatch.setattr(
        'qiita_v2.client.QiitaClient.delete_item', dammy_delete_success)

    token = load_accesstoken()
    write_accesstoken(token)
    runner = CliRunner()
    commands = ['delete',
                'dammy id', ]
    result = runner.invoke(cmd, commands, input='y')
    print(result.output)
    assert result.exit_code == 0
    remove_accesstoken()


def test_delete_error(monkeypatch):
    monkeypatch.setattr(
        'qiita_v2.client.QiitaClient.get_item', dammy_get_success)
    monkeypatch.setattr('qiita_v2.client.QiitaClient.delete_item', dammy_error)

    token = load_accesstoken()
    write_accesstoken(token)
    runner = CliRunner()
    commands = ['delete',
                '--force',
                'dammy id', ]
    result = runner.invoke(cmd, commands)
    print(result.output)
    assert result.exit_code == 1
    remove_accesstoken()


def test_delete_get_error(monkeypatch):
    monkeypatch.setattr('qiita_v2.client.QiitaClient.get_item', dammy_error)
    monkeypatch.setattr('qiita_v2.client.QiitaClient.delete_item', dammy_error)

    token = load_accesstoken()
    write_accesstoken(token)
    runner = CliRunner()
    commands = ['delete',
                '--force',
                'dammy id', ]
    result = runner.invoke(cmd, commands)
    print(result.output)
    assert result.exit_code == 1
    remove_accesstoken()
