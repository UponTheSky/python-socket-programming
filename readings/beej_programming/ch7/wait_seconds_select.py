import select
import sys


def main() -> None:
    poll = select.poll()
    poll.register(sys.stdin, select.POLLIN)

    print("Hit RETURN or wait 2.5 seconds for timeout")

    events = poll.poll(3000) # 3 seconds

    if not events:
        print("poll timed out!")

    for fd, event in events:
        if event & select.POLLIN:
            print(f"file descriptor {fd} is ready to read")
        else:
            print(f"unexpected event {event} has occurred")


if __name__ == "__main__":
    main()
