# -*- coding: utf-8 -*-
"""
top上传图片到淘宝图片空间
"""
import top.api

#这三个变量换成对应的数据
appkey = ""
secret = ""
sessionkey="你的sessionkey"


req=top.api.PictureUploadRequest()
req.set_app_info(top.appinfo(appkey,secret))

#你图片的分类id
req.picture_category_id=11111111111111111
req.img=top.api.FileItem('abc.jpg',open(r'd:/11.jpg', 'rb'))
req.image_input_title="s9127643.jpg"
req.title="图片名称2"
try:
    resp= req.getResponse(sessionkey)
    print(resp)
except Exception,e:
    print(e)

