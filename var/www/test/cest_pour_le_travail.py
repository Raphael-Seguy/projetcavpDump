import xlrd

listelundi = []
listemardi = []
listemercredi = []
listejeudi = []
listevendredi = []
def lecture(nom_fichier,nom_feuille):
    fichier = xlrd.open_workbook(nom_fichier)
    #print(fichier.nsheets) Nombres de feuilles
    #print(str(fichier.sheet_names())) Nom des feuilles
    feuille_1 = fichier.sheet_by_name(nom_feuille)
    #print(feuille_1.ncols)
    
    for y in range(0,feuille_1.ncols):
        if(y == 0 or y == 1):
            for x in range(0,feuille_1.nrows):
                if(feuille_1.cell_value(rowx = x,colx = y) != ""):
                    listelundi.append(feuille_1.cell_value(rowx = x, colx = y).split('\n'))
        elif (y == 2 or y == 3):
            for x in range(0,feuille_1.nrows):
                if(feuille_1.cell_value(rowx = x,colx = y) != ""):
                    listemardi.append(feuille_1.cell_value(rowx = x, colx = y).split('\n'))

        elif (y == 4 or y == 5):
            for x in range(0,feuille_1.nrows):
                if(feuille_1.cell_value(rowx = x,colx = y) != ""):
                    listemercredi.append(feuille_1.cell_value(rowx = x, colx = y).split('\n'))

        elif (y == 6 or y == 7):
            for x in range(0,feuille_1.nrows):
                if(feuille_1.cell_value(rowx = x,colx = y) != ""):
                    listejeudi.append(feuille_1.cell_value(rowx = x, colx = y).split('\n'))

        elif (y == 8 or y == 9):
            for x in range(0,feuille_1.nrows):
                if(feuille_1.cell_value(rowx = x,colx = y) != ""):
                    listevendredi.append(feuille_1.cell_value(rowx = x, colx = y).split('\n'))

        





nom_feuille = str(input("Nom de la feuille : "))
lecture("Horaire Cours 2019-2020 IG Q2-Q4.xlsx",nom_feuille)
Lecture("CAVP IG 19-20.xls","IG")

#Affichage de l'horaire du lundi, pour exemple
"""
print(listelundi[0])
for x in range(2,len(listelundi)):
    print(listelundi[x])

"""
