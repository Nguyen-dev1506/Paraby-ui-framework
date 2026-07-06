import sys
from paraby import run
from paraby.language_manager import get as _t, interactive_select

def main():
    if len(sys.argv) < 2:
        print(_t("cli_main_syntax"))
        sys.exit(1)

    # Hỗ trợ flag --lang để chọn ngôn ngữ
    if sys.argv[1] == "--lang":
        interactive_select()
        return

    run(sys.argv[1])

if __name__ == "__main__":
    main()
