import subprocess
import random
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define your character sets based on observed patterns
start_special_chars = ['>', ';', '\\']
inner_special_chars = [',', '}', '{', '(', ')', '[', ']', '|', '&', '#']
upper_letters = [chr(i) for i in range(65, 91)]  # A-Z
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def generate_pattern(min_length=6, max_length=16):
    """
    Generates a pattern with a length varying from min_length to max_length.
    """
    length = random.randint(min_length, max_length)
    pattern = [random.choice(start_special_chars)]
    while len(pattern) < length - 1:
        pattern.append(random.choice(upper_letters + digits))
        if random.randint(0, 4) == 0 and len(pattern) < length - 2:
            pattern.append(random.choice(inner_special_chars))
    pattern.append(random.choice(upper_letters + digits))
    return ''.join(pattern)

def run_hashcat_with_patterns(patterns, hash_file):
  """
  Executes Hashcat with the given patterns and hash file.
  """
  temp_wordlist = f'temp_{random.randint(1000, 1000000000)}.txt'
  with open(temp_wordlist, 'w') as f:
    for pattern in patterns:
      f.write(pattern + '\n')
  
  cmd = [
    'hashcat', '-m', '1800', '-a', '0', hash_file, temp_wordlist,
    '--potfile-disable', '--quiet', '--show'
  ]
  result = subprocess.run(cmd, capture_output=True, text=True)
  
  if os.path.exists(temp_wordlist):
    os.remove(temp_wordlist)

  if result.stdout.strip():
    return patterns, result.stdout.strip()
  else:
    return None

def find_password(hash_file, attempts=10000, workers=8, patterns_per_file=1000):
  """
  Attempts to find the password by generating patterns and using Hashcat in parallel.
  """
  with ThreadPoolExecutor(max_workers=workers) as executor:
    futures = [executor.submit(run_hashcat_with_patterns, [generate_pattern() for _ in range(patterns_per_file)], hash_file) for _ in range(attempts)]
    completed_attempts = 0
    for future in as_completed(futures):
      completed_attempts += 1
      print(f"Completed {completed_attempts} of {attempts} attempts.")
      result = future.result()
      if result:
        patterns, cracked = result
        print(f"Password found with patterns {patterns}: {cracked}")
        with open('cracked_password_for_Linux.txt', 'w') as f:
          f.write(cracked + '\n')
        return cracked
  print("Password not found within the attempt limit.")
  return None

if __name__ == "__main__":
    hash_file = '/Volumes/StorageAJR/MS_Cyber/CS559/Project2/rootForLinux.txt' 
    find_password(hash_file)
