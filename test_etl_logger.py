"""
ETL日志测试脚本

用于测试ETL日志记录功能
"""

from etl_logger import ETLLogger


def test_etl_logger():
    """测试ETL日志记录器"""
    
    print("=" * 80)
    print("ETL日志功能测试")
    print("=" * 80)
    print()
    
    # 测试1：记录抽数开始
    print("1. 测试记录抽数开始...")
    ETLLogger.log_extraction_start(
        source_id=1,
        source_name="MySQL_Test",
        source_type="mysql"
    )
    print("[OK] 完成")
    print()
    
    # 测试2：记录连接成功
    print("2. 测试记录连接成功...")
    ETLLogger.log_connection_success(
        source_name="MySQL_Test",
        source_type="mysql"
    )
    print("[OK] 完成")
    print()
    
    # 测试3：记录表抽取
    print("3. 测试记录表抽取...")
    ETLLogger.log_table_extracted(
        table_name="users",
        row_count=1000,
        size_bytes=524288,  # 512KB
        duration=0.12
    )
    ETLLogger.log_column_extracted(table_name="users", column_count=5)
    print("[OK] 完成")
    print()
    
    # 测试4：记录另一个表抽取
    print("4. 测试记录另一个表抽取...")
    ETLLogger.log_table_extracted(
        table_name="orders",
        row_count=5000,
        size_bytes=1048576,  # 1MB
        duration=0.25
    )
    ETLLogger.log_column_extracted(table_name="orders", column_count=8)
    print("[OK] 完成")
    print()
    
    # 测试5：记录表抽取失败
    print("5. 测试记录表抽取失败...")
    ETLLogger.log_table_failed(
        table_name="temp_table",
        error_msg="Table 'db.temp_table' doesn't exist"
    )
    print("[OK] 完成")
    print()
    
    # 测试6：记录关联关系
    print("6. 测试记录关联关系...")
    ETLLogger.log_relationship_extracted(
        constraint_name="fk_orders_user_id",
        table_name="orders",
        ref_table_name="users"
    )
    print("[OK] 完成")
    print()
    
    # 测试7：记录清除旧数据
    print("7. 测试记录清除旧数据...")
    ETLLogger.log_clear_old_metadata(
        source_id=1,
        tables_count=25
    )
    print("[OK] 完成")
    print()
    
    # 测试8：记录保存元数据
    print("8. 测试记录保存元数据...")
    ETLLogger.log_save_metadata(
        source_id=1,
        tables_count=2,
        columns_count=13,
        relationships_count=1
    )
    print("[OK] 完成")
    print()
    
    # 测试9：记录抽数成功
    print("9. 测试记录抽数成功...")
    ETLLogger.log_extraction_success(
        source_id=1,
        tables_count=2,
        relationships_count=1,
        duration=3.45
    )
    print("[OK] 完成")
    print()
    
    # 测试10：记录汇总
    print("10. 测试记录汇总...")
    ETLLogger.log_summary(
        total_tables=3,
        success_tables=2,
        failed_tables=1
    )
    print("[OK] 完成")
    print()
    
    print("=" * 80)
    print("所有测试完成！")
    print("=" * 80)
    print()
    print("请查看日志文件：logs/etl.log")
    print()


if __name__ == "__main__":
    test_etl_logger()
