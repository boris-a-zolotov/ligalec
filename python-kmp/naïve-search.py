def outstring(xcoord, ycoord, opaq, char):
    return "    \\node[ltr%s, opacity=%s] at (%f,%f) {%s};\n" % (char, opaq, 0.8 * xcoord, 0.8 * ycoord, char)


outStr = ""

inStr = "1212121212"
scStr = "12123"

for i in range(len(inStr)):
    outStr += outstring(i, 0.5, "1", inStr[i])

for i in range(len(inStr) - len(scStr) + 1):
    for j in range(len(scStr)):
        if scStr[j] == inStr[i + j]:
            outStr += outstring(i + j, -i - 1, "1", scStr[j])
        else:
            outStr += outstring(i + j, -i - 1, "0.45", scStr[j])

f = open("naïve-search.tex", "w")
f.write(outStr)
f.close()
