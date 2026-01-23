"""
统一所有页面的导航菜单顺序
"""
from pathlib import Path
import re

TEMPLATES_DIR = Path(__file__).parent / 'templates'

# 正确的导航菜单顺序
CORRECT_NAV = """<ul class="navbar-nav ms-auto" id="mainNavMenu">
                    <li class="nav-item">
                        <a class="nav-link" href="/">
                            <i class="fas fa-home me-1"></i>首页
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/dashboard">
                            <i class="fas fa-chart-line me-1"></i>资源概览
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/etl">
                            <i class="fas fa-sync-alt me-1"></i>ETL任务
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/data-sources">
                            <i class="fas fa-server me-1"></i>数据源管理
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/metadata">
                            <i class="fas fa-table me-1"></i>元数据浏览
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/history">
                            <i class="fas fa-history me-1"></i>抽取历史
                        </a>
                    </li>
                    <li class="nav-item" id="userManageNav">
                        <a class="nav-link" href="/users">
                            <i class="fas fa-users me-1"></i>用户管理
                        </a>
                    </li>
                </ul>"""


def get_page_active_class(filename):
    """根据页面文件名获取active类"""
    active_map = {
        'index.html': ('/', '首页'),
        'dashboard.html': ('/dashboard', '资源概览'),
        'etl.html': ('/etl', 'ETL任务'),
        'data_sources.html': ('/data-sources', '数据源管理'),
        'metadata.html': ('/metadata', '元数据浏览'),
        'history.html': ('/history', '抽取历史'),
        'users.html': ('/users', '用户管理'),
    }
    return active_map.get(filename, (None, None))


def fix_navbar_menu(file_path):
    """修复导航菜单"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 获取当前页面应该高亮的菜单项
    filename = file_path.name
    href, name = get_page_active_class(filename)

    if href is None:
        print(f"[SKIP] {filename} (无需修复)")
        return False

    # 替换导航菜单
    new_nav = CORRECT_NAV

    # 为当前页面添加 active 类
    if name in new_nav:
        new_nav = new_nav.replace(f'href="{href}"', f'href="{href}" class="nav-link active"')

    # 查找导航菜单的开始和结束
    start_pattern = r'<ul class="navbar-nav ms-auto" id="mainNavMenu">'
    end_pattern = r'</ul>\s*<ul class="navbar-nav ms-auto d-none" id="userMenu">'

    # 检查是否包含正确的导航菜单结构
    if start_pattern in content and end_pattern in content:
        # 提取导航菜单部分
        start_idx = content.find(start_pattern)
        end_idx = content.find(end_pattern, start_idx)

        if start_idx != -1 and end_idx != -1:
            # 替换导航菜单
            old_nav = content[start_idx:end_idx]
            new_content = content[:start_idx] + new_nav + content[end_idx:]

            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"[OK] {filename} (高亮: {name})")
            return True
        else:
            print(f"[WARN] {filename} (未找到导航菜单结构)")
            return False
    else:
        print(f"[WARN] {filename} (导航菜单结构不匹配)")
        return False


def main():
    print("=" * 60)
    print("统一所有页面的导航菜单顺序...")
    print("=" * 60)
    print()
    print("正确顺序:")
    print("1. 首页")
    print("2. 资源概览")
    print("3. ETL任务")
    print("4. 数据源管理")
    print("5. 元数据浏览")
    print("6. 抽取历史")
    print("7. 用户管理")
    print()
    print("=" * 60)
    print()

    # 处理所有HTML文件
    html_files = list(TEMPLATES_DIR.glob('*.html'))

    updated_count = 0
    for html_file in html_files:
        if html_file.name in ['login.html', 'cdn_assets.html']:
            continue

        if fix_navbar_menu(html_file):
            updated_count += 1

    print()
    print("=" * 60)
    print(f"完成！共更新 {updated_count} 个文件")
    print("=" * 60)
    print()
    print("下一步:")
    print("1. 清除浏览器缓存 (Ctrl + Shift + Delete)")
    print("2. 强制刷新页面 (Ctrl + F5)")
    print("3. 检查导航菜单顺序是否一致")


if __name__ == '__main__':
    main()
