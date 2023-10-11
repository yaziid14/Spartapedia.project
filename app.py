import os
from os.path import join, dirname
from dotenv import load_dotenv
from http import client
from flask import Flask, render_template, request, jsonify
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
import certifi

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI="mongodb+srv://azharyazied2:14juni2002@cluster0.4uh4rdq.mongodb.net/?retryWrites=true&w=majority"
DB_NAME="dbyzd"

cert = certifi.where()
client = MongoClient(MONGODB_URI, tlsCAFile=cert)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    og_imgage = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="twitter:image:alt"]')
    image = og_imgage['content']
    title = og_title['content'].split("⭐")
    # title = title1.split("⭐")
    desc = og_description['content']
    doc = {
        'image': image,
        'title': title[0],
        'description': desc,
        'star': star_receive,
        'comment': comment_receive
    }
    db.movie.insert_one(doc)
    return jsonify({'msg':'POST request!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.movie.find({}, {'_id': False}))
    return jsonify({'movies': movie_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

# python -m venv venv
# .\venv\Scripts\activate
# pip install flask bs4 requests pymongo dnspython