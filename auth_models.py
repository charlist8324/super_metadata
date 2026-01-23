from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import db_config
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联角色
    roles = relationship("UserRole", back_populates="user")
    
    def set_password(self, password):
        """设置密码哈希"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """检查密码是否正确"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)  # 如 'admin', 'viewer', 'editor'
    description = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联用户
    users = relationship("UserRole", back_populates="role")
    # 关联权限
    permissions = relationship("RolePermission", back_populates="role")


class UserRole(Base):
    __tablename__ = 'user_roles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")


class Permission(Base):
    __tablename__ = 'permissions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)  # 如 'view_metadata', 'manage_data_sources', 'manage_users'
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联角色
    roles = relationship("RolePermission", back_populates="permission")


class RolePermission(Base):
    __tablename__ = 'role_permissions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    permission_id = Column(Integer, ForeignKey('permissions.id'), nullable=False)
    granted_at = Column(DateTime, default=datetime.utcnow)
    
    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")


def init_auth_tables():
    """初始化认证相关的表"""
    engine = db_config.init_db()
    Base.metadata.create_all(bind=engine)
    
    # 创建默认角色
    with db_config.get_session() as session:
        # 检查是否已有角色
        existing_roles = session.query(Role).count()
        if existing_roles == 0:
            # 创建默认角色
            admin_role = Role(name='admin', description='管理员角色，拥有所有权限')
            viewer_role = Role(name='viewer', description='查看者角色，只能查看元数据')
            editor_role = Role(name='editor', description='编辑者角色，可以管理数据源和元数据')
            
            session.add_all([admin_role, viewer_role, editor_role])
            session.commit()
            
            # 创建默认权限
            permissions = [
                Permission(name='view_metadata', description='查看元数据'),
                Permission(name='manage_metadata', description='管理元数据'),
                Permission(name='view_data_sources', description='查看数据源'),
                Permission(name='manage_data_sources', description='管理数据源'),
                Permission(name='view_extraction_history', description='查看抽取历史'),
                Permission(name='manage_extraction_tasks', description='管理抽取任务'),
                Permission(name='manage_users', description='管理用户'),
                Permission(name='manage_roles', description='管理角色'),
            ]
            
            session.add_all(permissions)
            session.commit()
            
            # 为管理员角色分配所有权限
            admin_role = session.query(Role).filter(Role.name == 'admin').first()
            all_permissions = session.query(Permission).all()
            
            for perm in all_permissions:
                role_perm = RolePermission(role_id=admin_role.id, permission_id=perm.id)
                session.add(role_perm)
            
            session.commit()


if __name__ == '__main__':
    init_auth_tables()