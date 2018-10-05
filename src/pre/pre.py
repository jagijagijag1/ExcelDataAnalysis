import pandas as pd
import sys

def main(filepath):
    print('import ' + filepath)
    return filepath

if __name__ == '__main__':
    args = sys.argv
    if (len(args) != 1):
        print('specify excel file path')
        quit()
    main(args[1])
