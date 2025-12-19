def main():
    li1 = list(map(int, input().split()))
    li2 = list(map(int, input().split()))
    common = sorted(list(set(li1) & set(li2)))
    print(common)


if __name__ == "__main__":
    main()
