"""
PicX GUI - Modern graphical interface for PicX image optimization tool.

This is the main entry point for the application.
"""
import sys

# 首先加载libvips（Windows上需要在导入pyvips之前设置路径）
from gui.utils.libvips_loader import setup_libvips_path, get_backend_info

# 设置libvips路径
setup_libvips_path()

# 然后导入其他模块
import customtkinter as ctk
from gui.app import PicXApp


def main():
    """Main entry point for PicX GUI."""
    # 获取后端信息
    print("\n" + "=" * 50)
    print("PicX GUI - 图片优化工具")
    print("=" * 50)
    
    backends = get_backend_info()
    
    print("\n可用后端:")
    if backends["pillow"]:
        print("  ✓ Pillow (基础图片处理)")
    if backends["pyvips"]:
        print("  ✓ pyvips (大图和TIFF支持)")
    
    if not backends["pillow"]:
        print("\n错误: Pillow未安装，应用无法运行")
        print("请运行: pip install -r requirements.txt")
        input("\n按Enter键退出...")
        sys.exit(1)
    
    print("\n正在启动应用...")
    print("=" * 50 + "\n")
    
    try:
        app = PicXApp()
        app.mainloop()
    except KeyboardInterrupt:
        print("\n应用被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n致命错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按Enter键退出...")
        sys.exit(1)


if __name__ == "__main__":
    main()
