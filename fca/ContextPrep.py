import pandas as pd

reuters = "../DataEngineering/CleanTrainingData/clean_reuters_tdm.csv"
snippets = "../clean_snippets_tdm.csv"

def makeContextCsv(file, output_file):
    """ Generate a context csv from the input tdm """
    count = 0
    f = open(file)
    o = open(output_file, "w")
    header = f.readline()
    o.write(',' + header)

    while True:
        count += 1
        l = f.readline()
        if l == '':
            break
        else:
            bits = l[:-1].split(',')
            new_line = [str(count)]
            for i in bits:
                if i == "0":
                    new_line.append('')
                else:
                    new_line.append('X')
            o.write(','.join(new_line) + "\n")

    o.close()
    f.close()

"""
print("Writing snippets context...")
makeContextCsv(snippets, "snippets_ctxt.csv")
print("Writing reuters context...")
makeContextCsv(reuters, "reuters_ctxt.csv")
print("Done")
"""

def makeContext(file, output_file):
    """ Generate a .cxt file from an input tdm """

    tdm = pd.read_csv(file)
    print("Data loaded")
    rows, cols = tdm.shape
    print("Data shape: " + str(rows) + ", " + str(cols))

    # First section of cxt contains row and column number and list of objects, attributes
    f = open(output_file, "w")
    f.write("B\n\n" + str(rows) + "\n" + str(cols) + "\n\n")

    for i in range(1, rows + 1):
        f.write(str(i) + "\n")

    headers = list(tdm)
    for h in headers:
        f.write(h + "\n")

    print("Header section written")
    # Generate the cross table
    for i in range(rows):
        line = ''
        for h in headers:
            if tdm.ix[i, h] == 0:
                line += '.'
            else:
                line += 'X'
        f.write(line + "\n")

    print("Context complete")
    f.close()

#makeContext(reuters, "reuters.cxt")
makeContext(snippets, "snippets.cxt")