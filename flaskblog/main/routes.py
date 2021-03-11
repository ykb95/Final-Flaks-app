
from flask import render_template, request, Blueprint
from flaskblog.models import User, Post
from flask_paginate import Pagination, get_page_parameter, get_page_args
import os
os.getcwd()

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1 , type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

# 'AIRLINE', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'TOTAL_DELAY'
@main.route("/data")
def data():

    import pandas as pd
    import csv
    predictions = pd.read_csv("output.csv")

    # with open('output.csv') as csv_file:
        # predictions = csv.reader(csv_file, delimiter=',')

    search = False
    q = request.args.get('q')
    if q:
        search = True

    prediction_list = [row for row in predictions['TOTAL_DELAY']]        
    airline_list = [row for row in predictions['AIRLINE']]
    origin_airport_list = [row for row in predictions['ORIGIN_AIRPORT']]
    destination_airport_list = [row for row in predictions['DESTINATION_AIRPORT']]

    def get_prediction_list(offset=0, per_page=10, prediction_list=prediction_list):
        return prediction_list[offset: offset + per_page]

    def get_airline_list(offset=0, per_page=10, airline_list=airline_list):
        return airline_list[offset: offset + per_page]

    def get_origin_airport_list(offset=0, per_page=10, origin_airport_list=origin_airport_list):
        return origin_airport_list[offset: offset + per_page]

    def get_destination_airport_list(offset=0, per_page=10, destination_airport_list=destination_airport_list):
        return destination_airport_list[offset: offset + per_page]

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    prediction_list_pagination = get_prediction_list(offset=offset, per_page=per_page, prediction_list=prediction_list)
    airline_list_pagination = get_airline_list(offset=offset, per_page=per_page, airline_list=airline_list)
    origin_airport_list_pagination = get_origin_airport_list(offset=offset, per_page=per_page, origin_airport_list=origin_airport_list)
    destination_airport_list_pagination = get_destination_airport_list(offset=offset, per_page=per_page, destination_airport_list=destination_airport_list)    

    pagination = Pagination(page=page, per_page=per_page, total=len(prediction_list), search=search, record_name='Customer Id', css_framework='bootstrap4')
        
    return render_template("data.html" , len = 10, prediction_list_pagination = prediction_list_pagination, airline_list_pagination = airline_list_pagination, origin_airport_list_pagination=origin_airport_list_pagination , destination_airport_list_pagination=destination_airport_list_pagination , pagination = pagination)

    '''
    import pandas as pd

    #create dataframe
    df_marks = pd.DataFrame({'name': ['Somu', 'Kiku', 'Amol', 'Lini'],
         'physics': [68, 74, 77, 78],
        'chemistry': [84, 56, 73, 69],
        'algebra': [78, 88, 82, 87]})

    #render dataframe as html
    html = df_marks.to_html()

    #write html to file
    text_file = open("data.html", "w")
    text_file.write(html)
    text_file.close()
    '''
    # return render_template('data.html', title='Data')
