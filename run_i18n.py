#!/usr/bin/env python3

import sys
import os

def main():
    """Main launcher with language selection"""
    
    # check command line arguments
    lang = 'en'  # default language
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['en', 'zh', 'cn']:
            lang = 'zh' if sys.argv[1] == 'cn' else sys.argv[1]
    else:
        # detect system language
        try:
            import locale
            system_lang = locale.getdefaultlocale()[0]
            if system_lang and system_lang.startswith('zh'):
                lang = 'zh'
        except:
            pass
    
    # import and run GUI with selected language
    try:
        from renamer.gui_i18n import main as gui_main
        gui_main(lang)
    except KeyboardInterrupt:
        print("\nProgram terminated" if lang == 'en' else "\n程序已退出")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}" if lang == 'en' else f"错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
