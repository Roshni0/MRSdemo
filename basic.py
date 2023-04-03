from __future__ import (absolute_import, division, print_function, unicode_literals)
from flask import Flask, render_template,request,jsonify

app = Flask(__name__, template_folder='template')
import pandas as pd
import numpy as np
ratings = pd.read_csv(r'./model/ratings.csv', sep=',', encoding='latin-1', usecols=['userId','movieId','rating','timestamp'])
# Reading movies file
movies = pd.read_csv(r'./model/movies.csv', sep=',', encoding='latin-1', usecols=['movieId','title','genres'])
links = pd.read_csv(r'./model/links.csv', sep=',', encoding='latin-1', usecols=['movieId','imdbId','tmdbId'])
u_id = 0
movieInfo =  (pd.merge(movies, links, on='movieId'))
print(movieInfo)

df= pd.merge(ratings, movies, on= 'movieId')
df.head(10)
#most popular normal ratings
all_results = df.groupby('title').agg({'rating':'mean'}).sort_values(by='rating', ascending=False).head(10)
df_info= pd.merge(all_results, movies, on= 'title')
df_all = pd.DataFrame(df_info['movieId'].isin(df_info['movieId']))
print(df_all)
col_list = df_all['movieId'].tolist()
df_info
df_info['CC'] = col_list
df_info = df_info[['title', 'rating', 'movieId', 'genres','CC']]
df_info
df_info['prob'] = np.nan
import random
for index, row in df_info.iterrows():
    df_info.at[index, 'prob'] =  (random.randint(1, 100))
print(df_info)
def output(df):
    title=[]
    year=[]
    genres=[]
    prob=[]
    for index, row in df.iterrows():
           fullname = row['title']
           charloc = (fullname.rfind("("))
           name_title = fullname[:charloc]
           year_m = fullname[charloc+1:charloc+5]
           com = name_title.rfind(",")
           if com != -1:
               ac_name = name_title[com+1:] + name_title[:com]
           else:
               ac_name = name_title
           title.append(ac_name)
           
           pre_genre = row['genres']
           genres.append(pre_genre)
           year.append(year_m)
           pre_prop = row['prob']
           prob.append(pre_prop)
           #import imdb
           #access = imdb.IMDb()
          # id_imdb = (row['imdbId'])
           #movie = access.get_movie(id_imdb)=
    

    return title,year,genres,prob
for col in df_info.columns:
    print(col)
df_name,df_year,df_genres,df_prob = output(df_info)
#df_infonames,df_infoemoji, df_infogenres, df_infoyear_made, df_infooverview, df_infoimages,df_infocc, df_infoprob = output(df_info)

@app.route('/')
def home():
    if request.method == 'GET':
        return(render_template('main.html',df_name=df_name,df_year=df_year, df_genres=df_genres,df_prob=df_prob))
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)