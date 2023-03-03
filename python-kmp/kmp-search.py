text = "12131312212131213121213"
srch = "1213121213"
tikz = ""

prefixf = [0, 0, 1, 0, 1, 2, 3, 2, 3, 4]


def outstring(xcoord, ycoord, s) -> str:
    res = ""
    for i in range(len(s)):
        res += "    \\node at (%f,%f) {%s};\n" % (xcoord + i, ycoord, s[i])
    return res


def begin_frame():
    global tikz
    tikz += r"\begin{frame} \frametitle{ }"
    tikz += "\n"
    tikz += r"\begin{center} \begin{tikzpicture}[xscale=0.52]"
    tikz += "\n"
    tikz += r"    \draw[opacity=0] (2,-0.5) -- (2,5);"
    tikz += "\n"


def end_frame():
    global tikz
    tikz += r"\end{tikzpicture} \end{center} \end{frame}"
    tikz += "\n\n"


tpos = -1
spos = -1

begin_frame()

while tpos + len(srch) - spos - 1 < len(text) and spos < len(srch):
    print(tpos, spos)
    tikz += outstring(0, 0, text)
    tikz += outstring(tpos - spos, 1, srch)
    while tpos + 1 < len(text) and spos + 1 < len(srch) and text[tpos + 1] == srch[spos + 1]:
        tpos += 1
        spos += 1
        tikz += "    \\node[rotate=-90] at (%d,0.5) {\\(=\\)};\n" % tpos
    if tpos + 1 < len(text):
        tikz += "    \\node[rotate=-90] at (%d,0.5) {\\(\\ne\\)};\n" % (tpos + 1)
    end_frame()
    if tpos + 1 < len(text):
        begin_frame()
    if spos != -1:
        tikz += "    \\draw[Crimson,->] (%d,1.4) to[out=35,in=145] (%d,1.4);\n" % (
            tpos, tpos + spos - prefixf[spos] + 1)
        spos = prefixf[spos] - 1
    else:
        tpos += 1

f = open("kmp-search.tex", "w")
f.write(tikz)
f.close()
