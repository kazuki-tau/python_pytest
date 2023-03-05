# monkeypatchの動作
# - アトリビュートの変更
# - コンテキストマネージャ(monkeypatch.context)を使う方法
# - 環境変数の変更
# pytest-mockの動作
import platform

from app.baz import TargetObj


# monkeypatchの使い方の例
class TestTargetOjb:
    # アトリビュートの変更
    def test_method1(self, monkeypatch):
        # platform.systemの差し替え用に作成
        def mock_platform_system():
            return "Test OS"

        # builtinのplatform.sysetmを自作したmock_platform_systemに差し替え
        # ※ コンテキストマネージャを使わない方法だと、
        #   この関数内の後続のplatform.systemの動作に影響するので注意
        monkeypatch.setattr(platform, "system", mock_platform_system)

        target_obj = TargetObj(param="test_parm")
        # Test OSが出力される
        print(platform.system())

        assert target_obj.method1() == "test_parm, Test OS"

    # mockの影響範囲を限定させたい場合(monkeypatch.context)
    # pytest src/test/test_baz.py::TestTargetOjb::test_method3 -sv
    def test_method1_2(self, monkeypatch):
        # platform.systemの差し替え用に作成
        def mock_platform_system():
            return "Test OS"

        # with構文を使って、範囲を限定する
        # builtinのplatform.sysetmを自作したmock_platform_systemに差し替え
        with monkeypatch.context() as mock:
            mock.setattr(platform, "system", mock_platform_system)
            target_obj = TargetObj(param="test_parm")
            result = target_obj.method1()

            # context内では文字列"Test OS"を返す(mock_platform_systemの返り値)
            print(platform.system())

        # contextを出ると、本来のplatform.system()の返り値になる
        print(platform.system())

        assert result == "test_parm, Test OS"

    # 環境変数の変更
    def test_method3(self, monkeypatch):
        # 環境変数を操作する
        monkeypatch.setenv("TEST_ENV", "BBB")
        target_obj = TargetObj(param="test_parm")

        assert target_obj.method2() == "BBB"
