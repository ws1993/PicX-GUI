"""libvips Windows加载器，用于在打包后自动加载内嵌的libvips。"""
import os
import sys
import platform


def setup_libvips_path():
    """
    设置libvips DLL搜索路径。
    
    在Windows上，需要将libvips的bin目录添加到DLL搜索路径中。
    
    Returns:
        bool: 成功返回True，失败返回False
    """
    if platform.system() != "Windows":
        # 非Windows系统，不需要特殊处理
        return True
    
    # 获取应用程序根目录
    if getattr(sys, 'frozen', False):
        # PyInstaller打包后的路径
        application_path = sys._MEIPASS
    else:
        # 开发环境路径
        application_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # libvips bin目录路径
    libvips_bin = os.path.join(application_path, "libs", "libvips", "bin")
    
    if os.path.exists(libvips_bin):
        # 将libvips bin目录添加到PATH
        os.environ["PATH"] = libvips_bin + os.pathsep + os.environ.get("PATH", "")
        
        # Python 3.8+ 需要显式添加DLL目录
        if hasattr(os, 'add_dll_directory'):
            os.add_dll_directory(libvips_bin)
        
        print(f"✓ libvips已加载: {libvips_bin}")
        return True
    else:
        print(f"⚠ 警告: libvips目录不存在: {libvips_bin}")
        print(f"  pyvips将使用系统安装的libvips（如果有）")
        return False


def check_pyvips():
    """
    检查pyvips是否可用。
    
    Returns:
        bool: 可用返回True，不可用返回False
    """
    try:
        import pyvips
        print(f"✓ pyvips版本: {pyvips.__version__}")
        
        # 尝试获取libvips版本
        try:
            vips_version = pyvips.API_mode
            print(f"✓ libvips API模式: {vips_version}")
        except:
            pass
            
        return True
    except ImportError:
        print("✗ 警告: pyvips未安装")
        print("  大图处理功能将不可用，仅能使用Pillow后端")
        return False
    except Exception as e:
        print(f"✗ 警告: pyvips加载失败: {e}")
        print("  大图处理功能将不可用")
        return False


def get_backend_info():
    """
    获取可用的后端信息。
    
    Returns:
        dict: 包含后端可用性的字典
    """
    backends = {
        "pillow": False,
        "pyvips": False
    }
    
    # 检查Pillow
    try:
        import PIL
        backends["pillow"] = True
        print(f"✓ Pillow版本: {PIL.__version__}")
    except ImportError:
        print("✗ Pillow未安装")
    
    # 检查pyvips
    backends["pyvips"] = check_pyvips()
    
    return backends
