from pathlib import Path

from click.testing import CliRunner
from qiita_v2.exception import QiitaApiException

from qiitacli.client import cmd

from . import load_accesstoken, remove_accesstoken, write_accesstoken

dammy_article_text = '''
title: dammy article
tags:
    - dammy
    - article
private: yes
---
# dammy article
'''


def dammy_post_success(*args, **kwargs):
    class dammy_response:
        status = 200

        def to_json(self):
            return {'success': 'success'}

    return dammy_response()


def dammy_post_error(*args, **kwargs):
    raise QiitaApiException('error')


def test_upload(monkeypatch):

    monkeypatch.setattr(
        'qiita_v2.client.QiitaClient.create_item', dammy_post_success)

    dammy_article_path = 'dammy_article.md'
    dammy_article = Path(dammy_article_path)
    with dammy_article.open('w') as f:
        f.write(dammy_article_text)

    token = load_accesstoken()
    write_accesstoken(token)
    runner = CliRunner()
    commands = ['upload',
                '--tweet',
                dammy_article_path]
    result = runner.invoke(cmd, commands, input='y')
    print(result.output)
    assert result.exit_code == 0

    remove_accesstoken()
    dammy_article.unlink()


def test_upload_error(monkeypatch):
    monkeypatch.setattr(
        'qiita_v2.client.QiitaClient.create_item', dammy_post_error)

    dammy_article_path = 'dammy_article.md'
    dammy_article = Path(dammy_article_path)
    with dammy_article.open('w') as f:
        f.write(dammy_article_text)

    token = load_accesstoken()
    write_accesstoken(token)
    runner = CliRunner()
    commands = ['upload',
                '--tweet',
                '--force',
                dammy_article_path]
    result = runner.invoke(cmd, commands)
    print(result.output)
    assert result.exit_code == 1

    remove_accesstoken()
    dammy_article.unlink()
