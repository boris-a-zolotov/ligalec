def outstring(xcoord, ycoord, colr, char):
    return "    \\node[%s] at (%f,%f) {%s};\n" % (colr, 0.8 * xcoord, 0.8 * ycoord, char)


outStr = ""

inStr = "1212121212"
scStr = "12123"

for i in range(len(inStr)):
    outStr += outstring(i, 0, "white", inStr[i])


f = open("intikz.tex", "w")
f.write(outStr)
f.close()
