Parts Implemented by Batuhan Özdöl
================================

Technical Structure of Code
---------------------------

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