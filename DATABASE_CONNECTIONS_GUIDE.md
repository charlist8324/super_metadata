# 数据库连接配置说明

## 📝 概述

为了统一管理所有数据库连接配置，本系统将所有数据库连接配置集中到 `database_connections.py` 文件中。

## 📂 配置文件结构

### database_connections.py - 统一数据库连接配置文件

这是系统中唯一的数据库连接配置文件，包含：

1. **系统数据库配置**（元数据存储库）
   - 连接URL
   - 连接池配置
   - 连接参数

2. **支持的数据库类型配置**
   - MySQL
   - PostgreSQL
   - SQL Server
   - Oracle
   - StarRocks

3. **数据库连接工具函数**
   - `get_connection_string()` - 生成连接字符串
   - `get_database_config()` - 获取数据库配置
   - `get_default_port()` - 获取默认端口
   - `is_database_supported()` - 检查是否支持
   - `get_supported_database_types()` - 获取所有支持的类型
   - `get_database_name()` - 获取数据库显示名称
   - `validate_database_connection()` - 验证连接配置

---

## 🔧 配置方式

### 方式一：环境变量（推荐）

通过环境变量配置数据库连接，方便在不同环境（开发、测试、生产）间切换：

```bash
# Windows
set DATABASE_URL=mysql+pymysql://root:password@localhost:3306/meta_db?charset=utf8mb4
set DB_POOL_SIZE=10
set DB_POOL_MAX_OVERFLOW=20
set DB_ECHO=False
set CONNECTION_TIMEOUT=30

# Linux/Mac
export DATABASE_URL=mysql+pymysql://root:password@localhost:3306/meta_db?charset=utf8mb4
export DB_POOL_SIZE=10
export DB_POOL_MAX_OVERFLOW=20
export DB_ECHO=False
export CONNECTION_TIMEOUT=30
```

### 方式二：修改配置文件

直接修改 `database_connections.py` 中的 `SYSTEM_DATABASE` 字典：

```python
SYSTEM_DATABASE = {
    # 修改系统数据库连接URL
    'url': 'mysql+pymysql://root:password@your-host:3306/meta_db?charset=utf8mb4',
    
    # 修改连接池配置
    'pool': {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    },
    
    # 修改连接参数
    'connect_args': {
        'connect_timeout': 30,
        'charset': 'utf8mb4'
    },
    
    # 是否输出SQL语句（用于调试）
    'echo': False,
}
```

---

## 📊 支持的数据库类型

| 数据库类型 | 驱动 | 默认端口 | 连接字符串格式 |
|-----------|------|---------|--------------|
| MySQL | pymysql | 3306 | `mysql+pymysql://user:pass@host:3306/db` |
| PostgreSQL | psycopg2 | 5432 | `postgresql+psycopg2://user:pass@host:5432/db` |
| SQL Server | pyodbc | 1433 | `mssql+pyodbc://user:pass@host:1433/db?driver=ODBC+Driver+17+for+SQL+Server` |
| Oracle | oracledb | 1521 | `oracle+oracledb://user:pass@host:1521/orcl` |
| StarRocks | pymysql | 9030 | `mysql+pymysql://user:pass@host:9030/db` |

---

## 🔌 使用示例

### 1. 生成数据库连接字符串

```python
from database_connections import get_connection_string

# 生成MySQL连接字符串
conn_str = get_connection_string(
    db_type='mysql',
    host='localhost',
    port=3306,
    username='root',
    password='password',
    database='mydb'
)
print(conn_str)
# 输出: mysql+pymysql://root:password@localhost:3306/mydb
```

### 2. 获取数据库配置

```python
from database_connections import get_database_config

# 获取Oracle配置
config = get_database_config('oracle')
print(config['name'])  # 输出: Oracle
print(config['port'])  # 输出: 1521
```

### 3. 检查数据库是否支持

```python
from database_connections import is_database_supported

if is_database_supported('mysql'):
    print("MySQL 支持")
else:
    print("MySQL 不支持")
```

### 4. 获取所有支持的数据库类型

```python
from database_connections import get_supported_database_types

types = get_supported_database_types()
print(types)
# 输出: ['mysql', 'postgresql', 'sqlserver', 'oracle', 'starrocks']
```

### 5. 验证连接配置

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

if is_valid:
    print("配置有效")
else:
    print(f"配置无效: {error}")
```

---

## 🔄 从旧配置迁移

如果您之前在 `config.py` 或 `db_config.py` 中直接修改了数据库配置，现在需要：

### 步骤1：设置环境变量（推荐）

```bash
# 设置系统数据库连接URL
export DATABASE_URL=mysql+pymysql://root:password@localhost:3306/meta_db?charset=utf8mb4
```

### 步骤2：或修改 database_connections.py

编辑 `database_connections.py` 文件，修改 `SYSTEM_DATABASE` 字典：

```python
SYSTEM_DATABASE = {
    'url': '你的数据库连接URL',
    # ... 其他配置
}
```

### 步骤3：删除旧配置

现在可以从以下文件中删除重复的数据库配置：
- `config.py` 中的 `SUPPORTED_DATABASES` 和 `DATABASE_URL`
- `db_config.py` 中的 `SUPPORTED_DATABASES` 和连接字符串生成逻辑

**注意**：这些文件已经更新为从 `database_connections.py` 导入配置，无需手动修改。

---

## 🚀 启动应用

### 开发环境

```bash
# 使用默认配置
python app.py

# 或使用环境变量覆盖
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/meta_db?charset=utf8mb4 python app.py
```

### 生产环境

```bash
# 必须设置环境变量
export DATABASE_URL=your-production-db-url
export SECRET_KEY=your-secret-key
python app.py
```

### 测试环境

```bash
export FLASK_ENV=testing
python app.py
```

---

## 📋 环境变量列表

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
| `SECRET_KEY` | Flask密钥 | dev-secret-key-for-metadata-manager |
| `DEBUG` | 调试模式 | False |
| `HOST` | 监听地址 | 0.0.0.0 |
| `PORT` | 监听端口 | 5000 |
| `FLASK_ENV` | Flask环境 | default |

---

## 🔍 故障排查

### 问题1：数据库连接失败

**检查项**：
1. 确认 `DATABASE_URL` 格式正确
2. 确认数据库服务正在运行
3. 确认用户名、密码正确
4. 检查网络连接

### 问题2：连接池耗尽

**解决方案**：
```bash
# 增加连接池大小
export DB_POOL_SIZE=20
export DB_POOL_MAX_OVERFLOW=40
```

### 问题3：连接超时

**解决方案**：
```bash
# 增加连接超时时间
export CONNECTION_TIMEOUT=60
```

---

## ✅ 总结

1. **所有数据库连接配置都在 `database_connections.py` 中统一管理**
2. **推荐使用环境变量配置**，便于不同环境切换
3. **其他配置文件（config.py, db_config.py）已更新**为从统一配置导入
4. **修改配置后无需重启应用**（如果使用环境变量）

---

## 📚 相关文件

- **database_connections.py** - 统一数据库连接配置文件
- **config.py** - 应用配置（从database_connections导入）
- **db_config.py** - 数据库配置类（从database_connections导入）
- **app.py** - 应用启动文件

---

**更新日期：** 2026-01-21
**版本：** 2.0
