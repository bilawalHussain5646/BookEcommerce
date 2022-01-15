from flask import Flask, flash, request, render_template, redirect, url_for, session, g,jsonify
from flask_mail import Mail
from datetime import datetime
from dateutil.relativedelta import relativedelta
from werkzeug.security import generate_password_hash
import webbrowser   
from SearchScript import Search
import seed
import schema
from Download_Link import FetchDownloadLink
# Flask application is created
app = Flask(__name__)

# Application secret key
app.secret_key = "Don't tell anyone"




mail = Mail(app)
# Created Main() for sending mail


# Route: Landing Page
# Description: It will be a static page for showing landing page
# Status: 

@app.route('/')
def landingpage():

        return render_template('Landing_Page.html')
        

# Route: Thank you
# Description: To show that payment is successfully done
# Status: 

@app.route('/success', methods=["GET","POST"])
def thankyou():
        return render_template('ThankYou.html')
        



# Route: Explore Books
# Description: Items will be displayed in this route
# Status: 

@app.route('/explore', methods=['GET', 'POST'])
def explorebooks():
    if 'email' in session:    
        g.email = session['email']     
        if request.method == 'POST': 
           
            if request.form['action'] == "search":
                searchText = request.form['search-text']
                data = Search(str(searchText))
                cart,Total = seed.FetchCart(session['email'])
                return render_template("Explore.html",data = data,cart=cart,searchText=searchText) 
        else:          # if Email is already in session
           # Then store it in g
            return render_template("Explore.html")  
    elif request.method == 'POST':
        if request.form['action'] == "search":
            searchText = request.form['search-text']
            data = Search(str(searchText))
            return render_template("Explore.html",data = data,searchText=searchText)
    else:  # Else

        return render_template("Explore.html")    # render explorebooks



# Route: Profile
# Description: It will display profile 
# Status: 

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'email' in session:   
        g.email = session['email']        # Then store it in g 
        if request.method == 'POST':      # When a post request is send to the profile
            if request.form['action'] == "ChangePassword":
                prevpass= request.form['prevpass']
                if seed.CheckRecord(session['email'],prevpass):
                    newpass= request.form['newpass']
                    confirmpass= request.form['confirmpass']
                    if (confirmpass == newpass):
                        newpass = generate_password_hash(newpass)
                        if seed.ChangePassword(session['email'],newpass):
                            flash("Password successfully updated!", "success")
                        else:
                            flash("Server Busy", "info")
                    else:
                        flash("Password didn't matched check your New and Confirm Password!","danger")
                else:
                    flash("Previous Password is incorrect. Enter again!", "danger")
                ## Will get details from form and update in the database
                return redirect(url_for('profile')) 
        else:       # if Email is already in session
            
            # fetch products
            return render_template('Profile.html',session=session)
    else:
        flash("Login to your account first ! ","warning")
        return redirect(url_for('login')) 
    

# Route: Downloads
# Description: It will display books that are available for download
# Status: 

@app.route('/downloads', methods=['GET', 'POST'])
def downloads():
    if 'email' in session:    
        g.email = session['email']        # Then store it in g 
        if request.method == 'POST':      # When a post request is send to the downloads
                if "Downloads" in request.form['action']:
                    downloadLink = request.form['action'].replace('Downloads','')
                    print("This is Download Link: ",downloadLink)
                    id_starting = downloadLink.rfind('-') + 1
                    print(downloadLink[id_starting])
                    temp = list(downloadLink)
                    temp[id_starting] = "d"
                    downloadLink = "".join(temp)
                    # print(downloadLink)
                    print(FetchDownloadLink(downloadLink))
                return redirect(url_for('downloads'))
        else:         
            
            product= seed.FetchHistory(session['email'])
            # render downloads route
            return render_template('Downloads.html',session=session,products=product)


    else:
        flash("Login to your account first ! ","warning")
        return redirect(url_for('login')) 



# Route: Login
# Description: Login Features are set in this route
# Status : Completed
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:               # if Email is already in session
        g.email = session['email']        # Then store it in g
        # And redirect it to contact_info route
        return redirect(url_for('explorebooks'))

    elif request.method == 'POST':      # When a post request is send to the login page
        # It will check the action if the action is login
        if (request.form['action'] == 'login'):
            # Email will be requested from the form and stored in email variable
            email = request.form['email']
            # Password is requested and stored in password field
            password = request.form['password']
            # send it to checkRecord method where our backend will check whether our login information is valid or invalid if valid it will send True else False
            resp = seed.CheckRecord(email, password)
            if (resp):        # if resp is True
                USER  = seed.FetchUser(email)
                session['email'] = email  # Store the email in session
                session['subscription'] = USER[0]
                session['subscription_start_date'] = USER[1]
                session['subscription_end_date'] = USER[2]
                # print(USER[0])
                # And Redirect it to contact_info route
                return redirect(url_for('landingpage'))
            else:     # Else
                # Show message that Email or password is invalid
                flash("Email or Password is invalid", "danger")
                # And redirect to login again
                return redirect(url_for('login'))
    else:  # Else
        return render_template("login.html")    # render login page


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# Route: Sign up Route
# Description: Add and display sign up form
# Status : Completed


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if 'email' in session:
        g.email = session['email']
        # print(session['email'])
        return redirect(url_for('explorebooks'))

    elif request.method == 'POST':

        if (request.form['action'] == 'signup'):

            password = request.form['password']
            confirmPassword = request.form['confirmPassword']
            if (password == confirmPassword):
                password = generate_password_hash(password)
                email = request.form['email']

                resp = seed.InsertRecord(email, password)
                if (resp):
                    flash("Account Created Successfully", "success")
                    return redirect(url_for('signup'))
                else:
                    flash("Use another email", "danger")
                    return redirect(url_for('signup'))
            else:
                flash("Password doesn't matched", "danger")
                return redirect(url_for('signup'))

    else:
        return render_template("signup.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# Route: Cart
# Description: Purchasing Items will be done in this route
# Status : 


@app.route('/add-cart', methods=['GET', 'POST'])
def cart():
    if 'email' in session:
        if session['subscription'] != None:
            return redirect(url_for('explorebooks'))
        else:
            g.email = session['email']
            if request.method == 'POST':
                link = request.form['action'].replace('addCart', '')
                if("addCart" in request.form['action']):
                    email = session['email']
                    id = "id" + link
                    title = "title"+link
                    imageURL = "imageURL" + link
                    id = request.form[id]
                    title = request.form[title]
                    imageURL = request.form[imageURL]
                    # print({"id": id,"title": title, "imageURL": imageURL,"Link": link})
                    # for storing data into Database
                    resp = seed.InsertAddCart(id,title,link,imageURL,"1.99",email)
                    if (resp):
                        flash("Book Added to Cart", "success")
                        return redirect(url_for('cart'))
                    else:
                        
                        flash("Book Not Added to Cart", "danger")
                        return redirect(url_for('explorebooks'))
                elif("Remove" in request.form['action']):
                    id = request.form['action'].replace('Remove', '')
                    email = session['email']
                    resp = seed.RemoveProduct(id,email)
                    if (resp):
                        flash("Book Successfully Removed", "success")
                        return redirect(url_for('cart'))
                    else:
                        
                        flash("Failed to remove Book from Cart", "danger")
                        return redirect(url_for('cart'))
                else:
                    flash("You are trying to access the page without permission", "danger")
                    return redirect(url_for('explorebooks'))

            else:
                # Fetch cart data from cart table
                cartinfo,Total = seed.FetchCart(session['email'])

            # send data to cart page
            return render_template('cart.html',cartinfo=cartinfo,Total=Total)
    else:
        flash("You haven't login yet", "warning")
        return redirect(url_for('login'))


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# Route: Cart
# Description: Purchasing Items will be done in this route
# Status : 


@app.route('/subscription', methods=['GET', 'POST'])
def subscription():
    if 'email' in session:
        
   
        print(datetime.today())
        if request.method == 'POST':
            subs ="yes"
            starting_date =datetime.today()
            print(starting_date)
            starting_date = starting_date.strftime("%Y-%m-%d %H:%M:%S")
            ending_date = datetime.today() +  relativedelta(months=1)
            ending_date = ending_date.strftime("%Y-%m-%d %H:%M:%S")

            seed.UpdateSubscription(session['email'],subs,starting_date,ending_date)

            session['subscription'] = subs
            session['subscription_start_date'] = starting_date
            session['subscription_end_date'] = ending_date
            
            flash("Successfully purchased subscription", "success")
            return redirect(url_for("subscription"))
                

        else:
            if session['subscription'] != None:
                    ending_date = datetime.strptime(session['subscription_end_date'], '%Y-%m-%d %H:%M:%S')
                    if session['subscription_end_date'] and ending_date >= datetime.today():
                        return render_template('subscription.html')
                    else:
                        session['subscription'] = None
                        session['subscription_start_date'] = None
                        session['subscription_end_date'] = None
                        res = seed.UpdateSubscription(session['email'],None,None,None)
                        flash("Your subscription is over", "warning")
                        return render_template('subscription.html')

            else:
                return render_template('subscription.html')
  
    else:
        flash("You haven't login yet", "warning")
        return redirect(url_for('login'))


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response



# Route: MovingData
# Description: MovingData to Downloads
# Status : 


@app.route('/process', methods=['GET' ,'POST'])
def process():
    if 'email' in session:
       
            if request.method == 'POST':
                if session['subscription'] != None:
                    ending_date = datetime.strptime(session['subscription_end_date'], '%Y-%m-%d %H:%M:%S')
                    if session['subscription_end_date'] and ending_date >= datetime.today():
                        downloadLink = request.form['action'].replace('downloadBook', '')
                        id_starting = downloadLink.rfind('-') + 1
                        # print(downloadLink[id_starting])
                        temp = list(downloadLink)
                        temp[id_starting] = "d"
                        downloadLink = "".join(temp)
                        # print(downloadLink)
                        downloadLink = FetchDownloadLink(downloadLink)
                        webbrowser.open_new_tab(downloadLink)
                        return redirect(url_for("explorebooks"))

                    else:
                        session['subscription'] = None
                        session['subscription_start_date'] = None
                        session['subscription_end_date'] = None
                        res = seed.UpdateSubscription(session['email'],None,None,None)
                        flash("Your subscription is over", "warning")
                        return redirect(url_for(explorebooks))
   
                else:
                    cart,Total = seed.FetchCart(session['email'])
                    for c in cart:

                        
                        downloadLink = c[2]
                        id_starting = downloadLink.rfind('-') + 1
                        # print(downloadLink[id_starting])
                        temp = list(downloadLink)
                        temp[id_starting] = "d"
                        downloadLink = "".join(temp)
                        # print(downloadLink)
                        downloadLink = FetchDownloadLink(downloadLink)

                        seed.InsertHistory(c[0],c[1],c[2],c[3],downloadLink,session['email'])
                        seed.RemoveProduct(c[0],session['email'])
                    
                    flash("Successfully Purchased", "success")
                    return "True"

            else:
                return redirect(url_for('UnAuthorized'))
    else:
        flash("Session Ended", "warning")
        return redirect(url_for('login'))

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


# Route: Privilages
# Description: Privilages Page
# Status : Completed

@ app.route("/unauthorized")
def UnAuthorized():
    return render_template("UnAuthorized.html")

# Route: Unknown Page
# Description: Unknown Page Page
# Status : Completed

@app.errorhandler(404)
def not_found(e):
    return render_template("Error.html")

@ app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


# Route: Logout
# Description: Logout the account
# Status : Completed



@ app.route("/logout")
def logout():
    if 'email' in session:
        session.pop('email', None)
        session.pop('subscription',None)
        session.pop('subscription_start_date',None)
        session.pop('subscription_end_date',None)
        flash("Account Logged Out", "success")
        return redirect(url_for('explorebooks'))
    else:
        flash("Session Ended", "danger")
        return redirect(url_for('login'))


@ app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


app.debug = True


if __name__ == '__main__':
    app.run(debug=True)
