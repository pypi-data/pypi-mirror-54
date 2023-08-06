import pytest
from click.testing import CliRunner

from qiitacli.client import cmd


def test_client_command():
    runner = CliRunner()
    result = runner.invoke(cmd)
    print(result.output)
    assert result.exit_code == 0


sub_commands = [
    ('upload'),
    ('update'),
    ('list'),
    ('status'),
    ('delete'),
]


@pytest.mark.parametrize("sub", sub_commands)
def test_subcommand(sub):
    runner = CliRunner()
    result = runner.invoke(cmd, [sub, '--help'])
    print(result.output)
    assert result.exit_code == 0


@pytest.mark.parametrize("sub", sub_commands)
def test_subcommand_verbose(sub):
    runner = CliRunner()
    result = runner.invoke(cmd, ['--verbose', sub, '--help'])
    print(result.output)
    assert result.exit_code == 0
