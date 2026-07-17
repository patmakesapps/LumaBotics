from voice import say, listen

def handle(text):
    """Turn the human's words into a reply. Returns None to quit."""

    words = text.lower().split()
    if not words:
        return "I did not catch that."
    w = words[0]
    if w in ("drive", "go", "forward"):
        return "Driving forward."
    if w in ("stop", "park", "halt"):
        return "Parking."
    if w in ("back", "reverse"):
        return "Backing up."

    if w == "turn":
        if len(words) > 1 and words[1] in ("left", "right"):
            return f"Turning {words[1]}."
        return "Turn which way?"

    if w in ("distance", "far"):
        return "No distance sensor connected yet."
    if w in ("quit", "exit", "bye"):
        return None
    return "I do not know that command yet."

say("Ready for commands.")
while True:
    reply = handle(listen())
    if reply is None:
        say("Goodbye.")
        break
    say(reply) 



