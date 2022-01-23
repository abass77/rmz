# liste_region = ['dakar','louga','tamba']
# list_test = ['255','100','1000' ]
# if 'dakar' in liste_region:
#     print('oui')
# else:
#     print('non')
#
# for i in liste_region:
#     print (i)
# #pour aficher chak element et son index
# for index,valeur in enumerate(liste_region):
#     print(index,valeur)
# for a,b in zip(liste_region,list_test):
#     print(a,b)
#
# print(list_test)
#
#
#
# def fib(n):
#     a = 0
#     b = 1
#     list_fib=[]
#     while a < n:
#         list_fib.append(a)
#         a,b = b,a+b
#     print(list_fib)
# fib(1000)


# #dictionn
# classeur = {
#     "positif":[],
#     "negatif":[],
# }
# def trier(classeur,nombre):
#     if nombre < 0:
#         classeur['negatif'].append(nombre)
#     else:
#         classeur['positif'].append(nombre)
#     return classeur
# trier(classeur,7)
# print (classeur.values())

#dictionnaire liste comprehention
import time
#
# liste_1= []
# for i in range(100000000):
#     liste_1.append(i**2)

# start =time.time()
# liste_2=[i**2 for i in range(10)]
# #print(liste_2)
# end=time.time()
# print(end-start)
#ON UTILISE LES LISTES COMPREHENTION POUR SIMPLIFIER LE CODE
#DIMINUER LE TEMP D EXECUTION

#liste_2#AUTRE AVANTAGE DES LISTE COMPRENTION EST POUR CREER DES NESTED LIST
#UN NESTED EST UN LIST QUI COMPREND D AUTRE LISTE

# LISTE_3= [[ i for i in range(3) ] for j in range(3) ]
# print(LISTE_3)

#dictionnaire comprehention

# prenom=['piere','jean','julie' ,'sophie']
# # dico= {k:v for k,v in enumerate(prenom)}
# # print(dico)
# # print(dico.values() )
# # print(dico.keys())
# # dico.values()
#
# ages=[24,62,10,23]
# dico2={prenom:ages for prenom,ages in zip(prenom,ages)}
#
# print(dico2)



# tuple_1=tuple(((i**2 for i in range(10)) ))
# print(tuple_1)

# classeur = {
#     "positive":[],
#     "negative":[]
# }
# def trier (classeur,nombre):
#     if nombre >=0:
#         classeur["positive"].append(nombre)
#     else:
#         classeur["negative"].append(nombre)
#     return classeur
#
# print(trier(classeur,676) )



#x=3.14
#print(round(x))

#round arondi la valeur decima
# la fonction abs retourne la valeur absolue de 3
# #fonction open
# f=  open('ficher.text','w')
# f.write('ibnou abass ')
# f.close()
# f.open('ficher.text', 'r')
# print(f.read())
# f.close
with open ('ficher.text' , 'w') as f:
    for i in range(10):
        f.write("{})^2={} \n" .format(i,i**2))


