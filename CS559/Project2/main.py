from PasswordFinder import PasswordFinder

if __name__ == "__main__":
    hash_file = '/Volumes/StorageAJR/MS_Cyber/CS559/Project2/rootForLinux.txt'
    password_finder = PasswordFinder(hash_file)
    password_finder.find_password()
