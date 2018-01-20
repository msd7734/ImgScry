import sys

import ImgScry

usage = "usage: ImgScry [options] set_abbreviation\n" +\
        "options:\n" +\
        " -f, --format\t Format output filenames with C-style string formatting.\n" +\
        " -q, --quality\t Image download quality (small, normal, large). Default is normal" +\
        " -s, --skip\t Attempt to skip files that have already been downloaded. Default is true" +\
        " -l, --limit\t Do not download more than this number of cards. Default is no limit"

nameformat = "%s"
def set_nameformat(s):
    global nameformat
    nameformat = s

quality = "normal"
quality_vals = ["small", "normal", "large"]
def set_quality(s):
    global quality
    if s in quality_vals:
        quality = s
    
skip = True
def set_skip(b):
    global skip
    skip = b.upper() == "TRUE"

limit = -1
def set_limit(i):
    global limit
    li = int(i)
    if li < 1:
        limit = -1
    else:
        limit = li

options = {"-f": set_nameformat,
           "--format": set_nameformat,
           "-q": set_quality,
           "--quality": set_quality,
           "-s": set_skip,
           "--skip": set_skip,
           "-l": set_limit,
           "--limit": set_limit}

if len(sys.argv) < 2:
    print usage
# could just match alphanumeric here
elif sys.argv[-1][0] == "-":
    print "Invalid set name"
elif len(sys.argv[1:-1]) % 2 != 0:
    print "Bad number of arguments"
else:
    setabbr = sys.argv[-1]
    i = 1
    for arg in sys.argv[1:-1]:
        if arg in options:
            try:
                options[arg](sys.argv[i+1])
            except ValueError as ve:
                print "The value for " + arg + " was incorrectly formatted."
                sys.exit()
        i += 1
    # print str([setabbr, nameformat, quality, skip, limit])
    ImgScry.run(setabbr, nameformat, quality, skip, limit)
