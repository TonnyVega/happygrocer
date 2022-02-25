from flask import Blueprint,render_template,request,url_for,redirect
from os import path
from flask_login import current_user, login_required
import psycopg2
from werkzeug.utils import redirect

tables = Blueprint('tables',__name__)

conn = psycopg2.connect(user='tdhbjbpwtrjlvv',
                        password='7f959ad6649dd32a65c45df4237f70604990e0e9d8f82ba16d643074de0a1b3c',
                        host='ec2-3-227-195-74.compute-1.amazonaws.com',
                        port='5432',
                        database='dah20ug77pnqp4')

cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS inventory(p_id SERIAL PRIMARY KEY,name VARCHAR(255),category VARCHAR(255),quantity INT NOT NULL,b_price INT NOT NULL,s_price INT NOT NULL, date_purchased TIMESTAMP DEFAULT NOW())")
cur.execute("CREATE TABLE IF NOT EXISTS sales(s_id SERIAL PRIMARY KEY ,p_id INT,name VARCHAR(100),sold INT,b_pice INT,s_price INT,sold_at DATE NOT NULL DEFAULT NOW())")



@tables.route('/inventory', methods=['GET','POST'])
@login_required
def inventory():
    if request.method== 'POST':
        cur=conn.cursor()
        name=request.form['name']
        cat=request.form['category']
        quantity=request.form['quantity']
        bp= request.form['b_price']
        sp=request.form['s_price']
        cur=conn.cursor()
        cur.execute(""" INSERT INTO inventory(name,category,quantity,b_price,s_price) VALUES (%(name)s,%(cat)s,%(quantity)s,%(bp)s,%(sp)s)""",{"name":name,"cat":cat,"quantity":quantity,"bp":bp,"sp":sp})
        conn.commit()
        return redirect('/inventory')
    else:
        cur=conn.cursor()
        cur.execute(""" SELECT * FROM inventory""")
        rows=cur.fetchall()
        return render_template('inventory.html',user=current_user, rows=rows)


@tables.route('/inventory/<int:x>',methods=['GET','POST'])
def item(x):
    
    cur=conn.cursor()
    cur.execute("""SELECT name FROM inventory WHERE p_id=%(p_id)s""",{"p_id":x})
    item=cur.fetchone()
    cur.execute("""SELECT p_id,name,category,quantity,b_price, s_price FROM inventory WHERE p_id= %(p_id)s""", {"p_id":x})
    x=cur.fetchall()
    print(item)

    if request.method == "POST":
        cur = conn.cursor()
        p_id=request.form["p_id"]
        name=request.form["name"]
        quantity= request.form["quantity"]
        b_price=request.form["b_price"]
        s_price=request.form["s_price"]
        cur.execute("""select quantity from inventory where p_id=%(p_id)s and name =%(name)s""",{"p_id":p_id, "name":name})
        y=cur.fetchone()
        quantity=int(quantity)
        b=y[0]-quantity
        if b>=0:
                sold=quantity
                cur.execute(""" UPDATE inventory SET quantity=%(b)s WHERE p_id=%(p_id)s AND name =%(name)s""",{"b":b,"name":name ,"p_id":p_id})
                cur.execute("""INSERT INTO sales(p_id,name,sold,b_price,s_price) VALUES(%(p_id)s,%(name)s,%(sold)s,%(b_price)s,%(s_price)s)""",{"p_id":p_id,"name":name,"sold":sold,"b_price":b_price,"s_price":s_price})
                conn.commit()           
                return render_template('item.html',user=current_user,rows=x)
   
    cur= conn.cursor()
    cur.execute("""SELECT inventory.name, inventory.quantity,sales.sold FROM inventory JOIN sales ON inventory.p_id= sales.p_id""")
    data=cur.fetchall()
    print('this is',data)
    colors= ['blue',
            'red']
    values=[row[0] for row in data]
    labels=[row[1] for row in data]
    return render_template('item.html',user=current_user,rows=x,values=values,labels=labels,data=data,colors=colors)


@tables.route('/sales', methods=['GET','POST'])
def view_item():
    cur=conn.cursor()
    cur.execute("""SELECT s_id,p_id,name,sold,b_price,s_price, sold_at FROM sales""")
    rows= cur.fetchall()
    return render_template('sales.html',rows=rows)


@tables.route('/sales/<int:x>')
def view_sales(x):
    cur=conn.cursor()
    cur.execute("""SELECT s_id,p_id,name,sold,b_price,s_price, sold_at FROM sales WHERE p_id=%(p_id)s""",{"p_id":x})
    x=cur.fetchall()
    return render_template('sales.html',rows=x)


@tables.route('/inventory',methods=['GET','POST'])
@login_required
def edit():
    if request.method == "POST":
        cur= conn.cursor()
        p_id= request.form["p_id"]
        name= request.form["name"]
        cat=request.form["category"]
        quantity= request.form["quantity"]
        b_price= request.form["b_price"]
        s_price= request.form["s_price"]
        cur.execute("""UPDATE inventory SET p_id=%(p_id)s,name=%(name)s,category=%(cat)s,quantity=%(quantity)s,b_price=%(b_price)s,s_price=%(s_price)s WHERE p_id=%(p_id)s""",{"p_id":p_id,"name":name,"category":cat,"quantity":quantity,"b_price":b_price,"s_price":s_price})
        conn.commit()
    return redirect(url_for('inventory'))


