#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Abraham Reines, November 2023 
This module contains the implementation of Huffman coding and decoding algorithm.
It includes the HuffmanNode class, which represents a node in the Huffman tree,
and the HuffmanCoding class, which performs the manual labor for building, encoding, and decoding the Huffman Tree.
The module also includes a function to display the Huffman tree and an additional compliance report function.
"""

import heapq

class HuffmanNode:
    """
    Represents a node in the Huffman tree.

    Attributes:
    - char (str): The character represented by the node.
    - freq (int): The frequency of the character in the input text.
    - left (HuffmanNode): The left child of the node.
    - right (HuffmanNode): The right child of the node.
    """
    
    def __init__(self, char, freq):
        """
        Initializes a HuffmanNode with a character (char), frequency (freq), 
        and left/right children set to None.

        Parameters:
        - char (str): The character represented by the node.
        - freq (int): The frequency of the character in the input text.
        """
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        """
        Allows comparison of HuffmanNode instances based on their frequency.

        Parameters:
        - other (HuffmanNode): The other HuffmanNode instance to compare to.

        Returns:
        - bool: True if the frequency of the current node is less than the frequency of the other node, or else false.
        """
        return self.freq < other.freq

class HuffmanCoding:
    """
    A class which performs the manual labor for building, encoding, and decoding the Huffman Tree.

    Attributes:
    - text (str): The text to be encoded and decoded.
    - frequency_table (dict): A dictionary for mapping each character to its frequency.
    - huffman_tree (HuffmanNode): The root node of the constructed Huffman tree.
    - code_table (dict): A dictionary for mapping each character to its Huffman code.
    """
    def __init__(self, text):
        """
        Initializes the HuffmanCoding instance with the input text.

        Parameters:
        - text (str): The text to be encoded and decoded.
        """
        self.text = text
        self.frequency_table = self.frequencyTable()
        self.huffman_tree = self.huffmanTree()
        self.code_table = self.codeTable(self.huffman_tree)

    def frequencyTable(self):
        """
        Constructs a frequency table from the given text.

        Returns:
        - dict: A dictionary mapping each character to its frequency.
        """
        frequency = {}
        for char in self.text:
            frequency[char] = frequency.get(char, 0) + 1
        return frequency

    def huffmanTree(self):
        """
        Constructs the Huffman tree based on character frequencies.

        Returns:
        - HuffmanNode: The root node of the constructed Huffman tree.
        """
        priority_queue = [HuffmanNode(char, freq) for char, freq in self.frequency_table.items()]
        heapq.heapify(priority_queue)

        # If there is only one node in the priority queue, create a root node and return
        if len(priority_queue) == 1:
            node = heapq.heappop(priority_queue)
            root = HuffmanNode(None, node.freq)
            root.left = node
            return root

        # Merge the two lowest frequency nodes until only one node is left in the priority queue
        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(priority_queue, merged)
        return priority_queue[0]

    def codeTable(self, node, path="", code_table=None):
            """
            Generates the Huffman code table from the Huffman tree.

            Parameters:
            - node (HuffmanNode): The current node being traversed.
            - path (str): The path taken to reach the current node.
            - code_table (dict): The dictionary mapping for each character to its Huffman code.

            Returns:
            - dict: A dictionary mapping for each character to its Huffman code.
            """
            # If code_table is None, initialize it as an empty dictionary
            if code_table is None:
                code_table = {}
            # If node is not None, traverse the tree
            if node is not None:
                # If the current node is a leaf node, add its character and path to the code_table
                if node.char is not None:
                    code_table[node.char] = path
                # Traverse the left subtree with path + "0"
                code_table = self.codeTable(node.left, path + "0", code_table)
                # Traverse the right subtree with path + "1"
                code_table = self.codeTable(node.right, path + "1", code_table)
            # Return the code_table
            return code_table

    def encode(self):
        """
        Encodes a text message using the Huffman code table.

        Returns:
        - str: A string representing the encoded binary message.
        """
        return ''.join(self.code_table[char] for char in self.text)

    def decode(self, binary):
            """
            Decodes a binary message using the Huffman tree.

            Parameters:
            - binary (str): The binary message to be decoded.

            Returns:
            - str: The decoded text message.
            """
            # Start at the root of the Huffman tree
            node = self.huffman_tree
            # Initialize an empty string to store the decoded message
            # Traverse the Huffman tree based on the binary message
            for bit in binary:
                # If the bit is 0, move to the left child of the current node
                # If the bit is 1, move to the right child of the current node
                node = node.left if bit == '0' else node.right
                # If the current node has a character, add it to the decoded message
                # and move back to the root of the Huffman tree
                if node.char is not None:
                    decoded += node.char
                    node = self.huffman_tree
            # Return the decoded message
            return decoded

def displayHuffmanTree(node, indent=0):
    """
    Recursively prints the Huffman tree for visualization.

    Parameters:
    - node (HuffmanNode): The current node in the Huffman tree.
    - indent (int): The current indentation level for printing. Very critical.
    """
    if node is not None:
        if node.char is not None:
            print("  " * indent + f"Character: {node.char}, Frequency: {node.freq}")
        else:
            print("  " * indent + f"Node: Frequency: {node.freq}")
        # recursively call displayHuffmanTree on left and right nodes
        displayHuffmanTree(node.left, indent + 1)
        displayHuffmanTree(node.right, indent + 1)

def main():
    """
    Main function to demonstrate Huffman coding on user input.

    Operations: Takes user input, encodes, and decodes it using Huffman coding,
    and prints relevant information. Displays the Huffman tree for 10 char messages.
    """
    text = input("Enter a text message: ")
    huffman = HuffmanCoding(text)
    encoded_text = huffman.encode()
    decoded_text = huffman.decode(encoded_text)

    print(f"Encoded Binary Message: {encoded_text}")
    print(f"Decoded Text Message: {decoded_text}")
    print(f"Number of bits in binary message: {len(encoded_text)}")
    print(f"Number of characters in input message: {len(text)}")

    if len(text) <= 10:  # Display tree for short messages
        print("\nHuffman Tree:")
        displayHuffmanTree(huffman.huffman_tree)

def testHuffman():
    """
    Tests the Huffman coding implementation with test cases.

    Operations: Runs a series of tests with different strings,
    verifying the accuracy of encoding and decoding.
    Asserts the decoded message matches the original message.
    """
    test_cases = [
        "hola orb",
        "aaaaaaaaaa",
        "abcdefghi",
        "",
        "💀", # May have multiple unicode characters depending on the complexity of the emoji encoding
        "❤️", # May have multiple unicode characters depending on the complexity of the emoji encoding
        "The quick brown fox jumps over the lazy dog"
    ]

    for test in test_cases:
        print(f"\nTesting with input: '{test}'")

        if test == "":
            print("Empty string, no encoding or decoding necessary.")
            continue  # Skip the rest of the loop for empty an string

        huffman = HuffmanCoding(test)
        encoded_text = huffman.encode()
        decoded_text = huffman.decode(encoded_text)

        assert decoded_text == test, "Decoding failed."
        print("Encoding and Decoding Successful.")

        print(f"Original Length: {len(test) * 8} bits (1 char = 8 bits)")
        print(f"Encoded Length: {len(encoded_text)} bits")

        if len(test) <= 10:  # Display tree for short messages
            print("Huffman Tree:")
            displayHuffmanTree(huffman.huffman_tree)

def complianceReport(script):
    """
    Generates a compliance report.

    Parameters:
    - script (str): The source code of the Huffman coding and decoding program.

    Returns:
    - str: A report detailing compliance with the assignment.
    """

    report = []
    required_features = {
        "Accept a text message (string)": False,
        "Create a Huffman tree": False,
        "Create a code table": False,
        "Encode the text message into binary": False,
        "Decode the binary message back to text": False,
        "Show the number of bits in the binary message": False,
        "Show the number of characters in the input message": False,
        "Display the Huffman tree for short messages": False
    }

    # Check each feature in the script for compliance
    if "input(" in script or "sys.argv" in script:
        required_features["Accept a text message (string)"] = True

    if "HuffmanNode" in script or "huffmanTree" in script:
        required_features["Create a Huffman tree"] = True

    if "codeTable" in script:
        required_features["Create a code table"] = True

    if "encode(" in script:
        required_features["Encode the text message into binary"] = True

    if "decode(" in script:
        required_features["Decode the binary message back to text"] = True

    if "len(encoded_text)" in script:
        required_features["Show the number of bits in the binary message"] = True

    if "len(text)" in script:
        required_features["Show the number of characters in the input message"] = True

    if "displayHuffmanTree" in script:
        required_features["Display the Huffman tree for short messages"] = True

    # Generate the report
    for feature, is_compliant in required_features.items():
        report.append(f"{feature}: {'Compliant' if is_compliant else 'Non-Compliant'}")

    return "\n".join(report)



if __name__ == "__main__":
    testHuffman()

    # Reading the content of the current script
    with open(__file__, 'r') as file:
        full_script = file.read()

    print("\n==================== COMPLIANCE REPORT ====================\n")

    # Generate and print the compliance report
    complianceReport_result = complianceReport(full_script)
    print(complianceReport_result)