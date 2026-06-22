"""自动下载并配置libvips Windows预编译包"""
import os
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path


# libvips配置
LIBVIPS_VERSION = "8.15.5"  # 可以修改为最新版本
LIBVIPS_FILENAME = f"vips-dev-w64-all-{LIBVIPS_VERSION}.zip"
LIBVIPS_URL = f"https://github.com/libvips/libvips/releases/download/v{LIBVIPS_VERSION}/{LIBVIPS_FILENAME}"
LIBVIPS_DIR = Path("libs/libvips")


def download_file(url, dest_path, chunk_size=8192):
    """
    下载文件并显示进度。
    
    Args:
        url: 下载URL
        dest_path: 目标路径
        chunk_size: 每次读取的块大小
    """
    try:
        with urllib.request.urlopen(url) as response:
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded = 0
            
            with open(dest_path, 'wb') as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"\r下载进度: {progress:.1f}% ({downloaded}/{total_size} bytes)", end='')
                    else:
                        print(f"\r已下载: {downloaded} bytes", end='')
            
            print()  # 换行
            return True
    except Exception as e:
        print(f"\n下载失败: {e}")
        return False


def download_libvips():
    """下载libvips Windows预编译包"""
    print("=" * 60)
    print(f"正在下载libvips {LIBVIPS_VERSION}...")
    print(f"URL: {LIBVIPS_URL}")
    print("=" * 60)
    
    # 创建临时目录
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    zip_file = temp_dir / LIBVIPS_FILENAME
    
    # 下载文件
    print("\n1. 下载libvips压缩包...")
    if not download_file(LIBVIPS_URL, zip_file):
        return False
    
    print(f"✓ 下载完成: {zip_file}")
    print(f"  文件大小: {zip_file.stat().st_size / (1024*1024):.2f} MB")
    
    # 解压文件
    print("\n2. 解压文件...")
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # 解压到临时目录
            extract_dir = temp_dir / "extract"
            extract_dir.mkdir(exist_ok=True)
            
            # 显示解压进度
            members = zip_ref.namelist()
            total = len(members)
            
            for i, member in enumerate(members, 1):
                zip_ref.extract(member, extract_dir)
                if i % 50 == 0 or i == total:
                    print(f"\r解压进度: {i}/{total} 文件", end='')
            
            print()  # 换行
        
        print("✓ 解压完成")
        
        # 查找vips-dev目录
        vips_dirs = list(extract_dir.glob("vips-dev-*"))
        if not vips_dirs:
            print("✗ 错误: 未找到vips-dev目录")
            return False
            
        vips_root = vips_dirs[0]
        print(f"  找到libvips目录: {vips_root.name}")
        
        # 创建目标目录
        print("\n3. 安装libvips...")
        LIBVIPS_DIR.mkdir(parents=True, exist_ok=True)
        
        # 复制bin目录
        src_bin = vips_root / "bin"
        dest_bin = LIBVIPS_DIR / "bin"
        
        if src_bin.exists():
            if dest_bin.exists():
                shutil.rmtree(dest_bin)
            shutil.copytree(src_bin, dest_bin)
            dll_count = len(list(dest_bin.glob("*.dll")))
            print(f"✓ 已复制bin目录到: {dest_bin}")
            print(f"  包含 {dll_count} 个DLL文件")
        else:
            print("✗ 错误: bin目录不存在")
            return False
        
        # 复制lib目录（可选）
        src_lib = vips_root / "lib"
        dest_lib = LIBVIPS_DIR / "lib"
        
        if src_lib.exists():
            if dest_lib.exists():
                shutil.rmtree(dest_lib)
            shutil.copytree(src_lib, dest_lib)
            print(f"✓ 已复制lib目录到: {dest_lib}")
        
        print("\n4. 清理临时文件...")
        shutil.rmtree(temp_dir)
        print("✓ 清理完成")
        
        print("\n" + "=" * 60)
        print("✓ libvips安装完成！")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n✗ 安装失败: {e}")
        return False


def check_libvips():
    """检查libvips是否已安装"""
    if (LIBVIPS_DIR / "bin").exists():
        dll_count = len(list((LIBVIPS_DIR / "bin").glob("*.dll")))
        print(f"✓ libvips已安装")
        print(f"  位置: {LIBVIPS_DIR / 'bin'}")
        print(f"  DLL文件: {dll_count} 个")
        return True
    return False


def main():
    """主函数"""
    print()
    print("=" * 60)
    print(" PicX GUI - libvips Windows 配置工具")
    print("=" * 60)
    print()
    
    # 检查现有安装
    if check_libvips():
        print()
        response = input("libvips已存在，是否重新下载？(y/N): ")
        if response.lower() != 'y':
            print("已取消")
            return
        print()
    
    # 下载和安装
    success = download_libvips()
    
    # 显示结果
    print()
    if success:
        print("✓ 配置完成！")
        print()
        print("下一步:")
        print("  1. 安装依赖: pip install -r requirements.txt")
        print("  2. 测试运行: python main.py")
        print("  3. 打包应用: build_windows.bat")
    else:
        print("✗ 配置失败！")
        print()
        print("请尝试手动下载:")
        print(f"  1. 访问: {LIBVIPS_URL}")
        print(f"  2. 下载并解压 {LIBVIPS_FILENAME}")
        print(f"  3. 将bin目录复制到: {LIBVIPS_DIR / 'bin'}")
    
    print()
    input("按Enter键退出...")


if __name__ == "__main__":
    main()
