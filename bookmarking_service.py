import json
import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True


##### Users #####
# Getting all users
@app.route('/bookmarking/users', methods=['GET']) 
def api_allUsers():
	conn = sqlite3.connect('bookmarks.db') 
	cur = conn.cursor() 
	
	sql = 'SELECT * FROM users ORDER BY user_id ASC;'
	cur.execute(sql)
	row_headers=[x[0] for x in cur.description]
	conn.commit()
	data = cur.fetchall()

	json_data = []

	count = 0
	for result in data:
		json_data.append(dict(zip(row_headers,result)))
		count = count + 1

	listuser = {"count": str(count), "users": json_data}
	return jsonify(listuser), 200


# Adding one or more new user(s)
@app.route('/bookmarking', methods=['POST']) 
def api_addUsers():
	userAdded = []
	data = request.json

	try:
		for user in data["users"]:
			userID = user["user_id"]
			userName = user["user_name"]
				
			conn = sqlite3.connect('bookmarks.db') 
			cur = conn.cursor()
			userSelect = cur.execute("""SELECT * FROM users WHERE user_id = '""" + userID + """';""").fetchall()
			if userSelect == []:
				userAdded.append(user)
				
				sql = cur.execute(""" INSERT INTO users (user_id, user_name) VALUES ('""" + userID + """', '""" + userName + """');""").fetchall()
				conn.commit()
			else:
				msg = {"reasons": [{"message": "User already exists",}]}		
				return jsonify(msg), 400
		
		count = 0
		for e in userAdded:
			count = count + 1
		newUser = {"count": str(count), "users": userAdded}

		return newUser, 201
	except:
		return "Internal Server Error", 500


# Deleting a user
@app.route('/bookmarking/<usrid>', methods=['DELETE']) 
def api_delUsers(usrid):
	conn = sqlite3.connect('bookmarks.db') 
	cur = conn.cursor() 
	usersSel = cur.execute("""SELECT * FROM users WHERE user_id = '""" + usrid + """';""").fetchall()
	
	if usersSel == []:
		msg = {"reasons": [{"message": "User not found"}]}
		return jsonify(msg), 404
	else:
		#return jsonify(usersSel)
		sql = cur.execute("""DELETE FROM users WHERE user_id = '""" + usrid + """';""").fetchall()			# del Table{users}
		sql = cur.execute("""DELETE FROM bookmarks WHERE user_id = '""" + usrid + """';""").fetchall()		# del Table{bookmarks}
		conn.commit()
		return "", 204


##### Bookmarks #####
# Getting all bookmarks
@app.route('/bookmarking/bookmarks', methods=['GET'])
def api_allBookmarks():
	conn = sqlite3.connect('bookmarks.db') 
	cur = conn.cursor()
	
	sql = 'SELECT * FROM bookmarks ORDER BY url, user_id ASC;'
	cur.execute(sql)
	row_headers=[x[0] for x in cur.description]
	conn.commit()
	data = cur.fetchall()

	json_data = []

	count = 0
	for result in data:
		json_data.append(dict(zip(row_headers,result)))
		count = count + 1

	all_bookmarks = {"count": str(count), "bookmarks": json_data}
	
	if 'tags' in request.args:
		tags = request.args['tags']
		
		sql = """SELECT * FROM bookmarks WHERE tags LIKE '%""" + tags + """%' ORDER BY url, user_id ASC;"""
		cur.execute(sql)
		row_headers=[x[0] for x in cur.description]
		conn.commit()
		data = cur.fetchall()

		json_data = []

		count = 0
		for result in data:
			json_data.append(dict(zip(row_headers,result)))
			count = count + 1

		all_bookmarks_tags = {"count": str(count), "bookmarks": json_data}
		return jsonify(all_bookmarks_tags), 200
	
	elif 'count' in request.args:
		count = request.args['count']
		
		sql = """SELECT * FROM bookmarks ORDER BY url, user_id ASC LIMIT """ + count + """;"""
		cur.execute(sql)
		row_headers=[x[0] for x in cur.description]
		conn.commit()
		data = cur.fetchall()

		json_data = []

		count = 0
		for result in data:
			json_data.append(dict(zip(row_headers,result)))
			count = count + 1
		
		all_bookmarks_count = {"count": str(count), "bookmarks": json_data}
		return jsonify(all_bookmarks_count), 200
	
	elif 'offset' in request.args:
		offset = request.args['offset']
		
		sql = """SELECT * FROM bookmarks ORDER BY url, user_id ASC LIMIT 1 OFFSET  """ + offset + """;"""
		cur.execute(sql)
		row_headers=[x[0] for x in cur.description]
		conn.commit()
		data = cur.fetchall()

		json_data = []

		count = 0
		for result in data:
			json_data.append(dict(zip(row_headers,result)))
			count = count + 1
		
		all_bookmarks_offset = {"count": str(count), "bookmarks": json_data}
		return jsonify(all_bookmarks_offset), 200
	
	else:
		return jsonify(all_bookmarks), 200


# Getting all bookmarks for a certain user
@app.route('/bookmarking/bookmarks/<usrid>', methods=['GET'])
def api_allBookmarksUsr(usrid):
	conn = sqlite3.connect('bookmarks.db') 
	cur = conn.cursor() 

	sql = """SELECT * FROM bookmarks WHERE user_id = '""" + usrid + """' ORDER BY url ASC;"""
	cur.execute(sql)
	row_headers=[x[0] for x in cur.description]
	conn.commit()
	data = cur.fetchall()

	json_data = []

	count = 0
	for result in data:
		json_data.append(dict(zip(row_headers,result)))
		count = count + 1
			
	allBkmark_usrid = {"count": str(count), "bookmarks": json_data}

	if 'tags' in request.args:
		tags = request.args['tags']
		
		sql = """SELECT * FROM bookmarks WHERE tags LIKE '%""" + tags + """%' ORDER BY url, user_id ASC;"""
		cur.execute(sql)
		row_headers=[x[0] for x in cur.description]
		conn.commit()
		data = cur.fetchall()

		json_data = []

		count = 0
		for result in data:
			json_data.append(dict(zip(row_headers,result)))
			count = count + 1
		
		allBkmark_usrid_tags = {"count": str(count), "bookmarks": json_data}
		return jsonify(allBkmark_usrid_tags), 200

	elif 'count' in request.args:
		count = request.args['count']
		
		sql = """SELECT * FROM bookmarks ORDER BY url, user_id ASC LIMIT """ + count + """;"""
		cur.execute(sql)
		row_headers=[x[0] for x in cur.description]
		conn.commit()
		data = cur.fetchall()

		json_data = []

		count = 0
		for result in data:
			json_data.append(dict(zip(row_headers,result)))
			count = count + 1
		
		allBkmark_usrid_count = {"count": str(count), "bookmarks": json_data}
		return jsonify(allBkmark_usrid_count), 200

	elif 'offset' in request.args:
		offset = request.args['offset']

		sql = """SELECT * FROM bookmarks ORDER BY url, user_id ASC LIMIT 1 OFFSET  """ + offset + """;"""
		cur.execute(sql)
		row_headers=[x[0] for x in cur.description]
		conn.commit()
		data = cur.fetchall()

		json_data = []

		count = 0
		for result in data:
			json_data.append(dict(zip(row_headers,result)))
			count = count + 1
		
		allBkmark_usrid_offset = {"count": str(count), "bookmarks": json_data}
		return jsonify(allBkmark_usrid_offset), 200
	
	else:
		if count == 0:
			msg = {"reasons": [{"message": "User not found"}]}
			return jsonify(msg), 404
		else:
			return jsonify(allBkmark_usrid)


# Getting a target bookmark for a certain user
@app.route('/bookmarking/bookmarks/<usrid>/<path:requesturl>', methods=['GET'])
def api_bookmarksUsr(usrid, requesturl):
	conn = sqlite3.connect('bookmarks.db') 
	cur = conn.cursor() 
	
	sql = """SELECT * FROM bookmarks WHERE user_id = '""" + usrid + """' AND url = '""" + requesturl + """';"""
	cur.execute(sql)
	row_headers=[x[0] for x in cur.description]
	conn.commit()
	data = cur.fetchall()

	json_data = []

	count = 0
	for result in data:
		json_data.append(dict(zip(row_headers,result)))
		count = count + 1
		
	bkmark_usrid = {"count": str(count), "bookmarks": json_data}
	return jsonify(bkmark_usrid)


# Adding one or more bookmark(s) for a user
@app.route('/bookmarking/<usrid>/bookmarks', methods=['POST'])
def api_addBookmarksUsr(usrid):
	bkmarkAdded_Usr = []
	data = request.json

	try:
		for bookmark in data["bookmarks"]:
			if bookmark["user_id"] == usrid:		
				url = bookmark["url"]
				tags = bookmark["tags"]
				text = bookmark["text"]
				userID = usrid

				conn = sqlite3.connect('bookmarks.db')
				cur = conn.cursor()
				
				bkmarkAdded_Usr_checkUsrID = cur.execute("""SELECT * FROM bookmarks WHERE user_id = '""" + userID + """';""").fetchall()
				bkmarkAdded_Usr_checkUrl = cur.execute("""SELECT * FROM bookmarks WHERE url = '""" + url + """' AND user_id = '""" + userID + """';""").fetchall()
				
				if bkmarkAdded_Usr_checkUsrID == []:
					msg = {"reasons": [{"message": "User not found"}]}
					return jsonify(msg), 404
				if bkmarkAdded_Usr_checkUrl != []:
					msg = {"reasons": [{"message": "Bookmark already exists"}]}
					return jsonify(msg), 400
				if bkmarkAdded_Usr_checkUsrID != [] and bkmarkAdded_Usr_checkUrl == []:
					bkmarkAdded_Usr.append(bookmark)
					sql = cur.execute("""INSERT INTO bookmarks (url, tags, text, user_id) VALUES ('""" + url + """', '""" + tags + """', '""" + text + """', '""" + userID + """');""").fetchall()
					conn.commit()

		count = 0
		for e in bkmarkAdded_Usr:
			count = count + 1

		result = {"count": str(count), "bookmarks": bkmarkAdded_Usr}
		return jsonify(result), 201
	except:
		return "Internal Server Error", 500


# Updating the title/tag(s) for one or more bookmark(s) for a target user
@app.route('/bookmarking/<usrid>/bookmarks/<path:requesturl>', methods=['PUT'])
def api_updateBookmarksUsr(usrid, requesturl):
	bkmarkupdate_Tag = []
	data = request.json
	
	try:
		for bookmark in data["bookmarks"]:
			if bookmark["user_id"] == usrid:		
				url = bookmark["url"]
				tags = bookmark["tags"]
				text = bookmark["text"]
				userID = usrid

				conn = sqlite3.connect('bookmarks.db')
				cur = conn.cursor()

				bkmarkupdate_Tag_checkUsrID = cur.execute("""SELECT * FROM bookmarks WHERE user_id = '""" + userID + """';""").fetchall()
				bkmarkupdate_Tag_checkUrl = cur.execute("""SELECT * FROM bookmarks WHERE url = '""" + url + """' AND user_id = '""" + userID + """';""").fetchall()
				
				if bkmarkupdate_Tag_checkUsrID == []:
					msg = {"reasons": [{"message": "User not found"}, {"message": "Bookmark not found" }]}
					return jsonify(msg), 404
				else:
					bkmarkupdate_Tag.append(bookmark)
					sql = cur.execute("""UPDATE bookmarks SET tags = '""" + tags + """' WHERE user_id = '""" + usrid + """';""").fetchall()
					conn.commit()
			else:
				msg = {"reasons": [{"message": "User not found"}, {"message": "Bookmark not found" }]}
				return jsonify(msg), 404

		count = 0
		for e in bkmarkupdate_Tag:
			count = count + 1

		result = {"count": str(count), "bookmarks": bkmarkupdate_Tag}
		return jsonify(result), 201
	except:
		return "Internal Server Error", 500


# Deleting a bookmark for a target user
@app.route('/bookmarking/<usrid>/bookmarks/<path:requesturl>', methods=['DELETE'])
def api_delBookmarksUsr(usrid, requesturl):
	try:
		conn = sqlite3.connect('bookmarks.db') 
		cur = conn.cursor()
		
		usersSel = cur.execute("""SELECT * FROM users WHERE user_id = '""" + usrid + """';""").fetchall()
		bookmarkSel = cur.execute("""SELECT * FROM bookmarks WHERE url = '""" + requesturl + """';""").fetchall()

		if usersSel == [] or bookmarkSel == []:
			msg = {"reasons": [{"message": "User not found"}, {"message": "Bookmark not found" }]}
			return jsonify(msg), 404
		else:
			sql = cur.execute("""DELETE FROM bookmarks WHERE url = '""" + requesturl + """' AND user_id = '""" + usrid + """';""").fetchall()
			conn.commit()
			return "", 204
	except:
		return "Internal Server Error", 500


app.run()