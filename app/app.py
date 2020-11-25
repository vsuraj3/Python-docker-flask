from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'employeeData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'BME'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM employeeInfo')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, employeeDetail=result)

@app.route('/view/<int:emp_id>', methods=['GET'])
def record_view(emp_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM employeeInfo WHERE id=%s', emp_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', employeeDetail=result[0])

@app.route('/edit/<int:emp_id>', methods=['GET'])
def form_edit_get(emp_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM employeeInfo WHERE id=%s', emp_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', employeeDetail=result[0])

@app.route('/edit/<int:emp_id>', methods=['POST'])
def form_update_post(emp_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Name'), request.form.get('Age'), request.form.get('Sex'),
                 request.form.get('Weight_lbs'), request.form.get('Height_in'),
                  emp_id)
    sql_update_query = """UPDATE employeeInfo e SET e.Name = %s, e.Age = %s, e.Sex = %s, e.Weight_lbs = 
    %s, e.Height_in = %s WHERE e.id = %s"""
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/employeeDetail/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New City Form')


@app.route('/employeeDetail/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Name'), request.form.get('Age'), request.form.get('Sex'),
                 request.form.get('Weight_lbs'), request.form.get('Height_in'))
    sql_insert_query = """INSERT INTO employeeInfo (Name, Age, Sex, Weight_lbs,Height_in) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:emp_id>', methods=['POST'])
def form_delete_post(emp_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM employeeInfo WHERE id = %s """
    cursor.execute(sql_delete_query, emp_id)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/api/v1/employeeDetail', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM employeeInfo')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/employeeDetail/<int:emp_id>', methods=['GET'])
def api_retrieve(emp_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM employeeInfo WHERE id=%s', emp_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/employeeDetail/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/employeeDetail/<int:emp_id>', methods=['PUT'])
def api_edit(emp_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/employeeDetail/<int:emp_id>', methods=['DELETE'])
def api_delete(emp_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
