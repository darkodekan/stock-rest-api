from flask import Flask, jsonify, request, render_template, make_response
from flask_restful import Resource, Api
from flask_mysqldb import MySQL
import random, configparser, logging


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
num_servers = config["general"]["num_servers"]
#add number of servers config file
app = Flask(__name__)

#setup mysql database credentials
app.config['MYSQL_USER'] = db_config["mysqluser"]
app.config['MYSQL_PASSWORD'] = db_config["mysqlpassword"]
app.config['MYSQL_HOST'] = db_config["mysqlhost"]
app.config['MYSQL_DB'] = db_config["mysqldatabase"]
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
api = Api(app)

UPDATE_SERVER_ID[1]=0
UPDATE_SERVER_ID[2]=0
UPDATE_SERVER_ID[3]=0

for server in servers_id:
	UPDATE_SERVER_ID[

class Product():
	def __init__(self, url, server_id):
		self.url = url
		self.server_id = server_id

#find location of link
def get_url_server_id(product_url):
	try:
    	conn = mysql.connect
    	cursor = conn.cursor()
    	servers_url = {}
    	sql = "SELECT * FROM products WHERE url=%s"
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
def get_all_products():
	try:
		products = list()
    	conn = mysql.connect
    	cursor = conn.cursor()
    	cursor.execute("SELECT * FROM products");
    	product_rows = cursor.fetchall()
    	cursor.close()
    	conn.close()
		for product in product_rows:
			products.append(Product(row["url"], row["server_id"])
    	return products
	except Exception as e:
		return None

def get_server_products(server_id):
	try:
		products = list()
		conn = mysql.connect
		cursor = conn.cursor()
		cursor.execute("SELECT FROM products WHERE server_id=%s", (server_id,))
		products_rows = cursor.fetchall()
		for row in products_row:
			products.append(Product(row["url"], row["server_id"])	
		cursor.close()
		conn.close()
		return products
	except Exception as e:
		return None
	
def is_product_exists(url):
	try:
		products = list()
		conn = mysql.connect
		cursor = conn.cursor()
		cursor.execute("SELECT FROM products WHERE url=%s", (url,))

	except Exception as e:
		return None
#add try and catch
def add_to_database(product):
	try:
        conn = mysql.connect
        cursor = conn.cursor()
        sql = "INSERT INTO products(url, server_id) VALUES(%s,%s)"
        cursor.execute(sql, (product.url, product.server_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
	except Exception as e:
		print(e)
		return False

def delete_from_database(product):  
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        sql = "DELETE FROM products WHERE url=%s"
        cursor.execute(sql, product.url)
        conn.commit()
        cursor.close()
        conn.close()
        return True
	except:
    	return False

def update_database(product1, product2):
	try:
		conn = mysql.connect
		cursor = conn.cursor()
		sql = "UPDATE products SET url=%s WHERE url=%s"
		cursor.execute(sql, product.url, product.url)
		conn.commit()
		cursor.close()
		conn.close()
		return True
	except Exception as e:
		return False

def login(login_info):
    conn = mysql.connect
    cursor = conn.cursor()
    sql = "SELECT * FROM admins WHERE username=%s AND password=%s"
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

def add(command):
	exists = is_product_exists(command["url"])
	if exists==True:
		success = None
        if command["server"]=="random":
             success = add_to_database(Product(command["url"], random.randint(1,3))
        else:
             success = add_to_database(Product(command["url"], num_server=command["server"]))
		if success:
			 return {"success":"true"}
		else:
			return {"success":"false"}
	else if exists == False:
		return {"success":"exists"}
	return {"success":"false"}
def delete(command):
	if exists == False:
    	success = delete_from_database(command["url"])
		if success:
			return {"success":"true"}
		else:
			return {"success":"false"}
	else if exists == True:
		return {"success":"exists"}
	return {"success":"false"}

def get_url_list():
	product_url_list = list()
	products = get_server_products(command["server_id"])
	if products:
		for product in products:
			product_url_list.append(product.url)	
		return {"product_url_list":product_url_list}			
	else:
		{"product_url_list":"fail"}
def get_server_update_id(id):
	
	
class Introduction(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("index.html"),200,headers)

class Database(Resource):
    def get(self):
        return {"message":get_all_links()}

    def post(self):
        command = request.get_json()
		exists = is_product_exists(command["url"])
        if command["action"] == "add":
			add(command,exists)
        elif command["action"] == "update":
			update(command,exists)
        elif command["action"] == "delete":
			delete(command,exists)
		elif command["action"] == "get_url_list":
			get_url_list(command, exists)
		elif command["action"] == "check_update":
			return update_id[command["server_id"]]
			

class Login(Resource):
	def post(self):
		login_json = request.get_json()
		if login(login_json):
			return {"success":True}
		else:
			return {"success":False}

api.add_resource(Introduction, "/")
api.add_resource(Database, "/database")
api.add_resource(ServerRetrieval, "/database/<int:num>")
api.add_resource(Login, "/login")

if __name__ == "__main__":
    app.run(debug=False)
