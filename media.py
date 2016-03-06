import webbrowser


class Movie():
    VALID_RATINGS = ["G", "PG", "PG-13", "R"]

    def __init__(self, movie_title, movie_storyline, poster_image,
                 trailer_youtube):
        '''To construct the movie class:

                Arguments:

                self -- represents the instance of the object
                movie_title -- represents the movie's title
                movie_storyline -- represents the movie's storyline
                poster_image -- represents the movie's poster image
                trailer_youtube -- represents the movie's trailer
        '''

        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube

    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)
