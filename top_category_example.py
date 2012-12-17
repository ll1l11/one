# -*- coding: utf-8 -*-
"""
获取淘宝图片空间分类信息的简单例子

appkey secret是申请top应用提供的
sessionkey可以根据http://container.open.taobao.com/container?appkey={你的appkey}获取
"""
import top.api

#换成自己对应的数据
appkey = ""
secret = ""
sessionkey=""

req=top.api.PictureCategoryGetRequest()
req.set_app_info(top.appinfo(appkey,secret))

try:
    resp= req.getResponse(sessionkey)
    for key in resp["picture_category_get_response"]["picture_categories"]["picture_category"]:
        print key
except Exception,e:
    print(e)
