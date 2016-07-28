print r'\documentclass{beamer}\begin{document}'

def frame_1(path):
    print r'\begin{frame}'
    print r'\includegraphics[width=\textwidth]{%s}' % path
    print r'\end{frame}'

frame_1('1800_5000_100_line.png')
frame_1('1600_5000_500_line.png')
frame_1('1400_5000_800_line.png')

def frame_4(path_ul, path_ur, path_dl, path_dr):
    print r'\begin{frame}'
    print r'\begin{columns}'
    print r'\begin{column}{0.5\textwidth}'
    print r'\includegraphics[width=\textwidth]{%s} \\' % path_ul
    print r'\includegraphics[width=\textwidth]{%s}' % path_dl
    print r'\end{column}'
    print r'\begin{column}{0.5\textwidth}'
    print r'\includegraphics[width=\textwidth]{%s} \\' % path_ur
    print r'\includegraphics[width=\textwidth]{%s}' % path_dr
    print r'\end{column}'
    print r'\end{columns}'
    print r'\end{frame}'

def frame_2(path_l, path_r):
    print r'\begin{frame}'
    print r'\begin{columns}'
    print r'\begin{column}{0.5\textwidth}'
    print r'\includegraphics[width=\textwidth]{%s}' % path_l
    print r'\end{column}'
    print r'\begin{column}{0.5\textwidth}'
    print r'\includegraphics[width=\textwidth]{%s}' % path_r
    print r'\end{column}'
    print r'\end{columns}'
    print r'\end{frame}'


frame_4(
    '1800_5000_100_triangle_gbb_A.png',
    '1800_5000_100_triangle_gbb_B.png',
    '1800_5000_100_triangle_gtt_0l_A.png',
    '1800_5000_100_triangle_gtt_0l_B.png'
)
frame_2(
    '1800_5000_100_triangle_gtt_1l_A.png',
    '1800_5000_100_triangle_gtt_1l_B.png'
)

frame_4(
    '1600_5000_500_triangle_gbb_A.png',
    '1600_5000_500_triangle_gbb_B.png',
    '1600_5000_500_triangle_gtt_0l_A.png',
    '1600_5000_500_triangle_gtt_0l_B.png'
)
frame_2(
    '1600_5000_500_triangle_gtt_1l_A.png',
    '1600_5000_500_triangle_gtt_1l_B.png'
)


frame_4(
    '1400_5000_800_triangle_gbb_A.png',
    '1400_5000_800_triangle_gbb_B.png',
    '1400_5000_800_triangle_gtt_0l_A.png',
    '1400_5000_800_triangle_gtt_0l_B.png'
)
frame_2(
    '1400_5000_800_triangle_gtt_1l_A.png',
    '1400_5000_800_triangle_gtt_1l_B.png'
)


print r'\end{document}'
