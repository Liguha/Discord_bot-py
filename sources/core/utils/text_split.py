MAX_LENGTH = 1950

def split_message(msg: str) -> list[str]:
    splitted: list[str] = []
    words = msg.split(" ")
    part: str = ""
    i: int = 0
    while i < len(words):
        word = words[i]
        if len(part) + len(word) < MAX_LENGTH:
            part += word + " "
        else:
            if len(part) > 0:
                splitted.append(part)
                part = ""
                continue
            else:
                chunks = len(word) // MAX_LENGTH
                splitted.extend([word[i:(i + MAX_LENGTH)] for i in range(0, chunks * MAX_LENGTH, MAX_LENGTH)])
                part = f"{word[(chunks * MAX_LENGTH):]} "
        i += 1
    if len(part) > 0:
        splitted.append(part)
    return splitted