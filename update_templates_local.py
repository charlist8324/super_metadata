"""
更新模板文件中的 CDN 引用为本地路径
"""
import os
from pathlib import Path
import re

# 模板目录
TEMPLATES_DIR = Path(__file__).parent / 'templates'

# 替换规则：CDN -> 本地路径
REPLACEMENTS = [
    # Bootstrap CSS
    (
        r'https://cdn\.jsdelivr\.net/npm/bootstrap@5\.3\.0/dist/css/bootstrap\.min\.css',
        "{{ url_for('static', filename='libs/bootstrap/css/bootstrap.min.css') }}"
    ),
    # Bootstrap JS
    (
        r'https://cdn\.jsdelivr\.net/npm/bootstrap@5\.3\.0/dist/js/bootstrap\.bundle\.min\.js',
        "{{ url_for('static', filename='libs/bootstrap/js/bootstrap.bundle.min.js') }}"
    ),
    # Font Awesome CSS
    (
        r'https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/6\.0\.0/css/all\.min\.css',
        "{{ url_for('static', filename='libs/fontawesome/css/all.min.css') }}"
    ),
    # Chart JS
    (
        r'https://cdn\.jsdelivr\.net/npm/chart\.js@4\.4\.0/dist/chart\.umd\.min\.js',
        "{{ url_for('static', filename='libs/chartjs/chart.umd.min.js') }}"
    ),
    # Bootcdn Bootstrap CSS (login.html 使用)
    (
        r'https://cdn\.bootcdn\.net/ajax/libs/bootstrap/5\.3\.0/css/bootstrap\.min\.css',
        "{{ url_for('static', filename='libs/bootstrap/css/bootstrap.min.css') }}"
    ),
    # Bootcdn Bootstrap JS
    (
        r'https://cdn\.bootcdn\.net/ajax/libs/bootstrap/5\.3\.0/js/bootstrap\.bundle\.min\.js',
        "{{ url_for('static', filename='libs/bootstrap/js/bootstrap.bundle.min.js') }}"
    ),
    # Bootcdn Font Awesome
    (
        r'https://cdn\.bootcdn\.net/ajax/libs/font-awesome/6\.4\.0/css/all\.min\.css',
        "{{ url_for('static', filename='libs/fontawesome/css/all.min.css') }}"
    ),
]


def update_template(file_path):
    """更新单个模板文件"""
    print(f"处理: {file_path.name}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 应用所有替换规则
    for pattern, replacement in REPLACEMENTS:
        content = re.sub(pattern, replacement, content)

    # 检查是否有修改
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK] 已更新")
        return True
    else:
        print(f"  [SKIP] 无需更新")
        return False


def main():
    print("=" * 60)
    print("开始更新模板文件中的 CDN 引用...")
    print("=" * 60)
    print()

    # 获取所有 HTML 模板文件
    template_files = list(TEMPLATES_DIR.glob('*.html'))

    if not template_files:
        print("[ERROR] 未找到模板文件")
        return

    updated_count = 0
    for template_file in template_files:
        if update_template(template_file):
            updated_count += 1
        print()

    print("=" * 60)
    print(f"更新完成！共更新 {updated_count}/{len(template_files)} 个文件")
    print("=" * 60)
    print()
    print("下一步:")
    print("1. 重启 Flask 应用")
    print("2. 刷新浏览器页面")
    print("3. 按 F12 检查资源加载状态")


if __name__ == '__main__':
    main()
