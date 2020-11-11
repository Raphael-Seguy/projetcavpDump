#!/usr/bin/env python
# enable debugging

import cgitb

import os

import xlrd

import requests

import pymysql as mariadb

cgitb.enable()

print("Content-Type:text/html;charset=utf-8")
print()

hostname = 'localhost'
username = 'spectator'
password = 'Test'
database = 'WebsiteDB'
connection = mariadb.connect(host=hostname,
                             user=username,
                             password=password,
                             db=database,
                             charset='utf8mb4',
                             cursorclass=mariadb.cursors.DictCursor)

print("Hello Traveller")
listelundi = []
listemardi = []
listemercredi = []
listejeudi = []
listevendredi = []

UEStockpile = []
AAStockpile = []
CoursStockpile =[]

tpleIndexQuad1 = (0,0)
tpleIndexQuad2 = (0,0)
tpleIndexQuad3 = (0,0)
tpleIndexQuad4 = (0,0)
tpleIndexQuad5 = (0,0)
tpleIndexQuad6 = (0,0)

class UE:
    def __init__(self,name,quad,credit,x,y,special):
        self.name = name
        self.quad = quad
        self.credit = credit
        self.pos = (x,y)
        self.special = special
class AA:
    def __init__(self,name,quad,heure,x,y):
        self.name = name
        self.quad = quad
        if(heure!=""):
            self.heure = heure
        else:
            self.heure = -1
        self.pos = (x,y)
class Cours:
	def __init__(self,name,quad,jour,start,end,room,other):
		self.name = name
		self.quad = quad
		self.jour = jour
		self.room = room
		self.start = start
		self.end = end
		self.other = other
  
def Lecture(nom_fichier,nom_feuille):
    fichier = xlrd.open_workbook(nom_fichier)
    feuille_1 = fichier.sheet_by_name(nom_feuille)
    iCols = int(feuille_1.ncols)
    iRows = int(feuille_1.nrows)
    for y in range(iRows):
        for x in range(iCols):
            if(feuille_1.cell_value(rowx = y, colx = x)!=""):
                if(type(feuille_1.cell_value(rowx = y, colx = x))==str):
                    if(feuille_1.cell_value(rowx = y, colx = x).find("Quadrimestre")!=-1):
                        if(feuille_1.cell_value(rowx = y, colx = x).find("1")!=-1):
                            tpleIndexQuad1 = (x,y)
                        elif(feuille_1.cell_value(rowx = y, colx = x).find("2")!=-1):
                            tpleIndexQuad2 = (x,y)
                        elif(feuille_1.cell_value(rowx = y, colx = x).find("3")!=-1):
                            tpleIndexQuad3 = (x,y)
                        elif(feuille_1.cell_value(rowx = y, colx = x).find("4")!=-1):
                            tpleIndexQuad4 = (x,y)
                        elif(feuille_1.cell_value(rowx = y, colx = x).find("5")!=-1):
                            tpleIndexQuad5 = (x,y)
                        elif(feuille_1.cell_value(rowx = y, colx = x).find("6")!=-1):
                            tpleIndexQuad6 = (x,y)
    for y in range(iRows):
        for x in range(iCols):
            if(feuille_1.cell_value(rowx = y, colx = x)!=""):
                if(type(feuille_1.cell_value(rowx = y, colx = x))==str):
                    if(feuille_1.cell_value(rowx = y, colx = x).startswith("UE") and feuille_1.cell_value(rowx = y, colx = x).find(">")==-1 and feuille_1.cell_value(rowx = y, colx = x).find("<")==-1):
                        if(feuille_1.cell_value(rowx = y, colx = x-2)!=""):    
                            sPre=feuille_1.cell_value(rowx = y, colx = x-2)
                        else:
                            sPre=""
                        if(feuille_1.cell_value(rowx = y, colx = x+3)!=""):
                            sCo = feuille_1.cell_value(rowx = y, colx = x+3)
                        else:
                            sCo=""
                        QuadRef = (tpleIndexQuad1,tpleIndexQuad2,tpleIndexQuad3,tpleIndexQuad4,tpleIndexQuad5,tpleIndexQuad6)
                        Quad=GetQuad(QuadRef,x,y)
                        temp = UE(feuille_1.cell_value(rowx = y, colx = x),Quad,feuille_1.cell_value(rowx = y, colx = x-1),x,y,"%s#%s"%(sPre,sCo))
                        UEStockpile.append(temp)
                    else:
                        if(feuille_1.cell_value(rowx = y, colx = x).find("ECTS")==-1 and feuille_1.cell_value(rowx = y, colx = x).find("Quadrimestre")==-1 and y<53):
                            if(x==tpleIndexQuad1[0] and y>=tpleIndexQuad1[1] and y<=tpleIndexQuad2[1]):
                                temp = AA(feuille_1.cell_value(rowx = y, colx = x),"Q1",feuille_1.cell_value(rowx = y, colx = x+3),x,y)
                                AAStockpile.append(temp)
                            elif(x==tpleIndexQuad1[0] and y>tpleIndexQuad2[1]):
                                temp = AA(feuille_1.cell_value(rowx = y, colx = x),"Q2",feuille_1.cell_value(rowx = y, colx = x+3),x,y)
                                AAStockpile.append(temp)
                            elif(x==tpleIndexQuad3[0] and y>=tpleIndexQuad3[1] and y<=tpleIndexQuad4[1]):
                                temp = AA(feuille_1.cell_value(rowx = y, colx = x),"Q3",feuille_1.cell_value(rowx = y, colx = x+3),x,y)
                                AAStockpile.append(temp)
                            elif(x==tpleIndexQuad3[0] and y>tpleIndexQuad4[1]):
                                temp = AA(feuille_1.cell_value(rowx = y, colx = x),"Q4",feuille_1.cell_value(rowx = y, colx = x+3),x,y)
                                AAStockpile.append(temp)
                            elif(x==tpleIndexQuad5[0] and y>=tpleIndexQuad5[1] and y<=tpleIndexQuad6[1]):
                                temp = AA(feuille_1.cell_value(rowx = y, colx = x),"Q5",feuille_1.cell_value(rowx = y, colx = x+3),x,y)
                                AAStockpile.append(temp)
                            elif(x==tpleIndexQuad5[0] and y>tpleIndexQuad6[1]):
                                temp = AA(feuille_1.cell_value(rowx = y, colx = x),"Q6",feuille_1.cell_value(rowx = y, colx = x+3),x,y)
                                AAStockpile.append(temp)
                        
def lecture(nom_fichier,nom_feuille):
    fichier = xlrd.open_workbook(nom_fichier)
    #print(fichier.nsheets) Nombres de feuilles
    #print(str(fichier.sheet_names())) Nom des feuilles
    feuille_1 = fichier.sheet_by_name(nom_feuille)
    #print(feuille_1.ncols)
    tpleLundi = (0,0)
    tpleMardi = (0,0)
    tpleMercredi = (0,0)
    tpleJeudi = (0,0)
    tpleVendredi = (0,0)
    quad = nom_feuille.split(" ")[1]
    
    for x in range(feuille_1.ncols):
        for y in range(feuille_1.nrows):
            if(feuille_1.cell_value(rowx = y,colx = x)!=""):
                if(feuille_1.cell_value(rowx = y,colx = x).find("LUNDI")!=-1):
                    tpleLundi = (x,y)
                elif(feuille_1.cell_value(rowx = y,colx = x).find("MARDI")!=-1):
                    tpleMardi = (x,y)
                elif(feuille_1.cell_value(rowx = y,colx = x).find("MERCREDI")!=-1):
                    tpleMercredi = (x,y)
                elif(feuille_1.cell_value(rowx = y,colx = x).find("JEUDI")!=-1):
                    tpleJeudi = (x,y)
                elif(feuille_1.cell_value(rowx = y,colx = x).find("VENDREDI")!=-1):
                    tpleVendredi = (x,y)
    for x in range(feuille_1.ncols):
        for y in range(feuille_1.nrows):
            if(feuille_1.cell_value(rowx = y,colx = x)!=""):
                information = feuille_1.cell_value(rowx = y,colx = x).split("\n")
                index=0
                nom = ""
                room = ""
                time = ""
                extra = ""
                bTimeFound = False
                for element in (information):
                    if(element.find("•")!=-1) and index<=4 :
                        room = element
                        guess = "•"
                        occurences = room.count(guess)
                        indices = [i for i, a in enumerate(room) if a == guess]
                        room = room[indices[0]+1:indices[1]]
                    elif index<2:
                        if(element.find("-")!=-1 and not bTimeFound):
                            time = element
                            bTimeFound=True
                        else:
                            nom = element
                    else:
                        extra+=element+"#"
                    index+=1
                extra = extra[0:len(extra)-2]
                if(y>tpleLundi[1]+1 and x>=tpleLundi[0] and x<tpleMardi[0]):
                    temp = Cours(nom,quad,"LUNDI",time.split("-")[0],time.split("-")[1],room,extra)
                    CoursStockpile.append(temp)
                elif(y>tpleMardi[1]+1 and x>=tpleMardi[0] and x<tpleMercredi[0]):
                    temp = Cours(nom,quad,"MARDI",time.split("-")[0],time.split("-")[1],room,extra)
                    CoursStockpile.append(temp)
                elif(y>tpleMercredi[1]+1 and x>=tpleMercredi[0] and x<tpleJeudi[0]):
                    temp = Cours(nom,quad,"MERCREDI",time.split("-")[0],time.split("-")[1],room,extra)
                    CoursStockpile.append(temp)
                elif(y>tpleJeudi[1]+1 and x>=tpleJeudi[0] and x<tpleVendredi[0]):
                    temp = Cours(nom,quad,"JEUDI",time.split("-")[0],time.split("-")[1],room,extra)
                    CoursStockpile.append(temp)
                elif(y>tpleVendredi[1]+1 and x>=tpleVendredi[0] and x<feuille_1.ncols-1):
                    temp = Cours(nom,quad,"VENDREDI",time.split("-")[0],time.split("-")[1],room,extra)
                    CoursStockpile.append(temp)
def GetQuad(QuadPos,x,y):
    if(QuadPos[0][0]<=x and QuadPos[2][0]>x and QuadPos[1][1]>y):
        return "Q1"
    elif(QuadPos[1][0]<=x and QuadPos[3][0]>x and QuadPos[3][1]<=y):
        return "Q2"
    elif(QuadPos[2][0]<=x and QuadPos[4][0]>x and QuadPos[1][1]>y):
        return "Q3"
    elif(QuadPos[3][0]<=x and QuadPos[5][0]>x and QuadPos[5][1]<=y):
        return "Q4"
    elif(QuadPos[4][0]<=x and QuadPos[5][1]>y):
        return "Q5"
    else:
        return "Q6"


def GetUE(UE,x,y):
    parent = ""
    OldDistance=None
    for element in(UE):
        if(x==element.pos[0]-1):
            if(y>element.pos[1]):
                NewDistance = abs(y-element.pos[1])
                if(OldDistance==None or NewDistance<OldDistance):
                    parent = element.name
                    OldDistance = NewDistance
            
    return parent        
#print(MakeGetRequest("request=UE"))
nom_feuille = str("IG Q2")
lecture("Horaire Cours 2019-2020 IG Q2-Q4.xlsx",nom_feuille)
nom_feuille = str("IG Q4")
lecture("Horaire Cours 2019-2020 IG Q2-Q4.xlsx",nom_feuille)
Lecture("CAVP IG 19-20.xls","IG")
try:


    with connection.cursor() as cursor:

        
        # SQL
        for element in (CoursStockpile):
            sqlCheckExist = "SELECT idCours FROM cours WHERE nom = (%s) AND quadri = (%s) AND jour = (%s) AND start = (%s) AND end = (%s) AND room = (%s)"
            val = (element.name,element.quad,element.jour,element.start,element.end,element.room)
            cursor.execute(sqlCheckExist,val)
            connection.commit()
            if(cursor.rowcount<1):
                sqlInsertCours = "INSERT INTO cours(nom,quadri,jour,start,end,room) VALUES (%s,%s,%s,%s,%s,%s)"
                val = (element.name,element.quad,element.jour,element.start,element.end,element.room)
                cursor.execute(sqlInsertCours,val)
                connection.commit()

        for element in(UEStockpile):
            sqlCheckExist = "SELECT idUE FROM ue WHERE nom = (%s) AND quad = (%s) AND ects = (%s)"
            val = (element.name,element.quad,element.credit)
            cursor.execute(sqlCheckExist,val)
            connection.commit()
            if(cursor.rowcount<1):
                sqlInsertUE = "INSERT INTO ue(nom,quad,ects) VALUES (%s,%s,%s)"
                val = (element.name,element.quad,element.credit)
                cursor.execute(sqlInsertUE,val)
                connection.commit()
                   
        QuadRef = (tpleIndexQuad1,tpleIndexQuad2,tpleIndexQuad3,tpleIndexQuad4,tpleIndexQuad5,tpleIndexQuad6)
        for element in (AAStockpile):
            sqlGetIdUE = "SELECT idUE FROM ue WHERE nom = (%s)"
            val =(str(GetUE(UEStockpile,element.pos[0],element.pos[1])))
            cursor.execute(sqlGetIdUE,val)
            connection.commit()
            result = cursor.fetchall()
            idTemp = str(result[0]['idUE'])
            heure = str(element.heure)
            sqlCheckExist = "SELECT idAA FROM aa WHERE nom = (%s) AND quad = (%s) AND heure = (%s) AND idUE = (%s)"
            temp = (element.name, element.quad, heure, idTemp)
            cursor.execute(sqlCheckExist,temp)
            connection.commit()
            if(cursor.rowcount<1):
                heure = str(element.heure)
                sqlInsertAA = "INSERT INTO aa(nom,quad,heure,idUE) VALUES (%s,%s,%s,%s)"
                temp = (element.name, element.quad, heure, idTemp)
                cursor.execute(sqlInsertAA,temp)
                connection.commit()
                   
    print()

       
finally:
    # Close connection.
    connection.close()


#Affichage de l'horaire du lundi, pour exemple

#print(listelundi[0])
#for x in range(2,len(listelundi)):
	#print(listelundi[x])
    #print("\n")




