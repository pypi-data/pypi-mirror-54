import yaml
from yaml.error import YAMLError

from qiitacli.exceptions import QiitaCliParseError


def parse(filestream, separator='---'):
    '''
    Parse options and body from FileStream

    Args:
        filestream _io.TextIOWrapper: parse file stream object
        separator str: separator for options and body

    Returns:
        dict: {'options': options, 'body': body}

    Raises:
        QiitaCliParseError
    '''
    lines = filestream.readlines()
    options = parse_option(lines)
    body = parse_body(lines)
    res = {'options': options, 'body': body}
    return res


def parse_option(lines, separator='---'):
    '''
    Parse options and body from FileStream

    Args:
        lines list: string list
        separator str: separator for options and body

    Returns:
        dict: options

    Raises:
        QiitaCliParseError
    '''
    text = ''.join(lines)
    options = {}
    require_options = ['title', 'tags']
    try:
        loads = yaml.safe_load_all(text)
        options = next(loads)
    except YAMLError as error:
        raise QiitaCliParseError(error)

    for require_option in require_options:
        if require_option not in options.keys():
            msg = 'options validate is failed.'
            msg += '{} is required.'.format(require_option)
            raise QiitaCliParseError(msg)

    return options


def parse_body(lines, separator='---'):
    '''
    Parse options and body from FileStream

    Args:
        lines list: string list
        separator str: separator for options and body

    Returns:
        str: body

    Raises:
        QiitaCliParseError
    '''
    # 2行目以降でセパレーターが来るまでを、 ヘッダーとし無視する。
    separat_lineno = 1
    for lineno in range(separat_lineno, len(lines)):
        line = lines[lineno]
        if line.startswith(separator):
            separat_lineno = lineno + 1

    if separat_lineno == 1:
        msg = 'Separator Not Found. Separator is {}'.format(separator)
        raise QiitaCliParseError(msg)

    body = ''.join(lines[separat_lineno:])
    return body
