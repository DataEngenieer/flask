from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error
import os
from werkzeug.utils import secure_filename
from controllers.funciones_home import *
from minio import Minio
from minio.error import S3Error

PATH_URL = "public/empleados"


@app.route('/registrar-empleado', methods=['GET'])
def viewFormEmpleado():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/form_empleado.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/form-registrar-empleado', methods=['POST'])
def formEmpleado():
    if 'conectado' in session:
        if 'foto_empleado' in request.files:
            foto_perfil = request.files['foto_empleado']
            resultado = procesar_form_empleado(request.form, foto_perfil)
            if resultado:
                return redirect(url_for('lista_empleados'))
            else:
                flash('El empleado NO fue registrado.', 'error')
                return render_template(f'{PATH_URL}/form_empleado.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/lista-de-empleados', methods=['GET'])
def lista_empleados():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_empleados.html', empleados=sql_lista_empleadosBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/inventario', methods=['GET'])
def lista_inventario():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/listar_inventario.html', inventario=sql_lista_inventariobodegaBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/inventario_oms', methods=['GET'])
def lista_inventario_oms():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/listar_inventario_oms.html', inventario_oms=sql_lista_inventariobodegaBD_oms())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/token', methods=['GET'])
def lista_token():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/listar_token.html', token=sql_lista_token(session.get('token'),session.get('campaing')))
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route("/detalles-empleado/", methods=['GET'])
@app.route("/detalles-empleado/<int:idEmpleado>", methods=['GET'])
def detalleEmpleado(idEmpleado=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idEmpleado es None o no está presente en la URL
        if idEmpleado is None:
            return redirect(url_for('inicio'))
        else:
            detalle_empleado = sql_detalles_empleadosBD(idEmpleado) or []
            return render_template(f'{PATH_URL}/detalles_empleado.html', detalle_empleado=detalle_empleado)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Buscador de empleados
@app.route("/buscando-empleado", methods=['POST'])
def viewBuscarEmpleadoBD():
    resultadoBusqueda = buscarEmpleadoBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL}/resultado_busqueda_empleado.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})

# Buscador de inventario
@app.route("/buscando-inventario", methods=['POST'])
def viewBuscarInventarioBD():
    resultadobusquedainv = buscarInventarioBD(request.json['busqueda'])
    if resultadobusquedainv:
        return render_template(f'{PATH_URL}/resultado_busqueda_inventario.html', dataBusqueda_inv=resultadobusquedainv)
    else:
        return jsonify({'fin': 0})
    
@app.route("/buscando-inventario-bodega", methods=['POST'])
def viewBuscarInventarioBD_bodega():
    resultadobusquedainv_bodega = buscarInventarioBD_bodega(request.json['busqueda'])
    if resultadobusquedainv_bodega:
        return render_template(f'{PATH_URL}/resultado_busqueda_inventario_bodega.html', dataBusqueda_inv_bod=resultadobusquedainv_bodega)
    else:
        return jsonify({'fin': 0})
    
@app.route("/buscando-inventario-bodega-oms", methods=['POST'])
def viewBuscarInventarioBD_bodega_oms():
    busqueda = request.json.get('busqueda')
    resultadobusquedainv_oms = buscarInventarioBD_bodega_oms(busqueda)
    if resultadobusquedainv_oms:
        return render_template(f'{PATH_URL}/resultado_busqueda_inventario_oms.html', dataBusqueda_inv_oms=resultadobusquedainv_oms)
    else:
        return jsonify({'fin': 0})
    

@app.route("/buscando-inventario-bodega-pro", methods=['POST'])
def viewBuscarInventarioBD_bodega_pro():
    try:
        # Obtenemos ambos parámetros de búsqueda desde el JSON
        busqueda = request.json.get('busqueda')  # bodega
        busqueda2 = request.json.get('busqueda2')  # producto
        
        # Llamamos a la función de búsqueda pasando ambos parámetros
        resultadobusquedainv_bodega_pro = buscarInventarioBD_bodega_pro(busqueda, busqueda2)
        
        if resultadobusquedainv_bodega_pro:
            # Si hay resultados, los pasamos a la plantilla para que se rendericen
            return render_template(f'{PATH_URL}/resultado_busqueda_inventario_bodega_pro.html', dataBusqueda_inv_bod_pro=resultadobusquedainv_bodega_pro)
        else:
            # Si no hay resultados, devolvemos un JSON indicando que no se encontraron resultados
            return jsonify({'fin': 0})
    except Exception as e:
        # Manejo de errores, en caso de algún fallo
        return jsonify({'error': str(e)}), 500


@app.route("/editar-empleado/<int:id>", methods=['GET'])
def viewEditarEmpleado(id):
    if 'conectado' in session:
        respuestaEmpleado = buscarEmpleadoUnico(id)
        if respuestaEmpleado:
            return render_template(f'{PATH_URL}/form_empleado_update.html', respuestaEmpleado=respuestaEmpleado)
        else:
            flash('El empleado no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion de empleado
@app.route('/actualizar-empleado', methods=['POST'])
def actualizarEmpleado():
    resultData = procesar_actualizacion_form(request)
    if resultData:
        return redirect(url_for('lista_empleados'))


@app.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    if 'conectado' in session:
        resp_usuariosBD = lista_usuariosBD()
        return render_template('public/usuarios/lista_usuarios.html', resp_usuariosBD=resp_usuariosBD)
    else:
        return redirect(url_for('inicioCpanel'))


@app.route('/borrar-usuario/<string:id>', methods=['GET'])
def borrarUsuario(id):
    resp = eliminarUsuario(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('usuarios'))

# eliminar equipo digital
@app.route('/borrar-equipo/<string:id>', methods=['GET'])
def eliminar_equipo(id):
    resp = eliminarequipo(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('listar_equipos'))
    
# enviar sms equipo
@app.route('/enviar-equipo', methods=['POST'])
def enviar_equipo():
    data = request.json  # Recibir datos en formato JSON
    
    # Obtener valores del JSON
    id_equipo = data.get("id")
    numero = data.get("telefono")

    # Validaciones
    if not numero or not numero.isdigit() or len(numero) != 10:
        return jsonify({"error": "Número de teléfono inválido"}), 400
    mensaje = f'Gracias por tu interes en el equipo: {id_equipo}'
    # Enviar el SMS
    resultado = enviar_sms(numero,mensaje)
    return jsonify(resultado)  # Responder con el resultado


@app.route('/borrar-empleado/<string:id_empleado>/<string:foto_empleado>', methods=['GET'])
def borrarEmpleado(id_empleado, foto_empleado):
    resp = eliminarEmpleado(id_empleado, foto_empleado)
    if resp:
        flash('El Empleado fue eliminado correctamente', 'success')
        return redirect(url_for('lista_empleados'))


@app.route("/descargar-informe-empleados/", methods=['GET'])
def reporteBD():
    if 'conectado' in session:
        return generarReporteExcel()
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route("/listar_equipos", methods=['GET'])
def listar_equipos():
    if 'conectado' in session:
        resp_equiposBD = lista_equiposBD()
        return render_template('public/empleados/listar_equipos.html', resp_equiposBD=resp_equiposBD)
    else:
        return redirect(url_for('listar_equipos'))

@app.route("/cliente", methods=['GET'])
def cliente():
    equipo = {"imagen1": "https://bucket-production-6b48.up.railway.app/inventario-equipo/prueba_img4.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=QtuJZ2idPCTtD5RbRmWN%2F20250203%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250203T163606Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=534b3c8644fe5878bee8f473c6d9bcb06c318d33c0ae0ba83e12192004d713ff"}
    if 'conectado' in session:
        return render_template('public/empleados/cliente.html', equipo=equipo)
    else:
        return redirect(url_for('listar_equipos'))





@app.route('/agregar_equipo', methods=['GET', 'POST'])
def agregar_equipo():
    if 'conectado' in session:
        if request.method == 'POST':
            # Captura los datos del formulario
            tipo_equipo = request.form.get('tipo_equipo')
            marca = request.form.get('marca')
            gamma = request.form.get('gamma')
            nombre_equipo = request.form.get('nombre_equipo')
            descripcion = request.form.get('descripcion')
            red = request.form.get('red')
            colores = request.form.getlist('colores')  # Manejo de select múltiple
            colores_str = ','.join(colores)

            
                    # Configuración de MinIO
            minio_client = Minio(
                "bucket-production-6b48.up.railway.app",  # Dirección del servidor MinIO
                access_key="QtuJZ2idPCTtD5RbRmWN",
                secret_key="l7SoPJjtGQ2xGKdZdwIzCJkGD0lNINzpSegDe3Ai",
                secure=True  # True si usas HTTPS
            )

            # Verificar que el bucket existe
            bucket_name = "inventario-equipo"
            if not minio_client.bucket_exists(bucket_name):
                minio_client.make_bucket(bucket_name)
        
        
            # Rutas para guardar las imágenes
            UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'inventario_equipos')
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)  # Crea el directorio si no existe
            
            # Función para subir imágenes a MinIO
            def subir_a_minio(archivo, nombre_equipo, numero):
                if archivo and archivo.filename:
                    extension = os.path.splitext(archivo.filename)[1]
                    filename = secure_filename(f"{nombre_equipo}_img{numero}{extension}")

                    # Subir a MinIO
                    minio_client.put_object(
                        bucket_name, filename, archivo, length=-1, part_size=10*1024*1024, content_type=archivo.content_type
                    )

                    # Retornar la URL de acceso
                    url_archivo = minio_client.presigned_get_object(bucket_name, filename)
                    return f"{url_archivo}"
                
                return None
            
            # Subir imágenes y obtener las URLs
            ruta_imagen1 = subir_a_minio(request.files.get('imagen1'), nombre_equipo, 1)
            ruta_imagen2 = subir_a_minio(request.files.get('imagen2'), nombre_equipo, 2)
            ruta_imagen3 = subir_a_minio(request.files.get('imagen3'), nombre_equipo, 3)
            ruta_imagen4 = subir_a_minio(request.files.get('imagen4'), nombre_equipo, 4)
            
            # Archivos de imágenes
            #imagen1 = request.files.get('imagen1')
            #imagen2 = request.files.get('imagen2')
            #imagen3 = request.files.get('imagen3')
            #imagen4 = request.files.get('imagen4')
            
            # Función para guardar imágenes

            def guardar_imagen(archivo, nombre_equipo, numero):
                if archivo and archivo.filename:
                    # Asegura que el nombre del archivo sea seguro
                    filename = secure_filename(f"{nombre_equipo}_img{numero}{os.path.splitext(archivo.filename)[1]}")

                    ruta_imagen = os.path.join(UPLOAD_FOLDER, filename)

                    archivo.save(ruta_imagen)  # Guarda la imagen en la ruta correspondiente

                    return f"static/inventario_equipos/{filename}"
                
                return None
            
            
                    # Imprime las rutas de las imágenes en la consola
            #print("Rutas de las imágenes:")
            #if ruta_imagen1:
            #    print(f"Imagen 1: {ruta_imagen1}")
            #if ruta_imagen2:
            #    print(f"Imagen 2: {ruta_imagen2}")
            #if ruta_imagen3:
            #    print(f"Imagen 3: {ruta_imagen3}")
            #if ruta_imagen4:
            #    print(f"Imagen 4: {ruta_imagen4}")
            
            try:
                try:
                    print("Intentando conectar a la base de datos...")
                    conexion = connectionBD_railway()  
                    print("Conexión exitosa")
                except Exception as e:
                    print(f"Error al conectar a la BD: {e}")
                    return "Error de conexión a la base de datos", 500
                cursor = conexion.cursor()

                query = """
                    INSERT INTO `inventario_digital` (`producto`, `tipo_equipo`, `marca`, `gamma`, `descripcion`, `colores`, `imagen1`, `imagen2`, `imagen3`, `imagen4`, `camara`, `pantalla`, `procesador`, `memoria_interna`, `bateria`, `ram`, `nfc`, `red`,`creator`) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """
                cursor.execute(query, (
                    nombre_equipo, tipo_equipo, marca, gamma, descripcion, colores_str,
                    ruta_imagen1, ruta_imagen2, ruta_imagen3, ruta_imagen4,
                    request.form.get('caracteristica1'),  # Camara
                    request.form.get('caracteristica2'),  # Pantalla
                    request.form.get('caracteristica3'),  # Procesador
                    request.form.get('caracteristica4'),  # Memoria Interna
                    request.form.get('caracteristica5'),  # Batería
                    request.form.get('caracteristica6'),  # RAM
                    request.form.get('nfc', 'No'),  # NFC (opcional)
                    red,
                    session.get('email')
                ))
                conexion.commit()
                print(f"Equipo guardado en BD con imágenes en MinIO.")

                cursor.close()
                conexion.close()

                return redirect(url_for('listar_equipos'))
            except Exception as e:
                print(f"Error al guardar los datos: {e}")
                return f"Error al guardar los datos: {str(e)}", 500  
        
        return render_template('public/empleados/agregar_equipo.html') 
    else:
        return redirect(url_for('loginCliente'))
    
    

@app.route('/ver_equipo/<int:id_equipo>')
def ver_equipo(id_equipo):
    try:
        conexion = connectionBD_railway()  
        cursor = conexion.cursor()

        query = """
            SELECT * FROM inventario_digital WHERE id = ?
        """
        cursor.execute(query, (id_equipo,))
        equipo = cursor.fetchone()

        if equipo:
            # Crear un diccionario con los datos del equipo para pasar a la plantilla
            datos_equipo = {
                'id': equipo[0],
                'producto': equipo[1],
                'tipo_equipo': equipo[2],
                'marca': equipo[3],
                'gamma': equipo[4],
                'descripcion': equipo[5],
                'colores': equipo[6],
                'imagen1': equipo[7],
                'imagen2': equipo[8],
                'imagen3': equipo[9],
                'imagen4': equipo[10],
                'camara': equipo[11],
                'pantalla': equipo[12],
                'procesador': equipo[13],
                'memoria_interna': equipo[14],
                'bateria': equipo[15],
                'ram': equipo[16],
                'nfc': equipo[17],
                'red': equipo[18],
                'creator': equipo[19]
            }

            return render_template('public/empleados/ver_equipo.html', equipo=datos_equipo)
        else:
            return "Equipo no encontrado", 404

        cursor.close()
        conexion.close()
    except Exception as e:
        print(f"Error al obtener los datos del equipo: {e}")
        return f"Error al obtener los datos del equipo: {str(e)}", 500