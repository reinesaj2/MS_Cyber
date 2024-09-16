import subprocess
import random
import os

# HashcatRunner class
class HashcatRunner:
    def __init__(self, hash_file):
        self.hash_file = hash_file

    def run_with_patterns(self, patterns):
        temp_wordlist = f'temp_{random.randint(1000, 1000000000)}.txt'
        with open(temp_wordlist, 'w') as f:
            for pattern in patterns:
                f.write(pattern + '\n')

        cmd = ['hashcat', '-m', '1800', '-a', '0', self.hash_file, temp_wordlist, '--potfile-disable', '--quiet', '--show']
        result = subprocess.run(cmd, capture_output=True, text=True)

        if os.path.exists(temp_wordlist):
            os.remove(temp_wordlist)

        if result.stdout.strip():
            return patterns, result.stdout.strip()
        else:
            return None