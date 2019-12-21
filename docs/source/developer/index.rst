Developer Guide
===============

Database Design
---------------

**include the E/R diagram(s)**

Code
----

**explain the technical structure of your code**

   .. code-block:: python

      def find_author_inner(author):
			with dbapi2.connect(url) as connection:
				cursor = connection.cursor()
				sorgu = "SELECT * FROM ARTICLES inner join USERS on author = USERS.id  WHERE author = %s"
				cursor.execute(sorgu,(author,))
				user = cursor.fetchall()
				cursor.close()
				return user
	
   Articles table stores article informations and its author id. This code provides to take author name by inner join with Users table.
	
   .. code-block:: python
	
	  def find_author(author):
			with dbapi2.connect(url) as connection:
				cursor = connection.cursor()
				sorgu = "SELECT * FROM ARTICLES WHERE author = %s"
				cursor.execute(sorgu,(author,))
				user = cursor.fetchall()
				cursor.close()
				return user
				
   This function returns articles that its author is given as parameter.
	
   .. code-block:: python

	  def find_articles():
			with dbapi2.connect(url) as connection:
				cursor = connection.cursor()
				sorgu = "SELECT * FROM ARTICLES"
				cursor.execute(sorgu)
				articles = cursor.fetchall()
				cursor.close()
				return articles
			
   This function returns all articles in our database.
	
   .. code-block:: python
	
	  def find_favourites(userid):
		with dbapi2.connect(url) as connection:
			cursor = connection.cursor()
			sorgu = "SELECT * FROM FAVOURITES inner join MUSICS on musics.id = musicid  WHERE userid = %s"
			cursor.execute(sorgu,(userid,))
			musics = cursor.fetchall()
			cursor.close()
			return musics
	
   This function provides to take music information which is added to favourite list by user whose id is parameter.

   .. code-block:: python
	
	  def find_musics_id(id):
		with dbapi2.connect(url) as connection:
			cursor = connection.cursor()
			sorgu = "SELECT * FROM MUSICS where id = %s"
			cursor.execute(sorgu,(id,))
			music = cursor.fetchone()
			cursor.close()
			return music
			
   Function that returns music which has given id.
	
   .. code-block:: python
	
	  def find_articles_id(id):
		with dbapi2.connect(url) as connection:
			cursor = connection.cursor()
			sorgu = "SELECT * FROM ARTICLES where id = %s"
			cursor.execute(sorgu,(id,))
			articles = cursor.fetchone()
			cursor.close()
			return articles
			
   This function returns article which has given id.
	
   .. code-block:: python
	  def delete_musics_id(id):
		with dbapi2.connect(url) as connection:
			cursor = connection.cursor()
			sorgu = "delete FROM MUSICS where id = %s"
			cursor.execute(sorgu,(id,))
			cursor.close()

	  def delete_articles_id(id):
		with dbapi2.connect(url) as connection:
			cursor = connection.cursor()
			sorgu = "delete FROM ARTICLES where id = %s"
			cursor.execute(sorgu,(id,))
			cursor.close()

      def delete_user_username(username):
		with dbapi2.connect(url) as connection:
			cursor = connection.cursor()
			sorgu = "delete FROM USERS where username = %s"
			cursor.execute(sorgu,(username,))
			cursor.close()
	
   Functions that deletes music, article and user has given id or username.
	
   .. code-block:: python
	  def find_keyword(keyword):
		with dbapi2.connect(url) as connection:
			cursor = connection.cursor()
			sorgu = "Select * from articles where title like '%" + keyword + "%'"
			cursor.execute(sorgu) 
			word = cursor.fetchall()
			connection.commit()
			cursor.close()
			return word
	
   This function is used in search operation which user can type an article title to read it. This function lists all articles, its title contains word that user typed.
	
   I wanted to inform about this functions because the number of functions is too much for each operation.
	
   Jinja template is used for rendering html pages.
   .. code-block:: python
	  {% if session["logged_in"] and session["username"]=="admin" %}
		  <li class="nav-item active">
            <a class="nav-link" href="/admindashboard"> Dashboard</a>
          </li>
          <li class="nav-item active">
            <a class="nav-link" href="/logout"> Log out</a>
          </li>
          {% elif session["logged_in"] %}
          <li class="nav-item active">
            <a class="nav-link" href="/userdashboard"> Dashboard</a>
          </li>

   Navbar is designed by looking at session. If user is admin it navigates to admindashboard otherwise, to userdashboard.
   Flash messages are used to inform user about the operations.
   .. code-block:: python
	  @app.route("/admindashboard")
	  @login_required
	  def admindashboard():
		articles = find_articles()
		musics = find_musics()
		return render_template("admindashboard.html",articles=articles,musics=musics)

   In admin dashboard, admin can insert article and musics but user can only publish articles, they can add musics to their favourite list and see their list on user dashboard.
	
   .. code-block:: python
	  @app.route("/login",methods=["GET","POST"])    
	  def login():
		form = LoginForm(request.form)
		if request.method == "POST":
			username = form.username.data
			password_entered = form.password.data
			result = find_username(username)
			if (result != None):
				data = result       
				real_password = data[5]
				if( sha256_crypt.verify(password_entered,real_password)):   
					if (request.form.get("login")!= None):
						flash("Login successfully","success")  
						user = User(data[3],data[2],data[3],data[4],data[5])
						user.set_id(data[0])
						login_user(user,remember=True)
						session["username"] = username
						session["logged_in"] = True
						return redirect(url_for("index"))  
					flash("Login successfully","success")
					user = User(data[3],data[2],data[3],data[4],data[5])
					user.set_id(data[0])
					login_user(user,remember=False)
					session["logged_in"] = True
					session["username"]=username
					return redirect(url_for("index"))
				else:
					flash("Wrong password","danger")
					return redirect(url_for("login"))
			else:
				flash("User not exists !","danger")
				return redirect(url_for("login"))
		elif request.method == "GET":
			return render_template("login.html",form=form)
		return render_template("login.html",form=form)

   Login is controlled by checking the users tables. Is password is matching, is user given username exists, etc. conditions are checked.
	
   .. code-block:: python
	  @app.route("/music/<string:id>")
	  def music(id):
		music = find_musics_id(id)
		if music != None:
			return render_template("music.html",music=music)
		else:
			return render_template("music.html")
	
   Music's information are listing by finding its information on table and send fetched music to necessary page. Article's information are seen by same function.
	
	
.. toctree::

   member1

