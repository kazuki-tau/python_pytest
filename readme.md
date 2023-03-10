# pytestの基本的な使い方
## 内容
1. fixtureのついて
2. パラメータの与え方について
3. pytestの組み込みマーカーについて
4. mockについて  
・monkeypatchの使い方  

#### ※ これらのの実装の例をsrc配下に置いている
```
テスト対象: python_pytest/src/app  
テスト:    python_pytest/src/test  
```

## 0. 簡単におさらい
- pytestの要件:  
pytest requires: Python 3.7+ or PyPy3.(https://docs.pytest.org/en/7.1.x/getting-started.html#install-pytest)  

- pytestのテスト関数の命名方法
・ファイル名
test_〇〇.py
もしくは、
〇〇_test.py

・関数名
test_func.py
もしくは、
func_test.py

・クラス名
Test〇〇

- インストール方法
```shell
$ pip install pytest

```

- 使い方  

```python
# test_add.py
import pytest

def add(a: int, b: int) -> int:
    return a + b

def test_add(a, b):
    assert add(a, b) == a + b
```

- 実行方法
```shell
$ pytest test_add.py
```

## 1. fixture
### fixture(フィクスチャ)とは  
 → テスト関数の実行に先立って(場合によっては後に)、pytestが実行する関数


### どういう時に使うか
- テストデータの準備
- テストを実行する前にシステムの状態を特定の状態にする  
...等テストを行う前の事前準備(場合によっては後処理)

### fixtureの使い方
pytestでは関数の前に@pytest.fixtureのデコレータをつける


```python
import pytest

#### fixtureの定義方法 ####
# setupでDBに接続し、yieldでコネクションを返す。
# teardownでDBのコネクションを閉じる。
@pytest.fixture()
def connect_db():
    # setup(前処理)
    # connect database
    db = ...
    db.connect()

    yield db # yieldで返した値をテスト関数の中で使うことができる
    # teardown
    # yield以降がteardown(後処理になる)
    # close db session
    db.close()

# setupでテストディレクトリを作成する。
# teardownで作成したテストディレクトリを削除する
@pytest.fixture()
def make_test_directory():
    # setup
    os.makedir("test_directory")
    yield
    # teardown
    os.remove("test_directory")

# 単に値を返すfixture
@pytest.fixture()
def calculate_some_value():
    return "some value" # return した値をテスト関数の中で使うことができる。単にreturnとした場合は、teardown(後処理)は行われない



# テスト対象の関数
def some_func(db, some_value):
    ...

# テスト関数
#### fixtureをテスト関数のなかで使う方法 ####
# fixtureを使う場合は、テスト関数の引数に渡す
def test_calculation(connect_db, make_test_directory, calculate_some_value):
    some_func(connect_db, calculate_some_value)

```

(補足)  
setup:    テスト関数の実行前に行う処理(前処理)  
teardown: テスト関数の実行後に行う処理(後処理)  

### fixture scope
setupとteardownの実行単位

- function  
テスト関数ごとに1回実行される。(デフォルトはfunction)

```python

@pytest.fixture(scope="function")
def function_scope():
    # setup
    ...
    yield
    # teardown


def test_scope(function_scope):
    # この関数内の実行前にsetup, この関数実行後にteardownがそれぞれ1回実行される
    pass

```

- class　　
テストクラスごとに1回実行される
```python

@pytest.fixture(scope="class")
def class_scope():
    # setup
    ...
    yield
    # teardown

# TestScopeクラス全体で1回fixtureが実行される
# 同一クラス無いで複数回、同じfixtureが使われたとしても、実行されるのは一度のみ
class TestScope:
    def test_scope1(class_scope): # setupが実行される。
        pass

    def test_scope2(class_scope):
        pass

    def test_scope3(class_scope):
        pass

```

- module
モジュールごとに1回実行される
```python

@pytest.fixture(scope="module")
def module_scope():
    # setup
    ...
    yield
    # teardown

```

- package
パッケージごとに一回実行される

```
src
├── app
│   ├── package1
│   └── package2
└── test
    ├── package1        # パッケージ単位で1回実行(このディレクトリのテストで1回実行)
    │   ├── __init__.py
    │   ├── test_aaa.py
    │   └── test_bbb.py
    └── package2        # パッケージ単位で1回実行(このディレクトリのテストで1回実行)
        ├── __init__.py
        ├── test_ccc.py
        └── test_ddd.py
```


```python

@pytest.fixture(scope="package")
def package_scope():
    # setup
    ...
    yield
    # teardown

```

- session  
pytestコマンドでの実行単位で一回実行される


```python

@pytest.fixture(scope="session")
def session_scope():
    # setup
    ...
    yield
    # teardown

```

### fixtureの実行順序の確認方法

```shell
$ pytest --setup-show <テスト対象のディレクトリ、ファイル、関数...等>

```

### fixtureが定義されている場所を突き止める


```shell
$ pytest --fixtures -v


```

### fixtureの共有方法
conftest.pyをテストファイルと同じディレクトリか、親ディレクトリに配置する
(※ pytestによって自動的にimportされるので、明示的にimportする必要がない)




## 組み込みfixture
pytest側であらかじめ用意されているfixtureのこと
テスト関数や、fixture関数の引数で与えることによって使える
pytest --fixturesで組み込みfixture一覧を書くにできる

### tmp_path, tmp_path_factory　　
一時ディレクトリを作成する機能

### capsys
標準出力(stdout), 標準エラー(stderr)をキャプチャする

### caplog
pythonのloggingで出力された内容をキャプチャする

### monkeypatch
環境、またはアプリケーションのコードの変更に使うfixture(モック)

### request
実行中のテスト関数に関する情報を提供するfixture(fixtureのパラメータ化でよく使う)

## 2. パラメータ化
### 関数のパラメータ化
@pytest.mark.parametrize()

```python
# テスト対象の関数
def add(a: int, b: int) -> int:
    return a + b

# パラメータを定義
@pytest.mark.parametrize(
    ("param1", "param2", "expected_value"),
    [
        (1, 2, 3),
        (3, 4, 7)
    ]
)
def test_add(param1, param2, expected_value): # テスト関数の引数に渡すと、パラメータを使える
    result = add(param1, param2)
    assert result == expected_value


```

### fixtureのパラメータ化
```python

@pytest.fixture(params=[(1,2,3), (3,4,7)])
def generate_params(request): # 組み込み関数のrequestを使う
    return request.param

def test_add(generate_params): # generate_paramsに1回目: (1,2,3)、2回目: (3,4,7)が入ってくる
    result = add(generate_params[0], generate_params[1])
    assert result == expected_value[2]

```

### 関数のパラメータとfixtureのパラメータの組み合わせ

```python
# テスト対象の関数
def add(a: int, b: int) -> int:
    return a + b


@pytest.fixture(params=["state_1", "state_2"])
def generate_params(request): # 組み込み関数のrequestを使う
    os.environ["state"] = request.param

# パラメータを定義
@pytest.mark.parametrize(
    ("param1", "param2", "expected_value"),
    [
        (1, 2, 3),
        (3, 4, 7)
    ]
)
def test_add(param1, param2, expected_value, generate_params):
    result = add(param1, param2)
    assert result == expected_value

# fixtureのパラメータ数 × 関数のパラメータ数　の回数だけ実行される
# この場合、 2 × 2で合計4回テスト関数が実行される
```

## 3.pytestの組み込みマーカーについて

- @pytest.mark.skip(reason=None)  
意図的にスキップしたいテストがある場合に使用する(reasonに理由を記載できる)

- @pytest.mark.skipif(condition, *, reason=None)
  いずれかの条件がTrueの場合、テストをskipする

- @pytest.mark.xfail(condition, *, reason=None, raises=None, run=True, strict=False)  
  テストが失敗すると想定されていることをpytestnに伝える

- @pytest.mark.parametrize
  関数のパラメータ化に使用する

...等他にも存在する

※ 組み込みマーカー以外にも、カスタムマーカー(自作できる)があるがここでは割愛

## 4. mockについて
### 組み込みfixtureのmonkeypatchの使い方について  
・monkeypatchの主なメソッド  
- setattr(target, name, value, raising=True)  
属性を設定する  

- delattr(target, name, raising=True)
属性を削除する  

- setitem(dic, name, value)  
辞書のエントリを設定する  

- delitem(dic, name, raising=True)  
辞書のエントリを削除する  

- setenv(name, value, prepend=True)  
環境変数を設定する  

- delenv(name, raising=True)  
環境変数を削除する  

- syspath_preprend(path)  
sys.pathの先頭にpathを追加する

- chdir(path)  
作業ディレクトリを変更する  

### 使い方の例
```python
# テスト対象のクラス
import os
import platform


class TargetObj:
    def __init__(self, param) -> None:
        self.param = param

    def method1(self) -> str:
        return f"{self.param}, {platform.system()}"

    def method2(self) -> str:
        return os.getenv("TEST_ENV")

```

```python
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
```