"""
下载 Font Awesome 字体文件
"""
import os
import urllib.request
from pathlib import Path

# 创建 webfonts 目录
WEBFONTS_DIR = Path(__file__).parent / 'static' / 'libs' / 'fontawesome' / 'webfonts'
WEBFONTS_DIR.mkdir(parents=True, exist_ok=True)

# Font Awesome 6.0.0 字体文件
# GitHub releases 链接
FONTS_ZIP_URL = "https://github.com/FortAwesome/Font-Awesome/releases/download/6.0.0/fontawesome-free-6.0.0-web.zip"

# 字体文件列表（从 zip 中提取）
FONT_FILES = [
    'fa-solid-900.woff2',
    'fa-regular-400.woff2',
    'fa-brands-400.woff2',
    'fa-v4compatibility.ttf'  # 兼容性字体
]


def download_zip():
    """下载 zip 文件"""
    print(f"下载 Font Awesome 6.0.0...")
    print(f"URL: {FONTS_ZIP_URL}")

    zip_path = Path(__file__).parent / 'fontawesome-web.zip'

    try:
        urllib.request.urlretrieve(FONTS_ZIP_URL, zip_path)
        print(f"[OK] 下载完成: {zip_path.name}")
        print(f"    大小: {os.path.getsize(zip_path)} 字节")
        return zip_path
    except Exception as e:
        print(f"[FAIL] 下载失败: {e}")
        return None


def extract_fonts(zip_path):
    """提取字体文件"""
    import zipfile

    print()
    print("提取字体文件...")

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 列出 zip 中的文件
            all_files = zip_ref.namelist()

            # 查找并提取字体文件
            extracted_count = 0
            for font_file in FONT_FILES:
                # 在 zip 中查找字体文件
                for zip_file in all_files:
                    if zip_file.endswith(font_file):
                        # 提取文件
                        with zip_ref.open(zip_file) as source:
                            output_path = WEBFONTS_DIR / font_file
                            with open(output_path, 'wb') as target:
                                target.write(source.read())
                            print(f"[OK] {font_file}")
                            extracted_count += 1
                            break

        print(f"[OK] 共提取 {extracted_count} 个字体文件")

        # 删除 zip 文件
        os.remove(zip_path)
        print(f"[OK] 已删除 zip 文件")

        return extracted_count > 0

    except Exception as e:
        print(f"[FAIL] 提取失败: {e}")
        return False


def main():
    print("=" * 60)
    print("下载 Font Awesome 字体文件")
    print("=" * 60)
    print()

    # 下载 zip 文件
    zip_path = download_zip()
    if not zip_path:
        print()
        print("[ERROR] 下载失败，请手动下载")
        print()
        print("手动下载步骤：")
        print("1. 访问: " + FONTS_ZIP_URL)
        print("2. 解压 zip 文件")
        print("3. 复制 webfonts/ 目录下的所有文件到:")
        print(f"   {WEBFONTS_DIR}")
        return

    # 提取字体文件
    success = extract_fonts(zip_path)

    print()
    print("=" * 60)
    if success:
        print("下载完成！")
    else:
        print("下载失败！")
    print("=" * 60)
    print()

    if success:
        print("下一步：")
        print("1. 刷新浏览器页面")
        print("2. 检查图标是否正常显示")


if __name__ == '__main__':
    main()
