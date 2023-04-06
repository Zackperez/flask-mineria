from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'renault' #nombre de la BD
mysql = MySQL(app)

@app.route('/')
def bienvenida():
    return jsonify({"bienvenida": "hola"})

@app.route("/insertar_datos_vehiculo/", methods = ['POST'])
def insertar_datos_vehiculo():

    datos_usuario_temporal = []
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

@app.route("/modificar_datos_vehiculo", methods=['POST'])
def modificar_datos_vehiculo():

    datos_vehiculo = {
        'modificar_id': request.json['modificarId'],
        'modificar_año': request.json['modificarAño'],
        'modificar_modelo': request.json['modificarModelo'],
        'modificar_kilometraje': request.json['modificarKilometraje'],
        'modificar_precio': request.json['modificarPrecio']
    }

    id = datos_vehiculo['modificar_id']
    año = datos_vehiculo['modificar_año']
    modelo = datos_vehiculo['modificar_modelo']
    kilometraje = datos_vehiculo['modificar_kilometraje']
    precio = datos_vehiculo['modificar_precio']

    cur = mysql.connection.cursor()
    sql = ("UPDATE tabla_renault SET precio = %s, modelo = %s, año = %s, kilometraje = %s WHERE id = %s")
    val = (precio, modelo, año, kilometraje, id)
    cur.execute(sql,val)
    cur.close()
    mysql.connection.commit()
    print("Modificación realizada ")
    return jsonify({"informacion":"Registro exitoso del usuario y sus respuestas"})

@app.route("/eliminar_datos_vehiculo/<id>", methods=['DELETE'])
def eliminar_datos_vehiculo(id):

    cur = mysql.connection.cursor()

    sql = ("DELETE FROM tabla_renault WHERE id = %s")
    val = (id,)
    cur.execute(sql,val)
    cur.close()
    mysql.connection.commit()
    print("eliminación realizada ")
    return jsonify({"informacion":"Registro exitoso del usuario y sus respuestas"})

#RUTA PARA MOSTRAR DATOS EN LA TABLA
#Mostrar los registros de la BD en la tabla
@app.route('/mostrar_registros_tabla/', methods=['GET'])
def mostrar_registros_tabla():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tabla_renault')
    registros = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    resultado = []
    for registro in registros:
        resultado.append(dict(zip(columnas, registro)))
    return jsonify(resultado)


# RUTAS PARA LAS GRÁFICAS
#@app.route('/get_user_info', methods = ['GET'])
@app.route('/get_user_info', methods = ['GET'])
def recibir_usuario_info():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT modelo, COUNT(*) as COUNT FROM tabla_renault GROUP BY modelo ORDER BY modelo ASC')
        rv = cur.fetchall()
        cur.close()
        payload = []
        for result in rv:
            usuarios_contenido ={"modelo" : result[0], "cantidad" :result[1]}
            payload.append(usuarios_contenido)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"error":e})
    
#Muestra la cantidad de carros que hay según el año
#@app.route('/cant_carros_por_ano', methods = ['GET'])
@app.route('/carros_por_anio', methods = ['GET'])
def mostrar_cantidad():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT año, COUNT(*) as COUNT FROM tabla_renault GROUP BY año ORDER BY año ASC')
        rv = cur.fetchall()
        cur.close()
        payload = []
        for result in rv:
            usuarios_contenido ={"año" : result[0], "cantidad" :result[1]}
            payload.append(usuarios_contenido)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"error":e})

@app.route('/precio_segun_km', methods = ['GET'])
def precio_segun_km():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT precio, kilometraje, año FROM tabla_renault')
        rv = cur.fetchall()
        cur.close()
        payload = []
        for result in rv:
            usuarios_contenido ={"precio" : result[0], "kilometraje" :result[1], "año" :result[2]}
            payload.append(usuarios_contenido)
        print(payload)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"error":e})

@app.route('/mostrar_vehiculo/<id>', methods=['GET'])
def getAllById(id):
    try:
        print("la id es",id)
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM tabla_renault WHERE id = %s', [id])
        rv = cur.fetchall()
        cur.close()
        return jsonify(rv)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})

if __name__ == '__main__':
    app.run(debug = True, port = 4000)