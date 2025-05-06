from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import bcrypt
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
swagger = Swagger (app)

#conexion a la base de datos
def conectar (vhost, vuser, vpass, vdb):
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset='utf8mb4')
    return conn

#ruta para consulta general
@app.route("/", methods= ['GET'] )
def consulta_general ():
    """
    consulta general del baúl de contraseña
    ---
    responses:
       200:
         description: Lista de registros
    """
    try:
        conn =conectar('localhost', 'root', '123456', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario")
        datos = cur.fetchall()
        data = []
        for row in datos:
            datos = {'id_baul': row[0], 'plataforma': row[1], 'usuario': row[2], 'clave': row[3] }
            data.append(datos)
        cur.close()
        conn.close()
        return jsonify ({'baul': data, 'mensaje': 'baúl de contraseñas'})
    except Exception as ex:
        print (ex)
        return jsonify({'mensaje': 'Error'})

#ruta para consulta individual
@app.route("/consulta_individual/<codigo>", methods=['GET'])
def consulta_individual(codigo):
    """
    Consulta individual por ID
    ---
    parameters:
    - name: codigo
      in: path
      required: true
      type: integer
    responses:
      200:
      description: Registro encontrado
    """
    try:
        conn =conectar('localhost', 'root', '123456', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM usuario WHERE id_baul = '{codigo}' ")
        datos = cur.fetchone()
        cur.close()
        conn.close()
        if datos:
            datos = {'id_baul': datos[0], 'plataforma': datos[1], 'usuario': datos[2], 'clave': datos[3]}
            return jsonify({'baul': datos, 'mensaje': 'Registro encontrado'})
        else:
            return jsonify({'mensaje': 'Registro encontrado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})
    
#ruta para registro
@app.route("/registro/", methods= ['POST'])
def registro():
    """
    registrar nueva contraseña
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema: 
          type: object
          properties:
            plataforma:
              type: string
            usuario:
              type: string
            clave:
              type: string
    responses:
    200:
        description: registro agregado
    """
    try:
        data = request.get_json()
        plataforma= data['plataforma']
        usuario= data['usuario']
        clave= bcrypt.hashpw(data['clave'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn =conectar('localhost', 'root', '123456', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("INSERT INTO usuario (plataforma, usuario, clave) VALUES (%s,%s,%s)",
                     (plataforma, usuario, clave))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'registro agregado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

#ruta para eliminar registro
@app.route("/eliminar/<codigo>", methods= ['DELETE'])
def eliminar(codigo):
    """
    Eliminar registro ID
    ---
    parameters:
      - name: codigo
        in: path
        required: true
        type: integer
    responses:
      200:
        description: registro eliminado
    """
    try:
        conn =conectar('localhost', 'root', '123456', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("DELETE FROM usuario WHERE id_baul = %s", (codigo,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Eliminado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})
    
#ruta para actualizar registro
@app.route("/actualizar/<codigo>", methods= ['PUT'])
def actualizar(codigo):
    """
    Actualizar registro por ID
    ---
    parameters:
      - name: codigo
        in: path
        required: true 
        type: interger
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            plataforma:
              type: string
            usuario:
              type: string
            clave:
              type: string
    responses:
      200:
        description: registro agregado
    """
    try:
        data = request.get_json()
        plataforma= data['plataforma']
        usuario= data['usuario']
        clave= bcrypt.hashpw(data['clave'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn =conectar('localhost', 'root', '123456', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("UPDATE usuario SET plataforma= %s,  usuario= %s, clave= %s WHERE id_baul = %s",
                     (plataforma, usuario, clave, codigo))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'registro actualizado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})
    
if __name__ == '__main__':
    app.run(debug=True)