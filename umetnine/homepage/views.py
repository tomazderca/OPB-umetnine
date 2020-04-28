from django.shortcuts import render

izdelki = [
    {
        'avtor': 'Tip1',
        'naslov': 'Zelena Veja',
        'vsebina': 'Slika',
        'datum': 'danes'
    },
{
        'avtor': 'Tip2',
        'naslov': 'Rdeca Veja',
        'vsebina': 'Kip',
        'datum': 'vceraj'
    },
]

def home(request):
    popularno = {
        'izdelki': izdelki
    }
    return render(request, 'homepage/home.html', popularno)


def about(request):
    return render(request, 'homepage/about.html', {'naslov': 'About'})

