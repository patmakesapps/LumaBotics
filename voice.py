def say(text):
    # TODO Sunday: espeak-ng -> wav -> aplay through the WM8960
    print(f"ROBOT: {text}")

def listen():
    # TODO Sunday: arecord from the mics -> speech-to-text -> return the words
    return input("YOU: ")   

if __name__ == "__main__":
    say("Say something and I will repeat it")
    heard = listen()
    say(f"You said: {heard}")    