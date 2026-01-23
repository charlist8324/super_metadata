# 数据库连接配置统一完成

## ✅ 更新完成

所有数据库连接配置已经统一到 `database_connections.py` 文件中！

---

## 📁 新增/修改的文件

### 新增文件

1. **database_connections.py** - 统一数据库连接配置文件
   - 系统数据库配置（元数据存储库）
   - 支持的数据库类型配置
   - 数据库连接工具函数
   - 配置验证函数

2. **test_database_connections.py** - 配置测试脚本
   - 测试所有配置功能
   - 验证连接字符串生成
   - 验证配置验证

3. **DATABASE_CONNECTIONS_GUIDE.md** - 配置使用指南
   - 详细的配置说明
   - 使用示例
   - 故障排查

### 修改的文件

1. **config.py** - 更新为从统一配置导入
   - 移除重复的 `SUPPORTED_DATABASES`
   - 移除硬编码的 `DATABASE_URL`
   - 从 `database_connections.py` 导入配置

2. **db_config.py** - 更新为从统一配置导入
   - 移除重复的 `SUPPORTED_DATABASES`
   - 移除连接字符串生成逻辑
   - 从 `database_connections.py` 导入配置和函数

---

## 🎯 配置方式

### 方式一：环境变量（推荐）

通过环境变量配置数据库连接：

```bash
# Windows
set DATABASE_URL=mysql+pymysql://root:password@localhost:3306/meta_db?charset=utf8mb4
set DB_POOL_SIZE=10
set DB_POOL_MAX_OVERFLOW=20
set DB_ECHO=False

# Linux/Mac
export DATABASE_URL=mysql+pymysql://root:password@localhost:3306/meta_db?charset=utf8mb4
export DB_POOL_SIZE=10
export DB_POOL_MAX_OVERFLOW=20
export DB_ECHO=False
```

### 方式二：修改配置文件

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

---

## 📊 支持的数据库

| 数据库类型 | 驱动 | 默认端口 |
|-----------|------|---------|
| MySQL | pymysql | 3306 |
| PostgreSQL | psycopg2 | 5432 |
| SQL Server | pyodbc | 1433 |
| Oracle | oracledb | 1521 |
| StarRocks | pymysql | 9030 |

---

## 🔧 统一配置文件功能

### 1. 系统数据库配置

```python
from database_connections import SYSTEM_DATABASE

# 获取系统数据库URL
url = SYSTEM_DATABASE['url']

# 获取连接池配置
pool_config = SYSTEM_DATABASE['pool']

# 获取连接参数
connect_args = SYSTEM_DATABASE['connect_args']

# 获取SQL输出配置
echo = SYSTEM_DATABASE['echo']
```

### 2. 数据库配置工具函数

```python
from database_connections import get_connection_string

# 生成连接字符串
conn_str = get_connection_string(
    db_type='mysql',
    host='localhost',
    port=3306,
    username='root',
    password='password',
    database='mydb'
)
```

### 3. 数据库信息查询

```python
from database_connections import (
    get_database_config,
    get_default_port,
    is_database_supported,
    get_supported_database_types,
    get_database_name
)

# 获取数据库配置
config = get_database_config('oracle')

# 获取默认端口
port = get_default_port('postgresql')

# 检查是否支持
if is_database_supported('mysql'):
    print("MySQL 支持")

# 获取所有支持的类型
types = get_supported_database_types()

# 获取数据库显示名称
name = get_database_name('mysql')  # MySQL
```

### 4. 配置验证

```python
from database_connections import validate_database_connection

# 验证连接配置
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

---

## 🚀 使用示例

### 1. 配置开发环境数据库

```bash
# Windows
set DATABASE_URL=mysql+pymysql://root:dev_password@localhost:3306/meta_db?charset=utf8mb4
python app.py

# Linux/Mac
export DATABASE_URL=mysql+pymysql://root:dev_password@localhost:3306/meta_db?charset=utf8mb4
python app.py
```

### 2. 配置生产环境数据库

```bash
# Windows
set DATABASE_URL=mysql+pymysql://root:prod_password@prod-host:3306/meta_db?charset=utf8mb4
set SECRET_KEY=your-production-secret-key
python app.py

# Linux/Mac
export DATABASE_URL=mysql+pymysql://root:prod_password@prod-host:3306/meta_db?charset=utf8mb4
export SECRET_KEY=your-production-secret-key
python app.py
```

### 3. 配置连接池大小

```bash
# 增加连接池大小（适用于高并发场景）
set DB_POOL_SIZE=20
set DB_POOL_MAX_OVERFLOW=40
python app.py
```

---

## 📋 环境变量完整列表

| 变量名 | 说明 | 默认值 |
|-------|------|--------|
| `DATABASE_URL` | 系统数据库连接URL | MySQL连接到本地数据库 |
| `DB_POOL_SIZE` | 连接池大小 | 10 |
| `DB_POOL_MAX_OVERFLOW` | 连接池最大溢出数 | 20 |
| `DB_POOL_RECYCLE` | 连接回收时间（秒） | 3600 |
| `DB_ECHO` | 是否输出SQL | False |
| `CONNECTION_TIMEOUT` | 连接超时（秒） | 30 |
| `QUERY_TIMEOUT` | 查询超时（秒） | 60 |
| `EXTRACTION_BATCH_SIZE` | 抽取批量大小 | 100 |
| `EXTRACTION_TIMEOUT` | 抽取超时（秒） | 3600 |
| `LOG_LEVEL` | 日志级别 | INFO |
| `LOG_FILE` | 日志文件名 | metadata_manager.log |
| `SECRET_KEY` | Flask密钥 | dev-secret-key |
| `DEBUG` | 调试模式 | False |
| `HOST` | 监听地址 | 0.0.0.0 |
| `PORT` | 监听端口 | 5000 |
| `FLASK_ENV` | Flask环境 | default |

---

## 🔄 从旧配置迁移

如果您之前在 `config.py` 或 `db_config.py` 中直接修改了数据库配置：

### 步骤1：设置环境变量（推荐）

```bash
# 设置数据库连接URL
export DATABASE_URL=your-database-url
```

### 步骤2：或修改 database_connections.py

编辑 `database_connections.py`，修改 `SYSTEM_DATABASE` 字典。

### 步骤3：无需修改其他文件

`config.py` 和 `db_config.py` 已自动从 `database_connections.py` 导入配置。

---

## 🧪 测试配置

运行测试脚本验证配置：

```bash
python test_database_connections.py
```

测试内容包括：
- ✅ 系统数据库配置
- ✅ 支持的数据库类型
- ✅ 每个数据库的配置
- ✅ 连接字符串生成
- ✅ 默认端口获取
- ✅ 数据库类型检查
- ✅ 数据库显示名称
- ✅ 连接配置验证
- ✅ 无效配置识别

---

## 📚 相关文档

- **database_connections.py** - 统一配置文件源码
- **DATABASE_CONNECTIONS_GUIDE.md** - 详细使用指南
- **test_database_connections.py** - 配置测试脚本

---

## ✅ 优势

1. **统一管理** - 所有数据库连接配置在一个文件中
2. **易于维护** - 修改配置只需编辑一个文件
3. **环境隔离** - 支持通过环境变量配置不同环境
4. **类型安全** - 提供类型提示和验证
5. **工具函数** - 提供丰富的工具函数方便使用
6. **向后兼容** - 保持与现有代码的兼容性

---

## 🚀 下一步

1. **配置环境变量** - 根据您的环境设置 `DATABASE_URL`
2. **测试连接** - 运行测试脚本验证配置
3. **启动应用** - 使用新配置启动应用

---

**更新日期：** 2026-01-21
**版本：** 2.0
