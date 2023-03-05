# スコープの確認と共通fixtureの呼び出し確認
import os

import pytest

from app.foo_bar import bar, foo


# scopeごとのfixture実行順序の確認(--setup-show)
#  pytest --setup-show src/test/test_foo_bar.py
@pytest.fixture(scope="function")
def function_scope():
    print("function scope(default)")


@pytest.fixture(scope="class")
def class_scope():
    print("class scope")


@pytest.fixture(scope="module")
def module_scope():
    print("module scope")


@pytest.fixture(scope="package")
def package_scope():
    print("package scope")


@pytest.fixture(scope="session")
def session_scope():
    print("session scope")


# fixtureの実行順序は, pytest --setup-show <テスト対象ディレクトリ、ファイル、関数...等> で確認できる
# function < class < module < package < session の順にスコープが大きくなる
class TestCalc:
    def test_foo(
        self, function_scope, class_scope, module_scope, package_scope, session_scope
    ):
        print(foo())

    def test_bar(
        self, function_scope, class_scope, module_scope, package_scope, session_scope
    ):
        print(bar(1, 2))

    # conftest.pyに記載のfixtureを使う
    def test_common_fixture(self, common_fixture):
        pass


# パラメータ
# 関数のパラメータ化と、fixtureのパラメータの組み合わせ
# fixtureのパラメータの数に対して、関数のパラメータ(@pytest.mark.parametrizeで定義したもの)分
# 実行される
# このテスト関数だと、以下のように4パターン実行される
# state_1: (1, 2, 3)
# state_1: (3, 4, 7)
# state_2: (1, 2, 3)
# state_2: (3, 4, 7)
#
# pytest src/test/test_foo_bar.py::test_add -v
@pytest.fixture(params=["state_1", "state_2"])
def generate_params(request):
    os.environ["state"] = request.param


# パラメータを定義
@pytest.mark.parametrize(("param1", "param2", "expected_value"), [(1, 2, 3), (3, 4, 7)])
def test_add(param1, param2, expected_value, generate_params):  # generate_paramsを引数に取る
    result = bar(param1, param2)
    assert result == expected_value
