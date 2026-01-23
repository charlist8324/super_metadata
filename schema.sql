-- ============================================
-- Super MetaData 元数据管理系统数据库建表脚本
-- 版本：1.0.0
-- 数据库类型：SQLite / MySQL / PostgreSQL / SQL Server
-- ============================================

-- ============================================
-- 1. 用户表 (users)
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT 1,
    is_admin BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- ============================================
-- 2. 角色表 (roles)
-- ============================================
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255),
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 3. 权限表 (permissions)
-- ============================================
CREATE TABLE IF NOT EXISTS permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 4. 用户角色关联表 (user_roles)
-- ============================================
CREATE TABLE IF NOT EXISTS user_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    UNIQUE(user_id, role_id)
);

-- ============================================
-- 5. 角色权限关联表 (role_permissions)
-- ============================================
CREATE TABLE IF NOT EXISTS role_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    granted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    UNIQUE(role_id, permission_id)
);

-- ============================================
-- 6. 数据源表 (data_sources)
-- ============================================
CREATE TABLE IF NOT EXISTS data_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL,  -- mysql, postgresql, sqlserver, oracle
    host VARCHAR(255) NOT NULL,
    port INTEGER NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    database VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_data_sources_type ON data_sources(type);

-- ============================================
-- 7. 表元数据表 (table_metadata)
-- ============================================
CREATE TABLE IF NOT EXISTS table_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name VARCHAR(255) NOT NULL,
    schema_name VARCHAR(255),
    row_count BIGINT,
    size_bytes BIGINT,
    comment TEXT,
    datasource_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (datasource_id) REFERENCES data_sources(id) ON DELETE CASCADE
);

CREATE INDEX idx_table_metadata_datasource ON table_metadata(datasource_id);
CREATE INDEX idx_table_metadata_name ON table_metadata(table_name);
CREATE INDEX idx_table_metadata_schema ON table_metadata(schema_name);

-- ============================================
-- 8. 字段元数据表 (column_metadata)
-- ============================================
CREATE TABLE IF NOT EXISTS column_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    column_name VARCHAR(255) NOT NULL,
    data_type VARCHAR(100) NOT NULL,
    is_nullable VARCHAR(10) NOT NULL,
    default_value VARCHAR(255),
    column_comment TEXT,
    ordinal_position INTEGER,
    table_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (table_id) REFERENCES table_metadata(id) ON DELETE CASCADE
);

CREATE INDEX idx_column_metadata_table ON column_metadata(table_id);
CREATE INDEX idx_column_metadata_name ON column_metadata(column_name);

-- ============================================
-- 9. 表关联关系表 (table_relationships)
-- ============================================
CREATE TABLE IF NOT EXISTS table_relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    constraint_name VARCHAR(255),
    table_id INTEGER NOT NULL,
    referenced_table_id INTEGER NOT NULL,
    column_name VARCHAR(255) NOT NULL,
    referenced_column_name VARCHAR(255) NOT NULL,
    constraint_type VARCHAR(50) NOT NULL,  -- FOREIGN KEY, PRIMARY KEY
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (table_id) REFERENCES table_metadata(id) ON DELETE CASCADE,
    FOREIGN KEY (referenced_table_id) REFERENCES table_metadata(id) ON DELETE CASCADE
);

CREATE INDEX idx_table_relationships_table ON table_relationships(table_id);
CREATE INDEX idx_table_relationships_ref_table ON table_relationships(referenced_table_id);

-- ============================================
-- 10. 抽取历史记录表 (extraction_history)
-- ============================================
CREATE TABLE IF NOT EXISTS extraction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datasource_id INTEGER NOT NULL,
    extraction_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL,  -- success, failed
    message TEXT,
    extracted_tables INTEGER,
    etl_task_id INTEGER,
    FOREIGN KEY (datasource_id) REFERENCES data_sources(id) ON DELETE CASCADE,
    FOREIGN KEY (etl_task_id) REFERENCES etl_tasks(id) ON DELETE SET NULL
);

CREATE INDEX idx_extraction_history_datasource ON extraction_history(datasource_id);
CREATE INDEX idx_extraction_history_time ON extraction_history(extraction_time);
CREATE INDEX idx_extraction_history_task ON extraction_history(etl_task_id);

-- ============================================
-- 11. ETL任务表 (etl_tasks)
-- ============================================
CREATE TABLE IF NOT EXISTS etl_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    task_type VARCHAR(50) NOT NULL,  -- full, incremental, schema_only
    datasource_id INTEGER NOT NULL,
    schedule_type VARCHAR(50) NOT NULL,  -- interval, cron, manual
    interval_value INTEGER,
    interval_unit VARCHAR(20),  -- minutes, hours, days, weeks
    cron_expression VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active',  -- active, inactive
    description TEXT,
    last_run DATETIME,
    next_run DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (datasource_id) REFERENCES data_sources(id) ON DELETE CASCADE
);

CREATE INDEX idx_etl_tasks_datasource ON etl_tasks(datasource_id);
CREATE INDEX idx_etl_tasks_status ON etl_tasks(status);
CREATE INDEX idx_etl_tasks_type ON etl_tasks(task_type);

-- ============================================
-- 初始化数据
-- ============================================

-- 插入默认角色
INSERT OR IGNORE INTO roles (name, description) VALUES
    ('admin', '管理员角色，拥有所有权限'),
    ('user', '普通用户角色，可以管理数据源和查看元数据'),
    ('viewer', '只读用户角色，只能查看元数据');

-- 插入默认权限
INSERT OR IGNORE INTO permissions (name, description) VALUES
    ('view_metadata', '查看元数据'),
    ('manage_metadata', '管理元数据'),
    ('view_data_sources', '查看数据源'),
    ('manage_data_sources', '管理数据源'),
    ('view_extraction_history', '查看抽取历史'),
    ('manage_extraction_tasks', '管理抽取任务'),
    ('manage_users', '管理用户'),
    ('manage_roles', '管理角色');

-- 为管理员角色分配所有权限
INSERT OR IGNORE INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r, permissions p
WHERE r.name = 'admin';

-- 插入默认管理员账户
-- 密码: admin123 (生产环境请立即修改！）
INSERT OR IGNORE INTO users (username, email, password_hash, full_name, is_admin, is_active)
VALUES (
    'admin',
    'admin@example.com',
    'pbkdf2:sha256:260000$SaltValue$HashValue',  -- 实际哈希值需要在应用中生成
    '系统管理员',
    1,
    1
);

-- 为管理员分配角色
INSERT OR IGNORE INTO user_roles (user_id, role_id)
SELECT u.id, r.id
FROM users u, roles r
WHERE u.username = 'admin' AND r.name = 'admin';

-- ============================================
-- 建表完成
-- ============================================
