"""
测试 Oracle 外键关系查询

用于验证外键关系查询 SQL 是否正确
"""

from sqlalchemy import create_engine, text
from urllib.parse import quote_plus


def test_oracle_foreign_key_query():
    """测试 Oracle 外键关系查询"""

    # 配置数据库连接信息 - 请替换为您的实际信息
    config = {
        'host': 'localhost',        # 替换为您的 Oracle 主机
        'port': 1521,              # 端口
        'username': 'your_username', # 替换为您的用户名
        'password': 'your_password', # 替换为您的密码
        'database': 'orcl'          # 替换为您的服务名或 SID
    }

    print("=" * 80)
    print("Oracle 外键关系查询测试")
    print("=" * 80)
    print()

    try:
        # 构建连接字符串
        encoded_username = quote_plus(config['username'])
        encoded_password = quote_plus(config['password'])
        encoded_database = quote_plus(config['database'])

        connection_string = (
            f"oracle+oracledb://{encoded_username}:{encoded_password}"
            f"@{config['host']}:{config['port']}/{encoded_database}"
        )

        print(f"连接字符串: oracle+oracledb://{config['username']}:****@{config['host']}:{config['port']}/{config['database']}")
        print()

        # 创建引擎
        engine = create_engine(connection_string)

        # 连接数据库
        print("正在连接数据库...")
        with engine.connect() as connection:
            print("✓ 连接成功！")
            print()

            # 测试查询 1：检查 user_constraints 结构
            print("1. 检查 user_constraints 视图结构...")
            query1 = text("""
                SELECT column_name
                FROM user_tab_columns
                WHERE table_name = 'USER_CONSTRAINTS'
                ORDER BY column_id
                FETCH FIRST 10 ROWS ONLY
            """)
            result1 = connection.execute(query1)
            columns1 = [row[0] for row in result1]
            print(f"   user_constraints 包含的字段（前10个）:")
            for col in columns1:
                print(f"     - {col}")
            print()

            # 测试查询 2：检查 user_cons_columns 结构
            print("2. 检查 user_cons_columns 视图结构...")
            query2 = text("""
                SELECT column_name
                FROM user_tab_columns
                WHERE table_name = 'USER_CONS_COLUMNS'
                ORDER BY column_id
                FETCH FIRST 10 ROWS ONLY
            """)
            result2 = connection.execute(query2)
            columns2 = [row[0] for row in result2]
            print(f"   user_cons_columns 包含的字段（前10个）:")
            for col in columns2:
                print(f"     - {col}")
            print()

            # 测试查询 3：获取外键约束数量
            print("3. 获取外键约束数量...")
            query3 = text("""
                SELECT COUNT(*) as fk_count
                FROM user_constraints
                WHERE constraint_type = 'R'
            """)
            result3 = connection.execute(query3).fetchone()
            print(f"   外键约束数量: {result3.fk_count}")
            print()

            if result3.fk_count > 0:
                # 测试查询 4：测试外键关系查询（修正后的版本）
                print("4. 测试外键关系查询（修正后的版本）...")
                query4 = text("""
                    SELECT
                        fk.constraint_name,
                        fk.table_name,
                        fk_col.column_name,
                        pk.table_name AS referenced_table_name,
                        pk_col.column_name AS referenced_column_name
                    FROM user_constraints fk
                    JOIN user_cons_columns fk_col 
                        ON fk.constraint_name = fk_col.constraint_name 
                        AND fk.table_name = fk_col.table_name
                    JOIN user_constraints pk 
                        ON fk.r_constraint_name = pk.constraint_name
                    JOIN user_cons_columns pk_col 
                        ON pk.constraint_name = pk_col.constraint_name 
                        AND pk.table_name = pk_col.table_name
                        AND fk_col.position = pk_col.position
                    WHERE fk.constraint_type = 'R'
                    FETCH FIRST 5 ROWS ONLY
                """)

                result4 = connection.execute(query4)
                print(f"   外键关系（前5个）:")
                for row in result4:
                    print(f"     - {row.table_name}.{row.column_name} -> {row.referenced_table_name}.{row.referenced_column_name}")
                    print(f"       约束名: {row.constraint_name}")
                print()
            else:
                print("   数据库中没有外键约束，跳过外键关系查询测试")
                print()

            print("=" * 80)
            print("✓ 所有测试完成！")
            print("=" * 80)

    except Exception as e:
        print(f"❌ 错误: {e}")
        print()
        print("提示：")
        print("  1. 请检查数据库连接信息是否正确")
        print("  2. 请确保 Oracle 数据库正在运行")
        print("  3. 请确保用户有查询权限")
        print()


if __name__ == "__main__":
    print("⚠️  注意：请先修改脚本中的数据库连接信息")
    print()
    print("需要修改的配置项：")
    print("  - host: Oracle 主机地址")
    print("  - port: Oracle 端口（默认 1521）")
    print("  - username: 数据库用户名")
    print("  - password: 数据库密码")
    print("  - database: 服务名或 SID（例如 orcl）")
    print()
    
    confirm = input("是否已修改配置并继续测试？(y/n): ")
    if confirm.lower() == 'y':
        test_oracle_foreign_key_query()
    else:
        print("测试已取消，请修改配置后重新运行。")
