import json


def main():
    d = json.loads(input())
    cleaned = {k: v for k, v in d.items() if v is not None}
    print(cleaned)


if __name__ == "__main__":
    main()
