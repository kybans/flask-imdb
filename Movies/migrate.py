from appholder import *
# from Movies.views import movies_blueprint


from sqlalchemy import Column, DateTime, Integer, String, text,Float






class Movie(db.Model):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True, name='id')
    movie_name = Column(String(12), name='movie_name')
    director_name = Column(String(12), name='director_name')
    imdb_score = Column(Float, name='imdb_score')
    popularity = Column(Float,name='99popularity')
    update_dttm = Column(DateTime(True), server_default=text("now()"), name='update_dttm')
    create_dttm = Column(DateTime(True), server_default=text("now()"), name='create_dttm')
    status = Column(String(1), name='status', default='A')
    

class Genre(db.Model):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True, name='id')
    genre_name = Column(String(10), name='genre_name')
    update_dttm = Column(DateTime(True), server_default=text("now()"), name='update_dttm')
    create_dttm = Column(DateTime(True), server_default=text("now()"), name='create_dttm')
    status = Column(String(1), name='status', default='A')


class MovieGenre(db.Model):
    __tablename__ = 'movie_genre'

    id = Column(Integer, primary_key=True, name='id')
    movie_id = Column(Integer,db.ForeignKey('movie.id'))
    genre_id = Column(Integer,db.ForeignKey('genre.id'))
    update_dttm = Column(DateTime(True), server_default=text("now()"), name='update_dttm')
    create_dttm = Column(DateTime(True), server_default=text("now()"), name='create_dttm')
    status = Column(String(1), name='status', default='A')




if __name__ == '__main__':
   manager.run()