from flask import Flask, jsonify, request, render_template, make_response, Response
from flask_restful import Resource, Api
from flask_mysqldb import MySQL
import random, configparser, logging
import time

class Product():
	def __init__(self, product_id, server_id):
		self.product_id = product_id
		self.server_id = server_id
	def __repr__(self):
		return { "product_id" : self.product_id, "server_id" : self.server_id}

#logging and logging configuration
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "LOGGING.log", level = logging.DEBUG, format = LOG_FORMAT)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger()

#read configuration file
config = configparser.ConfigParser()
config.read("SETTINGS.ini")
db_config = config["database"]
admin_config = config["admin"]
num_servers = len(config["general"]["server_ids"].split(","))
#add number of servers config file
app = Flask(__name__)

#setup mysql database credentials
app.config['MYSQL_USER'] = db_config["mysql_user"]
app.config['MYSQL_PASSWORD'] = db_config["mysql_password"]
app.config['MYSQL_HOST'] = db_config["mysql_host"]
app.config['MYSQL_DB'] = db_config["mysql_database"]
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
api = Api(app)



#wrapper from mysql, handles all low level stuff
def database_execute(sql, values=None):
	result = None
	conn = mysql.connect
	cursor = conn.cursor()
	if values:
		cursor.execute(sql, values) 
	else:
		cursor.execute(sql)
	if "INSERT" in sql or "UPDATE" in sql or "DELETE" in sql:
		conn.commit()
	else:
		result = cursor.fetchall()
	cursor.close()
	conn.close()
	return result
#update id
#create new table to update ids and return them
	#mysql statement
	#turn it into json

#find location of link
#display contents of database
#factory design
def get_all_products(json=None):
	try:
		products = list()
		result = database_execute("SELECT * FROM product");
		for row in result:
			if json=="json":
				products.append(Product(row["product_id"], row["server_id"]))
			elif json==None:
				product.append(Product(row["product_id"], row["server_id"])__repr__)
		return products
	except Exception as e:
		print(e)

def get_json_product(product_id):
	try:
		result = database_execute("SELECT * FROM product WHERE product_id=%s", (product_id,));
		return Product(result[0]["product_id"], result[0]["server_id"]).__repr__()
	except Exception as e:
		print(e)
		return None
def get_products_server(server_id, json_form="json"):
	try:
		products = list()
		result = database_execute("SELECT * FROM product WHERE server_id=%s", (server_id,))
		for row in result:
			if json_form == True:
				products.append(Product(row["product_id"], row["server_id"]))				else:
				product.append(Product(row["product_id"], row["server_id"]))
		return products
	except Exception as e:
		print(e)
		return None
	
def is_product_database(product_id):
	try:
		products = list()
		result = database_execute("SELECT FROM product WHERE product_id=%s", (product_id,))

		
	except Exception as e:
		return None
#add try and catch
def add_to_database(product):
	try:
		sql = "INSERT INTO product(product_id, server_id) VALUES(%s,%s)"
		database_execute(sql, (product.product_id, product.server_id))
		return True
	except Exception as e:
		print(e)
		return False

def delete_from_database(product_id):  
	try:
		sql = "DELETE FROM product WHERE product_id=%s"
		database_execute(sql, (product_id,))
		return True
	except Exception as e:
		print(e)

def update_database(product_id1, product_id2):
	try:
		sql = "UPDATE product SET product_id=%s WHERE product_id=%s"
		database_execute(sql, (product_id2, product_id1))
		return True
	except Exception as e:
		return False

def login(login_info):
    sql = "SELECT * FROM admin WHERE username=%s AND password=%s"
    username = admin_config["username"]
    password = admin_config["password"]
    database_execute(sql, (username, password))
    if user is not None:
        if len(user)==0:
            return False
        else:
            return True
    return False

#should we make factory design?
def get_server_update_id(id):
	pass	
	
class Introduction(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("index.html"),200,headers)

class AllProducts(Resource):
	def get(self):
		return get_all_json_products()

	def post(self):
		json_object = request.get_json()
		add_to_database(Product(json_object["product_id"],json_object["server_id"])) 

#MAKE JSON OBJECT TO PYTHON OBJECT CONVERTER

class OneProduct(Resource):
	def get(self,product_id):
		return get_json_product(product_id) 
	def delete(self, product_id):
		delete_from_database(product_id)
	def put(self, product_id):
		json_object = request.get_json()
		print(json_object)
		update_database(product_id, json_object["product_id"])

class Login(Resource):
	def post(self):
		login_json = request.get_json()
		if login(login_json):
			return {"success":True}
		else:
			return {"success":False}
class ProductsServer(Resource):
	def get(self, server_id):
		products  = get_products_server_json(server_id)
		if products:
			return Response(products, status=200, mimetype='application/json')
		else:
			return Response("hheey", status=404, mimetype='application/json')
class Update(Resource):
	def get(self, server_id):
		return {"update_id" : get_update_id(server_id)}
	
		
	

api.add_resource(Introduction, "/")
api.add_resource(AllProducts, "/product")
api.add_resource(OneProduct, "/product/product_id/<string:product_id>")
api.add_resource(ProductsServer, "/product/server_id/<int:server_id>")
api.add_resource(Update, "/update/server_id/<int:server_id>")
api.add_resource(Login, "/login")

if __name__ == "__main__":
    app.run(debug=True)
