import pandas as pd
import sys
import re

concat_str = '-'

def main(filepath, headers):
    result = []

    print('import ' + filepath)
    print('extract columns named as ' + ','.join(headers))
    df = pd.read_excel(filepath, sheet_name=None, header=None)
    #print(df)

    # for each sheet
    for sheetkey in df:
        print('sheet: ' + sheetkey)
        sheet = df[sheetkey]
        h_index, use_cols, concat_cols = extractHeaderIndexOf(sheet, headers)

        if (h_index == -1):
            # if no header, exit
            print('no header found on sheet ' + sheetkey)
            return

        #print('found header on line ' + str(h_index) + ', use_cols is ' + str(use_cols) + ', concat_cols is ' + str(concat_cols))
        result.append(extractSpecifiedColumn(filepath, sheetkey, h_index, use_cols, concat_cols))

    #print(result)

    return result

'''
extract row index of header of sheet
'''
def extractHeaderIndexOf(sheet, headers):
    #print(sheet)
    for index, row in sheet.iterrows():
        use_cols, concat_cols = headerRowIndices(headers, row)
        if (len(use_cols) != 0):
            # if header row found, retrun index
            return index, use_cols, concat_cols
    # if no header, return -1
    return -1, [], {}

def headerRowIndices(headers, row):
    use_cols = []
    concat_cols = {}
    current_header = ''
    for i, col in enumerate(row):
        if (current_header != '' and str(col) == 'nan'):
            # if blank column exists, mark as concat col
            concat_cols[current_header].append(i)
            use_cols.append(i)
        for h in headers:
            if (re.match(h, str(col))):
                # if row contains one of the header string, append to use_cols
                use_cols.append(i)
                current_header = col
                concat_cols[current_header] = [i]
                break
    # if row contseins all header string, return true
    return use_cols, concat_cols

def extractSpecifiedColumn(filepath, sheetkey, h_index, use_cols, concat_cols):
    df = pd.read_excel(filepath, sheet_name=sheetkey, header=h_index, usecols=use_cols)

    # fill NaN with empty string
    df = df.fillna("")

    # concat Unnamed columns and its left
    concat_col_str = ''
    concat_col = pd.DataFrame({})
    for col in df:
        if (str(col).startswith("Unnamed")):
            # TODO: remove unneccesary concatinator
            concat_col = concat_col + concat_str + df[col]
            concat_col = concat_col.str.strip('-')
            df.drop(col, axis=1, inplace=True)
        elif (concat_col_str != '' and not concat_col.empty):
            df[concat_col_str] = concat_col
            # re-init
            concat_col_str = ''
            concat_col = pd.DataFrame({})
        else:
            concat_col_str = col
            concat_col = df[col]

    #print("result:")
    #print(df)

    return df

"""
check index is in headers or not
"""
def isTargetHeader(index, headers):
    for h in headers:
        if (re.match(h, str(index))):
            return True
    return False

"""
Extract specified column from Excel file
arg1: Excel file path
arg2: header string (regex) of target column
"""
if __name__ == '__main__':
    args = sys.argv
    if (len(args) < 3):
        print('specify excel file path & header string (regex)')
        quit()
    main(args[1], args[2:])
    # for test
    # filepath = '/Users/ryo/works/python/ExcelDataAnalysis/test/data/test_book.xlsx'
    # headers = ['Item', 'Default', 'Val*']
    # main(filepath, headers)
