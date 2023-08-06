#Bottle PyPugjs Template

Este es un plugin de *bottle* para poder usar la libreria de **pypugjs** en las vistas

##Inicio rapido

El plugin de **bottle-pypugjs** permite usar la tres formas que *bottle* define para manejar los templates

.. code-block:: python

    from bottle import route, install
    from bottle.ext.pypugjs import template, view, Plugin

    # Usando la funcion template
    @route('/index')
    def index():
        return template('index.pug')

    # Usando el decorador view
    @route('/index')
    @view('index.pug')
    def index():
        return {}

    app.install(Plugin())

    # Usando el argumento *template* en la ruta que provee el plugin
    @route('/index', template='index.pug')
    def index():
        return {}

Con estos ejemplos se resume el funcionamiento del plugin.
