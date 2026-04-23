# FOF Data Gateway

`fof-data-gateway` 是 FOF 财富管理平台的数据网关与轻量服务层，负责对外提供更聚焦的数据访问能力，用于承接基金、FOF、组合、市场、管理人等查询类接口，以及短信、视频能力和部分集成场景。它和主业务后台配合使用，适合作为数据聚合层或 BFF 风格服务。

## 核心能力

- FOF、基金、组合、市场、管理人等数据访问接口
- 认证与鉴权密钥管理
- 短信能力与视频能力接口封装
- 面向外部应用或轻前端场景的接口输出
- 通过统一配置与 `surfing` 依赖接入共享数据与配置体系

## 技术栈

- Web 框架：`Flask 1.1`
- ORM / 迁移：`SQLAlchemy`、`Flask-Migrate`
- 缓存：`Redis`、`Flask-Caching`
- 搜索：`Elasticsearch`
- 部署：`Gunicorn`、`gevent`、`Docker`
- 依赖扩展：`surfing`、`PyJWT`、`tencentcloud-sdk-python`

## 代码结构

```text
fof-data-gateway/
├── apps/                 # 业务蓝图，如 auth、fof、fund、markets、portfolio
├── bases/                # 配置、数据库、缓存与通用基类
├── configs/              # 配置加载与模板
├── extensions/           # 第三方封装，如短信、视频、ES、CAS
├── migrations/           # 数据库迁移脚本
├── models/               # 数据模型
├── routers/              # 蓝图注册入口
├── utils/                # 通用工具
├── manager.py            # 启动与命令入口
└── Dockerfile            # 容器化启动定义
```

## 主要接口域

当前注册的主要蓝图包括：

- `auth`
- `index`
- `fof`
- `fund`
- `sms`
- `basic`
- `tx_video`
- `haifeng`
- `markets`
- `portfolio`
- `management`

## 快速开始

### 1. 准备环境

建议环境：

- `Python 3.7.x`
- `MySQL`
- `Redis`
- 可用的 `surfing` 配置文件

### 2. 安装依赖

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install surfing --upgrade --no-cache-dir
```

### 3. 准备配置

项目默认从固定路径加载配置：

```python
/shared/fof/etc/config.py
```

可以先用模板初始化：

```bash
mkdir -p /shared/fof/etc
cp configs/config.py.template /shared/fof/etc/config.py
```

建议至少确认这些配置：

- `DB_URI`
- `SECRET_KEY`
- `LOG_PATH`
- `TEMP_PATH`
- `SURFING_CONFIG`

## 本地运行

开发环境：

```bash
python manager.py runserver -h 0.0.0.0 -p 8006
```

生产环境：

```bash
gunicorn -w 2 -k gevent --timeout 60 -b 0.0.0.0:8006 manager:app
```

## 常用命令

### 数据库迁移

```bash
python manager.py db init
python manager.py db migrate -m "init"
python manager.py db upgrade
python manager.py db history
```

### 创建接入密钥

```bash
python manager.py init_sec --app_id your_app_id --app_sec your_app_secret
```

这个命令会创建一个 `AuthSecret` 记录，用于网关调用方接入。

## Docker 运行

```bash
docker build -t fof-data-gateway .
docker run --rm -p 8006:8006 \
  -v /shared/fof/etc/config.py:/shared/fof/etc/config.py \
  fof-data-gateway
```

## 使用建议

- 这个仓库更适合承担数据读取、聚合和轻业务接口，不建议把重运营逻辑继续堆进网关层。
- 若与主后台一起部署，建议统一配置、日志目录和 `surfing` 依赖版本。
- 发布到外部环境前，请检查配置文件与日志路径是否适配目标服务器。

## README 说明

这份 README 结合了当前的蓝图注册、启动命令、配置加载方式和 Docker 启动参数，适合作为 GitHub 首页说明和接手文档。
