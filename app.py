from flask_fontawesome import FontAwesome
from flask import render_template, redirect, url_for, request, jsonify
from models import app, db, Product, Supplier, User
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

# from flask_jwt_extended import create_access_token, current_user, jwt_required, JWTManager, get_jwt,
# verify_jwt_in_request

fa = FontAwesome(app)  # Extension de Flask para FontAwesome

# Basado en https://flask-jwt-extended.readthedocs.io/en/stable/automatic_user_loading/
# Setup the Flask-JWT-Extended extension
# app.config["JWT_SECRET_KEY"] = "super-secret"
# app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
# jwt = JWTManager(app)   # Extensión de Flask para JWT Tokens


# =========================================================
# 	             AUTENTICACION USUARIOS
# =========================================================

# NOTA!!! NO SE SI CONTINUAR CON FLASK_JWT O ES MEJOR FLASK_LOGIN,
# SEGUN LO QUE HE LEIDO PARA MANTENER SESIONES DE USUARIO ES MEJOR LA SEGUNDA.

# Here is a custom decorator that verifies the JWT is present in the request,
# as well as insuring that the JWT has a claim indicating that this user is
# an administrator
'''def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper'''

# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
'''@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id'''

# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
'''@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()'''

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
'''@app.route("/login", methods=["POST"])
def login():
    # If-else, por si se hace la peticion por postman o a traves del formulario web de login
    if request.is_json:
        username = request.json.get("username", None)
        password = request.json.get("password", None)
    else:
        username = request.form["username"]
        password = request.form["password"]
    user = User.query.filter_by(username=username).one_or_none()
    if not user or not user.check_password(password):
        return jsonify("Wrong username or password"), 401
    access_token = create_access_token(identity=user)
    #return jsonify(message="Login succeeded!", access_token=access_token), 200
    return redirect(url_for("home", access_token=access_token))'''

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
'''@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # We can now access our sqlalchemy User object via `current_user`.
    return jsonify(id=current_user.id, full_name=current_user.full_name, username=current_user.username)'''

# SIGN UP: Web para crear nuevo usuario
'''@app.route('/sign_up')
def sign_up():
    return render_template("new_user.html")'''

# Funcion add_user(): Agrega la tarea rellena en el formulario a la bbdd
# Incluido el tto. de excepciones, para cuando no rellenamos un campo obligatorio
'''@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        user = User(username=request.form['username'], full_name=request.form['full_name'])
        db.session.add(user)
        db.session.commit()
        db.session.close()
    except Exception as e:
        print("Fallo al crear usuario")
        print(e)
    return redirect(url_for("home"))'''

# =========================================================
# 	                       HOME
# =========================================================

# Variables globales para el carro de la compra
cart_items_references = []
cart_summary_dict = dict()
qty_items_cart = 0
cost_total = 0.0


# Web de inicio, home
@app.route('/', methods=['GET', 'POST'])
def home():
    complex_filters = False

    # Parametros para la paginacion
    page = request.args.get('page', default=1, type=int)
    per_page = 9

    # Parametros para aplicar los filtros de la barra de navegacion y del buscador, respectivamente.
    filter_by_category = request.args.get('filter_by_category', default=None, type=str)
    category = request.args.get('category', default=None, type=str)
    search = request.args.get('search', default=None, type=str)
    search_format = "%{}%".format(search)

    # Si la peticion es POST, significa, que estamos aplicando los filtros laterales.
    # Recogemos los parametros introducidos en el formulario.
    if request.method == 'POST':
        checks_category = request.form.getlist('check_category')
        price_min = float(request.form['price_min'])
        price_max = float(request.form['price_max'])
        checks_brand = request.form.getlist('check_brand')
        # Realizo una lista que recoja el rango de precios permitidos. Muchos fallos y pruebas, da problemas la
        # precision de los flotantes
        # range_of_price = list(np.arange(int(price_min)*100, int(price_max)*100)/100)
        range_of_price = np.arange(price_min, price_max, 0.5)
        complex_filters = True

    # Mensajes de exito o error en la gestion de productos
    msg = request.args.get('msg', default=None, type=str)
    success = request.args.get('success', default=None, type=int)

    # A continuacion, el codigo de gestion del carro de la compra. Si la vble. global de nº de articulos es 0, se
    # inicializan al cero todas las vble. Sino, se obtienen los argumentos y si ha existido cambio en el carrito,
    # se actualiza el diccionario con la lista de referencias de items en el carro mas reciente.
    global qty_items_cart
    global cart_summary_dict
    if qty_items_cart != 0:
        qty_items_cart_final = qty_items_cart
        cost_total_final = cost_total
        change_in_cart = request.args.get('change_in_cart', default=None, type=int)
        if change_in_cart is not None:
            cart_items = request.args.getlist('cart_items')
            cart_summary_final = dict()
            for item in cart_items:
                product = Product.query.filter_by(reference=int(item)).first()
                product_to_cart = (product.reference, product.category, product.name, product.selling_price)
                qty_item = cart_items.count(item)
                cart_summary_final[product_to_cart] = qty_item
            cart_summary_dict = cart_summary_final
    else:
        qty_items_cart_final = 0
        cost_total_final = 0.0
        cart_summary_dict = dict()

    # Query de los productos en base a los filtros que apliquen:
    # (1) Enlaces de la barra de navegacion o el footer
    # (2) Buscador del header
    # (3) Filtros laterales
    # (4) Sin filtros
    if filter_by_category is not None:
        products = Product.query.filter_by(category=filter_by_category).paginate(page, per_page, error_out=False)
    elif search is not None:
        if category is not None:
            products = Product.query.filter_by(category=category).filter(
                Product.description.like(search_format)).paginate(page, per_page, error_out=False)
        else:
            products = Product.query.filter(Product.description.like(search_format)).paginate(page, per_page,
                                                                                              error_out=False)
    elif complex_filters:
        if len(checks_category) > 0 and len(checks_brand) > 0:
            products = Product.query.filter(Product.category.in_(checks_category) &
                                            Product.selling_price.in_(range_of_price) &
                                            Product.brand.in_(checks_brand)).paginate(page, per_page, error_out=False)
        elif len(checks_category) == 0 and len(checks_brand) == 0:
            products = Product.query.filter(Product.selling_price.in_(range_of_price)).paginate(page, per_page,
                                                                                                error_out=False)

        elif len(checks_category) == 0:
            products = Product.query.filter(Product.selling_price.in_(range_of_price) &
                                            Product.brand.in_(checks_brand)).paginate(page, per_page, error_out=False)
        else:
            products = Product.query.filter(Product.category.in_(checks_category) &
                                            Product.selling_price.in_(range_of_price)).paginate(page, per_page,
                                                                                                error_out=False)
    else:
        products = Product.query.paginate(page, per_page, error_out=False)

    # Se recurre a un for para obtener las distintas categorias almacenadas en la bbdds y la cantidad de productos
    # de cada una de ellas. Se almacena en un diccionario y se envia al front para los filtros laterales.
    # Lo mismo con las marcas.
    all_products = Product.query.all()
    all_categories = {}
    all_brands = {}
    for p in all_products:
        if p.category not in all_categories:
            all_categories[p.category] = 1
        else:
            all_categories[p.category] += 1
        if p.brand not in all_brands:
            all_brands[p.brand] = 1
        else:
            all_brands[p.brand] += 1

    # De lo ultimo realizado, para probar a trabajar con Pandas
    # Genero el dataframe leyendo de la bbdd
    # Implementacion para obtener el top 3 de ventas y paso a lista las columnas requeridas para trabajar en el front
    df = pd.read_sql_query("SELECT * from product", con=db.engine)
    top_selling = df.nlargest(3, ['sales'], keep='all')
    top_selling_reference = top_selling['reference'].tolist()
    top_selling_category = top_selling['category'].tolist()
    top_selling_name = top_selling['name'].tolist()
    top_selling_price = top_selling['selling_price'].tolist()

    return render_template("index.html", products_list=products, categories_dict=all_categories,
                           brands_dict=all_brands, cart_summary=cart_summary_dict, qty_cart_final=qty_items_cart_final,
                           cost_total=cost_total_final, msg=msg, success=success, top_selling_name=top_selling_name,
                           top_selling_category=top_selling_category, top_selling_price=top_selling_price,
                           top_selling_reference=top_selling_reference)


# Web de detalles del producto seleccionado
@app.route('/product_details', methods=['GET'])
def product_details():
    # Parametros para aplicar filtros
    reference = request.args.get('reference', type=int)
    # Query de los productos en base a los filtros que apliquen
    product = Product.query.filter_by(reference=reference).first()
    return render_template("product_details.html", product=product)


# Ruta que agrega la referencia del producto a la lista de articulos en el carrito, incrementando el precio final
# en el importe del producto y sumando 1 al nª de articulos en la cesta. He usado una vble. (entera pq booleana me da
# errores) para indicar que estoy realizando modificaciones en el carro, change_in_cart.
@app.route('/add_to_cart')
def add_to_cart():
    global qty_items_cart
    global cost_total
    qty_items_cart += 1
    reference = request.args.get('reference', type=int)
    product = Product.query.filter_by(reference=reference).first()
    cart_items_references.append(reference)
    change_in_cart = 1
    cost_total += product.selling_price
    return redirect(url_for("home", cart_items=cart_items_references, change_in_cart=change_in_cart))


# Igual que la funcion anterior, pero eliminando y restando del carrito el/los articulo/s seleccionado/s.
# Incluye el transito de mensajes de exito, en caso de procesar la limpieza de carrito tras la compra.
@app.route('/remove_item_cart')
def remove_item_cart():
    global qty_items_cart
    global cost_total
    # Mensajes de exito o error en la gestion de productos
    msg = request.args.get('msg', default=None, type=str)
    success = request.args.get('success', default=None, type=int)
    # qty_items_cart -= 1
    reference = request.args.get('reference', type=int)
    references = request.args.getlist('references')
    if reference is not None:
        product = Product.query.filter_by(reference=reference).first()
        cart_items_references.remove(reference)
        qty_items_cart -= 1
        change_in_cart = 1
        cost_total -= product.selling_price
    elif references is not None:
        for ref in references:
            product = Product.query.filter_by(reference=ref).first()
            cart_items_references.remove(int(ref))
            qty_items_cart -= 1
            change_in_cart = 1
            cost_total -= product.selling_price
    # cost_total -= product.selling_price
    return redirect(url_for("home", cart_items=cart_items_references, change_in_cart=change_in_cart, msg=msg,
                            success=success))


# Realizacion del pedido. Genera un mensaje de exito de compra o error si no hay stock suficiente del producto.
# Actualiza los campos de stock del articulo y nº de ventas, si hay stock suficiente.
# Redirecciona a la home si no hay stock o a remove_item_cart si lo hay para limpiar el carrito.
@app.route('/place_order')
def place_order():
    references = []
    for key in cart_summary_dict.keys():
        product = Product.query.filter_by(reference=key[0]).first()
        reference = product.reference
        item_stock = product.stock
        if cart_summary_dict[key] <= item_stock:
            product.stock -= cart_summary_dict[key]
            product.sales += cart_summary_dict[key]
            db.session.commit()
            db.session.close()
            msg = "Successfully ordered product!"
            success = 1
            for i in range(0, cart_summary_dict[key]):
                references.append(reference)
        else:
            msg = "Failed to order product! Insufficient stock!"
            success = 0
            return redirect(url_for("home", msg=msg, success=success))
    return redirect(url_for("remove_item_cart", references=references, msg=msg, success=success))


# =========================================================
# 	                       USER
# =========================================================

# A futuro, requerira autenticacion.
@app.route('/checkout')
def checkout():
    return render_template("checkout.html", cart_summary=cart_summary_dict, cost_total=cost_total)


# =========================================================
# 	                       ADMIN
# =========================================================

# Home del administrador, desde donde accede a la gestion de productos y proveedores,
# o a la visualizacion de estadisticas. Requerira autenticacion, con el rol de admin.
@app.route('/admin', methods=['GET'])
# @jwt_required()
def admin():
    """token = request.args.get('access_token', type=str)
    verify_jwt_in_request()
    print("Usuario.....", current_user.id)"""
    return render_template("admin.html")


# -------------------------
# 	     PRODUCTS
# -------------------------

# Web principal de productos, del stock. Muestra los productos de bbdds. Incluye paginacion.
# Filtra los productos devueltos, en funcion de las busquedas seleccionadas.
@app.route('/stock', methods=['GET', 'POST'])
def stock():
    complex_filters = False

    # Parametros para la paginacion
    page = request.args.get('page', default=1, type=int)
    per_page = 5

    # Parametros para aplicar los filtros de la barra de navegacion y del buscador, respectivamente.
    filter_by_category = request.args.get('filter_by_category', default=None, type=str)
    category = request.args.get('category', default=None, type=str)
    search = request.args.get('search', default=None, type=str)
    search_format = "%{}%".format(search)

    # Si la peticion es POST, significa, que estamos aplicando los filtros laterales.
    # Recogemos los parametros introducidos en el formulario.
    if request.method == 'POST':
        checks_category = request.form.getlist('check_category')
        price_min = float(request.form['price_min'])
        price_max = float(request.form['price_max'])
        checks_brand = request.form.getlist('check_brand')
        # Realizo una lista que recoja el rango de precios permitidos. Muchos fallos y pruebas, da problemas la
        # precision de los flotantes
        # range_of_price = list(np.arange(int(price_min)*100, int(price_max)*100)/100)
        range_of_price = np.arange(price_min, price_max, 0.5)
        complex_filters = True

    # Mensajes de exito o error en la gestion de productos
    msg = request.args.get('msg', default=None, type=str)
    success = request.args.get('success', default=None, type=int)

    # Query de los productos en base a los filtros que apliquen:
    # (1) Enlaces de la barra de navegacion o el footer
    # (2) Buscador del header
    # (3) Filtros laterales
    # (4) Sin filtros
    if filter_by_category is not None:
        products = Product.query.filter_by(category=filter_by_category).paginate(page, per_page, error_out=False)
    elif search is not None:
        if category is not None:
            products = Product.query.filter_by(category=category).filter(
                Product.description.like(search_format)).paginate(page, per_page, error_out=False)
        else:
            products = Product.query.filter(Product.description.like(search_format)).paginate(page, per_page,
                                                                                              error_out=False)
    elif complex_filters:
        if len(checks_category) > 0 and len(checks_brand) > 0:
            products = Product.query.filter(Product.category.in_(checks_category) &
                                            Product.selling_price.in_(range_of_price) &
                                            Product.brand.in_(checks_brand)).paginate(page, per_page, error_out=False)
        elif len(checks_category) == 0 and len(checks_brand) == 0:
            products = Product.query.filter(Product.selling_price.in_(range_of_price)).paginate(page, per_page,
                                                                                                error_out=False)

        elif len(checks_category) == 0:
            products = Product.query.filter(Product.selling_price.in_(range_of_price) &
                                            Product.brand.in_(checks_brand)).paginate(page, per_page, error_out=False)
        else:
            products = Product.query.filter(Product.category.in_(checks_category) &
                                            Product.selling_price.in_(range_of_price)).paginate(page, per_page,
                                                                                                error_out=False)
    else:
        products = Product.query.paginate(page, per_page, error_out=False)

    # Se recurre a un for para obtener las distintas categorias almacenadas en la bbdds y la cantidad de productos
    # de cada una de ellas. Se almacena en un diccionario y se envia al front para los filtros laterales.
    # Lo mismo con las marcas.
    all_products = Product.query.all()
    all_categories = {}
    all_brands = {}
    for p in all_products:
        if p.category not in all_categories:
            all_categories[p.category] = 1
        else:
            all_categories[p.category] += 1
        if p.brand not in all_brands:
            all_brands[p.brand] = 1
        else:
            all_brands[p.brand] += 1

    return render_template("stock.html", products_list=products, categories_dict=all_categories,
                           brands_dict=all_brands, msg=msg, success=success)


# Funcion editar(): Si es peticion GET, a traves del link de editar del stock.html, carga el template edit_product.html
# Si es peticion POST, al rellenar el formulario de edicion, edita el producto de la bbdd.
# Tto. de excepciones como en la funcion crear()
@app.route('/edit_product', methods=['GET', 'POST'])
def edit_product():
    reference = request.args.get('reference', type=int)
    product = Product.query.filter_by(reference=reference).first()
    if request.method == 'GET':
        return render_template("edit_product.html", product=product)
    elif request.method == 'POST':
        try:
            product.category = request.form['category']
            product.name = request.form['name']
            product.brand = request.form['brand']
            product.description = request.form['description']
            product.purchase_price = request.form['purchase_price']
            product.selling_price = request.form['selling_price']
            product.stock = request.form['stock']
            product.sales = request.form['sales']
            db.session.commit()
            db.session.close()
            msg = "Successfully edited product!"
            success = 1
        except Exception as e:
            msg = "Failed to edit product!"
            success = 0
        return redirect(url_for("stock", msg=msg, success=success))


# Funcion eliminar(): Elimina el producto indicado por parametro de la bbdd.
@app.route('/delete_product', methods=['GET'])
def delete_product():
    reference = request.args.get('reference', type=int)
    Product.query.filter_by(reference=reference).delete()
    db.session.commit()
    db.session.close()
    msg = "Successfully deleted product!"
    success = 1
    return redirect(url_for("stock", msg=msg, success=success))


# Formulario web para añadir nuevo producto
@app.route('/new_product')
def new_product():
    return render_template("new_product.html")


# Funcion crear(): Agrega el producto relleno en el formulario a la bbdd.
# Incluido el tto. de excepciones, para cuando no rellenamos un campo obligatorio.
@app.route('/add_product', methods=['POST'])
def add_product():
    try:
        product = Product(category=request.form['category'], name=request.form['name'], brand=request.form['brand'],
                          description=request.form['description'], purchase_price=request.form['purchase_price'],
                          selling_price=request.form['selling_price'], stock=request.form['stock'],
                          sales=request.form['sales'])
        db.session.add(product)
        db.session.commit()
        db.session.close()
        msg = "Successfully added product!"
        success = 1
    except Exception as e:
        msg = "Failed to add product!"
        success = 0
    return redirect(url_for("stock", msg=msg, success=success))


# -------------------------
# 	     SUPPLIERS
# -------------------------

# Web principal de proveedores. Muestra todos los proveedores de bbdds.
@app.route('/suppliers', methods=['GET'])
def suppliers():
    # Parametros para la paginacion
    page = request.args.get('page', default=1, type=int)
    per_page = 5

    # Mensajes de exito o error en la gestion de proveedores
    msg = request.args.get('msg', default=None, type=str)
    success = request.args.get('success', default=None, type=int)

    # Query de todos los proveedores
    all_suppliers = Supplier.query.paginate(page, per_page, error_out=False)
    return render_template("suppliers.html", suppliers_list=all_suppliers, msg=msg, success=success)


# Funcion editar(): Si es peticion GET, a traves del link de editar del suppliers.html,
# carga el template edit_supplier.html
# Si es peticion POST, al rellenar el formulario de edicion, edita el supplier de la bbdd.
# Tto. de excepciones como en la funcion crear()
@app.route('/edit_supplier', methods=['GET', 'POST'])
def edit_supplier():
    reference = request.args.get('reference', type=int)
    supplier = Supplier.query.filter_by(reference=reference).first()
    if request.method == 'GET':
        return render_template("edit_supplier.html", supplier=supplier)
    elif request.method == 'POST':
        try:
            supplier.name = request.form['name']
            supplier.direction = request.form['direction']
            supplier.cif = request.form['cif']
            supplier.bank_account = request.form['bank_account']
            supplier.phone = request.form['phone']
            db.session.commit()
            db.session.close()
            msg = "Successfully edited supplier!"
            success = 1
        except Exception as e:
            msg = "Failed to edit supplier!"
            success = 0
        return redirect(url_for("suppliers", msg=msg, success=success))


# Funcion eliminar(): Elimina el proveedor indicado por parametro de la bbdd.
@app.route('/delete_supplier')
def delete_supplier():
    reference = request.args.get('reference', type=int)
    Supplier.query.filter_by(reference=reference).delete()
    db.session.commit()
    db.session.close()
    msg = "Successfully deleted supplier!"
    success = 1
    return redirect(url_for("suppliers", msg=msg, success=success))


# Web para añadir nuevo proveedor.
@app.route('/new_supplier')
def new_supplier():
    return render_template("new_supplier.html")


# Funcion crear(): Agrega el proveedor relleno en el formulario a la bbdd.
# Incluido el tto. de excepciones, para cuando no rellenamos un campo obligatorio.
@app.route('/add_supplier', methods=['POST'])
def add_supplier():
    try:
        supplier = Supplier(name=request.form['name'], direction=request.form['direction'], cif=request.form['cif'],
                            bank_account=request.form['bank_account'], phone=request.form['phone'])
        db.session.add(supplier)
        db.session.commit()
        db.session.close()
        msg = "Successfully added supplier!"
        success = 1
    except Exception as e:
        msg = "Failed to add supplier!"
        success = 0
    return redirect(url_for("suppliers", msg=msg, success=success))


# -------------------------
# 	    STATISTICS
# -------------------------

@app.route('/statistics')
def statistics():
    # PANDAS: Genero un dataframe a partir de la bbdds
    # Incluyo una columna de beneficios calculada a partir de dos columnas de la bbdds
    df = pd.read_sql_query("SELECT * from product", con=db.engine)
    df['benefits'] = df['selling_price'] - df['purchase_price']
    # Genero dos subconjuntos de datos con los cuales generare cada una de las tres graficas
    sales4category = df.groupby(['category']).sum('sales')
    benefits4category = df.groupby(['category']).mean('benefits')
    # Implemento las graficas
    plt.style.use('classic')
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 5))
    ax1.bar(x=sales4category.index, height=sales4category['stock'].values, color='#D10024')
    ax1.set_title("Stock for category", fontsize=12)
    ax1.tick_params(axis='x', labelrotation=45)
    ax2.bar(x=sales4category.index, height=sales4category['sales'].values, color='#D10024')
    ax2.set_title("Sales for category", fontsize=12)
    ax2.tick_params(axis='x', labelrotation=45)
    ax3.bar(x=benefits4category.index, height=benefits4category['benefits'].values, color='#D10024')
    ax3.set_title("Benefits for category", fontsize=12)
    ax3.tick_params(axis='x', labelrotation=45)
    plt.tight_layout()
    # Codigo para guardar la figura y poder insertarla en el html
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    buffer = b''.join(buf)
    b2 = base64.b64encode(buffer)
    plot_url2 = b2.decode('utf-8')
    return render_template("statistics.html", plot_url=plot_url2)


if __name__ == '__main__':
    db.create_all()  # Creamos el modelo de datos
    app.run(debug=True)  # debug=True, al modificar codigo, el servidor de Flask se reinicia solo
