#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:50:51 2023

This is a supplemental program to Huffman_tree_coding_decoding exercise. 
It imports the HuffmanNode and HuffmanCoding modules.
It not only decodes messages, but also displays the Huffman Trees being built. 

@author: abrahamreines
"""

import os
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
from Huffman_tree_coding_decoding import HuffmanCoding

def plotHuffmanTree(node, pos=None, x=0, y=0, layer=1, G=None):
    """
    Recursively plots the Huffman Tree using networkx.
    Args:
        node (HuffmanNode): The current node in the Huffman Tree.
        pos (dict, optional): The positions of nodes for plotting.
        G (networkx.DiGraph, optional): The directed graph being constructed.
    Returns:
        tuple: Tuple containing the graph (G) and positions of nodes (pos).
    """
    if G is None:
        G = nx.DiGraph()
    if pos is None:
        pos = {}
    if node is not None:
        G.add_node(node, label=node.char if node.char else '#')
        pos[node] = (x, y)
        if node.left:
            G.add_edge(node, node.left)
            plotHuffmanTree(node.left, pos, x - 1 / layer, y - 1, layer + 0.5, G)
        if node.right:
            G.add_edge(node, node.right)
            plotHuffmanTree(node.right, pos, x + 1 / layer, y - 1, layer + 0.5, G)
    return G, pos

def displayHuffmanTree(root, file_path='huffman_tree.png'):
    """
    Saves the Huffman Tree visualization as an image.
    Args: 
        root (HuffmanNode): The root of the Huffman Tree.
        file_path (str): The path to save the plot image.
    """
    G, pos = plotHuffmanTree(root)
    labels = {node: G.nodes[node]['label'] for node in G.nodes}

    # Set global font properties
    matplotlib.rcParams['font.family'] = 'Apple Color Emoji'

    nx.draw(G, pos, labels=labels, with_labels=True, arrows=False, node_size=1000)
    plt.savefig(file_path)
    print(f"Huffman tree plot saved to {file_path}")

def exampleUsage():
    """ Demonstrates the usage of Huffman coding with example text cases and saves tree plots. """
    test_cases = [
        "hello world",
        "🔥💀",
        "831Five",
        "Abraham",
        "😊❤️⬆️😢"
    ]

    # Create a directory to save plots
    os.makedirs("huffman_plots", exist_ok=True)

    for test in test_cases:
        print(f"\nTest case: '{test}'")
        huffman = HuffmanCoding(test)
        encoded_text = huffman.encode()
        decoded_text = huffman.decode(encoded_text)

        print(f"Encoded Binary Message: {encoded_text}")
        print(f"Decoded Text Message: {decoded_text}")
        print(f"Number of bits in binary message: {len(encoded_text)}")
        print(f"Number of characters in input message: {len(test)}")

        if len(test) <= 10:  # Save tree plot for moderate messages
            sanitized_test = ''.join([c if c.isalnum() else "_" for c in test])  # sanitize the test string for file naming
            file_name = f"huffman_plots/tree_{sanitized_test}.png"
            displayHuffmanTree(huffman.huffman_tree, file_path=file_name)
            plt.close()  # Close the plot after saving

def main():
    """
    Main function to demonstrate Huffman coding and save tree plots.
    """
    exampleUsage()
    print()
    try:
        text = input("Enter a text message (10 char max): ").strip()
        if not text:
            raise ValueError("Empty string provided")

        huffman = HuffmanCoding(text)
        encoded_text = huffman.encode()
        decoded_text = huffman.decode(encoded_text)

        print(f"Encoded Binary Message: {encoded_text}")
        print(f"Decoded Text Message: {decoded_text}")
        print(f"Number of bits in binary message: {len(encoded_text)}")
        print(f"Number of characters in input message: {len(text)}")

        if len(text) <= 10:  # Save tree plot for the input message
            file_name = f"huffman_plots/tree_{text.replace(' ', '_')}.png"
            displayHuffmanTree(huffman.huffman_tree, file_path=file_name)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()