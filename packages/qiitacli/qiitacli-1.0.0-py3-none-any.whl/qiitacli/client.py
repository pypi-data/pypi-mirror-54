#!/usr/bin/env python3

import click
from qiita_v2.client import QiitaClient
from qiita_v2.exception import QiitaApiException

from qiitacli.accesstoken import get_accesstoken
from qiitacli.exceptions import QiitaCliParseError
from qiitacli.option_parser import parse

VERBOSE = False


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def cmd(verbose):
    global VERBOSE
    if verbose:
        VERBOSE = verbose


@cmd.command()
@click.option('--id', '-i', is_flag=True, help='Show with article id')
@click.option('--date', '-d', is_flag=True, help='Show with article update date')  # noqa E501
@click.option('--tags', '-t', is_flag=True, help='Show with article tags')
@click.option('--url', '-u', is_flag=True, help='Show with article url')
@click.option('--separator', '-s', help='separator')
def list(id, date, tags, url, separator):
    '''
    List your article
    '''
    token = get_accesstoken()
    client = QiitaClient(access_token=token)
    res = None
    try:
        res = client.get_authenticated_user_items()
    except QiitaApiException as error:
        click.echo('Command failed: {}'.format(error))
        raise click.Abort()

    str_header = ''
    str_format = ''
    if separator is None:
        separator = '|'
    if id:
        str_header += 'id' + separator
        str_format += '{id}' + separator
    if date:
        str_header += 'date' + separator
        str_format += '{date}' + separator
    str_header += 'title'
    str_format += '{title}'
    if tags:
        str_header += separator + 'tags'
        str_format += separator + '{tags}'
    if url:
        str_header += separator + 'url'
        str_format += separator + '{url}'
    str_header += '\n'
    str_format += '\n'

    output_str = str_header

    for article in res.to_json():
        id = article['id']
        date = article['updated_at']
        url = article['url']
        title = article['title']
        tags_list = [t['name'] for t in article['tags']]
        tags = ','.join(tags_list)
        output_str += str_format.format(id=id,
                                        date=date,
                                        url=url,
                                        title=title,
                                        tags=tags)
    click.echo(output_str)


@cmd.command()
@click.argument('article', required=True, type=click.File('r'))  # noqa E501
@click.option('--force', '-f', is_flag=True, help='Force upload article')
@click.option('--tweet', '-T', is_flag=True, help='Tweet when article upload[Require Twitter linkage settnigs]')  # noqa E501
def upload(article, force, tweet):
    '''
    Upload new article
    '''
    if VERBOSE:
        click.echo('articlefile: [{}]'.format(article.name))

    token = get_accesstoken()
    client = QiitaClient(access_token=token)
    params = {}

    option_with_body = None
    try:
        option_with_body = parse(article)
    except QiitaCliParseError as error:
        click.echo('Command failed: {}'.format(error))
        raise click.Abort()
    body = option_with_body['body']
    options = option_with_body['options']
    params['body'] = body
    params['title'] = options['title']
    params['private'] = options.get('private', False)
    tags = options['tags']
    tag_and_versions = []
    for tag in tags:
        tag_and_versions.append({
            'name': tag,
        })
    params['tags'] = tag_and_versions
    params['tweet'] = tweet

    if VERBOSE:
        click.echo('post params: {}'.format(params))

    if not force:
        click.confirm('Are you sure you want to upload?', abort=True)

    res = None
    try:
        res = client.create_item(params=params)
    except QiitaApiException as error:
        click.echo('Command failed: {}'.format(error))
        raise click.Abort()
    click.echo('status code: {}'.format(res.status))
    if VERBOSE:
        click.echo('response json: {}'.format(res.to_json()))


@cmd.command()
@click.argument('article_id', required=True)
@click.option('--force', '-f', is_flag=True, help='Force delete article')
def delete(article_id, force):
    '''
    Delete article
    '''
    token = get_accesstoken()
    client = QiitaClient(access_token=token)
    res = None
    try:
        res = client.get_item(article_id)
    except QiitaApiException as error:
        click.echo('Command failed: {}'.format(error))
        raise click.Abort()
    title = res.to_json()['title']
    click.echo('title: {}'.format(title))
    if not force:
        click.confirm('Are you sure you want to delete?', abort=True)
    try:
        res = client.delete_item(article_id)
        click.echo('status code: {}'.format(res.status))
    except QiitaApiException as error:
        click.echo('Command failed: {}'.format(error))
        raise click.Abort()


@cmd.command()
@click.argument('article_id', required=True)
@click.argument('article', required=True, type=click.File('r'))  # noqa E501
@click.option('--force', '-f', is_flag=True, help='Force update article')
def update(article_id, article, force):
    '''
    Update article
    '''
    if VERBOSE:
        click.echo('article id: [{}]'.format(article_id))

    token = get_accesstoken()
    client = QiitaClient(access_token=token)
    res = None
    try:
        res = client.get_item(article_id)
    except QiitaApiException as error:
        click.echo('Command failed: {}'.format(error))
        raise click.Abort()
    title = res.to_json()['title']
    click.echo('title: [{}]'.format(title))
    click.echo('articlefile: [{}]'.format(article.name))
    if not force:
        click.confirm('Are you sure you want to update?', abort=True)

    params = {}
    option_with_body = None
    try:
        option_with_body = parse(article)
    except QiitaCliParseError as error:
        click.echo('Command failed: {}'.format(error))
        raise click.Abort()
    body = option_with_body['body']
    options = option_with_body['options']
    params['body'] = body
    params['title'] = options['title']
    params['private'] = options.get('private', False)
    tags = options['tags']
    tag_and_versions = []
    for tag in tags:
        tag_and_versions.append({
            'name': tag,
        })
    params['tags'] = tag_and_versions

    if VERBOSE:
        click.echo('patch params: {}'.format(params))

    res = None
    try:
        res = client.update_item(article_id, params=params)
    except QiitaApiException as error:
        click.echo('Command failed: {}'.format(error))
        raise click.Abort()
    click.echo('status code: {}'.format(res.status))
    if VERBOSE:
        click.echo('response json: {}'.format(res.to_json()))


@cmd.command()
def status():
    '''
    Show authenticated user data
    '''
    token = get_accesstoken()
    client = QiitaClient(access_token=token)
    res = None
    try:
        res = client.get_authenticated_user()
    except QiitaApiException as error:
        click.echo('Command failed: {}'.format(error))
        raise click.Abort()
    output_str = '''id              : {id}
name            : {name}
location        : {location}
description     : {description}
followees_count : {followees_count}
followers_count : {followers_count}
items_count     : {items_count}
facebook_id     : {facebook_id}
github_name     : {github_login_name}
linkedin_id     : {linkedin_id}
twitter_name    : {twitter_screen_name}
'''.format(**res.to_json())
    click.echo(output_str)
