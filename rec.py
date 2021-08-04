import numpy as np
import pandas as pd
import json
from flask import Flask,render_template,request,jsonify
app=Flask(__name__)
df1=pd.read_csv('movies.csv')
df2=pd.read_csv('ratings.csv')
df=pd.merge(df1,df2)
df=df.drop('genres',axis=1)
# ratings_users=df.pivot_table(index=['userId'],columns=['title'],values='rating')
# ratings_users=ratings_users.dropna(thresh=10,axis=1).fillna(0)
# corr_matrix=ratings_users.corr(method='pearson')

with open("./templates/columns.json", "r") as f:
    __data_columns = json.load(f)['data_columns']
       

# def get_similar(movie_name,rating):
#     similar_ratings = corr_matrix[movie_name]*(rating-2.5)
#     similar_ratings = similar_ratings.sort_values(ascending=False)
#     print(type(similar_ratings))
#     return similar_ratings.head(10)

@app.route('/')
def hello():
    return render_template('index.html',__data_columns=__data_columns)
@app.route('/predict',methods=['GET','POST'])
def predict():

    name=request.form["name"]
    n=str(request.form["movie_name"])
    r=int(request.form["ratings"]) 

    a=[n,r]
    def get_similar(movie_name,rating):
        ratings_users=df.pivot_table(index=['userId'],columns=['title'],values='rating')
        ratings_users=ratings_users.dropna(thresh=10,axis=1).fillna(0)
        corr_matrix=ratings_users.corr(method='pearson')
        similar_ratings = corr_matrix[movie_name]*(rating-2.5)
        similar_ratings = similar_ratings.sort_values(ascending=False)
        return similar_ratings.head(10)

    similar_scores = pd.DataFrame()

    similar_scores = similar_scores.append(get_similar(a[0],a[1]),ignore_index = True)    
    print(a)
    return render_template('index.html')
    


    

# def get_similar(movie_name,rating):
#     similar_ratings = corr_matrix[movie_name]*(rating-2.5)
#     similar_ratings = similar_ratings.sort_values(ascending=False)
#     return similar_ratings.head(10)
# n="'burbs, The (1989)"
# r=4
# a=[n,r]

# similar_scores = pd.DataFrame()

# similar_scores = similar_scores.append(get_similar(a[0],a[1]),ignore_index = True)    
# print(similar_scores.columns)




app.run(debug=True, port=80)  