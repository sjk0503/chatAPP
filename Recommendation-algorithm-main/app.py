from flask import Flask, request, render_template
import Project  # Project.py fayli bilan bir xil papkada ekanligiga ishonch hosil qiling

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    favorite_movie = request.form['favorite_movie']
    genre = request.form['genre']
    country = request.form['country']
    try:
        rating = float(request.form['rating'])
    except ValueError:
        rating = 0.0

    try:
        result = Project.main(favorite_movie, genre, country, rating)
    except Exception as e:
        result = f"오류 발생: {e}"

    return result

if __name__ == '__main__':
    app.run(debug=True)

