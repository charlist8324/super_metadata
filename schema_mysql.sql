-- ============================================
-- Super MetaData 元数据管理系统数据库建表脚本 (MySQL版本）
-- 版本：1.0.0
-- ============================================

-- ============================================
-- 1. 用户表 (users)
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active TINYINT(1) DEFAULT 1,
    is_admin TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 2. 角色表 (roles)
-- ============================================
CREATE TABLE IF NOT EXISTS roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255),
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 3. 权限表 (permissions)
-- ============================================
CREATE TABLE IF NOT EXISTS permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 4. 用户角色关联表 (user_roles)
-- ============================================
CREATE TABLE IF NOT EXISTS user_roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_role (user_id, role_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 5. 角色权限关联表 (role_permissions)
-- ============================================
CREATE TABLE IF NOT EXISTS role_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    role_id INT NOT NULL,
    permission_id INT NOT NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    UNIQUE KEY uk_role_permission (role_id, permission_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 6. 数据源表 (data_sources)
-- ============================================
CREATE TABLE IF NOT EXISTS data_sources (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL COMMENT 'mysql, postgresql, sqlserver, oracle',
    host VARCHAR(255) NOT NULL,
    port INT NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    `database` VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 7. 表元数据表 (table_metadata)
-- ============================================
CREATE TABLE IF NOT EXISTS table_metadata (
    id INT PRIMARY KEY AUTO_INCREMENT,
    table_name VARCHAR(255) NOT NULL,
    schema_name VARCHAR(255),
    row_count BIGINT,
    size_bytes BIGINT,
    comment TEXT,
    datasource_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (datasource_id) REFERENCES data_sources(id) ON DELETE CASCADE,
    INDEX idx_datasource (datasource_id),
    INDEX idx_table_name (table_name),
    INDEX idx_schema_name (schema_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 8. 字段元数据表 (column_metadata)
-- ============================================
CREATE TABLE IF NOT EXISTS column_metadata (
    id INT PRIMARY KEY AUTO_INCREMENT,
    column_name VARCHAR(255) NOT NULL,
    data_type VARCHAR(100) NOT NULL,
    is_nullable VARCHAR(10) NOT NULL,
    default_value VARCHAR(255),
    column_comment TEXT,
    ordinal_position INT,
    table_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (table_id) REFERENCES table_metadata(id) ON DELETE CASCADE,
    INDEX idx_table_id (table_id),
    INDEX idx_column_name (column_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 9. 表关联关系表 (table_relationships)
-- ============================================
CREATE TABLE IF NOT EXISTS table_relationships (
    id INT PRIMARY KEY AUTO_INCREMENT,
    constraint_name VARCHAR(255),
    table_id INT NOT NULL,
    referenced_table_id INT NOT NULL,
    column_name VARCHAR(255) NOT NULL,
    referenced_column_name VARCHAR(255) NOT NULL,
    constraint_type VARCHAR(50) NOT NULL COMMENT 'FOREIGN KEY, PRIMARY KEY',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (table_id) REFERENCES table_metadata(id) ON DELETE CASCADE,
    FOREIGN KEY (referenced_table_id) REFERENCES table_metadata(id) ON DELETE CASCADE,
    INDEX idx_table_id (table_id),
    INDEX idx_referenced_table_id (referenced_table_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 10. 抽取历史记录表 (extraction_history)
-- ============================================
CREATE TABLE IF NOT EXISTS extraction_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    datasource_id INT NOT NULL,
    extraction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL COMMENT 'success, failed',
    message TEXT,
    extracted_tables INT,
    etl_task_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (datasource_id) REFERENCES data_sources(id) ON DELETE CASCADE,
    FOREIGN KEY (etl_task_id) REFERENCES etl_tasks(id) ON DELETE SET NULL,
    INDEX idx_datasource_id (datasource_id),
    INDEX idx_extraction_time (extraction_time),
    INDEX idx_etl_task_id (etl_task_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 11. ETL任务表 (etl_tasks)
-- ============================================
CREATE TABLE IF NOT EXISTS etl_tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    task_type VARCHAR(50) NOT NULL COMMENT 'full, incremental, schema_only',
    datasource_id INT NOT NULL,
    schedule_type VARCHAR(50) NOT NULL COMMENT 'interval, cron, manual',
    interval_value INT,
    interval_unit VARCHAR(20) COMMENT 'minutes, hours, days, weeks',
    cron_expression VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active' COMMENT 'active, inactive',
    description TEXT,
    last_run TIMESTAMP NULL,
    next_run TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (datasource_id) REFERENCES data_sources(id) ON DELETE CASCADE,
    INDEX idx_datasource_id (datasource_id),
    INDEX idx_status (status),
    INDEX idx_task_type (task_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 初始化数据
-- ============================================

-- 插入默认角色
INSERT IGNORE INTO roles (name, description) VALUES
    ('admin', '管理员角色，拥有所有权限'),
    ('user', '普通用户角色，可以管理数据源和查看元数据'),
    ('viewer', '只读用户角色，只能查看元数据');

-- 插入默认权限
INSERT IGNORE INTO permissions (name, description) VALUES
    ('view_metadata', '查看元数据'),
    ('manage_metadata', '管理元数据'),
    ('view_data_sources', '查看数据源'),
    ('manage_data_sources', '管理数据源'),
    ('view_extraction_history', '查看抽取历史'),
    ('manage_extraction_tasks', '管理抽取任务'),
    ('manage_users', '管理用户'),
    ('manage_roles', '管理角色');

-- 为管理员角色分配所有权限
INSERT IGNORE INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r, permissions p
WHERE r.name = 'admin';

-- ============================================
-- 建表完成
-- ============================================
