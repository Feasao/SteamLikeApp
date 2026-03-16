import subprocess
import os
import sys
from scripts.data_fetch import main as Data_fetch
from scripts.specials import main as Specials
from scripts.pop100 import main as Popular100
from scripts.wishlist import main as Wishlist
from scripts.similarity import main as Similarity
scripts = [
    Data_fetch,
    Specials,
    Popular100,
    Wishlist,
    Similarity,
]

def main():
    print("Fetching your games...")
    Data_fetch()
    print("Fetching specials...")
    Specials()
    print("Fetching popular...")
    Popular100()
    print("Fetching wishlist...")
    Wishlist()
    print("Computing similarity...")
    Similarity()
    print("Done.")

if __name__ == "__main__":
    main()
