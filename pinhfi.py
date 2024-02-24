# -*- coding: utf-8 -*-
import sys

from py12306.app import *
from py12306.helpers.cdn import Cdn
from py12306.log.common_log import CommonLog
from py12306.query.query import Query
from py12306.user.user import User
from py12306.web.web import Web


def main():
    load_argvs()
    CommonLog.print_welcome()
    App.run()
    CommonLog.print_configs()
    App.did_start()

    App.run_check()
    Query.check_before_run()

    ####### 运行任务
    Web.run()
    Cdn.run()
    User.run()
    Query.run()
    if not Const.IS_TEST:
        while True:
            sleep(10000)
    else:
        if Config().is_cluster_enabled(): stay_second(5)  # 等待接受完通知
    CommonLog.print_test_complete()
