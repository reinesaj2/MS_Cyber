"""
Author: Abraham Reines
Created: Mon Apr  1 13:16:18 PDT 2024
Modified: Wed Apr  3 13:35:50 PDT 2024
Name of file: BackofEnvelope.py
"""

def What_is_the_search_time(BytesForFile, SignatureForBytes, HowManyComparisons):
    """
    time to search file with signature size using the Boyer-Moore algorithm
    
    Parameters:
    BytesForFile (int): bytes in the file
    SignatureForBytes (int): bytes for virus signature
    HowManyComparisons (int): 8-character comparisons of CPU in a second
    
    Returns:
    float: time for search the file (s)
    """
    # this is worst case
    Comparisons = BytesForFile
    TimeSec = Comparisons / (HowManyComparisons * 8)
    
    return TimeSec

def Readable_seconds(seconds):
    """
    Convert seconds to readable format 
    
    Parameters:
    seconds (float): seconds 
    
    Returns:
    str: days or years
    """
    # Constants
    SecondsForDay = 86400
    DaysForYear = 365.25
    
    if seconds < SecondsForDay:
        return f"{seconds} seconds"
    elif seconds < SecondsForDay * DaysForYear:
        days = seconds / SecondsForDay
        return f"{days:.2f} days"
    else:
        years = seconds / (SecondsForDay * DaysForYear)
        return f"{years:.2f} years"

# Constants
BytesForFile = 160 * (10**9)  # 160GB
SignatureForBytes = 1 * (2**10)  # 1KB
HowManyComparisons = 4 * (10**9)  # 8-character comparisons per second

#  1KB signature
OneSig = What_is_the_search_time(BytesForFile, SignatureForBytes, HowManyComparisons)
readable_OneSig = Readable_seconds(OneSig)

#  1 million signatures
MillSig = OneSig * 1_000_000
readable_MillSig = Readable_seconds(MillSig)

# results
print(f"Time for 1KB signature: {readable_OneSig}")
print(f"Time for 1 million 1KB signatures: {readable_MillSig}")
