# -*- coding: utf-8 -*-
import json
import logging
import os

import click
from prettytable import PrettyTable

from mootdx.affairs import Affairs
from mootdx.quotes import Quotes
from mootdx.reader import Reader
from mootdx.server import Server

logger = logging.getLogger(__name__)


@click.group()
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, verbose):
    ctx.obj["VERBOSE"] = verbose


@cli.command(help='读取股票在线行情数据.')
@click.option('-o', '--output', default=None, help='输出文件')
@click.option('-s', '--symbol', default='600001', help='股票代码')
@click.option('-a', '--action', default='bars', help='操作类型')
@click.option('-m', '--market', default='std', help='证券市场')
def quotes(symbol, method, market, output):
    client = Quotes.factory(market=market, multithread=True, heartbeat=True)  # 标准市场

    try:
        feed = getattr(client, method)(symbol=symbol)
        feed.to_csv(output) if output else None
        print(feed)
    except Exception as e:
        raise e


@cli.command(help='读取股票本地行情数据.')
@click.option('-d', '--tdxdir', default='c:\\newtdx', help='通达信数据目录')
@click.option('-s', '--symbol', default='600001', help='股票代码')
@click.option('-a', '--action', default='daily', help='操作类型')
@click.option('-m', '--market', default='std', help='证券市场')
def reader(symbol, method, market, tdxdir):
    client = Reader.factory(market=market, tdxdir=tdxdir)  # 标准市场

    try:
        feed = getattr(client, method)(symbol=symbol)
        print(feed)
    except Exception as e:
        raise e


@cli.command(help='测试行情服务器.')
@click.option('-l', '--limit', default='5', help='显示最快前几个，默认 5.')
@click.option('-w', '--write', count=True, help='将最优服务器IP写入配置文件 ~/.mootdx/config.json.')
@click.option('-v', '--verbose', count=True)
def bestip(limit, verbose, write):
    bestip = Server(limit=int(limit), verbose=verbose)
    config = os.path.join(os.environ['HOME'], '.mootdx/config.josn')

    if write:
        if not os.path.exists(config):
            os.mkdir(os.path.join(os.environ['HOME'], '.mootdx'))

        json.dump({'BESTIP': bestip[0]}, open(config, 'w'))
        print('[√] 已经将最优服务器IP写入配置文件 {}'.format(config))


@cli.command(help='财务文件下载&解析.')
@click.option('-p', '--parse', default=None, help='解析文件内容')
@click.option('-l', '--files', count=True, help='列出文件列表')
@click.option('-f', '--fetch', default=None, help='下载全部文件')
# @click.option('-o', '--output', default='output.csv', help='下载文件目录')
@click.option('-d', '--downdir', default='output', help='下载文件目录')
@click.option('-v', '--verbose', count=True)
def affair(parse, files, fetch, downdir, verbose):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    affairs = Affairs.files()

    if files:
        t = PrettyTable(["filename", "filesize", "hash"])
        t.align["filename"] = "l"
        t.align["filesize"] = "l"
        t.align["hash"] = "l"
        t.padding_width = 1

        for x in affairs:
            t.add_row([x['filename'], x['filesize'], x['hash']])

        print(t)

    if fetch:
        if fetch == 'all':
            Affairs.fetch(downdir=downdir)
        else:
            Affairs.fetch(downdir=downdir, filename=fetch.strip('.zip') + '.zip')

    if parse:
        files = [x['filename'] for x in affairs]

        if parse in files:
            if os.path.exists(os.path.join(downdir, parse)):
                df = Affairs.parse(downdir=downdir, filename=parse.strip('.zip') + '.zip')
                print(df)
            else:
                logger.error('file not found.')


def execute():
    cli(obj={})


if __name__ == "__main__":
    execute()
