from openpyxl import load_workbook

liste = []
listesecondaire = []

def recup (nom_fichier, liste):
    wb = load_workbook(nom_fichier, read_only = True)
    ws = wb.active
    for i, row in enumerate(ws.rows):
        liste.append([])
        for cell in row:
            if(cell.value != None):
                liste[i].append(cell.value)
                
def nettoyer(liste,listesecondaire):
    for x in range(0,len(liste)):
        if(len(liste[x])!= 0):
            listesecondaire.append(liste[x])
            
    
recup("Horaire Cours 2019-2020 IG Q2-Q4.xlsx",liste)
nettoyer(liste,listesecondaire)





