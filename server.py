from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras
import sys
reload(sys)
sys.setdefaultencoding("UTF8")

app = Flask(__name__)

def connectToDB():
    connectionString = 'dbname=world user=searcher password=a1b8clo host=localhost'
    try:
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database.")

@app.route('/', methods=['GET', 'POST'])
def mainIndex():
    #Show the main page
    if request.method == 'GET':
        return render_template('index.html', selectedMenu='Home')
    #Show the search page
    elif request.method == 'POST':
        conn=connectToDB()
        cur=conn.cursor()
        
        try:
            query = {'place': request.form['worldSearch']}
            print("Query found")
            cur.execute("SELECT name, code, continent FROM Country WHERE name = %(place)s OR Code = %(place)s OR Continent = %(place)s;", query)
            headers = ['Country', 'Code', 'Continent']
            if cur.rowcount == 0:
                headers = ['City', 'District', 'Country']
                cur.execute("SELECT name, district, countryCode FROM City WHERE name = %(place)s OR district = %(place)s;", query)
        except:
            print("ERROR executing SELECT")
            
        try:
            searchResults = cur.fetchall()
        except:
            return render_template('index.html', selectedMenu='Nothing')
        
        if cur.rowcount == 0:
            return render_template('index.html', selectedMenu='Nothing')
            
        return render_template('index.html', selectedMenu='Find', results=searchResults, headers=headers)

"""
@app.route('/find', methods=['POST'])
def find():
    return render_template('find.html')
"""



if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=8080)