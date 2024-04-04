from datetime import datetime
import os

def Wang_to_Reines(file_location, me):
    """ name and date in a TLA+ file """

    # directory of the current script
    DIRScript = os.path.dirname(__file__)
    DIRPath = os.path.join(DIRScript, file_location)

    print("Starting update process...")

    try:
        # read TLA+ file
        with open(DIRPath, 'r', encoding='utf-8') as file:
            what_is_in_there = file.readlines()

        print("File read successfully. Searching for the author's name...")

        # find the line with Dr.Wang's name
        for i, line in enumerate(what_is_in_there):
            if 'Xunhua Wang' in line:
                # Replace with yours truly
                what_is_in_there[i] = f'(* {me}, {datetime.now().strftime("%m/%d/%Y")} *)\n'
                break
        else:
            print("Dr. Wang name not found in file.")
            return

        # update file with changes
        with open(DIRPath, 'w', encoding='utf-8') as file:
            file.writelines(what_is_in_there)

        print("File updated!")

    except FileNotFoundError:
        print(f"{file_location} was not found.")
    except Exception as e:
        print(f"error occurred: {e}")

# This works on HourClock3.tla also!
Wang_to_Reines('HourClock.tla', 'Abraham J. Reines')