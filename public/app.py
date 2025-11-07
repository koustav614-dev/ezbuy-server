from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# ----------------------------
# Database connection
# ----------------------------
conn_obj = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Abhijit@99",
    database="ezbuy"
)
cur_obj = conn_obj.cursor(dictionary=True)

# ----------------------------
# USER ROUTES
# ----------------------------

@app.route("/")
def login_page():
    """Default route – login page"""
    return render_template("login.html")

@app.route("/index")
def index():
    """Homepage (after login or registration)"""
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login route"""
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]

        query = "SELECT * FROM registration WHERE Username=%s"
        cur_obj.execute(query, (username,))
        result = cur_obj.fetchone()

        if result and password == result["Password"]:
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Registration route"""
    if request.method == "POST":
        username = request.form["Username"]
        email = request.form["Email"]
        password = request.form["Password"]

        sql = "INSERT INTO registration (Username, Email, Password) VALUES (%s, %s, %s)"
        try:
            cur_obj.execute(sql, (username, email, password))
            conn_obj.commit()
            return redirect(url_for("index"))
        except mysql.connector.Error as e:
            return render_template("login.html", error=f"Error: {e}")
    return render_template("login.html")

# ----------------------------
# PRODUCT ROUTES
# ----------------------------
@app.route("/product-details/<int:product_id>")
def product_details(product_id):
    """Dynamic product detail pages"""
    return render_template(f"product-details-{product_id}.html")

# ----------------------------
# ADMIN PANEL ROUTES
# ----------------------------
@app.route("/admin")
def admin_panel():
    """Admin panel – show product list"""
    cur_obj.execute("SELECT * FROM products")
    products = cur_obj.fetchall()
    return render_template("admin.html", products=products)

@app.route("/add_product", methods=["POST"])
def add_product():
    """Add a new product from admin form"""
    name = request.form["name"]
    price = request.form["price"]
    description = request.form["description"]
    image_url = request.form["image_url"]

    sql = "INSERT INTO products (name, price, description, image_url) VALUES (%s, %s, %s, %s)"
    cur_obj.execute(sql, (name, price, description, image_url))
    conn_obj.commit()

    return redirect(url_for("admin_panel"))

@app.route("/delete_product/<int:id>")
def delete_product(id):
    """Delete a product from admin panel"""
    cur_obj.execute("DELETE FROM products WHERE id = %s", (id,))
    conn_obj.commit()
    return redirect(url_for("admin_panel"))

@app.route("/product")
def product():
    """Display all products for customers (not admin)."""
    cur_obj.execute("SELECT * FROM products")
    products = cur_obj.fetchall()
    return render_template("product.html", products=products)


# ----------------------------
# RUN APP
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
