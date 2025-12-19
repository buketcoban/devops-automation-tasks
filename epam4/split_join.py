def main():
    sentence = input()
    words = sentence.split(' ')
    reversed_words = [word[::-1] for word in words]
    result = ' '.join(reversed_words)
    print(result)


if __name__ == "__main__":
    main()

