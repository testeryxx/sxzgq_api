import allure
import pytest

from common.excel_driver import ExcelDriver

from config import *
from key_words.key_words import KeyWords


class TestCheck:
    all_data = ExcelDriver.read_excel()
    keywords = KeyWords()

    # 私有方法，生成allure测试标题
    def __dynamic_title(self, all_data):
        # 动态生成标题
        # allure.dynamic.title(data[11])
        # 如果存在自定义标题
        if all_data["caseName"] is not None:
            # 动态生成标题
            # allure.dynamic.title(all_data["caseName"])
            allure.dynamic.parameter('case_data', '[]')
            casename = 'ID:({})-{}'.format(all_data["id"], all_data["caseName"])
            allure.dynamic.title(casename)

        if all_data["storyName"] is not None:
            # 动态获取story模块名
            allure.dynamic.story(all_data["storyName"])

        if all_data["featureName"] is not None:
            # 动态获取feature模块名
            allure.dynamic.feature(all_data["featureName"])

        if all_data["remark"] is not None:
            # 动态获取备注信息
            allure.dynamic.description(all_data["remark"])

        if all_data["rank"] is not None:
            # 动态获取级别信息(blocker 阻断、critical 关键、normal 正常、minor 次要、trivial 琐碎)
            allure.dynamic.severity(all_data["rank"])

    # 重运行机制
    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @pytest.mark.parametrize("case_data", all_data)
    def test_project_check(self, case_data):
        self.__dynamic_title(case_data)
        try:
            url = case_data['url'] + case_data['path']
            params = eval(case_data['params']) if isinstance(case_data['params'], str) else None
            data = case_data['data'] if isinstance(case_data['data'], str) else None
            method = case_data['method']
            if method == 'get':
                headers = X_TOKEN_GET
            elif method == 'post':
                headers = X_TOKEN_POST
            dict_data = {
                "url": url,
                "headers": headers,
                "params": params,
                "data": data
            }

        except Exception:
            print(GET_EXCEL_DATA_ERROR)
        else:

            res = getattr(self.keywords, method)(**dict_data)

        try:
            msg = self.keywords.extract_res(res.text, case_data['actualResult'])
        except Exception:
            print(GET_MSG_ERROR)
        else:
            if case_data['expectResult'] == msg:
                value = ASSERT_SUCCESS
            else:
                value = ASSERT_FALSE
            ExcelDriver.write_excel(row=case_data['id'], value=value)
        finally:
            assert case_data['expectResult'] == msg
            # ExcelDriver.write_excel(row=case_data['id'], value=value)


