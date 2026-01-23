# StarRocks数据库支持实现文档

## 📋 实现概述

已成功为Super MetaData 元数据管理系统添加StarRocks数据库支持。

## ✅ 完成的工作

### 1. 后端实现

#### 1.1 创建StarRocks抽取器类
**文件**：`extractor_base.py`

**类名**：`StarRocksMetadataExtractor`

**继承关系**：继承自 `MySQLMetadataExtractor`

**原因**：StarRocks是基于MySQL协议的MPP（大规模并行处理）数据库，可以复用MySQL的大部分元数据查询逻辑

**实现方法**：
- `get_table_list()` - 获取所有表列表
- `get_table_metadata()` - 获取表元数据
- `get_column_metadata()` - 获取列元数据
- `get_row_count()` - 获取表行数
- `get_table_size()` - 获取表数据大小
- `get_table_relationships()` - 获取表关联关系
- `get_table_update_time()` - 获取表更新时间

#### 1.2 更新API路由
**文件**：`api.py`

**修改内容**：
1. 导入StarRocks抽取器：
```python
from extractor_base import (
    MySQLMetadataExtractor, 
    PostgreSQLMetadataExtractor, 
    SQLServerMetadataExtractor, 
    OracleMetadataExtractor,
    StarRocksMetadataExtractor  # 新增
)
```

2. 更新EXTRACTOR_MAP：
```python
EXTRACTOR_MAP = {
    'mysql': MySQLMetadataExtractor,
    'postgresql': PostgreSQLMetadataExtractor,
    'sqlserver': SQLServerMetadataExtractor,
    'oracle': OracleMetadataExtractor,
    'starrocks': StarRocksMetadataExtractor  # 新增
}
```

### 2. 前端实现

#### 2.1 数据源管理页面
**文件**：`templates/data_sources.html`

**修改内容**：在数据库类型下拉框中添加StarRocks选项
```html
<select class="form-select" id="type" required>
    <option value="">请选择数据库类型</option>
    <option value="mysql">MySQL</option>
    <option value="postgresql">PostgreSQL</option>
    <option value="sqlserver">SQL Server</option>
    <option value="oracle">Oracle</option>
    <option value="starrocks">StarRocks</option>  <!-- 新增 -->
</select>
```

## 🔧 技术实现细节

### StarRocks元数据查询

#### 表列表查询
```sql
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = :database_name
AND TABLE_TYPE = 'BASE TABLE'
```

#### 表元数据查询
```sql
SELECT TABLE_COMMENT AS comment
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = :database_name
AND TABLE_NAME = :table_name
```

#### 列元数据查询
```sql
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE,
    COLUMN_DEFAULT,
    ORDINAL_POSITION,
    COLUMN_COMMENT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = :database_name
AND TABLE_NAME = :table_name
ORDER BY ORDINAL_POSITION
```

#### 关联关系查询
```sql
SELECT 
    CONSTRAINT_NAME,
    TABLE_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = :database_name
AND REFERENCED_TABLE_SCHEMA = :database_name
AND REFERENCED_TABLE_NAME IS NOT NULL
```

### StarRocks特性

1. **兼容MySQL协议**：可以直接使用PyMySQL驱动连接
2. **使用MySQL的INFORMATION_SCHEMA**：查询元数据的方式与MySQL一致
3. **支持增量抽取**：通过UPDATE_TIME判断表是否变更
4. **支持外键关系**：可以正确读取表间的关联关系

## 📝 使用方法

### 1. 添加StarRocks数据源

1. 登录系统
2. 进入"数据源管理"页面
3. 点击"添加数据源"按钮
4. 填写表单：
   - **数据源名称**：自定义名称
   - **数据库类型**：选择"StarRocks"
   - **主机地址**：StarRocks服务器地址
   - **端口**：默认9030（StarRocks FE端口）
   - **用户名**：数据库用户名
   - **密码**：数据库密码
   - **数据库名**：数据库名称
5. 点击"测试连接"验证配置
6. 点击"保存"完成添加

### 2. 执行元数据抽取

1. 在数据源列表中找到StarRocks数据源
2. 点击"抽取"按钮，或创建ETL任务
3. 选择抽取类型：
   - **全量抽取**：抽取所有表的完整元数据
   - **增量抽取**：只抽取变更的表
   - **仅结构抽取**：只抽取表结构，不统计数据量

### 3. 浏览元数据

1. 进入"元数据浏览"页面
2. 选择StarRocks数据源
3. 查看表列表和表详情
4. 查看字段列表、类型、长度、注释等信息

## ⚠️ 注意事项

### 连接配置

- **默认端口**：StarRocks FE默认端口为9030
- **驱动要求**：使用PyMySQL驱动（与MySQL相同）
- **连接字符串**：
  ```
  mysql+pymysql://user:password@host:9030/database
  ```

### 功能限制

1. **兼容性**：StarRocks元数据查询基于MySQL协议，功能与MySQL基本一致
2. **增量抽取**：依赖INFORMATION_SCHEMA.TABLES的UPDATE_TIME字段
3. **外键关系**：如果StarRocks配置了外键，可以正确识别

### 性能建议

1. **大表统计**：COUNT(*)和表大小查询可能较慢
2. **增量抽取**：建议在大数据量场景下使用增量抽取
3. **定时任务**：合理安排抽取时间，避免影响业务

## 🎯 数据库对比

| 特性 | MySQL | StarRocks |
|------|-------|-----------|
| 协议 | MySQL | 兼容MySQL |
| 默认端口 | 3306 | 9030 |
| 元数据查询 | INFORMATION_SCHEMA | INFORMATION_SCHEMA |
| 外键支持 | ✅ | ✅ |
| 增量抽取 | ✅ | ✅ |
| 并行处理 | 否 | 是（MPP架构） |

## 🔍 故障排查

### 连接失败
1. 检查主机地址和端口是否正确
2. 确认StarRocks FE服务是否启动
3. 验证用户名和密码
4. 检查网络连接

### 抽取失败
1. 查看服务器日志了解错误详情
2. 确认用户有访问INFORMATION_SCHEMA的权限
3. 检查数据库是否包含大量表，可能超时

### 元数据不准确
1. 执行手动增量抽取
2. 检查表权限
3. 确认数据库元数据是否及时更新

## 📚 参考资源

- StarRocks官方文档：https://docs.starrocks.io/
- MySQL INFORMATION_SCHEMA：https://dev.mysql.com/doc/refman/8.0/en/information-schema.html
- PyMySQL文档：https://pymysql.readthedocs.io/

## 📝 文件修改记录

| 文件 | 修改内容 | 状态 |
|------|---------|------|
| extractor_base.py | 新增StarRocksMetadataExtractor类 | ✅ 完成 |
| api.py | 导入StarRocks抽取器并更新映射 | ✅ 完成 |
| data_sources.html | 添加StarRocks数据库类型选项 | ✅ 完成 |

---

**实现日期**：2026-01-15
**版本**：v1.0.1
**作者**：纯AI打造
