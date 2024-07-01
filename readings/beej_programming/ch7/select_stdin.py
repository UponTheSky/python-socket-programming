import select
import sys

TIMEOUT = 2.5


def main() -> None:
    rlist, _, _ = select.select([sys.stdin], [], [], TIMEOUT)

    if not rlist:
        print("Timeout!")
    
    print(rlist[0].readline(100))


if __name__ == "__main__":
    main()
    