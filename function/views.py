import re
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import transaction
from .models import QuadFunction
from .forms import QuadForm, QuadForm2, NewUserForm
from django.contrib.auth import login
from django.contrib import messages
import matplotlib.pyplot as plt
import numpy as np
import datetime
from django.http import FileResponse

"""
Wyjątek w momencie, gdy widok wykresu będzie za mały
"""
class RangeError(Exception):
    pass
'''
Funckja, która przygotowuje przykład wpisany z formularza pod wzór dla funckji kwadratowej
'''
def prepare(example: str):
    example = example.lower()
    if "x^2" in example:
        if_x = False
        a_b_c = []
        count_minus = 0
        prepare = example.replace(" ", "").lower().replace("x^2", "&1").replace("x", "&1").replace("+", "&+&") \
            .replace("-", "&-&").replace("(", "&(&").replace(")", "&)&").replace("(", "").replace(")", "")


        if len(prepare) > 6 and "&1" in prepare[4:]: #sprwadza czy jest wyrazenie typu x^2+x czy x^1+1
            if_x = True


        func_y = re.split(r'[&]', prepare)
        func_y = [word for word in func_y if word != '']



        for i in range(0, len(func_y)):

            if func_y[i].isdigit() is False:
                if func_y[i] == '-':
                    count_minus += 1
                    func_y[i] = ''

                    if func_y[i + 1].isdigit():
                        if count_minus % 2 != 0:
                            func_y[i] = "-"

                        else:
                            func_y[i] = "+"

                        count_minus = 0


        func_y.append("")
        for i in range(0, len(func_y)):
            if func_y[i].isdigit() and func_y[i + 1].isdigit():
                func_y[i] = str(int(func_y[i]) * int(func_y[i + 1]))
                func_y[i + 1] = ""

        func_y_tmp = []
        func_y = [word for word in func_y if word != '']
        for i in range(0, len(func_y)):
            if func_y[i].isdigit():
                func_y_tmp.append(func_y[i - 1])
                func_y_tmp.append(func_y[i])

        if func_y_tmp[0].isdigit():
            a_b_c.append(int(func_y_tmp[1]))


        for i in range(0, len(func_y_tmp)):
            if func_y_tmp[i] == "+" and func_y_tmp[i + 1].isdigit():
                a_b_c.append(int(func_y_tmp[i + 1]))
            elif func_y_tmp[i] == "-" and func_y_tmp[i + 1].isdigit():
                a_b_c.append(-1 * int(func_y_tmp[i + 1]))
        return a_b_c, if_x

    else:
        print("Function prepare error")


"""
Funkcja wylicza wartości funkcji dla podanego x
"""
def findQuad(args, x):
    try:
        if len(args[0]) == 1:
            return args[0][0] * (x ** 2)
        elif len(args[0]) == 2 and args[1]: #jak jest x^2+x
            return args[0][0] * (x ** 2) + args[0][1] * x
        elif len(args[0]) == 2 and args[1] is False: #jak jest x^2+1
            return args[0][0] * (x ** 2) + args[0][1]
        else:
            return args[0][0] * (x ** 2) + args[0][1] * x + args[0][2]
    except TypeError:
        print("Function findQuad error")

"""
Funkcja tworzy wykres dla podanych wartości
"""
def quad_function(name,exec,start_x,end_x,range_plot, x1=None,x2=None,y1=None,y2=None):

    plt.figure(figsize=(10,8), dpi=100)



    x = np.arange(start_x, end_x, range_plot)
    y = findQuad(prepare(exec), x=x)


    plt.xlabel('oś x')
    plt.ylabel('oś y')
    plt.axhline(y=0, color="#cccccc")
    plt.axvline(x=0, color="#cccccc")
    plt.title(f'Wykres {exec}')

    plt.plot(x, y)

    if x1 != None and x2 != None:
        x1, x2 = int(x1), int(x2)
        if x1 > x2:
            plt.xlim([x2, x1])
        else:
            plt.xlim([x1, x2])


    if y1 != None and y2 != None:
        y1, y2 = int(y1), int(y2)
        if y1 > y2:
            plt.ylim([y2, y1])
        else:
            plt.ylim([y1, y2])


    image = f"plots/{name}.jpg"
    plt.savefig("media/"+image)

    return image, y

"""
Funkcja zwraca stronę, która zawiera informacje, że należy się zalogować
"""
def index(request):
    return render(request, 'main.html')


"""
Funkcja zbiera dane z formularzy i  przekazuje je do funkcji tworzącej wykres oraz do Bazy Danych. Funkcja posiada 
dekorator, który wymusza autoryzacje oraz dekorator atomic.transaction zabezpieczający transakcje, aby nie tworzyć
nowego rekordu, gdy podczas zapisu wystąpi błąd. Funkcja umożliwia również zmiany widoku stworzonego wykresu
z prywatnego na publiczny. W funckji możemy również konfigurować wykres według naszego uznania. 
  
"""
@login_required
def function(request):
    form_quad = QuadForm(request.POST or None, request.FILES or None)
    quads = QuadFunction.objects.all()


    status = False

    with transaction.atomic():
        if form_quad.is_valid():
            func = form_quad.save(commit=False)
            func.user = request.user
            query = QuadFunction.objects.filter(example=request.POST['example'], user=request.user)


            if "x^2" in request.POST['example'].lower() and "*" not in request.POST['example'].lower():
                fun = quad_function( f"{request.user}_{datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S_%f')}",
                                    request.POST['example'], start_x=func.start_x, end_x=func.end_x, range_plot=func.range_plot,
                                    x1=func.x1_range, x2=func.x2_range, y1=func.y1_range, y2=func.y2_range)


                plot = fun[0]



                if query.exists() is False:

                    func.plot = plot
                    func.save()


                elif query.exists():

                    query_new = query[0]
                    query_new.start_x, query_new.end_x, query_new.range_plot, query_new.x1_range, query_new.x2_range,\
                    query_new.y1_range, query_new.y2_range = func.start_x, func.end_x,\
                    func.range_plot, func.x1_range, func.x2_range, func.y1_range, func.y2_range
                    query_new.plot = plot
                    query_new.save()






    if request.method == "POST":

        try:


            if request.POST["name"] == "form_quad" and "x^2" in request.POST['example'].lower():

                status = True
                quads = quads.filter(example=request.POST['example'], user=request.user).order_by('-date')[0]

                example = request.POST['example']
                result = prepare(example)
                if (len(result[0]) == 2 and result[1] == False) or len(result[0]) == 1:
                    p = 0
                    delta = - 4 * result[0][0] * result[0][1]
                    q = (-1*(delta))/(4*result[0][0])

                else:
                    p = (-1 * (result[0][1])) / (2 * result[0][0])
                    delta = (result[0][1]**2 )- 4 * result[0][0] * result[0][2]
                    q = (-1 * (delta)) / (4 * result[0][0])


                rang_y1 = range(int(fun[1].tolist().pop(0)), int(q))
                rang_y2 = range(int(q), int(fun[1].tolist().pop()))


                if func.y1_range != None or func.y2_range != None:
                    if int(func.y1_range) in rang_y1 or int(func.y2_range) in rang_y2:
                        raise RangeError()
                    elif int(func.y2_range) < q:
                        raise RangeError()



        except UnboundLocalError:
            messages.error(request, "W Example został uzyty niedozwolony znak. Proszę spróbować użyć formatu np. 3x^2+2x+1, bez znaku mnożenia *", extra_tags="example")

        except TypeError:
            messages.error(request, "Podano tylko jeden x lub y range z dwóch. Proszę podać całość, np x1_range i x2_range.", extra_tags="type")

        except RangeError:
            messages.error(request, "Wykres wyszedł poza skale. Powiększ wykres", extra_tags="chart")




    return render(request, 'function.html', {"title_of_website": 'Calculate', 'form_quad': form_quad,"quads": quads,
                                              "status": status})

"""
Funkcja umożliwa wyświetlenie historii swoich wykresów na podstronie.
"""
def history(request):
    if request.method == "POST":

        if "form_private" in request.POST["name"].split(" "):
            ob = QuadFunction.objects.get(id=int(request.POST["name"].split(" ")[1]))
            ob.private = False
            ob.save()
        elif "form_public" in request.POST["name"].split(" "):
            ob = QuadFunction.objects.get(id=int(request.POST["name"].split(" ")[1]))
            ob.private = True
            ob.save()


    quads_hist = QuadFunction.objects.filter(user=request.user).order_by('-date')

    return render(request, 'history.html', {"title_of_website": 'History', "quads_hist": quads_hist})

"""
Funkcja umożliwa obliczenie największej i najmniejszej wartości funkcji kwadratowej dla podanego zakresu.
"""
def values(request):
    quads = QuadFunction.objects.filter(user=request.user).order_by('-date')
    form_quad = QuadForm2(initial={"example": quads[0].example, "start_x": quads[0].start_x, "end_x": quads[0].end_x}, instance=QuadFunction)
    status  =False
    max_val = None
    min_val = None
    if request.method == "POST":
        form_quad = QuadForm2(request.POST)
        if form_quad.is_valid():
            status = True
            example = request.POST['example']
            result = prepare(example)
            if (len(result[0]) == 2 and result[1] == False) or len(result[0]) == 1:
                p = 0
            else:
                p = -1*(result[0][1]/(2*result[0][0]))

            start_x = int(request.POST['start_x'])
            end_x = int(request.POST['end_x'])
            rang_x = range(start_x,end_x)

            y1 = findQuad(prepare(example), x=start_x)
            y2 = findQuad(prepare(example), x=end_x)

            if int(p) in rang_x:
                y_p = findQuad(prepare(example), x=p)
            else:
                y_p = None

            max_val = max((y1, y2, y_p))
            min_val = min((y1, y2, y_p))


    return render(request, 'values.html', {"title_of_website": 'Values', 'form_quad': form_quad,
                                              "status": status, "max_val":max_val, "min_val":min_val})




"""
Funkcja umożliwia wyświetlenie wykresu.
"""
def plots(request, file):
    picture = get_object_or_404(QuadFunction, plot='plots/' + file)
    if request.user == picture.user and picture.private or picture.private == False:
        response = FileResponse(picture.plot)
        return response
    return HttpResponse("Nie możesz wyświetlić tej strony z powodu braku dostępu")

"""
Funkcja umożliwia stworzenie nowego konta poprzez formularz
"""
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request, "Rejesestracja zakończona sukcesem")
            return redirect("main")
        messages.error(request, "Coś poszło nie tak")
    form = NewUserForm()
    return render(request, "registration/register.html", {"register_form": form})

