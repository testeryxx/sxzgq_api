import logging
import pytest
from key_words.key_words import KeyWords


# 整个过程都有效，则用session,获取token
@pytest.fixture(scope="session")
def token_fix():
    apikey = KeyWords()
    url = 'http://192.168.1.149:5500/api/v1/verify_code/captcha'
    params = None
    data = None
    res = apikey.post(url=url, params=params, data=data)
    res_json = res.json()
    token = apikey.extract_res(res_json, "$..token")
    return token


# 夹具打印日志，使用钩子函数
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    out = yield
    res = out.get_result()
    if res.when == "call":
        logging.info(f"用例ID：{res.nodeid}")
        logging.info(f"测试结果：{res.outcome}")
        logging.info(f"故障表示：{res.longrepr}")
        logging.info(f"异常：{call.excinfo}")
        logging.info(f"耗时：{res.duration}")
        logging.info("******************************")
