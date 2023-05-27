from converter import process_completion, generate_completion


def listen():
    while True:
        sentence = input("Enter a command or a query (press Enter to finish): ")
        if sentence:
            completion = generate_completion(sentence)
            if completion is None:
                continue
            print(process_completion(completion))
        else:
            break


def main():
    listen()


if __name__ == "__main__":
    main()
