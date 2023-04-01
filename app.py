from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app)
# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'renault' #nombre de la BD
mysql = MySQL(app)

respuesta_obtenida = []
datos_usuario_temporal = []


@app.route('/')
def bienvenida():
    return jsonify({"bienvenida": "hola"})

@app.route("/agregar_usuario_temporal", methods=['POST'])
def agregar_usuario_temporal():
    datos_usuario = {
        'id_usuario': request.json['Id_usuario'],
        'nombre': request.json['Nombre'],
        'apellido': request.json['Apellido'],
        'respuesta_abdominal': request.json['Respuesta_abdominal'],
        'respuesta_diarrea': request.json['Respuesta_diarrea'],
        'respuesta_estrenimiento': request.json['Respuesta_estrenimiento'],
        'respuesta_acidez': request.json['Respuesta_acidez'],
        'respuesta_vomitos': request.json['Respuesta_vomitos'],
    }
    
    datos_usuario_temporal.append(datos_usuario)
    Id_usuario = datos_usuario['id_usuario']
    Nombre = datos_usuario['nombre']
    Apellido = datos_usuario['apellido']
    Respuesta_abdominal = datos_usuario['respuesta_abdominal']
    Respuesta_diarrea = datos_usuario['respuesta_diarrea']
    Respuesta_estrenimiento = datos_usuario['respuesta_estrenimiento']
    Respuesta_acidez = datos_usuario['respuesta_acidez']
    Respuesta_vomitos = datos_usuario['respuesta_vomitos']

#Funcion insertar datos
@app.route("/insertar_datos/", methods = ['POST'])
def insertar_datos():
    datos_usuario = {
        'modelo': request.json['campo_modelo'],
        'año': request.json['campo_año'],
        'kilometraje': request.json['campo_kilometraje'],
        'precio': request.json['campo_precio']
    }

    datos_usuario_temporal.append(datos_usuario)

    modelo = datos_usuario['modelo']
    año = datos_usuario['año']
    kilometraje = datos_usuario['kilometraje']
    precio = datos_usuario['precio']
    cur = mysql.connection.cursor()

    cur.execute("INSERT INTO tabla_renault (modelo, año, kilometraje, precio) VALUES (%s,%s,%s,%s)", (modelo, año, kilometraje, precio))
    cur.close()
    mysql.connection.commit()
    print("Datos añadidos a la BD ")
    return jsonify({"informacion":"Registro exitoso del usuario y sus respuestas"})

@app.route('/mostrar_datos_tabla/', methods=['GET'])
def mostrar_tabla():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tabla_renault')
    registros = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    resultado = []
    for registro in registros:
        resultado.append(dict(zip(columnas, registro)))
    return jsonify(resultado)

@app.route("/respuesta_sbr/<id>", methods = ['GET'])
def respuesta_sbr(id):
    try:

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Usuario_Respuestas WHERE Id_Usuario LIKE %s',[id])
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in rv:
            content = {"id_usuario":result[0],"Nombre":result[1],"Apellido":result[2],"Respuesta_abdominal":result[3],"Respuesta_diarrea":result[4],"Respuesta_estrenimiento":result[5],"Respuesta_acidez":result[6],"Respuesta_vomitos":result[7],"Diagnostico_final":result[8]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})



if __name__ == '__main__':
    app.run(debug = True, port = 4000)