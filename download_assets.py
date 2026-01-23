"""
手动下载前端资源到本地
"""
import os
import urllib.request
import urllib.error
from pathlib import Path

# 创建目录
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / 'static'
LIBS_DIR = STATIC_DIR / 'libs'

# 创建目录结构
dirs_to_create = [
    LIBS_DIR / 'bootstrap' / 'css',
    LIBS_DIR / 'bootstrap' / 'js',
    LIBS_DIR / 'fontawesome' / 'css',
    LIBS_DIR / 'fontawesome' / 'webfonts',
    LIBS_DIR / 'chartjs'
]

for d in dirs_to_create:
    d.mkdir(parents=True, exist_ok=True)

# 下载配置
DOWNLOADS = [
    {
        'name': 'Bootstrap CSS',
        'url': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
        'path': LIBS_DIR / 'bootstrap' / 'css' / 'bootstrap.min.css'
    },
    {
        'name': 'Bootstrap JS',
        'url': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
        'path': LIBS_DIR / 'bootstrap' / 'js' / 'bootstrap.bundle.min.js'
    },
    {
        'name': 'Font Awesome CSS',
        'url': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
        'path': LIBS_DIR / 'fontawesome' / 'css' / 'all.min.css'
    },
    {
        'name': 'Chart.js',
        'url': 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js',
        'path': LIBS_DIR / 'chartjs' / 'chart.umd.min.js'
    }
]


def download_file(url, path):
    """下载文件"""
    print(f"[下载] {url}")
    try:
        urllib.request.urlretrieve(url, path)
        file_size = os.path.getsize(path)
        print(f"[完成] {path.name}")
        print(f"       大小: {file_size} 字节")
        return True
    except Exception as e:
        print(f"[失败] {e}")
        return False


def main():
    print("=" * 60)
    print("开始下载前端资源到本地...")
    print("=" * 60)
    print()

    success_count = 0
    total_count = len(DOWNLOADS)

    for item in DOWNLOADS:
        print(f"\n{item['name']}")
        print("-" * 60)

        if download_file(item['url'], item['path']):
            success_count += 1
        else:
            print(f"[警告] {item['name']} 下载失败，请手动下载")

    print()
    print("=" * 60)
    print(f"下载完成！成功: {success_count}/{total_count}")
    print("=" * 60)
    print()

    # Font Awesome 字体文件说明
    print("注意：Font Awesome 的字体文件（webfonts）需要单独下载")
    print("下载链接：https://use.fontawesome.com/releases/v6.0.0/fontawesome-free-6.0.0-web.zip")
    print("解压后将 webfonts/ 目录下的所有文件复制到 static/libs/fontawesome/webfonts/")
    print()
    print("如果不需要图标，可以先使用 CSS 文件（图标可能无法显示）")
    print()

    print("下一步：")
    print("1. 运行 python update_templates.py 更新模板引用")
    print("2. 重启 Flask 应用")
    print("3. 刷新浏览器页面")


if __name__ == '__main__':
    main()
