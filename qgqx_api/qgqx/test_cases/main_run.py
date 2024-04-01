import pytest, os

if __name__ == '__main__':
    pytest.main(["-s", "--alluredir", "./result", "--clean-alluredir"])
    os.system("allure generate ./result -o ./report_allure --clean")
