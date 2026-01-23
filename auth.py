"""
用户认证和权限管理模块
"""
from functools import wraps
from flask import session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db_manager import get_db_session
from sqlalchemy import text
from datetime import datetime
from exceptions import AuthenticationException, AuthorizationException
import logging


class User:
    """用户类"""
    def __init__(self, id=None, username=None, email=None, password_hash=None, 
                 full_name=None, role='user', is_active=True, created_at=None, last_login=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.full_name = full_name
        self.role = role  # admin, user, viewer
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.last_login = last_login
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }


def init_auth_tables():
    """初始化认证相关的数据库表（兼容MySQL和SQLite）"""
    try:
        with get_db_session() as session:
            # 检查数据库类型
            engine_dialect = str(session.bind.dialect.name).lower()
            
            if engine_dialect == 'mysql':
                # MySQL语法
                session.execute(text("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(100) UNIQUE NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        full_name VARCHAR(255),
                        role VARCHAR(20) DEFAULT 'user',
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        last_login DATETIME DEFAULT NULL
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """))
            else:
                # SQLite语法
                session.execute(text("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username VARCHAR(100) UNIQUE NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        full_name VARCHAR(255),
                        role VARCHAR(20) DEFAULT 'user',
                        is_active BOOLEAN DEFAULT 1,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        last_login DATETIME
                    )
                """))
            
            session.commit()
            
            # 检查是否有admin用户，如果没有则创建默认管理员
            result = session.execute(text("SELECT COUNT(*) FROM users WHERE username = 'admin'")).fetchone()
            if result[0] == 0:
                admin_password_hash = generate_password_hash('admin123')
                session.execute(text("""
                    INSERT INTO users (username, email, password_hash, full_name, role, is_active)
                    VALUES ('admin', 'admin@example.com', :password, '系统管理员', 'admin', 1)
                """), {'password': admin_password_hash})
                session.commit()
                print("默认管理员账户已创建: admin / admin123")
    except Exception as e:
        logging.error(f"初始化认证表失败: {str(e)}")
        raise AuthenticationException(f"初始化认证表失败: {str(e)}")


def get_user_by_username(username):
    """根据用户名获取用户"""
    try:
        with get_db_session() as session:
            result = session.execute(
                text("SELECT * FROM users WHERE username = :username OR email = :username"),
                {'username': username}
            ).fetchone()
            
            if result:
                return User(
                    id=result[0],
                    username=result[1],
                    email=result[2],
                    password_hash=result[3],
                    full_name=result[4],
                    role=result[5],
                    is_active=bool(result[6]),
                    created_at=result[7],
                    last_login=result[8]
                )
            return None
    except Exception as e:
        logging.error(f"查询用户失败: {str(e)}")
        raise AuthenticationException(f"查询用户失败: {str(e)}")


def get_user_by_id(user_id):
    """根据ID获取用户"""
    try:
        with get_db_session() as session:
            result = session.execute(
                text("SELECT * FROM users WHERE id = :id"),
                {'id': user_id}
            ).fetchone()
            
            if result:
                return User(
                    id=result[0],
                    username=result[1],
                    email=result[2],
                    password_hash=result[3],
                    full_name=result[4],
                    role=result[5],
                    is_active=bool(result[6]),
                    created_at=result[7],
                    last_login=result[8]
                )
            return None
    except Exception as e:
        logging.error(f"查询用户失败: {str(e)}")
        raise AuthenticationException(f"查询用户失败: {str(e)}")


def login_user(username, password):
    """
    用户登录
    返回: (success, user_data, error_message)
    """
    try:
        user = get_user_by_username(username)
        
        if not user:
            return False, None, '用户名或密码错误'
        
        if not user.is_active:
            return False, None, '账户已被禁用'
        
        if not user.check_password(password):
            return False, None, '用户名或密码错误'
        
        # 更新最后登录时间
        with get_db_session() as db_session:
            db_session.execute(
                text("UPDATE users SET last_login = :now WHERE id = :id"),
                {'now': datetime.utcnow(), 'id': user.id}
            )
            db_session.commit()
        
        # 将用户ID存入session
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        session.permanent = True  # 设置session为永久性
        
        return True, user.to_dict(), None
    except Exception as e:
        logging.error(f"登录失败: {str(e)}")
        return False, None, f'登录失败: {str(e)}'


def logout_user():
    """用户登出"""
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)


def get_current_user():
    """获取当前登录用户"""
    user_id = session.get('user_id')
    if user_id:
        return get_user_by_id(user_id)
    return None


def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': '请先登录', 'error_code': 'AUTH_REQUIRED'}), 401
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """管理员权限验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': '请先登录', 'error_code': 'AUTH_REQUIRED'}), 401
        if session.get('role') != 'admin':
            return jsonify({'error': '需要管理员权限', 'error_code': 'INSUFFICIENT_PERMISSIONS'}), 403
        return f(*args, **kwargs)
    return decorated_function


def has_permission(permission):
    """检查当前用户是否有指定权限"""
    role = session.get('role')
    
    # 权限映射
    permissions = {
        'admin': ['view', 'edit', 'delete', 'admin', 'manage_users', 'manage_datasources', 'manage_etl'],
        'user': ['view', 'edit', 'manage_datasources', 'manage_etl'],
        'viewer': ['view']
    }
    
    if role and permission in permissions.get(role, []):
        return True
    return False


def permission_required(permission):
    """权限验证装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': '请先登录', 'error_code': 'AUTH_REQUIRED'}), 401
            if not has_permission(permission):
                return jsonify({'error': '权限不足', 'error_code': 'INSUFFICIENT_PERMISSIONS'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# 用户管理函数
def create_user(username, email, password, full_name=None, role='user'):
    """创建新用户"""
    try:
        # 检查用户名是否已存在
        existing_user = get_user_by_username(username)
        if existing_user:
            return False, '用户名已存在'
        
        password_hash = generate_password_hash(password)
        
        with get_db_session() as db_session:
            db_session.execute(text("""
                INSERT INTO users (username, email, password_hash, full_name, role, is_active)
                VALUES (:username, :email, :password, :full_name, :role, 1)
            """), {
                'username': username,
                'email': email,
                'password': password_hash,
                'full_name': full_name or username,
                'role': role
            })
            db_session.commit()
            return True, '用户创建成功'
    except Exception as e:
        logging.error(f"创建用户失败: {str(e)}")
        return False, f'创建用户失败: {str(e)}'


def update_user(user_id, **kwargs):
    """更新用户信息"""
    try:
        allowed_fields = ['email', 'full_name', 'role', 'is_active']
        updates = []
        params = {'id': user_id}
        
        for field in allowed_fields:
            if field in kwargs:
                updates.append(f"{field} = :{field}")
                params[field] = kwargs[field]
        
        if 'password' in kwargs and kwargs['password']:
            password_hash = generate_password_hash(kwargs['password'])
            updates.append("password_hash = :password_hash")
            params['password_hash'] = password_hash
        
        if not updates:
            return False, '没有要更新的字段'
        
        with get_db_session() as db_session:
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = :id"
            db_session.execute(text(query), params)
            db_session.commit()
            return True, '用户更新成功'
    except Exception as e:
        logging.error(f"更新用户失败: {str(e)}")
        return False, f'更新用户失败: {str(e)}'


def delete_user(user_id):
    """删除用户"""
    try:
        with get_db_session() as db_session:
            db_session.execute(text("DELETE FROM users WHERE id = :id"), {'id': user_id})
            db_session.commit()
            return True, '用户删除成功'
    except Exception as e:
        logging.error(f"删除用户失败: {str(e)}")
        return False, f'删除用户失败: {str(e)}'


def change_user_password(user_id, current_password, new_password):
    """修改用户密码"""
    try:
        with get_db_session() as db_session:
            # 获取用户信息
            result = db_session.execute(
                text("SELECT password_hash FROM users WHERE id = :id"),
                {'id': user_id}
            ).fetchone()

            if not result:
                return False, '用户不存在'

            # 验证当前密码
            if not check_password_hash(result[0], current_password):
                return False, '当前密码错误'

            # 更新密码
            new_password_hash = generate_password_hash(new_password)
            db_session.execute(
                text("UPDATE users SET password_hash = :password_hash WHERE id = :id"),
                {'password_hash': new_password_hash, 'id': user_id}
            )
            db_session.commit()

            return True, '密码修改成功'
    except Exception as e:
        logging.error(f"修改密码失败: {str(e)}")
        return False, f'修改密码失败: {str(e)}'


def get_all_users():
    """获取所有用户"""
    try:
        with get_db_session() as session:
            results = session.execute(text("SELECT * FROM users ORDER BY id")).fetchall()
            users = []
            for result in results:
                user = User(
                    id=result[0],
                    username=result[1],
                    email=result[2],
                    password_hash=result[3],
                    full_name=result[4],
                    role=result[5],
                    is_active=bool(result[6]),
                    created_at=result[7],
                    last_login=result[8]
                )
                users.append(user.to_dict())
            return users
    except Exception as e:
        logging.error(f"获取用户列表失败: {str(e)}")
        raise AuthenticationException(f"获取用户列表失败: {str(e)}")