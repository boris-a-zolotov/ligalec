outStr = ""

# inStr = "3221311"
inStr = "2222222"

for i in range(len(inStr)):
    outStr += "  \\node[ltr%s,right,text height=3ex,text depth=1ex] at (2 * %d, 1.5) {%s};\n" % (
        inStr[i], i, inStr[i])

for i in range(len(inStr) - 2):
    hsh = 0
    for j in range(3):
        outStr += "  \\draw (2 * %d, -%d) \\rthtd" % (i + j, i)
        outStr += "{\\textcolor{white}{\\( \\text{\\textcolor{ltr%s}{%s}} \\cdot 3^{%d} \\)}};\n" % (
            inStr[i + j], inStr[i + j], 2 - j)
        hsh += (ord(inStr[i + j]) - 48) * pow(3, 2 - j)
    hsh = hsh % 7
    outStr += "  \\draw (2 * %d + 1.35, -%d) \\rthtd{\\( + \\)}\n" % (i, i)
    outStr += "        (2 * %d + 3.35, -%d) \\rthtd{\\( + \\)}\n" % (i, i)
    outStr += "        (2 * %d + 5.35, -%d) \\rthtd{\\(= %d \\pmod 7 \\)};\n" % (i, i, hsh)

f = open("rabin-karp-coinc.tex", "w")
f.write(outStr)
f.close()
