"""
测试 Oracle 连接（使用 python-oracledb 瘦模式）

此脚本演示如何使用 python-oracledb 的瘦模式连接 Oracle 数据库，
无需安装 Oracle Instant Client。
"""

import oracledb

def test_oracle_thin_mode():
    """
    测试 Oracle 连接 - 瘦模式（Thin Mode）
    
    瘦模式优点：
    - 纯 Python 实现
    - 无需 Oracle Instant Client
    - 无需配置环境变量
    - 即插即用
    """
    
    # 配置数据库连接信息
    # 请替换为您的实际 Oracle 数据库信息
    config = {
        'user': 'your_username',      # 替换为您的用户名
        'password': 'your_password',    # 替换为您的密码
        'dsn': 'localhost:1521/orcl'   # 格式：主机名:端口号/服务名或SID
    }
    
    print("🚀 开始测试 Oracle 连接（瘦模式）...")
    print(f"📡 连接信息：DSN = {config['dsn']}")
    print()
    
    try:
        # 建立连接 - 默认就是 Thin Mode
        print("🔌 正在连接数据库...")
        connection = oracledb.connect(
            user=config['user'],
            password=config['password'],
            dsn=config['dsn']
        )
        print("✅ 连接成功！")
        print()
        
        # 获取数据库版本信息
        print("📊 数据库信息：")
        with connection.cursor() as cursor:
            # 查询数据库版本
            cursor.execute("SELECT * FROM v$version WHERE rownum = 1")
            version = cursor.fetchone()
            print(f"   Oracle 版本: {version[0] if version else 'Unknown'}")
            
            # 查询当前数据库时间
            cursor.execute("SELECT sysdate FROM dual")
            db_time = cursor.fetchone()
            print(f"   数据库时间: {db_time[0]}")
            
            # 查询当前用户
            cursor.execute("SELECT user FROM dual")
            current_user = cursor.fetchone()
            print(f"   当前用户: {current_user[0]}")
            
            # 查询默认表空间
            cursor.execute("""
                SELECT default_tablespace 
                FROM user_users
            """)
            tablespace = cursor.fetchone()
            print(f"   默认表空间: {tablespace[0] if tablespace else 'Unknown'}")
            
        print()
        print("🎉 测试完成！连接正常，可以开始使用。")
        
        return True
        
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"❌ 数据库错误:")
        print(f"   错误代码: {error.code}")
        print(f"   错误消息: {error.message}")
        print()
        print("💡 常见问题:")
        print("   1. 检查用户名、密码是否正确")
        print("   2. 检查 DSN 格式是否正确（host:port/service_name）")
        print("   3. 检查 Oracle 数据库是否正在运行")
        print("   4. 检查网络连接是否正常")
        print()
        print("📚 更多帮助: https://python-oracledb.readthedocs.io/")
        return False
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False
        
    finally:
        # 关闭连接
        if 'connection' in locals() and connection:
            connection.close()
            print("🔌 连接已关闭")


if __name__ == "__main__":
    print("=" * 60)
    print("Oracle 瘦模式连接测试")
    print("=" * 60)
    print()
    print("💡 提示：请在运行前修改代码中的数据库连接信息")
    print()
    
    success = test_oracle_thin_mode()
    
    print()
    print("=" * 60)
    if success:
        print("✅ 测试通过！")
    else:
        print("❌ 测试失败，请检查配置")
    print("=" * 60)
