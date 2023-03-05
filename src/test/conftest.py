# 共通で使いたいfixtureを定義する.
# テスト関数と同じ階層か、親のディレクトリに配置する.
import pytest


@pytest.fixture
def common_fixture():
    print("\n共通fixtureを実行.\n")
