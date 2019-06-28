#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from urlparse import urlparse
from com.aliyun.api.gateway.sdk import client
from com.aliyun.api.gateway.sdk.http import request
from com.aliyun.api.gateway.sdk.common import constant
from pai_tf_predict_proto import tf_predict_pb2


def predict(url, app_key, app_secret, request_data):
    cli = client.DefaultClient(app_key=app_key, app_secret=app_secret)
    body = request_data
    url_ele = urlparse(url)
    host = 'http://' + url_ele.hostname
    path = url_ele.path
    req_post = request.Request(host=host, protocol=constant.HTTP, url=path, method="POST", time_out=6000)
    req_post.set_body(body)
    req_post.set_content_type(constant.CONTENT_TYPE_STREAM)
    stat,header, content = cli.execute(req_post)
    return stat, dict(header) if header is not None else {}, content


def demo():
    # 以下三行的信息均可在EAS管控台的服务列表，点击服务名称查看
    app_key = ''
    app_secret = ''
    url = ''

    request = tf_predict_pb2.PredictRequest()
    # request.signature_name = 'predict'
    request.inputs['input_1'].dtype = tf_predict_pb2.DT_FLOAT  
    request.inputs['input_1'].array_shape.dim.extend([1,224,224,3]) 
    request.inputs['input_1'].float_val.extend([0] * 224*224*3)    


    # 将pb序列化成string进行传输
    request_data = request.SerializeToString()

    stat, header, content = predict(url, app_key, app_secret, request_data)
    if stat != 200:
        print 'Http status code: ', stat
        print 'Error msg in header: ', header['x-ca-error-message'] if 'x-ca-error-message' in header else ''
        print 'Error msg in body: ', content
    else:
        response = tf_predict_pb2.PredictResponse()
        response.ParseFromString(content)
        print(response)


if __name__ == '__main__':
    demo()
