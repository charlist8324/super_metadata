"""
下载前端依赖库到本地 static 目录
"""
import os
import urllib.request
import urllib.error
import zipfile
import shutil
from pathlib import Path

# 创建 libs 目录
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / 'static'
LIBS_DIR = STATIC_DIR / 'libs'

LIBS_DIR.mkdir(parents=True, exist_ok=True)

# 下载配置
DOWNLOADS = {
    'bootstrap': {
        'url': 'https://github.com/twbs/bootstrap/releases/download/v5.3.0/bootstrap-5.3.0-dist.zip',
        'target': LIBS_DIR / 'bootstrap',
        'extract': True,
        'paths': [
            'bootstrap-5.3.0-dist/css/bootstrap.min.css',
            'bootstrap-5.3.0-dist/css/bootstrap.css.map',
            'bootstrap-5.3.0-dist/js/bootstrap.bundle.min.js',
        ]
    },
    'fontawesome': {
        'url': 'https://use.fontawesome.com/releases/v6.0.0/fontawesome-free-6.0.0-web.zip',
        'target': LIBS_DIR / 'fontawesome',
        'extract': True,
        'paths': [
            'fontawesome-free-6.0.0-web/css/all.min.css',
            'fontawesome-free-6.0.0-web/css/all.css.map',
            'fontawesome-free-6.0.0-web/webfonts/*',
        ]
    },
    'chartjs': {
        'url': 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js',
        'target': LIBS_DIR / 'chartjs',
        'extract': False,
        'filename': 'chart.umd.min.js'
    }
}


def download_file(url, target_path):
    """下载文件"""
    print(f"下载: {url}")
    try:
        urllib.request.urlretrieve(url, target_path)
        print(f"  [OK] 下载完成: {target_path}")
        return True
    except urllib.error.URLError as e:
        print(f"  [FAIL] 下载失败: {e}")
        return False
    except Exception as e:
        print(f"  [ERROR] 错误: {e}")
        return False


def extract_zip(zip_path, target_dir, paths_to_copy):
    """解压 zip 文件并复制指定文件"""
    print(f"解压: {zip_path}")
    try:
        target_dir.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_path in paths_to_copy:
                try:
                    # 支持通配符
                    if '*' in file_path:
                        prefix = file_path.split('*')[0]
                        for file_name in zip_ref.namelist():
                            if file_name.startswith(prefix):
                                # 提取相对路径
                                rel_path = Path(file_name).relative_to(prefix.split('*')[0].split('/')[0])
                                output_path = target_dir / rel_path
                                output_path.parent.mkdir(parents=True, exist_ok=True)
                                with zip_ref.open(file_name) as source:
                                    with open(output_path, 'wb') as target:
                                        shutil.copyfileobj(source, target)
                                    print(f"  [OK] 提取: {rel_path}")
                    else:
                        # 提取单个文件
                        rel_path = Path(file_path).name
                        output_path = target_dir / rel_path
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        with zip_ref.open(file_path) as source:
                            with open(output_path, 'wb') as target:
                                shutil.copyfileobj(source, target)
                            print(f"  [OK] 提取: {rel_path}")
                except Exception as e:
                    print(f"  [WARN] 跳过 {file_path}: {e}")

        # 删除 zip 文件
        os.remove(zip_path)
        print(f"  [OK] 解压完成")
        return True
    except Exception as e:
        print(f"  [FAIL] 解压失败: {e}")
        return False


def main():
    print("=" * 60)
    print("开始下载前端依赖库...")
    print("=" * 60)
    print()

    for name, config in DOWNLOADS.items():
        print(f"\n【{name.upper()}】")

        if config['extract']:
            # 下载 zip 并解压
            zip_path = LIBS_DIR / f"{name}.zip"

            if not download_file(config['url'], zip_path):
                print(f"  [SKIP] 跳过 {name}")
                continue

            extract_zip(zip_path, config['target'], config['paths'])
        else:
            # 直接下载文件
            target_path = config['target'] / config['filename']
            target_path.parent.mkdir(parents=True, exist_ok=True)

            if not download_file(config['url'], target_path):
                print(f"  [SKIP] 跳过 {name}")
                continue

    print()
    print("=" * 60)
    print("下载完成！")
    print("=" * 60)
    print()
    print("目录结构:")
    print(f"  {STATIC_DIR}/")
    print(f"    css/")
    print(f"    js/")
    print(f"    libs/")
    print(f"      bootstrap/")
    print(f"        css/")
    print(f"        js/")
    print(f"      fontawesome/")
    print(f"        css/")
    print(f"        webfonts/")
    print(f"      chartjs/")
    print(f"        chart.umd.min.js")


if __name__ == '__main__':
    main()
