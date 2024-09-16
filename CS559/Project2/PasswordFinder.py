from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from HashcatRunner import HashcatRunner
from PatternGenerator import PatternGenerator

# PasswordFinder class
class PasswordFinder:
    def __init__(self, hash_file, attempts=10000, workers=8, patterns_per_file=1000):
        self.hash_file = hash_file
        self.attempts = attempts
        self.workers = workers
        self.patterns_per_file = patterns_per_file
        self.pattern_generator = PatternGenerator()
        self.hashcat_runner = HashcatRunner(hash_file)

    def print_status(self, futures):
        """
        Print the current status of the jobs.
        """
        total = len(futures)
        done = sum(1 for future in futures if future.done())
        running = sum(1 for future in futures if future.running())
        pending = total - done - running
        print(f"Total jobs: {total}, Done: {done}, Running: {running}, Pending: {pending}")
    
    def find_password(self):
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = [executor.submit(self.hashcat_runner.run_with_patterns, [self.pattern_generator.generate() for _ in range(self.patterns_per_file)]) for _ in range(self.attempts)]
            last_status_time = time.time()
            
            for future in as_completed(futures):
                # Periodically print the status
                if time.time() - last_status_time > 5:  # Every 5 seconds
                    self.print_status(futures)
                    last_status_time = time.time()
                
                # Your existing logic for handling completed futures
                
            # Final status report
            self.print_status(futures)