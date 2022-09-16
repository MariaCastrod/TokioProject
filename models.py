from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hmac import compare_digest

""" Tras varios problemas con pagination(), encuentro en un foro que es de Flask-SQLAlchemy y no de SQLAlchemy
por lo que tengo que modificar bastante el modelo de datos planteado inicialmente. 
Ademas, para no obtener errores de importacion circular,
se instancia el servidor web de Flask en este fichero y se vincula el objeto SQLAlchemy() a esta app especifica. """
# Se instancia el servidor web de Flask y se almacena
app = Flask(__name__)
# Conexion con la bbdd. Incluido el driver de mysql, instalado previamente
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/electro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Clase producto
class Product(db.Model):
    # EN LA EXTENSION FLASK-SQLALCHEMY NO ES NECESARIO INDICAR EL NOMBRE DE LA TABLA. COGE EL DE LA CLASE.
    # __tablename__ = "product"

    reference = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(200), nullable=True)
    name = db.Column(db.String(200), nullable=True)
    brand = db.Column(db.String(200), nullable=True)
    description = db.Column(db.String(200))
    purchase_price = db.Column(db.Float)
    selling_price = db.Column(db.Float)
    stock = db.Column(db.Integer)
    sales = db.Column(db.Integer)

    def __init__(self, category, name, brand, description, purchase_price, selling_price, stock, sales):
        self.category = category
        self.name = name
        self.brand = brand
        self.description = description
        self.purchase_price = purchase_price
        self.selling_price = selling_price
        self.stock = stock
        self.sales = sales

    def __repr__(self):
        return "Product {}: {}, {}€".format(self.reference, self.name, self.selling_price)

    def __str__(self):
        return "Product {}: {}, {}€".format(self.reference, self.name, self.selling_price)


# Clase Proveedor
class Supplier(db.Model):
    # __tablename__ = "supplier"

    reference = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    direction = db.Column(db.String(200), nullable=True)
    cif = db.Column(db.String(200), nullable=True)
    bank_account = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.Integer)

    def __init__(self, name, direction, cif, bank_account, phone):
        self.name = name
        self.direction = direction
        self.cif = cif
        self.bank_account = bank_account
        self.phone = phone

    def __repr__(self):
        return "Supplier {}: {}".format(self.reference, self.name)

    def __str__(self):
        return "Supplier {}: {}".format(self.reference, self.name)


# Clase Usuario. Ampliar los atributos y modificar la gestion de la contraseña.
class User(db.Model):
    # __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    full_name = db.Column(db.String(200), nullable=False)

    # NOTE: In a real application make sure to properly hash and salt passwords
    def check_password(self, password):
        return compare_digest(password, "password")

    def __repr__(self):
        return "User {}: {}".format(self.id, self.name)

    def __str__(self):
        return "User {}: {}".format(self.id, self.name)
