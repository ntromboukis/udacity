import fresh_tomatoes
import media

# The summaries are taken from IMDB

# Each one of these movie objects include
# the title, a short summary of the movie,
# a poster image from the movie, and a
# link to the movie's trailer.


toy_story = media.Movie(
    "Toy Story",
    "A story about a boy and his toys that come to life",
    "http://ia.media-imdb.com/images/M/MV5BNTE2Njk1NjcxMl5BMl5BanBnXkFtZTYwMDkyOTA5._V1_SX640_SY720_.jpg",  # noqa
    "https://www.youtube.com/watch?v=KYz2wyBy3kc")

avatar = media.Movie(
    "Avatar",
    "A paraplegic marine dispatched to the moon Pandora on a "
    "unique mission becomes torn between following his orders "
    "and protecting the world he feels is his home.",
    "http://ia.media-imdb.com/images/M/MV5BMTYwOTEwNjAzMl5BMl5BanBnXkFtZTcwODc5MTUwMw@@._V1_SY317_CR0,0,214,317_AL_.jpg",  # noqa
    "https://www.youtube.com/watch?v=5PSNL1qE6VY")

mad_max = media.Movie(
    "Mad Max",
    "A woman rebels against a tyrannical ruler in post apocalyptic"
    " Australia in search for her homeland with the help of a group "
    "of female prisoners, a psychotic worshiper, and a drifter named Max.",
    "http://ia.media-imdb.com/images/M/MV5BMTUyMTE0ODcxNF5BMl5BanBnXkFtZTgwODE4NDQzNTE@._V1_SY317_CR2,0,214,317_AL_.jpg",  # noqa
    "https://www.youtube.com/watch?v=hEJnMQG9ev8")

star_wars_tfa = media.Movie(
    "The Force Awakens",
    "Three decades after the defeat of the Galactic Empire, a new "
    "threat arises. The First Order attempts to rule the galaxy and "
    "only a ragtag group of heroes can stop them, along with the help "
    "of the Resistance.",
    "http://ia.media-imdb.com/images/M/MV5BOTAzODEzNDAzMl5BMl5BanBnXkFtZTgwMDU1MTgzNzE@._V1_SY317_CR0,0,214,317_AL_.jpg",  # noqa
    "https://www.youtube.com/watch?v=sGbxmsDFVnE")

inside_out = media.Movie(
    "Inside Out",
    "After young Riley is uprooted from her Midwest life and moved to San "
    "Francisco, her emotions - Joy, Fear, Anger, Disgust and Sadness - "
    "conflict on how best to navigate a new city, house, and school.",
    "http://ia.media-imdb.com/images/M/MV5BOTgxMDQwMDk0OF5BMl5BanBnXkFtZTgwNjU5OTg2NDE@._V1_SX214_AL_.jpg",  # noqa
    "https://www.youtube.com/watch?v=seMwpP0yeu4")

# Jurrasic World:
# best part of the movie is when one of the guests runs from the dinosaur
# with the margharitas in his hand.

jurassic_world = media.Movie(
    "Jurassic World",
    "A new theme park is built on the original site of Jurassic Park."
    " Everything is going well until the park's newest attraction--a "
    "genetically modified giant stealth killing machine--escapes"
    " containment and goes on a killing spree.",
    "http://ia.media-imdb.com/images/M/MV5BMTQ5MTE0MTk3Nl5BMl5BanBnXkFtZTgwMjczMzk2NTE@._V1_SX214_AL_.jpg",  # noqa
    "https://www.youtube.com/watch?v=RFinNxS5KN4")

avengers_age_of_ultron = media.Movie(
    "Avengers: Age of Ultron",
    "When Tony Stark and Bruce Banner try to jump-start a dormant peacekeeping"
    " program called Ultron, things go horribly wrong and it's up to Earth's "
    "Mightiest Heroes to stop the villainous Ultron from enacting his "
    "terrible plans.",
    "http://ia.media-imdb.com/images/M/MV5BMTU4MDU3NDQ5Ml5BMl5BanBnXkFtZTgwOTU5MDUxNTE@._V1_SY317_CR1,0,214,317_AL_.jpg",  # noqa
    "https://www.youtube.com/watch?v=JAUoeqvedMo")

the_martian = media.Movie(
    "The Martian",
    "During a manned mission to Mars, Astronaut Mark Watney is presumed dead "
    "after a fierce storm and left behind by his crew. But Watney has "
    "survived and finds himself stranded and alone on the hostile "
    "planet. With only meager supplies, he must draw upon his ingenuity,"
    " wit and spirit to subsist and find a way to signal to Earth that "
    "he is alive.",
    "http://ia.media-imdb.com/images/M/MV5BMTc2MTQ3MDA1Nl5BMl5BanBnXkFtZTgwODA3OTI4NjE@._V1_SY317_CR0,0,214,317_AL_.jpg",  # noqa
    "https://www.youtube.com/watch?v=ej3ioOneTy8")

ex_machina = media.Movie(
    "Ex Machina",
    "A young programmer is selected to participate in a groundbreaking "
    "experiment in artificial intelligence by evaluating the human "
    "qualities of a breathtaking female A.I.",
    "http://ia.media-imdb.com/images/M/MV5BMTUxNzc0OTIxMV5BMl5BanBnXkFtZTgwNDI3NzU2NDE@._V1_SX214_AL_.jpg",  # noqa
    "https://www.youtube.com/watch?v=XYGzRB4Pnq8")

furious_7 = media.Movie(
    "Furious 7",
    "Deckard Shaw seeks revenge against Dominic Toretto and his family "
    "for his comatose brother.",
    "http://ia.media-imdb.com/images/M/MV5BMTQxOTA2NDUzOV5BMl5BanBnXkFtZTgwNzY2MTMxMzE@._V1_SX214_AL_.jpg",  # noqa
    "https://www.youtube.com/watch?v=Skpu5HaVkOc")

minions = media.Movie(
    "Minions",
    "Minions Stuart, Kevin and Bob are recruited by Scarlet Overkill, a "
    "super-villain who, alongside her inventor husband Herb, hatches a "
    "plot to take over the world.",
    "http://ia.media-imdb.com/images/M/MV5BMTg2MTMyMzU0M15BMl5BanBnXkFtZTgwOTU3ODk4NTE@._V1_SX214_AL_.jpg",  # noqa
    "https://www.youtube.com/watch?v=Wfql_DoHRKc")

insurgent = media.Movie(
    "Insurgent",
    "Beatrice Prior must confront her inner demons and continue her fight "
    "against a powerful alliance which threatens to tear her society apart "
    "with the help from others on her side.",
    "http://ia.media-imdb.com/images/M/MV5BMTgxOTYxMTg3OF5BMl5BanBnXkFtZTgwMDgyMzA2NDE@._V1_SX214_AL_.jpg",  # noqa
    "https://www.youtube.com/watch?v=suZcGoRLXkU")

spy = media.Movie(
    "Spy",
    "A desk-bound CIA analyst volunteers to go undercover to infiltrate the "
    "world of a deadly arms dealer, and prevent diabolical global disaster.",
    "http://ia.media-imdb.com/images/M/MV5BNjI5OTQ0MDQxM15BMl5BanBnXkFtZTgwMzcwNjMyNTE@._V1_SX214_AL_.jpg",  # noqa
    "https://www.youtube.com/watch?v=ltijEmlyqlg")

spectre = media.Movie(
    "Spectre",
    "A cryptic message from Bond's past sends him on a trail to uncover "
    "a sinister organization. While M battles political forces to keep the "
    "secret service alive, Bond peels back the layers of deceit to reveal "
    "the terrible truth behind SPECTRE.",
    "http://ia.media-imdb.com/images/M/MV5BMjM2Nzg4MzkwOF5BMl5BanBnXkFtZTgwNzA0OTE3NjE@._V1_SX214_AL_.jpg",  # noqa
    "https://www.youtube.com/watch?v=z4UDNzXD3qA")

joy = media.Movie(
    "Joy",
    "Joy is the story of the title character, who rose to become founder "
    "and matriarch of a powerful family business dynasty.",
    "http://ia.media-imdb.com/images/M/MV5BMzc2MTI5Mzk0MV5BMl5BanBnXkFtZTgwMDIxMDg1NjE@._V1_SX214_AL_.jpg",  # noqa
    "https://www.youtube.com/watch?v=SN4MLMHET7w")

the_good_dinosaur = media.Movie(
    "The Good Dinosaur",
    "In a world where dinosaurs and humans live side-by-side, an Apatosaurus "
    "named Arlo makes an unlikely human friend.",
    "http://ia.media-imdb.com/images/M/MV5BMTc5MTg2NjQ4MV5BMl5BanBnXkFtZTgwNzcxOTY5NjE@._V1_SX214_AL_.jpg",  # noqa
    "https://www.youtube.com/watch?v=O-RgquKVTPE")

movies = [toy_story, avatar, mad_max, star_wars_tfa, inside_out,
          jurassic_world, avengers_age_of_ultron, the_martian, ex_machina,
          furious_7, minions, insurgent, spy, spectre, joy, the_good_dinosaur]

# this line tells fresh_tomatoes.py to use the movie objects above to
# create HTML for the movies page.
fresh_tomatoes.open_movies_page(movies)
