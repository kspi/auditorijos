Naudojimas:

Pirma reikia paleisti „dump_timetable.py“, kuris surenka duomenis iš
tvarkaraščių tinklalapio į „timetable.txt“. Tada reikia paleisti
„make_page.py“, kuris sugeneruoja „index.html“ bylą „output“ papkėje,
kurioje yra visos jam reikalingos bylos.

„dump_timetable.py“ programai reikia BeautifulSoup modulio iš
http://www.crummy.com/software/BeautifulSoup/ . Python programos
testuotos su Python 2.7. Jei naudojate Ubuntu ar Debian, tai turėtų
užtėkti su apt-get užinstaliuoti paketą „python-beautifulsoup“ ir
paleisti programas auksčiau aprašyta tvarka:

    sudo apt-get install python-beautifulsoup
    python dump_timetable.py
    python make_page.py
