import random

class PatternGenerator:
    start_special_chars = ['>', ';', '\\']
    inner_special_chars = [',', '}', '{', '(', ')', '[', ']', '|', '&', '#']
    upper_letters = [chr(i) for i in range(65, 91)]  # A-Z
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def __init__(self, min_length=6, max_length=16):
        self.min_length = min_length
        self.max_length = max_length

    def generate(self):
        length = random.randint(self.min_length, self.max_length)
        pattern = [random.choice(self.start_special_chars)]
        while len(pattern) < length - 1:
            pattern.append(random.choice(self.upper_letters + self.digits))
            if random.randint(0, 4) == 0 and len(pattern) < length - 2:
                pattern.append(random.choice(self.inner_special_chars))
        pattern.append(random.choice(self.upper_letters + self.digits))
        return ''.join(pattern)
