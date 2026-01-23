"""
批量替换系统名称

将所有文件中的"Super MetaData 元数据管理系统"替换为"Super MetaData Super MetaData 元数据管理系统"
"""

import os
import glob

def replace_system_name():
    """批量替换系统名称"""
    
    # 需要替换的文件模式
    file_patterns = [
        '*.html',           # HTML 模板文件
        '*.js',             # JavaScript 文件
        '*.py',             # Python 文件
        '*.sql',            # SQL 文件
        '*.md',             # Markdown 文件
        'LICENSE'           # 许可证文件
    ]
    
    # 旧名称和新名称
    old_name = 'Super MetaData 元数据管理系统'
    new_name = 'Super MetaData Super MetaData 元数据管理系统'
    
    # 需要处理的目录
    directories = [
        '.',                 # 根目录
        'templates',         # 模板目录
        'static/js',         # JavaScript 目录
    ]
    
    replaced_files = []
    skipped_files = []
    
    for directory in directories:
        if not os.path.exists(directory):
            continue
        
        for pattern in file_patterns:
            # 查找匹配的文件
            files = glob.glob(os.path.join(directory, pattern))
            
            for file_path in files:
                try:
                    # 读取文件内容
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 检查是否包含旧名称
                    if old_name in content:
                        # 替换
                        new_content = content.replace(old_name, new_name)
                        
                        # 写回文件
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        replaced_files.append(file_path)
                        print(f"[OK] {file_path}")
                    else:
                        skipped_files.append(file_path)
                        
                except Exception as e:
                    print(f"[ERROR] {file_path}: {e}")
    
    # 输出统计信息
    print()
    print("=" * 80)
    print("系统名称替换完成")
    print("=" * 80)
    print(f"替换文件数量: {len(replaced_files)}")
    print(f"跳过文件数量: {len(skipped_files)}")
    print()
    
    if replaced_files:
        print("已替换的文件：")
        for file_path in replaced_files:
            print(f"  - {file_path}")
        print()
    
    print(f"旧名称: {old_name}")
    print(f"新名称: {new_name}")
    print()
    print("=" * 80)


if __name__ == "__main__":
    replace_system_name()
