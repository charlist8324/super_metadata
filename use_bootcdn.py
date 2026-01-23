"""
切换到 BootCDN 国内镜像
快速解决 CDN 加载慢或失败的问题
"""
from pathlib import Path
import re

TEMPLATES_DIR = Path(__file__).parent / 'templates'

# 替换规则：国外 CDN -> BootCDN 国内镜像
REPLACEMENTS = [
    # Bootstrap CSS
    (
        r'https://cdn\.jsdelivr\.net/npm/bootstrap@5\.3\.0/dist/css/bootstrap\.min\.css',
        'https://cdn.bootcdn.net/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css'
    ),
    # Bootstrap JS
    (
        r'https://cdn\.jsdelivr\.net/npm/bootstrap@5\.3\.0/dist/js/bootstrap\.bundle\.min\.js',
        'https://cdn.bootcdn.net/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js'
    ),
    # Chart.js
    (
        r'https://cdn\.jsdelivr\.net/npm/chart\.js@4\.4\.0/dist/chart\.umd\.min\.js',
        'https://cdn.bootcdn.net/ajax/libs/Chart.js/4.4.0/chart.umd.min.js'
    ),
    # Font Awesome (cdnjs -> BootCDN)
    (
        r'https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/6\.0\.0/css/all\.min\.css',
        'https://cdn.bootcdn.net/ajax/libs/font-awesome/6.4.0/css/all.min.css'
    ),
]


def update_template(file_path):
    """更新单个模板文件"""
    print(f"处理: {file_path.name}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    modified = False

    # 应用所有替换规则
    for pattern, replacement in REPLACEMENTS:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            print(f"  [替换] {pattern[:50]}... -> BootCDN")
            modified = True

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK] 已保存")
        return True
    else:
        print(f"  [SKIP] 无需更新")
        return False


def main():
    print("=" * 60)
    print("切换到 BootCDN 国内镜像...")
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
    print(f"完成！共更新 {updated_count}/{len(template_files)} 个文件")
    print("=" * 60)
    print()
    print("下一步：")
    print("1. 重启 Flask 应用")
    print("2. 刷新浏览器页面")
    print("3. 按 F12 检查资源加载状态")
    print()
    print("回退方法：")
    print("  使用 git 恢复原始模板：")
    print("  git checkout HEAD -- templates/")
    print("  或重新下载项目")


if __name__ == '__main__':
    main()
