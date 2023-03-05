import os
import platform


class TargetObj:
    def __init__(self, param) -> None:
        self.param = param

    def method1(self) -> str:
        return f"{self.param}, {platform.system()}"

    def method2(self) -> str:
        return os.getenv("TEST_ENV")
