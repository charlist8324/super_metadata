"""
测试数据库连接配置

验证统一配置文件是否正常工作
"""

from database_connections import (
    SYSTEM_DATABASE,
    SUPPORTED_DATABASES,
    get_connection_string,
    get_database_config,
    get_default_port,
    is_database_supported,
    get_supported_database_types,
    get_database_name,
    validate_database_connection,
    DatabaseConfig
)


def test_database_connections_config():
    """测试数据库连接配置"""
    
    print("=" * 80)
    print("数据库连接配置测试")
    print("=" * 80)
    print()
    
    # 测试1：系统数据库配置
    print("1. 测试系统数据库配置...")
    print(f"   系统数据库URL: {SYSTEM_DATABASE['url']}")
    print(f"   连接池配置: {SYSTEM_DATABASE['pool']}")
    print(f"   连接参数: {SYSTEM_DATABASE['connect_args']}")
    print(f"   SQL输出: {SYSTEM_DATABASE['echo']}")
    print()
    
    # 测试2：支持的数据库类型
    print("2. 测试支持的数据库类型...")
    db_types = get_supported_database_types()
    print(f"   支持的数据库类型: {db_types}")
    print()
    
    # 测试3：每个数据库类型的配置
    print("3. 测试每个数据库类型的配置...")
    for db_type in db_types:
        config = get_database_config(db_type)
        print(f"   {db_type.upper()}:")
        print(f"     名称: {config['name']}")
        print(f"     驱动: {config['driver']}")
        print(f"     端口: {config['port']}")
        print(f"     方言: {config['dialect']}")
        if 'description' in config:
            print(f"     描述: {config['description']}")
        if 'note' in config:
            print(f"     备注: {config['note']}")
        print()
    
    # 测试4：生成连接字符串
    print("4. 测试生成连接字符串...")
    print("   MySQL:")
    print(f"     {get_connection_string('mysql', 'localhost', 3306, 'root', 'password', 'testdb')}")
    print("   PostgreSQL:")
    print(f"     {get_connection_string('postgresql', 'localhost', 5432, 'postgres', 'password', 'testdb')}")
    print("   SQL Server:")
    print(f"     {get_connection_string('sqlserver', 'localhost', 1433, 'sa', 'password', 'testdb')}")
    print("   Oracle:")
    print(f"     {get_connection_string('oracle', 'localhost', 1521, 'system', 'password', 'orcl')}")
    print("   StarRocks:")
    print(f"     {get_connection_string('starrocks', 'localhost', 9030, 'root', 'password', 'testdb')}")
    print()
    
    # 测试5：获取默认端口
    print("5. 测试获取默认端口...")
    for db_type in ['mysql', 'postgresql', 'sqlserver', 'oracle', 'starrocks']:
        port = get_default_port(db_type)
        print(f"   {db_type}: {port}")
    print()
    
    # 测试6：检查数据库是否支持
    print("6. 测试检查数据库是否支持...")
    print(f"   MySQL 支持: {is_database_supported('mysql')}")
    print(f"   PostgreSQL 支持: {is_database_supported('postgresql')}")
    print(f"   Oracle 支持: {is_database_supported('oracle')}")
    print(f"   MongoDB 支持: {is_database_supported('mongodb')}")
    print()
    
    # 测试7：获取数据库显示名称
    print("7. 测试获取数据库显示名称...")
    for db_type in ['mysql', 'postgresql', 'sqlserver', 'oracle']:
        name = get_database_name(db_type)
        print(f"   {db_type}: {name}")
    print()
    
    # 测试8：验证连接配置
    print("8. 测试验证连接配置...")
    valid, error = validate_database_connection(
        db_type='mysql',
        host='localhost',
        port=3306,
        username='root',
        password='password',
        database='testdb'
    )
    print(f"   有效配置: {valid}")
    if error:
        print(f"   错误: {error}")
    print()
    
    # 测试9：无效配置验证
    print("9. 测试无效配置验证...")
    valid, error = validate_database_connection(
        db_type='invalid_db',
        host='',
        port=99999,
        username='',
        password='',
        database=''
    )
    print(f"   有效配置: {valid}")
    print(f"   错误: {error}")
    print()
    
    # 测试10：DatabaseConfig 类
    print("10. 测试 DatabaseConfig 类...")
    print(f"   系统数据库URL: {DatabaseConfig.get_system_database_url()}")
    print(f"   SQL输出: {DatabaseConfig.is_echo_enabled()}")
    print()
    
    print("=" * 80)
    print("所有测试完成！")
    print("=" * 80)


if __name__ == "__main__":
    test_database_connections_config()
