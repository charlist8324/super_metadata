from db_manager import init_db_manager, get_db_session
from auth import create_user, get_user_by_username
from config import Config

def create_default_admin():
    """创建默认管理员账户"""
    init_db_manager(Config.DATABASE_URL)
    
    with get_db_session() as session:
        # 检查是否已有admin用户
        admin_user = get_user_by_username('admin')
        
        if admin_user:
            print("默认管理员账户已存在:")
            print(f"用户名: admin")
            print(f"邮箱: {admin_user.email}")
            print(f"角色: {admin_user.role}")
            return
        
        # 创建默认管理员
        success, message = create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            full_name='系统管理员',
            role='admin'
        )
        
        if success:
            print("默认管理员账户创建成功!")
            print(f"用户名: admin")
            print(f"密码: admin123")
            print(f"邮箱: admin@example.com")
            print(f"角色: admin")
        else:
            print(f"创建管理员账户失败: {message}")

if __name__ == '__main__':
    create_default_admin()