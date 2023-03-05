# モジュールスコープの確認
# 組み込み関数のtmp_path
# skip, skipifマーカーの使い方
# 実行方法: pytest src/test/test_write_file.py -sv
# ※ sオプションで標準出力をターミナルに出力する
import os
import shutil
from pathlib import Path

import pytest

from app.write_file import write_file

# モジュールscopeの確認
# モジュール単位で実行するfixture(ここではtest_write_file.pyで1回実行される)


@pytest.fixture(scope="module")
def make_test_dir() -> Path:
    # src/test(absolute directory)
    print("\n!!!! make_test_dirフィクスチャを実行 !!!!\n")
    test_output_dir = Path(__file__).parent.resolve() / Path("output")
    os.makedirs(test_output_dir)

    # teardown
    yield test_output_dir
    shutil.rmtree(test_output_dir)


def test_write_file1(make_test_dir):
    string = "test1 string."
    filepath = make_test_dir / Path("test_file1.txt")
    write_file(filepath, string)

    # 簡易的にするためファイルの存在チェックのみで、ファイルの中身はチェックしない
    assert filepath.exists()


# 引数にmake_test_dirが渡されるが、scopeがmoduleなので実行されない
def test_write_file2(make_test_dir):
    string = "test2 string."
    filepath = make_test_dir / Path("test_file2.txt")
    write_file(filepath, string)

    # 簡易的にするためファイルの存在チェックのみで、ファイルの中身はチェックしない
    assert filepath.exists()


# 組み込み関数のtmp_pathの使い方
# 組み込みfixtureのtmp_pathを使う
def test_write_file3(tmp_path: Path):
    string = "test3 string."
    filepath = tmp_path / Path("test_file3.txt")
    write_file(filepath, string)


# skipmマーカーの動作チェック
# テストを明示的にスキップさせる
@pytest.mark.skip(reason="ここにスキップする理由を記載する")
def test_skip():
    assert 1 / 0 == 0


# 条件付きスキップ
@pytest.mark.skipif(
    os.getenv("ENV_VARIABLE") is None, reason="環境変数: ENV_VARIABLEが存在しない場合はスキップ"
)
def test_skipif():
    assert os.environ["ENV_VARIABLE"] == "some_value"
