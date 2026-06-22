"""libvips诊断工具 - 检测DLL加载问题"""
import os
import sys
import ctypes
from pathlib import Path


def check_dll_architecture(dll_path):
    """检查DLL架构（32位或64位）"""
    try:
        with open(dll_path, 'rb') as f:
            # 读取DOS头
            f.seek(0x3C)
            pe_offset = int.from_bytes(f.read(4), 'little')
            
            # 跳到PE头
            f.seek(pe_offset)
            pe_sig = f.read(4)
            if pe_sig != b'PE\0\0':
                return "无效的PE文件"
            
            # 读取机器类型
            machine = int.from_bytes(f.read(2), 'little')
            
            if machine == 0x014c:
                return "32位 (x86)"
            elif machine == 0x8664:
                return "64位 (x64)"
            elif machine == 0xaa64:
                return "64位 (ARM64)"
            else:
                return f"未知架构 (0x{machine:04x})"
    except Exception as e:
        return f"检查失败: {e}"


def test_dll_load_methods(dll_path):
    """尝试不同的DLL加载方法"""
    results = {}
    
    # 方法1: 直接LoadLibrary
    try:
        h = ctypes.windll.LoadLibrary(str(dll_path))
        results["LoadLibrary (直接)"] = "✓ 成功"
        ctypes.windll.kernel32.FreeLibrary(h._handle)
    except Exception as e:
        results["LoadLibrary (直接)"] = f"✗ {e}"
    
    # 方法2: 使用AddDllDirectory
    try:
        bin_dir = os.path.dirname(dll_path)
        ctypes.windll.kernel32.AddDllDirectory(bin_dir)
        h = ctypes.windll.LoadLibrary(str(dll_path))
        results["LoadLibrary (AddDllDirectory)"] = "✓ 成功"
        ctypes.windll.kernel32.FreeLibrary(h._handle)
    except Exception as e:
        results["LoadLibrary (AddDllDirectory)"] = f"✗ {e}"
    
    # 方法3: 使用PATH
    try:
        bin_dir = os.path.dirname(dll_path)
        old_path = os.environ.get("PATH", "")
        os.environ["PATH"] = bin_dir + os.pathsep + old_path
        h = ctypes.windll.LoadLibrary(str(dll_path))
        results["LoadLibrary (PATH)"] = "✓ 成功"
        ctypes.windll.kernel32.FreeLibrary(h._handle)
        os.environ["PATH"] = old_path
    except Exception as e:
        results["LoadLibrary (PATH)"] = f"✗ {e}"
    
    # 方法4: CDLL
    try:
        h = ctypes.CDLL(str(dll_path))
        results["CDLL (直接)"] = "✓ 成功"
    except Exception as e:
        results["CDLL (直接)"] = f"✗ {e}"
    
    return results


def main():
    print("=" * 70)
    print(" PicX GUI - libvips 诊断工具")
    print("=" * 70)
    
    # 1. Python环境
    print("\n【1】Python 环境:")
    print(f"  版本: {sys.version}")
    print(f"  架构: {ctypes.sizeof(ctypes.c_voidp) * 8} 位")
    print(f"  可执行文件: {sys.executable}")
    
    # 2. libvips路径
    print("\n【2】libvips 路径:")
    libvips_bin = Path("libs/libvips/bin")
    print(f"  目录: {libvips_bin.absolute()}")
    print(f"  存在: {libvips_bin.exists()}")
    
    if not libvips_bin.exists():
        print("\n✗ 错误: libvips目录不存在")
        print("  请运行: python setup_libvips.py")
        return
    
    # 3. DLL文件
    print("\n【3】DLL 文件:")
    dll_files = list(libvips_bin.glob("*.dll"))
    print(f"  DLL数量: {len(dll_files)}")
    
    libvips_dll = libvips_bin / "libvips-42.dll"
    print(f"\n  libvips-42.dll:")
    print(f"    存在: {libvips_dll.exists()}")
    
    if libvips_dll.exists():
        print(f"    大小: {libvips_dll.stat().st_size:,} 字节")
        print(f"    架构: {check_dll_architecture(libvips_dll)}")
    else:
        print("    ✗ 文件不存在")
        return
    
    # 4. 关键依赖检查
    print("\n【4】关键依赖:")
    critical_dlls = [
        "libglib-2.0-0.dll",
        "libgobject-2.0-0.dll",
        "libc++.dll",
        "libexpat-1.dll"
    ]
    
    for dll_name in critical_dlls:
        dll_path = libvips_bin / dll_name
        exists = dll_path.exists()
        status = "✓" if exists else "✗"
        arch = ""
        if exists:
            arch = f" ({check_dll_architecture(dll_path)})"
        print(f"    {status} {dll_name}{arch}")
    
    # 5. DLL加载测试
    print("\n【5】DLL 加载测试:")
    load_results = test_dll_load_methods(libvips_dll)
    for method, result in load_results.items():
        print(f"  {method}: {result}")
    
    # 6. pyvips测试
    print("\n【6】pyvips 测试:")
    
    # 先设置路径
    os.environ["PATH"] = str(libvips_bin.absolute()) + os.pathsep + os.environ.get("PATH", "")
    if hasattr(os, 'add_dll_directory'):
        os.add_dll_directory(str(libvips_bin.absolute()))
    
    try:
        import pyvips
        print(f"  ✓ pyvips导入成功")
        print(f"    版本: {pyvips.__version__}")
        
        try:
            # 尝试创建一个简单图像
            image = pyvips.Image.black(10, 10)
            print(f"  ✓ pyvips功能正常")
        except Exception as e:
            print(f"  ✗ pyvips功能测试失败: {e}")
            
    except ImportError as e:
        print(f"  ✗ pyvips未安装: {e}")
    except Exception as e:
        print(f"  ✗ pyvips加载失败: {e}")
        import traceback
        print("\n详细错误:")
        traceback.print_exc()
    
    # 7. 建议
    print("\n【7】诊断建议:")
    
    # 检查Python和DLL架构是否匹配
    python_arch = ctypes.sizeof(ctypes.c_voidp) * 8
    dll_arch_str = check_dll_architecture(libvips_dll)
    
    if "32位" in dll_arch_str and python_arch == 64:
        print("  ✗ 架构不匹配: Python是64位，但libvips是32位")
        print("    解决: 下载64位版本的libvips")
    elif "64位" in dll_arch_str and python_arch == 32:
        print("  ✗ 架构不匹配: Python是32位，但libvips是64位")
        print("    解决: 使用64位Python或下载32位libvips")
    elif any("✗" in result for result in load_results.values()):
        print("  ⚠ DLL加载失败，可能原因:")
        print("    1. 缺少Visual C++运行时 (安装vc_redist.x64.exe)")
        print("    2. DLL依赖缺失 (检查上面的关键依赖)")
        print("    3. libvips版本不兼容 (尝试重新下载)")
    else:
        print("  ✓ 所有检查通过")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
    input("\n按Enter键退出...")
