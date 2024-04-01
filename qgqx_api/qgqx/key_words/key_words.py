import json
import allure
import jsonpath
import requests



class KeyWords:
    # get请求
    @allure.step('------发送get请求------')
    def get(self, url, params=None, **kwargs):
        return requests.get(url, params=params, **kwargs)

    # post请求
    @allure.step('------发送post请求------')
    def post(self, url, data=None, json=None, **kwargs):
        return requests.post(url, data=data, json=json, **kwargs)

    # 提取响应数据
    @allure.step('------提取响应数据------')
    def extract_res(self, response, expression):
        # 如果响应是字符串，转换成json
        if isinstance(response, str):
            response = json.loads(response)
        valuelist = jsonpath.jsonpath(response, expression)
        return valuelist[0]

    def teee(self):
        return "zhes getattr"

if __name__ == '__main__':
    data = KeyWords()
    # path = data.extract_res(res, '$..message')
    # print(path)
    # print(getattr(data, "post")())