#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python-bot series #1
このプログラムは引数にユーザーIDとメッセージを与えると
メッセージを送信し終了するプログラムです.

コマンドを1行書くだけでメッセージを送れるのでcron等と
連携させると便利かもしれないです.

使用例:
python bot1.py info1@kumaume2.ddo.jp "Hello world."
"""

from __future__ import print_function, unicode_literals
from datetime import date
import json
import logging
import os
import sys
import traceback
import warnings

# Deprecation Warning を抑制
warnings.filterwarnings("ignore", category=DeprecationWarning)

import xmpp


class Bot(object):
    def __init__(self, config_path):
        try:
            with open(config_path, 'rU') as conf:
                self.config = json.load(conf)
        except:
            raise Exception("Conld not read configuration: %s" % config_path)

    def send(self, to, message):
        """メッセージを送信する処理"""
        # ドメイン名が付加されていない場合は, ドメイン名を付加する
        if to.find("@") < 0:
            to = "{0}@{1}".format(to, self.config['domain'])

        try:
            # メッセージを作成して送信
            client = xmpp.Client(self.config['domain'], debug=[])
            client.connect(server=(self.config['server'], self.config['port']))
            client.auth(self.config['user'], self.config['pass'],
                        self.config['resource'])
            client.send(xmpp.Message(to, message))
            logging.info("Sent: To=<{0}> Message='{1}'".format(to, message))
        except:
            trace = str(traceback.format_exc(sys.exc_info()[2])).replace(
                '\n', ' ')
            logging.error("Error: To={0} Message={1} Trace={2}".format(
                to, message, trace))
        finally:
            client.disconnect()


if __name__ == "__main__":
    # 引数をチェックし, 不足していれば終了
    if len(sys.argv) <= 2:
        print("Usage: {0} <To> <Message>".format(sys.argv[0]), file=sys.stderr)
        sys.exit(0)

    dir_path = os.path.dirname(os.path.abspath(__file__)) + '/'
    logfile_path = dir_path + 'log_%s.log' % date.today().strftime("%Y%m")
    config_path = dir_path + 'xmpp.json'

    logging.basicConfig(filename=logfile_path, level=logging.DEBUG)

    bot = Bot(config_path)
    bot.send(sys.argv[1], sys.argv[2])
