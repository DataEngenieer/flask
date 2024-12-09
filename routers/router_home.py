from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_home import *

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
        return render_template(f'{PATH_URL}/listar_token.html', token=sql_lista_token())
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
    resultadobusquedainv_oms = buscarInventarioBD_bodega_oms(request.json['busqueda'])
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
