from functools import wraps
from flask import session, redirect, url_for, jsonify
from auth_models import User, UserRole, RolePermission, Permission
from db_config import db_config
import secrets
import hashlib
from datetime import datetime, timedelta


def generate_token():
    """生成随机令牌"""
    return secrets.token_urlsafe(32)


def hash_token(token):
    """对令牌进行哈希"""
    return hashlib.sha256(token.encode()).hexdigest()


def login_user(username, password):
    """
    用户登录
    返回: (success: bool, user_data: dict, error_message: str)
    """
    with db_config.get_session() as db_session:
        user = db_session.query(User).filter(
            (User.username == username) | (User.email == username),
            User.is_active == True
        ).first()
        
        if user and user.check_password(password):
            # 生成会话令牌
            session_token = generate_token()
            
            # 将用户信息存储到session
            session['user_id'] = user.id
            session['username'] = user.username
            session['logged_in'] = True
            session['session_token'] = session_token
            
            # 获取用户权限
            permissions = get_user_permissions(user.id)
            session['permissions'] = permissions
            
            return True, {
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
                'is_admin': user.is_admin,
                'permissions': permissions
            }, None
        
        return False, None, "用户名或密码错误"


def logout_user():
    """用户登出"""
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('logged_in', None)
    session.pop('session_token', None)
    session.pop('permissions', None)


def is_logged_in():
    """检查用户是否已登录"""
    return session.get('logged_in', False)


def get_current_user():
    """获取当前登录用户信息"""
    if not is_logged_in():
        return None
    
    user_id = session.get('user_id')
    with db_config.get_session() as db_session:
        user = db_session.query(User).filter(User.id == user_id).first()
        return user


def get_user_permissions(user_id):
    """
    获取用户的权限列表
    """
    permissions = []
    with db_config.get_session() as db_session:
        # 通过用户角色获取权限
        user_roles = db_session.query(UserRole).filter(UserRole.user_id == user_id).all()
        
        for user_role in user_roles:
            role_perms = db_session.query(RolePermission).filter(
                RolePermission.role_id == user_role.role_id
            ).all()
            
            for rp in role_perms:
                perm = db_session.query(Permission).filter(Permission.id == rp.permission_id).first()
                if perm:
                    permissions.append(perm.name)
    
    # 如果是管理员，添加所有权限
    user = db_session.query(User).filter(User.id == user_id).first()
    if user and user.is_admin:
        all_perms = db_session.query(Permission.name).all()
        all_perm_names = [p[0] for p in all_perms]
        permissions.extend(all_perm_names)
        permissions = list(set(permissions))  # 去重
    
    return permissions


def has_permission(permission_name):
    """
    检查当前用户是否拥有特定权限
    """
    if not is_logged_in():
        return False
    
    user_permissions = session.get('permissions', [])
    return permission_name in user_permissions or 'admin' in user_permissions


def login_required(f):
    """
    登录装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return jsonify({'error': '需要登录才能访问此资源'}), 401
        return f(*args, **kwargs)
    return decorated_function


def permission_required(permission_name):
    """
    权限装饰器
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not is_logged_in():
                return jsonify({'error': '需要登录才能访问此资源'}), 401
            if not has_permission(permission_name):
                return jsonify({'error': '权限不足'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def create_user(username, email, password, full_name=None, is_admin=False):
    """
    创建新用户
    """
    with db_config.get_session() as db_session:
        # 检查用户名或邮箱是否已存在
        existing_user = db_session.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            return False, "用户名或邮箱已存在"
        
        # 创建新用户
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            is_admin=is_admin
        )
        user.set_password(password)
        
        db_session.add(user)
        db_session.commit()
        
        # 分配默认角色（普通用户）
        if not is_admin:
            default_role = db_session.query(Role).filter(Role.name == 'viewer').first()
            if default_role:
                user_role = UserRole(user_id=user.id, role_id=default_role.id)
                db_session.add(user_role)
                db_session.commit()
        else:
            # 管理员分配管理员角色
            admin_role = db_session.query(Role).filter(Role.name == 'admin').first()
            if admin_role:
                user_role = UserRole(user_id=user.id, role_id=admin_role.id)
                db_session.add(user_role)
                db_session.commit()
        
        return True, "用户创建成功"


def assign_role_to_user(user_id, role_name):
    """
    为用户分配角色
    """
    with db_config.get_session() as db_session:
        role = db_session.query(Role).filter(Role.name == role_name).first()
        if not role:
            return False, "角色不存在"
        
        # 检查是否已有此角色
        existing = db_session.query(UserRole).filter(
            UserRole.user_id == user_id,
            UserRole.role_id == role.id
        ).first()
        
        if existing:
            return False, "用户已有此角色"
        
        user_role = UserRole(user_id=user_id, role_id=role.id)
        db_session.add(user_role)
        db_session.commit()
        
        return True, "角色分配成功"


def remove_role_from_user(user_id, role_name):
    """
    从用户移除角色
    """
    with db_config.get_session() as db_session:
        role = db_session.query(Role).filter(Role.name == role_name).first()
        if not role:
            return False, "角色不存在"
        
        user_role = db_session.query(UserRole).filter(
            UserRole.user_id == user_id,
            UserRole.role_id == role.id
        ).first()
        
        if not user_role:
            return False, "用户没有此角色"
        
        db_session.delete(user_role)
        db_session.commit()
        
        return True, "角色移除成功"