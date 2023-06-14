# django_quad_function
Aplikacja tworzy wykresy funkcji kwadratowej / The application creates graphs of quadratic functions

Aplikacja używa poetry, więc aby z tego skorzystać nalezy najpierw zainstalować te narzędzie.

1. Instalujemy poetry na naszym komupetzrze według instrukcji: https://python-poetry.org/docs/
2. Po instalacji należy sprawdzić komendą w konsoli (poetry --version) czy program jest wykrywany na naszym komputerze, jeśli nie, nalezy dodać ściężkę do programu wg. instrukcji w doukentacji.  
3. Klonujemy repozytorium do dowolnego folderu za pomoca: git clone https://github.com/Rachciach/django_quad_function
4. Wchodzimy w folder projektu, który został skolnowany z repozytorium.
5. Następnie uruchamiamy komende: poetry install. Poetry powinno utworzyć środowisko wirtualne wraz z potrzebnymi paczkami użytych w projekcie. 
6. Następnie w konsoli, w folderze projektu wpisujemy kolejną komende: poetry run python manage.py migrate
7. Ostatni krok to uruchomienia serwera aplikacji:  poetry run python manage.py runserver. Aplikacja domyślnie uzywania używa serwera na localhost z portem 8000: [https://127.0.0.1/8000](http://127.0.0.1:8000/)
8. Należy najpierw się zarejestrować przd pierwszym użciem aplikacji. Po wejściu w link http://127.0.0.1:8000/ należy kliknąć przycisk "Register".



Strona powita nas takim komunikatem. Należy się najpierw zalogować. W przypadku, gdy użytkownik nie posiada konta, aplikacja umożliwia mu jego stworzenie. 
      
Widok strony do logowania. 

![image](https://github.com/Rachciach/django_quad_function/assets/73002723/f005923b-486e-43b6-b813-7a4cb3ad8513)

Widok strony do rejestracji. 

![image](https://github.com/Rachciach/django_quad_function/assets/73002723/cb682593-5e04-4eac-9289-9fa9f27b91d7)

Główny widok aplikacji.

![image](https://github.com/Rachciach/django_quad_function/assets/73002723/9b56bccb-74a8-4cd2-b046-2498981e6dee)


Na samym środku strony znajduje się formularz, gdzie należy wprowadzić dane. Formularz wymaga wypełnienia co najmniej pola „example”, reszta jest domyślna. Formularz nie przyjmuje przykładów z dodatkowymi znakami typu „*”, tylko „3x^2+3x+1”. Białe znaki nie mają wpływu na wynik wykresu. 


Pola formularza:

    • example – należy podać jakiś przykład, np „3x^2+3x+1”
      
    • start_x – początek zakresu od którego x ma się rysować wykres
      
    • end_x – koniec zakresu do którego x ma się rysować wykres
      
    • range_plot – co jaką wartość ma być rysowany punkt dla danego zakresu
      
    • x1_range – początkowa wartość x od której ma się zaczynać widok wykresu
      
    • x2_range – końcowa wartość x do której ma się kończyć widok wykresu
      
    • y1_range – początkowa wartość y od której ma się zaczynać widok wykresu
      
    • y2_range – końcowa wartość y do której ma się kończyć widok wykresu

Po kliknięciu przycisku „Resolve” wyświetli się wykres poniżej formularzu dla podanego wcześniej przykładu. 

![image](https://github.com/Rachciach/django_quad_function/assets/73002723/50808de5-d672-4f38-bef1-007e184b0a4e)

Po prawej stronie głównej strony aplikacji znajdują się dwa dodatkowe linki. Pierwszy z nich „Zobacz historie” przeniesienie użytkownika do podstrony, gdzie aplikacja wyświetli cała historię tworzonych wykresów przez użytkownika. Tam wówczas użytkownik może zmienić prywatność wykresu, czy chce żeby wykres był możliwy do wyświetlenia przez innych użytkowników, czy tylko przez niego samego. 

![image](https://github.com/Rachciach/django_quad_function/assets/73002723/68307494-8ca7-42ca-a0ca-f6b75e7e8176)

Drugi link przeniesienie nas do podstrony, gdzie będziemy mogli wyliczyć największą i najmniejszą wartość funkcji dla danego zakresu. 

![image](https://github.com/Rachciach/django_quad_function/assets/73002723/371ffda3-2b85-45d0-8e4c-d7ebcd732921)
