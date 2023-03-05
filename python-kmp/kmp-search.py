text = "12131312212131213121213"
srch = "1213121213"
tikz = ""

prefixf = [0, 0, 1, 0, 1, 2, 3, 2, 3, 4]


def outstring(xcoord, ycoord, s) -> str:
    res = ""
    for i in range(len(s)):
        res += "    \\node[ltr%s] at (%f,%f) {%s};\n" % (s[i], xcoord + i, ycoord, s[i])
    return res


def begin_frame():
    global tikz
    tikz += r"\begin{frame} \frametitle{\kmpstext}"
    tikz += "\n"
    tikz += r"\begin{center} \begin{tikzpicture}[xscale=0.52]"
    tikz += "\n"
    tikz += r"    \draw[opacity=0] (2,0) -- (2,1.35);"
    tikz += "\n"


def end_frame():
    global tikz
    tikz += r"\end{tikzpicture} \end{center} \end{frame}"
    tikz += "\n\n"


tpos = -1
spos = -1

while tpos + len(srch) - spos - 1 < len(text) and spos < len(srch):
    begin_frame()
    tikz += outstring(0, 0, text)
    tikz += outstring(tpos - spos, 1, srch)
    while tpos + 1 < len(text) and spos + 1 < len(srch) and text[tpos + 1] == srch[spos + 1]:
        tpos += 1
        spos += 1
        tikz += "    \\node[rotate=-90] at (%d,0.5) {\\(=\\)};\n" % tpos
    if tpos + 1 < len(text):
        tikz += "    \\node[rotate=-90] at (%d,0.5) {\\(\\ne\\)};\n" % (tpos + 1)
    if spos > -1 and prefixf[spos] > 0:
        tikz += "    \\pause\n"
        tikz += "    \\draw[PaleGreen]\n"
        tikz += "         (%d,1.3) -- ++(-0.35,0) -- ++(0,-0.12) (%d,1.3)\n" % (tpos - spos, tpos - spos)
        tikz += "         -- ++(%d,0) -- ++(0.35,0) -- ++(0,-0.12)\n" % (prefixf[spos] - 1)
        tikz += "         (%d,1.3) -- ++(0.35,0) -- ++(0,-0.12) (%d,1.3)\n" % (tpos, tpos)
        tikz += "         -- ++(-%d,0) -- ++(-0.35,0) -- ++(0,-0.12);\n" % (prefixf[spos] - 1)
        spos = prefixf[spos] - 1
    elif spos == -1:
        tpos += 1
    else:
        spos = -1
    end_frame()

f = open("kmp-search.tex", "w")
f.write(tikz)
f.close()
