# 本项目纯AI打造，欢迎加入本人知识星球，可学习交流，可获得本项目支持

![描述](./pic/star.jpg)

# Super MetaData 元数据管理系统

> 纯AI打造的一站式元数据管理平台，轻松掌控您的数据资产

## 📋 项目简介

Super MetaData Super MetaData 元数据管理系统是一个功能强大的企业级元数据管理平台，支持多种主流数据库的元数据抽取、管理和展示。系统采用现代化的Web界面，提供直观的用户体验，帮助企业更好地理解和治理数据资产。

![描述](./pic/index.jpg)


## ✨ 核心特性

### 🎯 全面的数据库支持

- **MySQL**：完整支持表、字段、外键关系抽取
- **PostgreSQL**：支持表、字段、外键关系抽取
- **SQL Server**：完整支持表、字段、外键关系抽取（包含长度、精度信息）
- **Oracle**：完整支持表、字段、外键关系抽取（包含长度、精度信息）
- **StarRocks**/Doris：基于 MySQL 协议的 MPP 数据库支持

### 数据源管理

- 支持多种数据库类型：
  - MySQL
  - PostgreSQL
  - SQL Server
  - Oracle
  - StarRocks

- 集中管理数据源连接

- 实时测试连接状态

- 安全的密码存储

![描述](./pic/source.jpg)
![描述](./pic/resource.jpg)

### ✏️ 注释编辑功能

- **表注释编辑**：在线编辑和保存表注释
- **字段注释编辑**：
  - 在元数据浏览页面的表详情模态框中批量编辑
  - 在表详情页面单独编辑每个字段
  - 支持权限控制（管理员和普通用户可编辑）
- **实时保存**：修改后立即保存，无需额外操作
- **自动刷新**：保存后自动更新列表显示

### 元数据抽取

- **全量抽取**：抽取数据源中的所有表元数据

- **增量抽取**：只抽取新增或变更的表元数据，提升效率

- **仅结构抽取**：快速获取表结构信息，无需统计数据

- 自动获取表结构、字段信息、统计数据

- 支持表间关联关系（外键）抽取
  ![描述](./pic/etl_his.jpg)


### 元数据浏览

- 直观的表格展示

- 表详情查看：字段名、类型、长度、注释等完整信息

- **表注释手动编辑**：支持在线编辑和保存表注释

- **字段注释手动编辑**：

  - 在表详情模态框中编辑字段注释
  - 在表详情页面批量编辑字段注释
  - 支持权限控制（仅管理员和普通用户可编辑）

- 支持按数据源筛选

- 实时搜索和过滤

- 表统计信息（行数、数据大小）

- 表关联关系展示（外键关系）

  ![描述](./pic/metadta.jpg)
  ![描述](./pic/table_detail.jpg)

### ETL任务管理

- 可视化任务创建和配置

- 灵活的调度方式：

  - 时间间隔调度（分钟、小时、天、周）
  - CRON表达式调度
  - 手动执行

- 任务类型：全量抽取、增量抽取、仅结构抽取

- 任务状态管理和执行历史追踪

  ![描述](./pic/etl.jpg)

### 用户权限管理

- 多角色支持：

  - **管理员**：完整的系统管理权限
  - **普通用户**：数据查看和管理权限
  - **只读用户**：仅查看权限

- 个人信息管理

- 密码修改功能

- 操作权限控制

  ![描述](./pic/user.jpg)

### 数据统计分析

- 资源概览仪表板
- 数据源、表、字段数量统计
- 数据量统计和可视化
- 抽取历史记录

## 🏗️ 系统架构

```
Super MetaData Super MetaData 元数据管理系统
│
├── 前端层
│   ├── HTML5 + Bootstrap 5
│   ├── JavaScript (ES6+)
│   └── Font Awesome 图标库
│
├── 后端层
│   └── Flask Web 框架
│       ├── RESTful API
│       ├── 用户认证与授权
│       └── 业务逻辑处理
│
├── 数据访问层
│   ├── SQLAlchemy ORM
│   └── 元数据库
│
 └── 元数据抽取层
     ├── 抽取器基类 (MetadataExtractorBase)
     ├── MySQL 抽取器
     ├── PostgreSQL 抽取器
     ├── SQL Server 抽取器
     ├── Oracle 抽取器
     └── StarRocks 抽取器
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip 包管理器
- SQLite（默认）或其他支持的数据库

### 数据库驱动依赖

不同数据库需要安装对应的 Python 驱动：

```bash
# MySQL
pip install pymysql

# PostgreSQL
pip install psycopg2-binary

# SQL Server
pip install pyodbc

# Oracle
pip install oracledb

# StarRocks
pip install pymysql
```

### 安装步骤

1. **克隆仓库**

```bash
git clone https://github.com/yourusername/metadata-manager.git
cd metadata-manager
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

3. **初始化数据库**

```bash
python app.py
```

系统首次启动时会自动创建所需的数据库表。

4. **访问系统**

```
http://localhost:5000
```

5. **登录系统**

```
默认管理员账号：
用户名：admin
密码：admin123
```

⚠️ **安全提醒**：首次登录后请立即修改默认密码！

## 📦 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖：

- Flask 2.3.3 - Web 框架
- SQLAlchemy 2.0.21 - ORM 框架
- PyMySQL 1.1.0 - MySQL 驱动
- psycopg2-binary 2.9.9 - PostgreSQL 驱动
- python-dotenv 1.0.0 - 环境变量管理
- Werkzeug 2.3.7 - WSGI 工具箱
- oracledb - Oracle 驱动（可选，使用瘦模式无需 Instant Client）
- pyodbc - SQL Server 驱动（可选）

## 📖 使用指南

### 1. 添加数据源

1. 登录系统后，点击"数据源管理"
2. 点击"添加数据源"按钮
3. 填写数据源信息：
   - 数据源名称
   - 数据库类型
   - 主机地址
   - 端口号
   - 用户名
   - 密码
   - 数据库名
4. 点击"测试连接"验证配置
5. 点击"保存"完成添加

### 2. 创建ETL任务

1. 点击"ETL任务"菜单
2. 点击"添加任务"按钮
3. 配置任务信息：
   - 任务名称
   - 任务类型（全量抽取、增量抽取、仅结构抽取）
   - 选择数据源
   - 调度规则（时间间隔、CRON表达式、手动执行）
   - 任务描述
4. 保存任务

### 3. 执行元数据抽取

- **手动执行**：在任务列表中点击"执行"按钮
- **定时执行**：配置调度规则后，系统会自动执行
- **查看结果**：在"抽取历史"中查看执行结果

### 4. 浏览元数据

1. 点击"元数据浏览"菜单
2. 选择要查看的数据源
3. 查看表列表和统计信息
4. 点击"查看"按钮查看表的详细信息（字段、类型、长度、注释等）

### 5. 编辑表和字段注释

**编辑表注释**：

1. 在表详情模态框中，找到"注释"字段
2. 修改注释内容
3. 点击"保存"按钮

**编辑字段注释**（两种方式）：

- **方式一**：在元数据浏览页面的表详情模态框中
  1. 点击"字段信息"卡片右上角的"编辑"按钮
  2. 直接在字段注释列的输入框中编辑
  3. 点击"保存"按钮保存所有修改
  4. 点击"取消"按钮放弃修改

- **方式二**：在表详情页面（点击表名进入）
  1. 点击"编辑注释"按钮进入编辑模式
  2. 直接在字段注释列的输入框中编辑
  3. 点击"保存注释"按钮保存
  4. 点击"取消"按钮退出编辑模式

⚠️ **注意**：只有管理员和普通用户可以编辑注释，只读用户只能查看。

### 6. 用户管理（仅管理员）

1. 点击"用户管理"菜单
2. 查看所有用户列表
3. 添加新用户、编辑用户信息、删除用户
4. 管理用户角色和状态

### 7. 修改个人信息

所有用户都可以修改自己的个人信息和密码：

1. 点击用户名，选择"个人资料"
2. 修改邮箱和姓名
3. 在个人中心修改密码

## 🎯 技术亮点

### 1. 智能元数据抽取

- **统一抽取器接口**：基于抽象基类的可扩展设计
- **完整类型支持**：自动解析并展示完整的数据类型（包括长度、精度）
  - Oracle: `VARCHAR2(50)`, `NUMBER(10,2)`, `RAW(2000)`
  - SQL Server: `varchar(50)`, `decimal(10,2)`, `datetime2(3)`
  - MySQL: `VARCHAR(50)`, `DECIMAL(10,2)`
  - PostgreSQL: `VARCHAR(50)`, `NUMERIC(10,2)`
- **灵活的抽取模式**：
  - 全量抽取：获取所有表的完整元数据
  - 增量抽取：只抽取变更的表
  - 仅结构抽取：快速获取表结构，不统计行数和大小

### 2. 用户友好的交互体验

- **响应式设计**：适配各种屏幕尺寸
- **实时搜索和过滤**：快速定位目标数据
- **批量编辑**：一次性编辑多个字段的注释
- **权限控制**：基于角色的精细化权限管理
- **即时反馈**：操作成功/失败即时提示

### 3. 企业级特性

- **完整的用户管理**：多角色支持（管理员、普通用户、只读用户）
- **ETL 任务调度**：支持多种调度方式（时间间隔、CRON 表达式、手动执行）
- **抽取历史追踪**：完整记录每次抽取的详细信息
- **数据安全**：密码加密存储，会话管理

### 4. 可扩展性

- **模块化设计**：清晰的代码结构，易于扩展新功能
- **插件式抽取器**：轻松添加新的数据库支持
- **RESTful API**：标准化的 API 设计，便于集成

## 🔧 配置说明

### 📦 统一数据库连接配置

本系统已将所有数据库连接配置统一到 `database_connections.py` 文件中集中管理，提供更灵活、更易维护的配置方式。

#### 配置方式

**方式一：环境变量（推荐）**

通过环境变量配置数据库连接，方便在不同环境（开发、测试、生产）间切换：

```bash
# Windows
set DATABASE_URL=mysql+pymysql://root:password@localhost:3306/meta_db?charset=utf8mb4
set DB_POOL_SIZE=10
set DB_POOL_MAX_OVERFLOW=20

# Linux/Mac
export DATABASE_URL=mysql+pymysql://root:password@localhost:3306/meta_db?charset=utf8mb4
export DB_POOL_SIZE=10
export DB_POOL_MAX_OVERFLOW=20
```

**方式二：修改配置文件**

直接修改 `database_connections.py` 中的 `SYSTEM_DATABASE` 字典：

```python
SYSTEM_DATABASE = {
    'url': 'mysql+pymysql://root:password@your-host:3306/meta_db?charset=utf8mb4',
    'pool': {
        'pool_size': 10,
        'max_overflow': 20,
        # ...
    },
    # ...
}
```

#### 支持的数据库

| 数据库类型 | 驱动     | 默认端口 |
| ---------- | -------- | -------- |
| MySQL      | pymysql  | 3306     |
| PostgreSQL | psycopg2 | 5432     |
| SQL Server | pyodbc   | 1433     |
| Oracle     | oracledb | 1521     |
| StarRocks  | pymysql  | 9030     |

#### 使用示例

```python
# 生成数据库连接字符串
from database_connections import get_connection_string

conn_str = get_connection_string(
    db_type='mysql',
    host='localhost',
    port=3306,
    username='root',
    password='password',
    database='mydb'
)

# 检查数据库是否支持
from database_connections import is_database_supported

if is_database_supported('mysql'):
    print("MySQL 支持")

# 获取所有支持的数据库类型
from database_connections import get_supported_database_types

types = get_supported_database_types()
print(types)  # ['mysql', 'postgresql', 'sqlserver', 'oracle', 'starrocks']
```

#### 配置验证

```python
from database_connections import validate_database_connection

is_valid, error = validate_database_connection(
    db_type='mysql',
    host='localhost',
    port=3306,
    username='root',
    password='password',
    database='mydb'
)

if not is_valid:
    print(f"配置无效: {error}")
```

#### 环境变量列表

| 变量名                 | 说明               | 默认值                |
| ---------------------- | ------------------ | --------------------- |
| `DATABASE_URL`         | 系统数据库连接URL  | MySQL连接到本地数据库 |
| `DB_POOL_SIZE`         | 连接池大小         | 10                    |
| `DB_POOL_MAX_OVERFLOW` | 连接池最大溢出数   | 20                    |
| `DB_POOL_RECYCLE`      | 连接回收时间（秒） | 3600                  |
| `DB_ECHO`              | 是否输出SQL        | False                 |
| `CONNECTION_TIMEOUT`   | 连接超时（秒）     | 30                    |
| `QUERY_TIMEOUT`        | 查询超时（秒）     | 60                    |

#### 测试配置

运行测试脚本验证配置：

```bash
python test_database_connections.py
```

**详细说明**：请参考 [DATABASE_CONNECTIONS_GUIDE.md](DATABASE_CONNECTIONS_GUIDE.md)

---

### 环境变量

创建 `.env` 文件（可选）：

```env
# 数据库配置（已统一到 database_connections.py）
DATABASE_URL=sqlite:///metadata.db

# 会话密钥（生产环境请修改）
SECRET_KEY=your-secret-key-here

# 运行配置
FLASK_ENV=development
FLASK_DEBUG=False
```

### 数据库支持

默认使用 SQLite，生产环境建议使用 MySQL ：

```python
# MySQL
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/database_name

# PostgreSQL
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

**注意**：所有数据库连接配置现在都在 `database_connections.py` 中统一管理，建议优先使用该文件中的配置方式和工具函数。

## 🎯 抽取类型说明

| 抽取类型   | 说明                             | 适用场景             |
| ---------- | -------------------------------- | -------------------- |
| 全量抽取   | 抽取所有表的完整元数据           | 首次初始化、完全同步 |
| 增量抽取   | 只抽取新增或变更的表             | 定期同步、提升效率   |
| 仅结构抽取 | 只抽取表结构，不统计行数和数据量 | 快速预览、结构比对   |

## 👥 用户角色说明

| 角色              | 权限     | 说明                                      |
| ----------------- | -------- | ----------------------------------------- |
| 管理员 (admin)    | 完整权限 | 可以管理所有用户、数据源、ETL任务         |
| 普通用户 (user)   | 管理权限 | 可以创建和管理数据源、ETL任务，查看元数据 |
| 只读用户 (viewer) | 查看权限 | 只能查看元数据，不能创建或修改            |

## 🔒 安全建议

1. **修改默认密码**：首次登录后立即修改管理员密码
2. **配置 HTTPS**：生产环境必须使用 HTTPS
3. **使用强密码**：所有账户使用强密码
4. **定期备份**：定期备份元数据库
5. **限制访问**：配置防火墙规则，限制系统访问
6. **日志监控**：定期检查系统日志



## 🛠️ 开发指南

### 项目结构

```
metadata-manager/
├── app.py                 # 应用入口
├── api.py                 # API 路由和业务逻辑
├── auth.py                # 用户认证和授权
├── models.py              # 数据模型
├── db_config.py           # 数据库配置
├── extractor_base.py      # 元数据抽取器基类和实现
├── db_manager.py          # 数据库管理器
├── config.py              # 配置管理
├── exceptions.py          # 自定义异常
├── templates/             # HTML 模板
│   ├── index.html         # 首页
│   ├── login.html         # 登录页
│   ├── dashboard.html     # 仪表板
│   ├── data_sources.html  # 数据源管理
│   ├── etl.html          # ETL任务管理
│   ├── metadata.html      # 元数据浏览
│   ├── history.html       # 抽取历史
│   ├── users.html        # 用户管理
│   └── table_details.html # 表详情页面
├── static/                # 静态资源
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── main.js           # 主要 JavaScript
│       └── table_details.js # 表详情页面脚本
├── metadata.db           # SQLite 数据库（默认）
├── requirements.txt       # Python 依赖
├── README.md             # 项目文档
└── start.bat             # Windows 启动脚本
```

### 启动开发服务器

**Windows 用户**：

```bash
# 使用批处理文件启动
start.bat
```

**Linux/Mac 用户**：

```bash
# 直接运行
python app.py
```

访问：http://localhost:5000

**后台运行（Windows）**：

```powershell
# 使用 PowerShell
powershell.exe -Command "Start-Process -FilePath 'python.exe' -ArgumentList 'app.py' -WindowStyle Hidden"
```

**后台运行（Linux/Mac）**：

```bash
# 使用 nohup
nohup python app.py > server.log 2>&1 &

# 或使用 screen
screen -S metadata_manager
python app.py
# 按 Ctrl+A+D 分离会话
```

### 添加新功能

1. 在 `models.py` 中定义数据模型
2. 在 `api.py` 中添加 API 路由
3. 在 `templates/` 中创建 HTML 模板
4. 在 `static/js/` 中添加前端逻辑

## 🧪 测试

```bash
# 运行测试（如果存在）
python -m pytest tests/
```

## 📝 更新日志

### v1.3.3 (2026-01)

- ✨ 增加抽数过程状态展示（进行中）

### v1.3.2 (2026-01)

- ✨ 统一数据库配置
- ✨ 优化页面相应速度
- 🐛 修复 Oracle 数据库字段类型信息缺失问题

### v1.2.0 (2026-01)

- ✨ 新增 StarRocks 数据库支持
- ✨ 新增表注释手动编辑功能
- ✨ 新增字段注释手动编辑功能（模态框和详情页）
- 🐛 修复 Oracle 数据库字段类型信息缺失问题
- 🐛 修复 SQL Server 数据库字段类型信息缺失问题
- 🐛 修复 SQL Server 更新时间查询错误
- 🐛 修复元数据浏览和抽取历史页面登录状态丢失问题
- 🐛 修复表详情保存后页面假死问题
- 📝 优化用户权限控制

### v1.1.0 (2026-01)

- ✨ 新增表详情页面
- ✨ 新增表关联关系展示
- ✨ 新增抽取历史筛选功能
- 🐛 修复前端 JavaScript 报错问题
- 📝 优化页面加载性能

### v1.0.0 (2026-01)

- ✨ 初始版本发布
- 🎉 支持多种数据库元数据抽取（MySQL、PostgreSQL、SQL Server、Oracle）
- 👥 完整的用户权限管理
- 📊 数据可视化仪表板
- 🔄 ETL任务调度功能
- 🔍 元数据浏览和搜索
- 📖 表详情查看（字段信息、统计数据）

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## ❓ 常见问题 (FAQ)

### 1. 如何连接到远程数据库？

在添加数据源时，填写远程服务器的 IP 地址或域名即可：

- **主机地址**：例如 `192.168.1.100` 或 `db.example.com`
- **端口号**：确保端口已开放（MySQL:3306, PostgreSQL:5432, SQL Server:1433, Oracle:1521）
- **防火墙**：确保防火墙允许连接

### 2. 抽取失败怎么办？

常见的抽取失败原因和解决方法：

- **连接失败**：检查数据源配置是否正确，网络是否通畅
- **权限不足**：确保数据库用户有读取 INFORMATION_SCHEMA 或相应系统表的权限
- **表不存在**：检查数据库名称和表名是否正确
- **字符编码问题**：确保数据库字符编码与应用一致

### 3. 增量抽取不准确？

- **SQL Server**：由于使用 `STATS_DATE` 获取更新时间，可能无法准确反映数据变更，建议使用全量抽取
- **Oracle**：使用 `LAST_DDL_TIME`，只能反映 DDL 操作，不反映数据变更
- **其他数据库**：正常工作

### 4. 如何修改端口和密钥？

在 `.env` 文件中配置：

```env
# 修改端口
FLASK_PORT=5000

# 修改密钥（生产环境必须修改）
SECRET_KEY=your-very-long-and-random-secret-key
```

### 5. 如何备份数据？

使用 SQLite 时，直接复制 `metadata.db` 文件即可：

```bash
cp metadata.db metadata_backup_$(date +%Y%m%d).db
```

使用 MySQL/PostgreSQL 时，使用数据库自带的备份工具。

### 6. 如何重置管理员密码？

如果忘记管理员密码，可以执行以下 SQL 重置：

```sql
UPDATE users SET password='pbkdf2:sha256:260000$...' WHERE username='admin';
```

或者删除 `metadata.db` 文件，重启系统会自动创建新数据库。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📧 联系方式

- **邮箱**：changchunyouxiang@qq.com
- **项目地址**：https://github.com/yourusername/metadata-manager
- **问题反馈**：请在 GitHub Issues 中提交

## ⭐ Star History

如果这个项目对您有帮助，请给个 Star ⭐

## 📊 项目统计

- **代码行数**：约 5000+ 行
- **支持数据库**：5 种（MySQL、PostgreSQL、SQL Server、Oracle、StarRocks）
- **功能模块**：8 个
- **API 接口**：30+ 个

## 🙏 致谢

感谢所有为本项目做出贡献的开发者！

特别感谢以下开源项目：

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Font Awesome](https://fontawesome.com/)

---

<p align="center">
  <b>2026 Super MetaData Super MetaData 元数据管理系统 纯AI打造</b>
</p>

