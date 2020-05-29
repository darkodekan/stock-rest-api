from flask import Flask, jsonify, request, render_template, make_response
from flask_restful import Resource, Api
from flask_mysqldb import MySQL
import random, configparser, logging


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

#UPDATE_SERVER_ID[1]=0
#UPDATE_SERVER_ID[2]=0
#UPDATE_SERVER_ID[3]=0


#find location of link
def get_url_server_id(product_url):
	try:
		conn = mysql.connect
		cursor = conn.cursor()
		servers_url = {}
		sql = "SELECT * FROM product WHERE url=%s"
		cursor.execute(sql, (product_url,))
		product_row = cursor.fetchone()
		cursor.close()
		conn.close()
		if product_row:
			return product_row["server_id"]
		else:
			return None
	except Exception as e:
		return None
#display contents of database
def get_all_json_products():
	try:
		print("HEEY")
		products = list()
		conn = mysql.connect
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM product");
		product_rows = cursor.fetchall()
		print(product_rows)
		cursor.close()
		conn.close()
		for product_row in product_rows:
			print(product_row)
			products.append(Product(product_row["product_id"], product_row["server_id"]).__repr__())
		return products
	except Exception as e:
		print(e)
def get_json_product(product_id):
	try:
		conn = mysql.connect
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM product WHERE product_id=%s", (product_id,));
		product_row = cursor.fetchone()
		return Product(product_row["product_id"], product_row["server_id"]).__repr__()
	except:
		return None
def get_server_products(server_id):
	try:
		products = list()
		conn = mysql.connect
		cursor = conn.cursor()
		cursor.execute("SELECT FROM product WHERE server_id=%s", (server_id,))
		products_rows = cursor.fetchall()
		for row in products_row:
			products.append(Product(row["product_id"], row["server_id"]))	
		cursor.close()
		conn.close()
		return products
	except Exception as e:
		return None
	
def is_product_database(product_id):
	try:
		products = list()
		conn = mysql.connect
		cursor = conn.cursor()
		cursor.execute("SELECT FROM product WHERE product_id=%s", (product_id,))
		
	except Exception as e:
		return None
#add try and catch
def add_to_database(product):
	try:
		conn = mysql.connect
		cursor = conn.cursor()
		sql = "INSERT INTO product(product_id, server_id) VALUES(%s,%s)"
		cursor.execute(sql, (product.product_id, product.server_id))
		conn.commit()
		cursor.close()
		conn.close()
		return True
	except Exception as e:
		print(e)
		return False

def delete_from_database(product_id):  
	try:
		conn = mysql.connect
		cursor = conn.cursor()
		sql = "DELETE FROM product WHERE product_id=%s"
		cursor.execute(sql, (product_id,))
		conn.commit()
		cursor.close()
		conn.close()
		return True
	except Exception as e:
		print(e)

def update_database(product_id1, product_id2):
	try:
		conn = mysql.connect
		cursor = conn.cursor()
		sql = "UPDATE product SET product_id=%s WHERE product_id=%s"
		cursor.execute(sql, (product_id2, product_id1))
		conn.commit()
		cursor.close()
		conn.close()
		return True
	except Exception as e:
		return False

def login(login_info):
    conn = mysql.connect
    cursor = conn.cursor()
    sql = "SELECT * FROM admin WHERE username=%s AND password=%s"
    username = admin_config["username"]
    password = admin_config["password"]
    cursor.execute(sql, (username, password))
    user = cursor.fetchone()
    if user is not None:
        if len(user)==0:
            return False
        else:
            return True
    return False

def add(product):
	add_to_database(product)
def delete(product_id):
	success = delete_from_database(product_id)
	if success:
		return {"success":"true"}
	else:
		return {"success":"false"}

def get_server_products(command):
	product_url_list = list()
	products = get_server_products(command["server_id"])
	if products:
		for product in products:
			product_url_list.append(product.url)	
		return {"product_url_list":product_url_list}			
	else:
		{"product_url_list":"fail"}
def get_server_update_id(id):
	pass	
	
class Introduction(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("index.html"),200,headers)

class AllProducts(Resource):
	def get(self):
		return {"products":get_all_json_products()}

	def post(self):
		json_object = request.get_json()
		add_to_database(Product(json_object["product_id"],json_object["server_id"])) 

#MAKE JSON OBJECT TO PYTHON OBJECT CONVERTER

class OneProduct(Resource):
	def get(self,product_id):
		return get_json_product(product_id) 
	def delete(self, product_id):
		delete(product_id)
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
	pass

api.add_resource(Introduction, "/")
api.add_resource(AllProducts, "/products")
api.add_resource(OneProduct, "/products/<string:product_id>")
api.add_resource(ProductsServer, "/products/server/<int:num>")
api.add_resource(Login, "/login")

if __name__ == "__main__":
    app.run(debug=True)
