from django.shortcuts import render

izdelki = [
    {
        'avtor': 'Luigi Ademollo',
        'naslov': 'Fresco Decoration',
        'vsebina': 'https://www.wga.hu/art/a/ademollo/siena2.jpg',
        'datum': '1800-1810',
        'url': '/1'
    },
    {
        'avtor': 'Martin Zürn',
        'naslov': 'Madonna with Child',
        'vsebina': 'https://www.wga.hu/art/z/zurn/martin/madchil.jpg',
        'datum': '1601-1650',
        'url': '/2'
    },
]


def home(request):
    popularno = {
        'izdelki': izdelki
    }
    return render(request, 'homepage/home.html', popularno)


def about(request):
    return render(request, 'homepage/about.html', {'naslov': 'About'})


def fresco(request):
    return render(request, 'homepage/1.html', {'naslov': 'Fresco'})

def madonna(request):
    return render(request, 'homepage/2.html', {'naslov': 'Madonna'})