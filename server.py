from flask import Flask,render_template,url_for,request,redirect,flash,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from crud_restaurant import readAllRestaurant
from crud_menu import showAllMenu
from utility import getReviewsfromZomato
import json

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

engine = create_engine('sqlite:///app.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

engine = create_engine('sqlite:///app.db')
Base.metadata.engine = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/reviews/<int:rest_id>')
@app.route('/map/<int:rest_id>')
def getReviewsPy(rest_id):
    print(request.url)
    flag = request.args.get('flag')
    dummy = request.args.get('dummy')
    print(flag,dummy)
    restaurant = session.query(Restaurant).filter_by(id=rest_id).one()
    revs =  getReviewsfromZomato(restaurant.name+', '+restaurant.city)
    print(revs, jsonify(revs))
    return jsonify(data=revs)

@app.route('/')
def holdPage():
    restaurants = readAllRestaurant()
    return render_template('restaurantHome.html',restaurants=restaurants)

@app.route('/restaurant/<int:rest_id>')
def singleRestaurant(rest_id):
    restaurant = session.query(Restaurant).filter_by(id=rest_id).one()
    menus = showAllMenu(rest_id)
    return render_template('singleRestaurant.html',restaurant=restaurant,menus=menus)
    
@app.route('/restaurant/<int:rest_id>/newMenu', methods=['GET','POST'])
def createNewMenu(rest_id):
    print(request.method)
    if request.method == 'POST':
        print('I am here')
        newMenu = MenuItem(name=request.form['name'],
                           price=request.form['price'],description=request.form['desc'],course=request.form['course'],restaurant_id=rest_id)
        session.add(newMenu)
        session.commit()
        return redirect(url_for('singleRestaurant',rest_id=rest_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id=rest_id).one()
        return render_template('newMenu.html',restaurant=restaurant)

@app.route('/restaurant/<int:rest_id>/editmenu/<int:menu_id>',methods=['GET','POST'])
def editMenu(rest_id,menu_id):
    if request.method == 'POST':
        menu = session.query(MenuItem).filter_by(id=menu_id).one()
        menu.name = request.form['name']
        menu.price = request.form['price']
        menu.description = request.form['desc']
        menu.course = request.form['course']
        session.add(menu)
        session.commit()
        return redirect(url_for('singleRestaurant',rest_id = rest_id))
  
@app.route('/restaurant/<int:rest_id>/delmenu/<int:menu_id>',methods=['GET','POST'])
def delMenu(rest_id,menu_id):
    if request.method== 'POST':
        menu = session.query(MenuItem).filter_by(id=menu_id).one()
        session.delete(menu)
        session.commit()
        return redirect(url_for('singleRestaurant',rest_id = rest_id))
  


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'secret_key'
    app.run(host='0.0.0.0',port=8080)