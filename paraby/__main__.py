import sys
from paraby import run

def main():
    if len(sys.argv) < 2:
        print("Cú pháp: python3 -m paraby <tên_file.py | tên_file.pb>")
        sys.exit(1)
        
    run(sys.argv[1])

if __name__ == "__main__":
    main()
