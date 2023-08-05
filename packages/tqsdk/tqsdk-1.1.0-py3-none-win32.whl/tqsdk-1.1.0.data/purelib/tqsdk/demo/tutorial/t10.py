#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'chengzhi'

from tqsdk import TqApi

# 创建API实例.
api = TqApi()
# 获得上期所 cu1911 的行情引用，当行情有变化时 quote 中的字段会对应更新
quote = api.get_quote("SHFE.cu1911")

# 输出 cu1911 的最新行情时间和最新价
print(quote.datetime, quote.last_price)

# 关闭api,释放资源
api.close()
