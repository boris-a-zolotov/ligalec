def outstring(xcoord, ycoord, colr, char):
    return "    \\node[%s] at (%f,%f) {%s};\n" % (colr, 0.8 * xcoord, 0.8 * ycoord, char)


outStr = ""

inStr = "1212121212"
scStr = "12123"

for i in range(len(inStr)):
    outStr += outstring(i, 0.5, "white", inStr[i])

for i in range(len(inStr) - len(scStr) + 1):
    for j in range(len(scStr)):
        if scStr[j] == inStr[i + j]:
            outStr += outstring(i + j, -i - 1, "white", scStr[j])
        else:
            outStr += outstring(i + j, -i - 1, "white,opacity=0.45", scStr[j])

f = open("intikz.tex", "w")
f.write(outStr)
f.close()
