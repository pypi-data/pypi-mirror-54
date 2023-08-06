Bottle PyJWT
============

Este es un plugin de **bottle** para poder usar la libreria de *JWT*

Inicio rapido
-------------

El plugin de **bottle-pyjwt** permite usar autentificacion mediante token usando el estandar java *jwt*

    from bottle import route, install
    from bottle.ext.jwt import JwtPlugin

    validate = lambda auth, auth_role: auth == auth_role

    app.install(JwtPlugin(validate, "my secret", fail_redirect="/login"))

    @route("/", auth="any values and types")
    def example():
        return "OK"
        