from flask import Flask, abort, request
import json
from flask import jsonify
import pymongo


#Funcion para conectar con la base de datos MongoDB

def dataconnect():
    client = pymongo.MongoClient()
    db = client.admin
    return db


def eliminarRepetitionParaApp(datas):
    saveAppName = []
    Name = []
    for user in datas:
        name =user["Application"]
        Name.append(name)
        if (name in saveAppName):
            piji = 2
        else:
            saveAppName.append(name)
    return Name,saveAppName

def eliminarRepetitionParaVendor(datas):
    saveAppNameVendor = []
    NameVendor = []
    for user2 in datas:
        name = user2["Vendor"]
        NameVendor.append(name)
        if (name in saveAppNameVendor):
            piji = 2
        else:
            saveAppNameVendor.append(name)

    return NameVendor,saveAppNameVendor

def contarCantidadesApp(Name,saveAppName):
    f = open("Reporte.txt", "a+")
    count1 = 0
    for key1 in saveAppName:
        posicion = key1
        contador = 0

        for key2 in Name:
            if (key1 == key2):
                contador = contador + 1
        f.write("%d %s abierta(en camino)\r\n" % (contador, key1))

        count1 = count1 + contador
    return count1

def contarCantidadesVendor(Name,saveAppName):
    g = open("Reporte2.txt", "a+")
    count1 = 0
    for key1 in saveAppName:
        posicion = key1
        contador = 0

        for key2 in Name:
            if (key1 == key2):
                contador = contador + 1
        g.write("%d %s abierta(en camino)\r\n" % (contador, key1))

        count1 = count1 + contador
    return count1

def getappbyarea(data,area2):

    NameApp,saveAppNameApp=eliminarRepetitionParaApp(data)
    f = open("Reporte.txt", "a+")
    f.write("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<En %s tenemos>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> \r\n" % (area2))
    f.close()
    contador=contarCantidadesApp(NameApp, saveAppNameApp)
    return  contador


def getVendorbyarea(data,area2):

    NameVendor,saveAppNameVendor = eliminarRepetitionParaVendor(data)
    g = open("Reporte2.txt", "a+")
    g.write("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<En %s tenemos>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> \r\n" % (area2))
    g.close()
    contador=contarCantidadesVendor(NameVendor, saveAppNameVendor)
    return  contador

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/routas/<arguments>",  methods=['GET','POST'])
def hello1(arguments):
    if request.method == 'GET':
        return jsonify(arguments)
    if request.method == 'POST':
        return json.dumps(request.json)

@app.route("/Test")
def definirLasAreas():
    db = dataconnect()
    cursorCollectionCiscoFortigate = db.CiscoFortigate.find()
    guardados = []
    setCursor = []

    for user in cursorCollectionCiscoFortigate:
        cantidad = 0
        location = user["Location"]
        if (location in guardados):
            piji = 2
        else:
            guardados.append(location)
            cursor = db.CiscoFortigate.find({"Location": location})
            setCursor.append(cursor)
    return jsonify(guardados)
if __name__ == '__main__':
    app.run(debug=True)