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
Storage = None
def MakeGetRequest(request):
    r = requests.get("http://projectcavt.hopto.org/request.php/?"+request)
    if(r.status_code == requests.codes.ok):
        return r.text
    else:
        print("Error "+r.text)
from flask import Flask, request

app = Flask(__name__)

#Page Principale
@app.route('/')
def main():
    return """<html>
                   <head>
                      <script type="text/javascript" src="http://code.jquery.com/jquery-1.11.1.min.js"></script>
                      <script>
                           $(document).ready(function(){
                               $.ajax({
                                    type: 'POST',
                                    url: '/getUE',
                                    success: function(data){
                                     $('#viewUE').html(data);
                                    }
                                });
                                $('#btnUE').click(function(){

                                    $.ajax({
                                      type: 'POST',
                                      url: '/getUE',
                                      success: function(data){
                                        $('#viewUE').html(data);
                                      }
                                    });
                                });
                                $('#btnAA').click(function(){
                                    var selectedUE = $('#viewUE').children('option:selected').val();
                                    alert(selectedUE);
                                    $.ajax({
                                      type: 'POST',
                                      url: '/getAA',
                                      data : "id="+selectedUE,
                                      success: function(data){
                                        $('#viewAA').html(data);
                                      }
                                    });
                                });
                                $('#btnCours').click(function(){

                                    $.ajax({
                                      type: 'POST',
                                      url: '/getCours',
                                      success: function(data){
                                        $('#viewCours').html(data);
                                      }
                                    });
                                });
                           });
                      </script>
                   </head>
                   <body>
                   <label for="viewUE">pick ue :<select id="viewUE"><option selected="selected" value="0"></option>
                   </select></label>
                   <label for="viewAA">pick aa :<select id="viewAA">
                   </select></label>
                   <label for="viewCours">pick cours :<select id="viewCours">
                   </select></label>
                    <input type="button" id="btnUE" value="Get UE">
                    <input type="button" id="btnAA" value="Get AA">
                    <input type="button" id="btnCours" value="Get Cours">
                    </body>
                   </html>"""

#Une nouvelle page

@app.route('/getUE', methods=['POST'])
def view_do_something():

    if request.method == 'POST':
        #your database process here
        SQLUEREQUEST = 'SELECT ue.idUE as "ID",ue.nom as "UE nom",ue.ects as "Ects",SUM(aa.heure) as "Nbre tot heures" FROM ue INNER JOIN aa ON ue.idUE=aa.idUE GROUP BY ue.idUE'
        try:


            with connection.cursor() as cursor:

        
                # SQL
                cursor.execute(SQLUEREQUEST)
                connection.commit()
                rows = cursor.fetchall()

                options="<option selected='selected' value='0'></option>"
                for row in rows:
                    options+='<option value="%s">%s</option>'%(row["ID"],row["UE nom"])
                return options
                
                
                
        except Exception as e:
            return "Erreur db",e
            connection.rollback()
    else:
        return "NO OK"
@app.route('/getAA', methods=['POST'])
def view_do_something2():

    if request.method == 'POST':
        #your database process here
        SQLUEREQUEST = 'SELECT idAA as "ID",nom as Nom FROM aa WHERE idUE= (%s)'
        val=(request.values["id"])
        try:


            with connection.cursor() as cursor:

        
                # SQL
                cursor.execute(SQLUEREQUEST,val)
                connection.commit()
                rows = cursor.fetchall()

                options=""
                for row in rows:
                    options+='<option value="%s">%s</option>'%(row["ID"],row["Nom"])
                return options
                
                
                
        except Exception as e:
            return "Erreur db",e
            connection.rollback()
    else:
        return "NO OK"
@app.route('/getCours', methods=['POST'])
def view_do_something3():

    if request.method == 'POST':
        #your database process here
        SQLUEREQUEST = 'SELECT idCours as "ID",nom as "Nom" FROM cours'
        try:


            with connection.cursor() as cursor:

        
                # SQL
                cursor.execute(SQLUEREQUEST)
                connection.commit()
                rows = cursor.fetchall()

                options=""
                for row in rows:
                    options+='<option value="%s">%s</option>'%(row["ID"],row["Nom"])
                return options
                
                
                
        except Exception as e:
            return "Erreur db",e
            connection.rollback()
    else:
        return "NO OK"

if __name__ == '__main__':
    app.run(host="192.168.31.43")


