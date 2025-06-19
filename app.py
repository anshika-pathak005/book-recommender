from flask import Flask,render_template, request
# unpacking the pickle file
from fuzzywuzzy import process
import pickle
import numpy as np
import gzip

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))

# books = pickle.load(open('books.pkl','rb'))
with gzip.open("boooks.pkl.gz", "rb") as f:
    books = pickle.load(f)

similarity_score = pickle.load(open('similarity_score.pkl','rb'))


app = Flask(__name__)

# this route for home page
@app.route('/')
def index():
    return render_template('index.html',
                           book_name = popular_df['Book-Title'].to_list(),
                           author= popular_df['Book-Author'].to_list(),
                           image= popular_df['Image-URL-M'].to_list(),
                           votes= popular_df['num_ratings'].to_list(),
                           rating= [round(r, 2) for r in popular_df['avg_Ratings'].to_list()]

                           )

# this route for recommend page
@app.route('/recommend')
def recommend_UI_load():
    return render_template('recommend.html')

# @app.route('/recommend_books',methods=['post'])
# def recommend():
#     user_input = request.form.get('user_input')
#
#     index = np.where(pt.index == user_input)[0][0]
#     similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]
#
#     data = []
#     for i in similar_items:
#         item = []
#         temp_df = books[books['Book-Title'] == pt.index[i[0]]]
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
#         data.append(item)
#
#     print(data)
#
#     return render_template('recommend.html',data=data)

# Recommendation logic route
@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input_raw = request.form.get('user_input')
    all_titles = pt.index.tolist()
    match, score = process.extractOne(user_input_raw, all_titles)

    if score <= 60:
        return render_template('recommend.html',
                               data=[],
                               message="No close match found. Try again.")

    user_input = match  # Use the matched title

    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return render_template('recommend.html', data=data, match=user_input)

if __name__ == '__main__':
    app.run(debug=True)