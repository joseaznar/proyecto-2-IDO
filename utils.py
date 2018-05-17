from random import randint, random as rd
import pandas as pd
from datetime import datetime
import numpy

"""
En este archvo se tienen las funciones necesarias para implementar un algoritmo genético para varios
problemas predeterminados. 
"""


def random_ag(n, k):
    """
    Método que genera una población de tamaño n de forma "aleatoria" para el problema de mcbella
    :param n: tamaño de la población deseado
    :param k: número de pintalabios existentes
    :return: lista con la población generada o lista vacia en caso de no haber podido generarlo
    """
    # definimos una bandera que nos indique si terminó el método y un número máximo de iteraciones
    flag = True
    maxiter = n*n*n

    # vamos a iterar hasta tener la muestra deseada o cumplir el número máximo de iteraciones
    i = 0
    poblacion = []
    while flag and i < maxiter:
        fen = list()

        # generamos un número aleatorio de los k-1 valores posibles para la posición 1
        fen.append(randint(2, k))

        # iteramos hasta tener los k valores validos para este fenotipo y que no se repita
        # el fenotipo en la población
        cont = 1

        while cont < k:
            # generamos un aleatorio
            var = randint(1, k)

            # si nos sale el valor de la posición en la que estamos o se repite el valor
            if var == cont + 1 or var in fen:
                # si es la última posición y solo queda el 5 volvemos a empezar
                if var == k and cont + 1 == k:
                    break
                continue
            else:
                # en otro caso lo agregamos al fenotipo y aumentamos el contador
                fen.append(var)
                cont = cont + 1

        # si es la última posición y solo queda el último valor por poner volvemos a empezar
        if cont < k:
            continue

        # ahora revisamos si el fenotipo ya lo habíamos generado
        if fen in poblacion:
            i = i + 1
            continue
        else:
            # checamos si se tiene un ciclo
            if checa_ciclo(fen):
                i = i + 1
                continue
            else:
                # tenemos un fenotipo válido que no se repite, entonces lo agregamos a
                # la población, aumentamos le contador y revisamos si ya tenemos los n
                # fenotipos
                i = i + 1
                poblacion.append(fen)
                flag = not len(poblacion) == n

    # si no terminamos regresamos la lista vacia
    if flag:
        poblacion = list()

    return poblacion


def checa_ciclo(fen):
    """
    Método que revisa si existe un ciclo en el fenotipo dado.
    Notar que siempre se empieza en el tipo 1
    :param fen: fenotipo parcial (o total) a revisar
    :return: verdadero en caso que haya ciclo o falso en otro caso
    """
    # vamos a intentar seguir el camino de ciudades y ver si regresamos a alguna de las visitadas
    visitadas = []

    city = 1
    flag = False
    for i in range(1, len(fen)+1):
        # agregamos la ciudad a visitar
        city = fen[int(city-1)]

        # revisamos si ya visitamos la ciudad, lo que implicaría que hay un ciclo
        if city in visitadas:
            flag = True
            break

        # en caso de no ser un ciclo la agregamos
        visitadas.append(city)

    return flag


def fitness_mcbella(fen):
    """
    Método que calcula el fitness de un fenotipo dado
    :param fen: fenotipo a calcular
    :return: valor del fitness
    """
    # ponemos los valores de la matriz dada en la descripcion del problema
    f = [
        [0, 2, 2, 3, 4, 5, 4, 3, 5, 6],
        [2, 0, 1, 3, 3, 4, 6, 4, 3, 5],
        [2, 1, 0, 4, 5, 3, 2, 4, 1, 7],
        [3, 3, 4, 0, 2, 4, 5, 3, 5, 2],
        [4, 3, 5, 2, 0, 2, 4, 1, 2, 2],
        [5, 4, 3, 4, 2, 0, 3, 2, 1, 3],
        [4, 6, 2, 5, 4, 3, 0, 3, 2, 1],
        [3, 4, 4, 3, 1, 2, 3, 0, 5, 3],
        [5, 3, 1, 5, 2, 1, 2, 5, 0, 4],
        [6, 5, 7, 2, 2, 3, 1, 3, 4, 0],
    ]

    # sumamos los valores dada la función f
    suma = 0
    for i in range(0, len(fen)):
        suma = suma + f[i][int(fen[i]-1)]

    return suma


def crossover(fen_1, fen_2):
    """
    Método que combina dos fenotipos de forma aleatoria.
    :param fen_1: fenotipo 1
    :param fen_2: fenotipo 2
    :return: fenotipo nuevo cruzado o una lista vacia si se alcanzó el máximo de iteraciones
    """
    # iteramos hasta encontrar un fenotipo generado por los dados que no tenga algun ciclo
    flag = True
    fen = []
    cont = 0
    maxiter = len(fen_1)*len(fen_1)*len(fen_1)
    i = 0
    while flag and i < maxiter:
        var = rd()

        # si el valor es menor a 0.5 tomamos de fen_1
        if var <= 0.5:
            # revisamos que no esté en el arreglo
            if fen_1[cont] in fen:
                # en caso de estarlo iteramos hasta encontrar uno que no esté en el fenotipo nuevo
                # y sea valido
                while True:
                    # generamos el numero aleatorio
                    aux = randint(1, len(fen_1))

                    if aux in fen or aux == cont + 1:
                        # si ya nos ciclamos, nos salimos
                        if aux == len(fen_1) and cont + 1 == len(fen_1):
                            break
                        else:
                            # si no nos hemos ciclado volvemos a intentar
                            continue
                    else:
                        # si encontramos un valor válido lo ponemos
                        fen.append(aux)
                        cont = cont + 1
                        break
            else:
                # si no está en el arreglo lo agregamos
                fen.append(fen_1[cont])
                cont = cont + 1
        else:
            # revisamos que no esté en el arreglo
            if fen_2[cont] in fen:
                # en caso de estarlo iteramos hasta encontrar uno que no esté en el fenotipo nuevo
                # y sea valido
                while True:
                    # generamos el numero aleatorio
                    aux = randint(1, len(fen_2))

                    # vemos que no esté en el fenotipo nuevo y sea valido
                    if aux in fen or aux == cont + 1:
                        # si ya nos ciclamos, nos salimos
                        if aux == len(fen_2) and cont + 1 == len(fen_2):
                            break
                        else:
                            # si no nos hemos ciclado volvemos a intentar
                            continue
                    else:
                        # si encontramos un valor válido lo ponemos
                        fen.append(aux)
                        cont = cont + 1
                        break
            else:
                # si no está en el arreglo lo agregamos
                fen.append(fen_2[cont])
                cont = cont + 1

        # revisamos si ya terminamos
        flag = not len(fen_2) == len(fen)

        # si ya terminamos checamos si tiene un ciclo, en caso afirmativo volvemos a empezar
        if not flag and checa_ciclo(fen):
            fen = []
            flag = True
            cont = 0

        i = i + 1

    # revisamos si terminó o no
    if i >= maxiter:
        fen = []

    return fen


def algoritmo_genetico(iteraciones, n, k, fitness):
    """
    Método que implementa el algoritmo genético dadas las funciones que vienen como parámetros
    :param iteraciones: numero de iteraciones a realizar
    :param n: tamaño de la población
    :param k: tamaño de cada fenotipo
    :param fitness: función que evalua el fitness de un fenotipo dado
    :return: el mejor valor encontrado
    """
    t_0 = datetime.now()
    print("Inicia el método: " + str(t_0))
    # inicializamos la variable donde guardaremos el mejor optimo encontrado
    min_global = 10e8
    fen_min = []

    flag = True
    i = 0

    # generamos la muestra hasta que no regrese vacia, hacemos tres intentos
    cont = 0
    pob = []
    t_1 = datetime.now()
    while len(pob) == 0 and cont < 3:
        print("Generamos población inicial: " + str((t_1 - t_0).seconds))
        pob = random_ag(n, k)
        cont = cont + 1

    t_2 = datetime.now()
    print("Empezamos las iteraciones pedidas: " + str((t_2 - t_1).seconds))

    # iteramos el número de veces que viene en el parámetro
    while i < iteraciones:
        print("Iteración: " + str(i))
        print("Mínimo: " + str(min_global))

        # ponemos los datos en un dataframe
        poblacion = pd.DataFrame(data=pob)

        i = i + 1

        # calculamos el fitness de cada fila
        poblacion["fitness"] = poblacion.apply(lambda row: fitness(row), axis=1)

        # ordenamos con respecto a eso
        poblacion = poblacion.sort_values(by="fitness")

        # vemos si tenemos un minimo globla, lo guardamos si es el caso
        if poblacion.iloc[0]["fitness"] < min_global:
            min_global = poblacion.iloc[0]["fitness"]
            fen_min = list(poblacion.iloc[0][0:k])

        # calculamos la proba con respecto al fitness
        poblacion["proba"] = poblacion.apply(lambda row: 1-(0.9)*row["fitness"]/poblacion.iloc[n-1]["fitness"], axis=1)

        # revolvemos la muestra para darle más oportunidad a todos de salir
        poblacion.sample(frac=1)

        # iteramos hasta tener la nueva muestra
        j = 0
        pob = []
        while j < n:
            # ahora iteramos para obtener un crossover exitoso
            num = 0
            fen_1 = []
            fen_2 = []
            for elem in range(1, len(poblacion["proba"])):
                var = rd()

                if num == 0 and poblacion.iloc[elem]["proba"] > var:
                    fen_1 = list(poblacion.iloc[elem][0:k])
                    num = 1
                elif num == 1 and poblacion.iloc[elem]["proba"] > var:
                    fen_2 = list(poblacion.iloc[elem][0:k])
                    num = 2
                    break

            # si sacamos dos elementos de la muestra intentamos obtener un cruze
            feno = []
            if num == 2:
                feno = crossover(fen_1, fen_2)

            # si obtenemos una muestra exitosa y no la tenemos ya,
            # entonces la guardamos y aumentamos el contador
            if len(feno) > 0 and feno not in pob:
                pob.append(feno)
                j = j + 1

    t_4 = datetime.now()
    print("Duración total del método (s): " + str((t_4 - t_0).seconds))

    return [min_global, fen_min]


def fitness_ciudades(fen):
    """
    Método que calcula la función fitness para un fenotipo con putnos en R^2
    con la norma ecuclidiana (norma dos)
    :param fen: fenotipo indicando el orden de las ciudades a recorrer
    :return: valor real con el fitness
    """
    # abrimos el archivo con las coordenadas de las ciudades
    ciudades = open('berlin52.txt', 'r')
    ciudades = [[int(float(num)) for num in line.split(' ')] for line in ciudades if line != 'EOF\n' and line != 'EOF']

    # calculamos el valor sumando la distancia euclidiana por cada ciudad a visitar
    i = 0
    suma = 0
    for city in fen:
        x = list()
        x.append(ciudades[i][2])
        x.append(ciudades[i][1])

        y = list()
        y.append(ciudades[int(city-1)][2])
        y.append(ciudades[int(city-1)][1])

        coord = numpy.array([x, y])

        suma = suma + numpy.linalg.norm(coord)

        i = i + 1


    return suma

