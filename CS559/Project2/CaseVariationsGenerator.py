import itertools

class PVG:
    """
    Generates variations on a list of passwords.
    Author: Abraham Reines
    Date: 2024-02-05
    """

    def __init__(self, passwords, output_file="/Volumes/StorageAJR/School/CS559/Project2/password_varations.txt"):
        """Initialize the generator."""
        self.passwords = passwords
        self.output_file = output_file
        
    def generate_variations(self):
        """
        Generates and writes the password variations.
        """
        with open(self.output_file, 'w') as file:
            for password in self.passwords:
                # Generate all combinations of upper and lower case for each character
                variations = [''.join(var) for var in itertools.product(*([letter.lower(), letter.upper()] for letter in password))]
                file.write('\n'.join(variations) + '\n')
        print(f"Password variations generated successfully: {self.output_file}")

if __name__ == "__main__":
    passwords = ["MSKITTY666", "DENTURES", "DEPENDS", "MODELT", "OLDFOGY", "KANDW",
                 "CORNBREAD", "SUSPENDERS", "WHITE_RABB1T"]
    pvg = PVG(passwords)
    pvg.generate_variations()