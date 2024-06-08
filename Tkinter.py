from tkinter import *
import Project  # Project.py fayli bilan bir xil papkada ekanligiga ishonch hosil qiling

win = Tk()

win.geometry("1000x600")
win.title("영화 추천 시스템")
win.option_add("*Font", "맑은고딕 15")

label1 = Label(win, text="좋아하는 영화, 장르, 국가 및 최소 평점을 입력하세요.", padx=20, pady=10)
label1.pack(padx=20, pady=20)

label_movie = Label(win, text="좋아하는 영화:", padx=20, pady=10)
label_movie.pack(padx=20, pady=10)
entry_movie = Entry(win, width=100)
entry_movie.pack(padx=20, pady=10)

label_genre = Label(win, text="장르:", padx=20, pady=10)
label_genre.pack(padx=20, pady=10)
entry_genre = Entry(win, width=100)
entry_genre.pack(padx=20, pady=10)

label_country = Label(win, text="국가:", padx=20, pady=10)
label_country.pack(padx=20, pady=10)
entry_country = Entry(win, width=100)
entry_country.pack(padx=20, pady=10)

label_rating = Label(win, text="최소 평점:", padx=20, pady=10)
label_rating.pack(padx=20, pady=10)
entry_rating = Entry(win, width=100)
entry_rating.pack(padx=20, pady=10)

text = Text(win, width=100, height=15)
text.pack(padx=20, pady=20)


def get_recommendations():
    favorite_movie = entry_movie.get()
    genre = entry_genre.get()
    country = entry_country.get()
    try:
        rating = float(entry_rating.get())
    except ValueError:
        rating = 0.0

    try:
        result = Project.main(favorite_movie, genre, country, rating)
    except Exception as e:
        result = f"오류 발생: {e}"

    text.delete(1.0, END)
    text.insert(END, result)


btn = Button(win, text="추천", height=2, width=12, command=get_recommendations)
btn.pack()

win.mainloop()


