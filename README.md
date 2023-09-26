# Park
This is a parking stress test

```
Park
├─ .pytest_cache
│  ├─ CACHEDIR.TAG
│  ├─ README.md
│  └─ v
│     └─ cache
│        └─ stepwise
├─ .vscode
│  └─ settings.json
├─ poetry.lock
├─ pyproject.toml
├─ README.md
├─ resources
│  ├─ layout.csv
│  └─ temp.csv
├─ src
│  ├─ Car.py
│  ├─ main.py
│  ├─ Map.py
│  ├─ test.py
│  ├─ __init__.py
│  └─ __pycache__
│     ├─ Car.cpython-311.pyc
│     └─ Map.cpython-311.pyc
└─ tests
```

## 项目前置条件
- `Python` >= 3.8
- `Poetry` >= 1.6

## 项目依赖
### 依赖管理
本仓库采用 [Poetry](https://python-poetry.org/) 进行依赖管理，Poetry 的安装方法可参考 [官方文档](https://python-poetry.org/docs/#installation)。

克隆本仓库后，需要使用以下命令安装依赖：
```shell
poetry install
```

通过以下命令可导出 `requirements.txt` 文件，但不推荐使用该文件进行依赖管理，且不保证该文件的实时性：
```shell
poetry export -f requirements.txt --output requirements.txt
```

#### PyCharm 集成
有关 Poetry 与 PyCharm 的集成可参考 [JetBrains 官方文档](https://www.jetbrains.com/help/pycharm/poetry.html)。

#### VSCode 集成
在本项目目录下完成 `poetry install` 后，VSCode 应当自动识别并加载 Poetry 虚拟环境。

当打开 `.py` 文件时，右下角解释器应当显示类似如下图所示的信息：
![Alt text](img/image.png)

如 VSCode 没有自动识别，可尝试点击该位置并选中 Poetry 虚拟环境。

如未出现 Poetry 虚拟环境的提示，应当尝试在终端中执行 `poetry shell` 激活虚拟环境，再输入 `code .` 启动 VSCode。

## 代码规范
项目的 Python 代码应当在可能的情况下遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范。

推荐使用 Flake8 进行代码检查，但以下规则应当被抑制：
- `E501` 代码单行长度限制
- `W503` 二元运算符前换行

## 单元测试说明
暂时未完成
