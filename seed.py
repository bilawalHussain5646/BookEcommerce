import sqlite3
from werkzeug.security import check_password_hash
from flask import session
import os
import requests


def InsertRecord(email, password):
    connection = sqlite3.connect('ebook.db', check_same_thread=False)
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO users(email,password) VALUES (?,?)", (email, password))
        connection.commit()
        message = True
    except:
        message = False

    cursor.close()
    connection.close()
    return message

def ChangePassword(email, password):
    connection = sqlite3.connect('ebook.db', check_same_thread=False)
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE users set password=? WHERE email = ?", (password,email))
        connection.commit()
        message = True
    except:
        message = False

    cursor.close()
    connection.close()
    return message


def CheckRecord(email, password):
    connection = sqlite3.connect('ebook.db', check_same_thread=False)
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT password FROM users WHERE email=?", (email,))
        result = cursor.fetchone()

        if (check_password_hash(result[0], password)):
            print("Matched")
            connection.commit()
            message = True

        else:
            print("Password is incorrect")
            message = False
        connection.commit()

    except:
        print("Query issue")
        message = False

    cursor.close()
    connection.close()
    return message



def FetchUser(email):
    connection = sqlite3.connect('ebook.db', check_same_thread=False)
    cursor = connection.cursor()
    result = []
    try:
        cursor.execute(
            "SELECT subscription,subscription_start_date,subscription_end_date from users where email = ?",(email,))
        result = cursor.fetchone()
        
        connection.commit()

    except:
        # error in query
        pass

    cursor.close()
    connection.close()
    return result


def FetchProduct(product_id):
    connection = sqlite3.connect('ebook.db', check_same_thread=False)
    cursor = connection.cursor()
    
    product_name = ""
    product_price =""
    try:
        cursor.execute(
            "SELECT product_name,product_price from products where product_id = ?",(product_id,))
        result = cursor.fetchone()
        product_name = result[0]
        product_price = result[1]
        connection.commit()

    except:
        # error in query
        pass

    cursor.close()
    connection.close()
    return product_name,product_price


def FetchProducts():
    connection = sqlite3.connect('ebook.db', check_same_thread=False)
    cursor = connection.cursor()
    products = []
    try:
        cursor.execute(
            "SELECT product_id,product_name,product_price,availability from products")
        result = cursor.fetchall()
        for product in result:
            products.append(product)
        connection.commit()

    except:
        # error in query
        pass

    cursor.close()
    connection.close()
    return products


def InsertAddCart(product_id, product_name,product_link,product_image_url, product_price, email):
    message = False
    connection = sqlite3.connect('ebook.db', check_same_thread=False)
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO cart(product_id,product_name,product_link,product_image_url,product_price,email) VALUES (?,?,?,?,?,?)",
                       (product_id, product_name,product_link,product_image_url, product_price, email,))
        message = True
        connection.commit()

    except:
        message = False

    cursor.close()
    connection.close()
    return message



def UpdateSubscription(email,subscription,subscription_start_date,subscription_end_date):
    connection = sqlite3.connect('ebook.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET subscription=?,subscription_start_date = ?,subscription_end_date=? where email=?", (subscription,subscription_start_date,subscription_end_date, email,)) 
    connection.commit()
    cursor.close()
    connection.close()
    return "True"





def PurchaseItems(email):
    message = False
    connection = sqlite3.connect('ebook.db', check_same_thread=False)
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT product_id from cart where email =?",(email,))
            
        result = cursor.fetchall()
        for product in result:
                productID = product[0]
                print(productID)
                cursor.execute("SELECT availability from products where product_id = ?",(productID,))
                result1 = cursor.fetchone()
                availability = result1[0]
                print(availability)
                availability-=1
                cursor.execute("UPDATE products SET availability=? where product_id=?", (availability, product[0],))
        cursor.execute("DELETE from cart where email=?", (email,))
        message = True
        connection.commit()

    except:
        message = False
    

    cursor.close()
    connection.close()
    return message


def FetchCart(email):
    products = []
    Total :float = 0
    connection = sqlite3.connect('ebook.db', check_same_thread=False)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT product_id,product_name,product_link,product_image_url,product_price from cart where email =?",(email,))
        
        result = cursor.fetchall()
        for product in result:
            products.append(product)
            Total = Total + float(product[4])
    except:
        pass
    return products,Total
    

def RemoveProduct(product_id,email):
 
    connection = sqlite3.connect('ebook.db', check_same_thread=False)
    cursor = connection.cursor()
    try:
        cursor.execute("Delete from cart where email =? AND product_id = ?",(email,product_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except:
        cursor.close()
        connection.close()
        return False

    
def InsertHistory(product_id, product_name,product_link,product_image_url, downloadLink, email):
    message = False
    connection = sqlite3.connect('ebook.db', check_same_thread=False)
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO history(product_id,product_name,product_link,product_image_url,downloadLink,email) VALUES (?,?,?,?,?,?)",
                       (product_id, product_name,product_link,product_image_url, downloadLink, email,))
        message = True
        connection.commit()

    except:
        message = False

    cursor.close()
    connection.close()
    return message


def FetchHistory(email):
    products = []
    connection = sqlite3.connect('ebook.db', check_same_thread=False)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT product_id,product_name,product_link,product_image_url,downloadLink from history where email =?",(email,))
        
        result = cursor.fetchall()
        for product in result:
            products.append(product)
            
    except:
        pass
    # print(products)
    return products