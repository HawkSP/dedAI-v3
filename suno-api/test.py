import requests
import threading
from openai import OpenAI
from dotenv import load_dotenv
from predict import flatten_genre_data, process_bpm_emotions, predict_bpm
import json
import sys
import os
import time

# Load environment variables
load_dotenv('.env')

# Fetch the API key from environment variables

gpt_key = str(os.getenv("CHATGPT_API_KEY"))

client = OpenAI(api_key=gpt_key)


base_url = 'http://localhost:3000'

genre_data = {
    'Pop': [
        {'bpm': 96, 'Attention': 42, 'Engagement': 73, 'Excitement': 34, 'Interest': 46, 'Relaxation': 22,
         'Stress': 35},  # "Shape of You" by Ed Sheeran
        {'bpm': 113, 'Attention': 40, 'Engagement': 68, 'Excitement': 50, 'Interest': 50, 'Relaxation': 25,
         'Stress': 10},  # "Can't Stop the Feeling!" by Justin Timberlake
        {'bpm': 115, 'Attention': 90, 'Engagement': 70, 'Excitement': 45, 'Interest': 55, 'Relaxation': 20,
         'Stress': 20},  # "Uptown Funk" by Mark Ronson ft. Bruno Mars
        {'bpm': 120, 'Attention': 12, 'Engagement': 65, 'Excitement': 70, 'Interest': 43, 'Relaxation': 30,
         'Stress': 67},  # "Call Me Maybe" by Carly Rae Jepsen
        {'bpm': 160, 'Attention': 45, 'Engagement': 75, 'Excitement': 30, 'Interest': 50, 'Relaxation': 28,
         'Stress': 57},  # "Happy" by Pharrell Williams
        {'bpm': 105, 'Attention': 50, 'Engagement': 40, 'Excitement': 35, 'Interest': 47, 'Relaxation': 67,
         'Stress': 22},  # "Rolling in the Deep" by Adele
        {'bpm': 124, 'Attention': 38, 'Engagement': 46, 'Excitement': 42, 'Interest': 51, 'Relaxation': 24,
         'Stress': 39},  # "Firework" by Katy Perry
        {'bpm': 90, 'Attention': 46, 'Engagement': 80, 'Excitement': 37, 'Interest': 49, 'Relaxation': 26,
         'Stress': 19},  # "Roar" by Katy Perry
        {'bpm': 134, 'Attention': 43, 'Engagement': 72, 'Excitement': 60, 'Interest': 52, 'Relaxation': 29,
         'Stress': 34},  # "All About That Bass" by Meghan Trainor
        {'bpm': 135, 'Attention': 41, 'Engagement': 57, 'Excitement': 36, 'Interest': 86, 'Relaxation': 50,
         'Stress': 13},  # "Bad Guy" by Billie Eilish
        {'bpm': 119, 'Attention': 39, 'Engagement': 69, 'Excitement': 76, 'Interest': 45, 'Relaxation': 27,
         'Stress': 16}  # "Just Dance" by Lady Gaga
    ],

    'Rock': [
        {'bpm': 144, 'Attention': 56, 'Engagement': 55, 'Excitement': 35, 'Interest': 47, 'Relaxation': 30,
         'Stress': 38},  # "Bohemian Rhapsody" by Queen
        {'bpm': 116, 'Attention': 50, 'Engagement': 65, 'Excitement': 55, 'Interest': 60, 'Relaxation': 20,
         'Stress': 42},  # "Highway to Hell" by AC/DC
        {'bpm': 123, 'Attention': 58, 'Engagement': 50, 'Excitement': 45, 'Interest': 44, 'Relaxation': 35,
         'Stress': 40},  # "Enter Sandman" by Metallica
        {'bpm': 113, 'Attention': 53, 'Engagement': 70, 'Excitement': 50, 'Interest': 55, 'Relaxation': 25,
         'Stress': 37},  # "Under Pressure" by Queen & David Bowie
        {'bpm': 134, 'Attention': 70, 'Engagement': 89, 'Excitement': 98, 'Interest': 53, 'Relaxation': 28,
         'Stress': 10},  # "Thunderstruck" by AC/DC
        {'bpm': 167, 'Attention': 30, 'Engagement': 17, 'Excitement': 30, 'Interest': 57, 'Relaxation': 22,
         'Stress': 45},  # "Zombie" by The Cranberries
        {'bpm': 174, 'Attention': 60, 'Engagement': 56, 'Excitement': 40, 'Interest': 48, 'Relaxation': 32,
         'Stress': 39},  # "Run to the Hills" by Iron Maiden
        {'bpm': 92, 'Attention': 55, 'Engagement': 63, 'Excitement': 38, 'Interest': 82, 'Relaxation': 30,
         'Stress': 41},  # "Creep" by Radiohead
        {'bpm': 118, 'Attention': 54, 'Engagement': 60, 'Excitement': 70, 'Interest': 58, 'Relaxation': 24,
         'Stress': 12},  # "Don't Stop Believin'" by Journey
        {'bpm': 123, 'Attention': 57, 'Engagement': 67, 'Excitement': 43, 'Interest': 50, 'Relaxation': 29,
         'Stress': 34}  # "You Give Love a Bad Name" by Bon Jovi
    ],

    'Hip Hop': [
        {'bpm': 85, 'Attention': 40, 'Engagement': 62, 'Excitement': 10, 'Interest': 50, 'Relaxation': 20,
         'Stress': 38},  # "N.Y. State of Mind" by Nas
        {'bpm': 110, 'Attention': 60, 'Engagement': 68, 'Excitement': 35, 'Interest': 55, 'Relaxation': 18,
         'Stress': 42},  # "Alright" by Kendrick Lamar
        {'bpm': 96, 'Attention': 94, 'Engagement': 60, 'Excitement': 25, 'Interest': 48, 'Relaxation': 22,
         'Stress': 9},
        # "Juicy" by The Notorious B.I.G.
        {'bpm': 95, 'Attention': 43, 'Engagement': 70, 'Excitement': 30, 'Interest': 53, 'Relaxation': 24,
         'Stress': 40},  # "Gin and Juice" by Snoop Dogg
        {'bpm': 80, 'Attention': 47, 'Engagement': 64, 'Excitement': 40, 'Interest': 58, 'Relaxation': 19,
         'Stress': 35},  # "Can't Tell Me Nothing" by Kanye West
        {'bpm': 90, 'Attention': 50, 'Engagement': 61, 'Excitement': 20, 'Interest': 46, 'Relaxation': 25,
         'Stress': 39},  # "In Da Club" by 50 Cent
        {'bpm': 80, 'Attention': 38, 'Engagement': 65, 'Excitement': 15, 'Interest': 51, 'Relaxation': 50,
         'Stress': 37},  # "Stan" by Eminem
        {'bpm': 150, 'Attention': 41, 'Engagement': 59, 'Excitement': 32, 'Interest': 49, 'Relaxation': 23,
         'Stress': 34},  # "HUMBLE." by Kendrick Lamar
        {'bpm': 82, 'Attention': 53, 'Engagement': 63, 'Excitement': 22, 'Interest': 47, 'Relaxation': 27,
         'Stress': 12},  # "It Was A Good Day" by Ice Cube
        {'bpm': 154, 'Attention': 39, 'Engagement': 66, 'Excitement': 18, 'Interest': 52, 'Relaxation': 20,
         'Stress': 16}
        # "God's Plan" by Drake
    ],
    'Classical': [
        {'bpm': 60, 'Attention': 56, 'Engagement': 58, 'Excitement': 17, 'Interest': 49, 'Relaxation': 80,
         'Stress': 5},  # Moonlight Sonata by Beethoven
        {'bpm': 48, 'Attention': 60, 'Engagement': 60, 'Excitement': 15, 'Interest': 55, 'Relaxation': 90,
         'Stress': 10},  # Canon in D by Pachelbel
        {'bpm': 132, 'Attention': 58, 'Engagement': 57, 'Excitement': 60, 'Interest': 65, 'Relaxation': 30,
         'Stress': 20},  # Four Seasons: Spring by Vivaldi
        {'bpm': 110, 'Attention': 57, 'Engagement': 59, 'Excitement': 50, 'Interest': 46, 'Relaxation': 40,
         'Stress': 25},  # Symphony No. 40 by Mozart
        {'bpm': 50, 'Attention': 55, 'Engagement': 60, 'Excitement': 20, 'Interest': 60, 'Relaxation': 85,
         'Stress': 15},  # Air on the G String by Bach
        {'bpm': 60, 'Attention': 53, 'Engagement': 50, 'Excitement': 25, 'Interest': 55, 'Relaxation': 75,
         'Stress': 30},  # Clair de Lune by Debussy
        {'bpm': 106, 'Attention': 54, 'Engagement': 65, 'Excitement': 55, 'Interest': 60, 'Relaxation': 35,
         'Stress': 40},  # Hungarian Dance No. 5 by Brahms
        {'bpm': 120, 'Attention': 52, 'Engagement': 70, 'Excitement': 65, 'Interest': 70, 'Relaxation': 25,
         'Stress': 45},  # Ride of the Valkyries by Wagner
        {'bpm': 72, 'Attention': 50, 'Engagement': 55, 'Excitement': 30, 'Interest': 45, 'Relaxation': 70,
         'Stress': 20},  # Boléro by Ravel
        {'bpm': 68, 'Attention': 58, 'Engagement': 60, 'Excitement': 18, 'Interest': 52, 'Relaxation': 85,
         'Stress': 10}   # Gymnopédie No. 1 by Satie
    ],
    'Jazz': [
        {'bpm': 174, 'Attention': 40, 'Engagement': 62, 'Excitement': 33, 'Interest': 50, 'Relaxation': 33,
         'Stress': 41},  # Take Five by Dave Brubeck
        {'bpm': 120, 'Attention': 55, 'Engagement': 60, 'Excitement': 25, 'Interest': 48, 'Relaxation': 40,
         'Stress': 30},  # So What by Miles Davis
        {'bpm': 130, 'Attention': 50, 'Engagement': 65, 'Excitement': 35, 'Interest': 55, 'Relaxation': 45,
         'Stress': 25},  # Blue Rondo à la Turk by Dave Brubeck
        {'bpm': 136, 'Attention': 45, 'Engagement': 64, 'Excitement': 50, 'Interest': 52, 'Relaxation': 38,
         'Stress': 20},  # Giant Steps by John Coltrane
        {'bpm': 110, 'Attention': 68, 'Engagement': 66, 'Excitement': 20, 'Interest': 47, 'Relaxation': 50,
         'Stress': 35},  # My Favorite Things by John Coltrane
        {'bpm': 160, 'Attention': 38, 'Engagement': 70, 'Excitement': 40, 'Interest': 49, 'Relaxation': 50,
         'Stress': 18},  # A Love Supreme, Part 1: Acknowledgement by John Coltrane
        {'bpm': 105, 'Attention': 47, 'Engagement': 63, 'Excitement': 28, 'Interest': 51, 'Relaxation': 42,
         'Stress': 33},  # Moanin' by Art Blakey and the Jazz Messengers
        {'bpm': 126, 'Attention': 52, 'Engagement': 59, 'Excitement': 37, 'Interest': 53, 'Relaxation': 39,
         'Stress': 22},  # Birdland by Weather Report
        {'bpm': 115, 'Attention': 54, 'Engagement': 60, 'Excitement': 30, 'Interest': 55, 'Relaxation': 44,
         'Stress': 27},  # Watermelon Man by Herbie Hancock
        {'bpm': 135, 'Attention': 51, 'Engagement': 65, 'Excitement': 32, 'Interest': 54, 'Relaxation': 41,
         'Stress': 24}  # Freddie Freeloader by Miles Davis
    ],
    'Electronic': [
        {'bpm': 105, 'Attention': 63, 'Engagement': 60, 'Excitement': 29, 'Interest': 48, 'Relaxation': 25,
         'Stress': 40}, # Midnight City by M83
        {'bpm': 174, 'Attention': 65, 'Engagement': 75, 'Excitement': 85, 'Interest': 80, 'Relaxation': 25,
         'Stress': 30},  # Tarantula by Pendulum
        {'bpm': 140, 'Attention': 60, 'Engagement': 70, 'Excitement': 90, 'Interest': 75, 'Relaxation': 20,
         'Stress': 50},  # Scary Monsters and Nice Sprites by Skrillex
        {'bpm': 160, 'Attention': 50, 'Engagement': 65, 'Excitement': 85, 'Interest': 70, 'Relaxation': 15,
         'Stress': 40},  # money machine by 100 gecs
        {'bpm': 120, 'Attention': 58, 'Engagement': 55, 'Excitement': 45, 'Interest': 60, 'Relaxation': 70,
         'Stress': 15},  # Midnight by Lane 8
        {'bpm': 110, 'Attention': 62, 'Engagement': 60, 'Excitement': 40, 'Interest': 65, 'Relaxation': 75,
         'Stress': 10},  # Sunset Lover by Petit Biscuit
        {'bpm': 130, 'Attention': 57, 'Engagement': 80, 'Excitement': 85, 'Interest': 68, 'Relaxation': 35,
         'Stress': 25},  # Your Mind by Adam Beyer & Bart Skils
        {'bpm': 90, 'Attention': 52, 'Engagement': 50, 'Excitement': 30, 'Interest': 55, 'Relaxation': 80,
         'Stress': 18},  # Teardrop by Massive Attack
        {'bpm': 130, 'Attention': 60, 'Engagement': 78, 'Excitement': 70, 'Interest': 73, 'Relaxation': 40,
         'Stress': 22},  # Saltwater by Chicane
        {'bpm': 128, 'Attention': 64, 'Engagement': 85, 'Excitement': 80, 'Interest': 77, 'Relaxation': 30,
         'Stress': 35}  # Animals by Martin Garrix
    ],
}

def custom_generate_audio(payload):
    url = f"{base_url}/api/custom_generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()

def generate_audio_by_prompt(payload):
    url = f"{base_url}/api/generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()

def get_audio_information(audio_ids):
    url = f"{base_url}/api/get?ids={audio_ids}"
    response = requests.get(url)
    return response.json()

def get_image_information(image_ids):
    url = f"{base_url}/api/get?ids={image_ids}"
    response = requests.get(url)
    return response.json()


def generate_lyrics_by_prompt(payload):
    url = f"{base_url}/api/generate_lyrics"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()

def get_quota_information():
    url = f"{base_url}/api/get_limit"
    response = requests.get(url)
    return response.json()

def download_file_from_stream(url, destination, rename_to):
    temp_path = destination + '.temp'
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(temp_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    # Rename the file with a custom title
    final_path = os.path.join(os.path.dirname(destination), rename_to)
    os.rename(temp_path, final_path)
    print(f"Download completed and moved to: {final_path}")


def download_image(image_url, save_dir='images', title='image', image_counter=1):
    filename = f"{title}{image_counter}.png"
    full_path = os.path.join(save_dir, filename)
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(full_path, 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded and saved as: {filename}")
        return full_path  # This line can now be ignored in the context of the app
    else:
        print(f"Failed to download the image: {response.status_code}")
        return None

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def delete_file(file_path):
    os.remove(file_path)
    print(f"Deleted {file_path}")

def main():
    # Path to the JSON files
    emotion_file_path = 'data/emotion_data.json'
    genre_file_path = 'data/genre_data.json'


    emotion_values = read_json_file(emotion_file_path)
    desired_genre = read_json_file(genre_file_path)
    print(f"Emotion Data: {emotion_values}")
    print(f"Genre Data: {desired_genre}")


    # Generate flat data and models
    flat_data = flatten_genre_data(genre_data)
    models = process_bpm_emotions(flat_data)

    # Predict BPM
    predicted_bpm = predict_bpm(models, emotion_values)
    rounded_bpm = round(predicted_bpm) if predicted_bpm else None

    system_message = f"""
    You are an advanced music AI trained to craft precise and compelling music style descriptions. 
    Your task is to synthesize a description for a {rounded_bpm} BPM {desired_genre} song, capturing the essence of their emotions and blending creative flair with detailed accuracy.
    Translate numerical emotional responses into vivid descriptive language.
    Use these metrics to predict how the user is feeling and translate them into a compelling description of the song to either match or contrast the user's mood. 
    We want to reflect the user's mood through the song description but if the user is feeling stressed, a relaxing song could be recommended. 
    Use discression to decide how to match or contrast the user's mood based on the emotional metrics provided. 
    Focus on incorporating elements like instrumentation, mood into a compelling narrative, and a direction for the lyrical content.
    You should mention the BPM, the genre and a related sub genre if necessary, at least two instruments, one style, one mood, a direction for the vocals and the lyrical content, and mention the structure too like chorus, verse, bridge, and intro; using exactly precisely 100 characters long.
    The description must start with 'START' and end with 'END', strictly adhering to a total of 100 characters excluding 'START' and 'END'.
    Your output must strictly follow these guidelines to ensure it meets the specific character limit and content expectations.
    
    Here are some tricks to get better results from the Lyric Generator:

    In the prompt
    
    add a POV – even inanimate objects and abstract ideas can be the focus
    add a conflict – songs can be a moment in time where the outcome is uncertain
    add details – AI is very good at expanding on ideas, not as good at inventing original ideas.
    add a twist – a sudden change in the narrative can make the song more interesting
    add a resolution – a satisfying ending can make the song feel complete
    add a moral – a lesson learned can make the song more meaningful
    add a setting – the time and place can set the mood for the song
    add a character – a protagonist can drive the narrative of the song
    add a theme – a recurring idea can tie the song together
    add a tone – the mood of the song can be set by the language used
    
    Here is a list of prompt styles you can use but do not use the artist's name within the song description these are just ideas for the prompt:
    Drake: HipHop, Trap, male vocals
    Bruno Mars: Funk, Dance Pop, Groovy, male vocals
    Fleetwood Mac: Classic Rock, Mellifluous
    Ed Sheeran: Folk, Acoustic Guitar, male vocals
    Tim McGraw: Country, Americana, male vocals
    Elton John: Piano Pop Rock, Theatrical, male vocals
    Dolly Parton: Country, Storytelling, female vocals
    Red Hot Chili Peppers: Funk Rock, Stadium, heavy drums
    Coldplay: Alternative Rock, Atmospheric
    Taylor Swift: Pop, Alternative Folk, Emotional, female vocals
    Elvis Presley: 50s Rock, Hero Theme, male vocals
    Adele: Soul, Emotional, Torch-Lounge, female vocals
    Ariana Grande: Pop, Dance Pop, Ethereal, female vocals
    Billie Eilish: Pop, Dark, Minimal, female vocals
    The Weeknd: RnB, Dark, Cinematic, male vocals
    Beyoncé: RnB, Anthemic, Danceable, female vocals
    Kendrick Lamar: HipHop, Lyrical, Storytelling, male vocals
    Lady Gaga: Pop, Theatrical, Dance, female vocals
    Jay-Z: HipHop, Aggressive, Storytelling, male vocals
    Rihanna: RnB, Dance Pop, Festive, female vocals
    Kanye West: HipHop, Progressive, Eclectic, male vocals
    Justin Bieber: Pop, Danceable, Chillwave, male vocals
    Katy Perry: Pop, Glitter, Festive, female vocals
    Snoop Dogg: Rap, Funk, Chill, male vocals
    Metallica: Heavy Metal, Power
    AC/DC: Hard Rock, Stomp
    Madonna: Dance Pop, High-NRG, female vocals
    David Bowie: 70s British Rock, Art, Eclectic, male vocals
    Bob Dylan: Folk, Storytelling, Acoustic Guitar, male vocals
    Post Malone: Rap, Ethereal, Ambient, male vocals
    Maroon 5: Pop Rock, Danceable, male vocals
    Shakira: Latin, Dance Pop, Festive, female vocals
    Dua Lipa: Disco, Dance Pop, Groovy, female vocals
    Michael Jackson: 80s Pop, Dance, Iconic, male vocals
    Prince: Funk, Eclectic, Glam, male vocals
    Miley Cyrus: Pop, Rock, Party, female vocals
    Cardi B: Rap, Aggressive, Party, female vocals
    Imagine Dragons: Rock, Anthemic, Emotion
    Camila Cabello: Pop, Latin Jazz, Festive, female vocals
    Harry Styles: Pop, Rock, Groovy, male vocals
    Sam Smith: Soul, Emotional, Lounge, male vocals
    Lizzo: Pop, Funk, Empowering, female vocals
    Daft Punk: Electronic, Dance, Futuristic
    Gorillaz: Alternative Rock, Electronic, Unusual
    The Beatles: 60s British Pop, Classic, Rock
    Queen: Rock, Operatic, Theatrical, Male Vocals
    Led Zeppelin: Hard Rock, Blues Rock, Epic
    Pink Floyd: Rock, Progressive, Atmospheric
    The Rolling Stones: Rock, Blues Rock, Classic
    Bob Marley: Reggae, Peaceful, Soulful, male vocals
    Frank Sinatra: 1940s big band, Lounge Singer, male vocals
    Aretha Franklin: Soul, Gospel, Powerful, female vocals
    Whitney Houston: Pop, RnB, Emotional, female vocals
    Stevie Wonder: Soul, Funk, Joyful, male vocals
    The Chainsmokers: EDM, Dance, Party
    Nicki Minaj: Rap, Danceable, Bold, female vocals
    Green Day: Punk Rock, Aggressive, Youthful
    Nirvana: Grunge, Dark, Raw, Male Vocals
    Amy Winehouse: Soul, Jazz, Torch-Lounge, female vocals
    Linkin Park: Rock, Nu Metal, Emotional
    Aerosmith: Rock, Hard Rock, Classic
    Bon Jovi: Rock, Anthem, Stadium
    Billy Joel: Pop, Rock, Storytelling, male vocals
    Phil Collins: Pop, Rock, Emotional, soundtrack, male vocals
    Genesis: Rock, Progressive, Art
    The Eagles: Rock, Country Rock, Harmonious
    The Doors: Rock, Psychedelic, Mysterious
    Janis Joplin: Rock, Blues Rock, Raw Emotion, female vocals
    Jimi Hendrix: Rock, Psychedelic, Guitar Virtuoso, male vocals
    The Who: Rock, Hard Rock, Theatrical
    Black Sabbath: Heavy Metal, Doom
    Iron Maiden: Heavy Metal, Epic, Theatrical
    Judas Priest: Heavy Metal, Power, Leather
    Motorhead: Heavy Metal, Rock’n’Roll, Aggressive
    Slayer: Thrash Metal, Aggressive, Dark
    Ozzy Osbourne: Heavy Metal, Dark, Theatrical, male vocals
    Skrillex: Dubstep, Electronic, Intense, male vocals
    Calvin Harris: EDM, Dance, Festive, male vocals
    Avicii: EDM, Melodic, Euphoric, male vocals
    Arctic Monkeys: Indie Rock, Garage, Cool
    Tame Impala: Psychedelic Rock, Dreamy, Mellifluous
    The Strokes: Indie Rock, Cool, Raw
    Vampire Weekend: Indie Rock, Eclectic, Upbeat
    Kings of Leon: Rock, Emotional, Raw
    The Killers: Rock, Synthpop, Anthemic, male vocals
    System of a Down: Metal, Political, Eccentric
    Radiohead: Alternative Rock, Experimental, Atmospheric
    Foo Fighters: Rock, Alternative, Energetic
    Muse: Rock, Progressive, Theatrical
    Tool: Progressive Metal, Dark, Complex
    Rage Against the Machine: Rap Metal, Political, Aggressive
    Pearl Jam: Grunge, Rock, Emotional
    Soundgarden: 90s Grunge, Heavy, Dark
    Alice in Chains: Grunge, Dark, Melodic
    Sigur Rós: Post-Rock, Ethereal, Atmospheric, Icelandic
    Björk: Alternative, Experimental, Unusual, female vocals
    Enya: New Age, Ethereal, Calm, female vocals
    Deadmau5: Electronic, House, Progressive
    Marshmello: EDM, Dance, Happy
    Zedd: EDM, Dance Pop, Energetic, male vocals
    The XX: Indie Pop, Minimal, Atmospheric
    Lana Del Rey: Pop, Sadcore, Cinematic, female vocals
    Kacey Musgraves: Country, Pop, Mellifluous, female vocals
    St. Vincent: Art Rock, Eclectic, Unusual, female vocals
    Childish Gambino: HipHop, Funk, Thoughtful, male vocals
    SZA: RnB, Neo Soul, Emotional, female vocals
    Frank Ocean: RnB, Soulful, Introspective, male vocals
    Tyler, The Creator: HipHop, Eclectic, Unusual, male vocals
    Solange: RnB, Soul, Artistic, female vocals
    Brockhampton: HipHop, Alternative, Collective
    Janelle Monáe: Funk, RnB, Sci-Fi, female vocals
    Mac DeMarco: Indie Pop, Slacker Rock, Chill, male vocals
    Rufus Du Sol: Electronic, Dance, Atmospheric
    Bon Iver: Indie Folk, Ethereal, Intimate, male vocals
    Florence + The Machine: Indie Rock, Dramatic, Ethereal
    Jack White: Rock, Blues, Raw, male vocals
    Gary Clark Jr.: Blues Rock, Soulful, Gritty, male vocals
    Leon Bridges: Soul, RnB, Retro, male vocals
    Brittany Howard: Rock, Soul, Powerful, female vocals
    Alabama Shakes: Rock, Blues Rock, Soulful
    Glass Animals: Psychedelic Pop, Groovy, Eclectic
    Portugal, The Man: Alternative Rock, Psychedelic, Catchy
    FKA Twigs: RnB, Electronic, Avant-Garde, female vocals
    The National: Indie Rock, Melancholy, Introspective
    MGMT: Psychedelic Pop, Electronic, Playful
    Empire of the Sun: Electronic, Pop, Theatrical
    Grimes: Art Pop, Electronic, Experimental, female vocals
    James Blake: Electronic, Soul, Minimalist, male vocals
    The War on Drugs: Indie Rock, Heartland Rock, Melodic
    Sufjan Stevens: Indie Folk, Baroque Pop, Intimate, male vocals
    Bonobo: Downtempo, Electronic, Ambient
    Caribou: Electronic, Psychedelic, Dance
    Four Tet: Electronic, Ambient, Textural
    Jamie xx: Electronic, House, Minimal
    Nicolas Jaar: Electronic, Experimental, Atmospheric, male vocals
    Flying Lotus: Electronic, Experimental HipHop, Fusion, male vocals
    Thundercat: Funk, Jazz, Experimental, male vocals
    Kamasi Washington: Jazz, Fusion, Epic, male vocals
    Massive Attack: Trip Hop, Dark, Atmospheric
    Portishead: Trip Hop, Dark, Cinematic
    Aphex Twin: IDM, Electronic, Experimental, male vocals
    Boards of Canada: IDM, Downtempo, Nostalgic
    Burial: Dubstep, Ambient, Mysterious
    J Dilla: HipHop, Soulful, Experimental, male vocals
    MF DOOM: HipHop, Abstract, Lyrical, male vocals
    Kendrick Lamar: HipHop, Conscious, Lyrical, male vocals
    Blink-182: emo pop rock, male vocals
    Green Day: Punk Rock, Aggressive, Youthful
    Phoebe Bridgers: Bedroom, grungegaze, catchy, psychedelic, acoustic tape recording, female vocals
    
    Also, try these fun and unique styles:

    Uplifting atmospheric worship ballad with ethereal vocals and sweeping orchestral arrangements
    Live music, heavy metal with solo guitar, symphonic elements, and aggressive power vocals
    Bedroom-produced grungegaze, catchy, psychedelic, with acoustic tape recording and lo-fi aesthetics
    Rapid-fire rap, 140 bpm, deep bass beats, aggressive delivery in a minor key, creating high tension
    Chillwave electronic, ambient textures, slow-tempo, reverb-heavy vocals, and a dreamy synth backdrop
    Futuristic cyberpunk EDM, high-energy beats, distorted synth lines, and neon-lit, dystopian themes
    Acoustic folk, storytelling lyrics, warm vocal harmonies, fingerstyle guitar, and soft percussion
    Vintage jazz lounge, classic standards, smooth trumpet solos, upright bass, and sultry female vocals
    Baroque pop, intricate melodies, orchestral arrangements, harpsichord flourishes, and poetic lyrics
    Glam rock revival, flamboyant performance, glittery costumes, catchy hooks, and guitar solos
    Sultry RnB, smooth beats, seductive vocals, late-night vibes, and lush production
    Dark ambient, atmospheric soundscapes, slow-moving textures, and an unsettling, eerie mood
    Tropical house, upbeat, sun-kissed melodies, steel drums, breezy vocals, and a laid-back rhythm
    Psychedelic funk, groovy bass lines, wah-wah guitars, trippy effects, and energetic brass sections
    Epic cinematic scores, sweeping orchestral movements, heroic themes, and stirring emotional peaks
    Minimal techno, repetitive beats, subtle progression, hypnotic rhythms, and a deep, underground feel
    Indie surf rock, jangly guitars, beachy vibes, carefree vocals, and upbeat, sunny melodies
    Soulful gospel choir, powerful lead vocals, uplifting messages, organ accompaniment, and handclaps
    Aggressive trap metal, distorted 808s, screamed vocals, chaotic energy, and mosh-pit inducing breakdowns
    Contemporary classical piano, emotive compositions, dynamic range, and nuanced performance
    Gypsy jazz, acoustic guitars, fast-paced swing rhythms, violin solos, and a lively, festive atmosphere
    Dream pop, ethereal vocals, shimmering guitars, lush synths, and a sense of nostalgic longing
    Balkan electro swing, energetic brass ensembles, electronic beats, folk melodies, and infectious dance rhythms
    Hardcore punk, fast tempos, political lyrics, raw vocals, and a DIY ethos
    Space ambient, cosmic soundscapes, slow-evolving textures, and a sense of infinite exploration
    punk rock, ska punk, rock, rap, indie pop
    gregorian chorale, choir, carried singing, epic, majestic, ecclesiastical
    math rock, J-pop, mutation funk, bounce drop, dubstep, edm, 160bpm,
    anime opening, heavy metal, male vocal
    80's,post-punk, punk, Retrowave,slow
    Pentatonic Scale, Modern Classic, Game Music, Guzheng & Piano & Chinese Drum & Cello, Slow, Sad, Mellow
    80s pop, creepy, synth
    """

    # Crafting the prompt for OpenAI API
    prompt = f"""
    Craft a concise, 100-character music style description for a {rounded_bpm} BPM song that embodies the genre: {desired_genre}.
    Context: User enjoys {desired_genre} with typical emotional responses: 
    Attention: {emotion_values['Attention']}%, 
    Engagement: {emotion_values['Engagement']}%, 
    Excitement: {emotion_values['Excitement']}%, 
    Relaxation: {emotion_values['Relaxation']}%, 
    Interest: {emotion_values['Interest']}%, 
    Stress: {emotion_values['Stress']}%, 
    Your description should transform emotional metrics into engaging narrative elements without using percentages. 
    Use these metrics to predict how the user is feeling and translate them into a compelling description of the song to either match or contrast the user's mood. 
    We want to reflect the user's mood through the song description but if the user is feeling stressed, a relaxing song could be recommended. 
    Use discression to decide how to match or contrast the user's mood based on the emotional metrics provided. 
    Consider mentioning the song's mood, its instrumental texture, and the overall feel. 
    You should mention the BPM, the genre and a related sub genre if necessary, at least two instruments, one style, one mood, a direction for the vocals and the lyrical content
    You can guide the lyrics using a theme, a setting, a character, a tone, a moral, a resolution, a twist, a detail, a conflict, or a POV, and mention the structure too like chorus, verse, bridge, and intro; using exactly precisely 100 characters long. 
    Ensure your description is creative, packed with vivid imagery and precisely 100 characters long (excluding 'START' and 'END'). 
    Begin with 'START' and end with 'END'. 
    Do not use any artist's name within the song description. 
    Your output must strictly follow these guidelines to ensure it meets the specific character limit and content expectations.
    Here is a list of prompt styles you can use but do not use the artist's name within the song description these are just ideas for the prompt:
    Drake: HipHop, Trap, male vocals
    Bruno Mars: Funk, Dance Pop, Groovy, male vocals
    Fleetwood Mac: Classic Rock, Mellifluous
    Ed Sheeran: Folk, Acoustic Guitar, male vocals
    Tim McGraw: Country, Americana, male vocals
    Elton John: Piano Pop Rock, Theatrical, male vocals
    Dolly Parton: Country, Storytelling, female vocals
    Red Hot Chili Peppers: Funk Rock, Stadium, heavy drums
    Coldplay: Alternative Rock, Atmospheric
    Taylor Swift: Pop, Alternative Folk, Emotional, female vocals
    Elvis Presley: 50s Rock, Hero Theme, male vocals
    Adele: Soul, Emotional, Torch-Lounge, female vocals
    Ariana Grande: Pop, Dance Pop, Ethereal, female vocals
    Billie Eilish: Pop, Dark, Minimal, female vocals
    The Weeknd: RnB, Dark, Cinematic, male vocals
    Beyoncé: RnB, Anthemic, Danceable, female vocals
    Kendrick Lamar: HipHop, Lyrical, Storytelling, male vocals
    Lady Gaga: Pop, Theatrical, Dance, female vocals
    Jay-Z: HipHop, Aggressive, Storytelling, male vocals
    Rihanna: RnB, Dance Pop, Festive, female vocals
    Kanye West: HipHop, Progressive, Eclectic, male vocals
    Justin Bieber: Pop, Danceable, Chillwave, male vocals
    Katy Perry: Pop, Glitter, Festive, female vocals
    Snoop Dogg: Rap, Funk, Chill, male vocals
    Metallica: Heavy Metal, Power
    AC/DC: Hard Rock, Stomp
    Madonna: Dance Pop, High-NRG, female vocals
    David Bowie: 70s British Rock, Art, Eclectic, male vocals
    Bob Dylan: Folk, Storytelling, Acoustic Guitar, male vocals
    Post Malone: Rap, Ethereal, Ambient, male vocals
    Maroon 5: Pop Rock, Danceable, male vocals
    Shakira: Latin, Dance Pop, Festive, female vocals
    Dua Lipa: Disco, Dance Pop, Groovy, female vocals
    Michael Jackson: 80s Pop, Dance, Iconic, male vocals
    Prince: Funk, Eclectic, Glam, male vocals
    Miley Cyrus: Pop, Rock, Party, female vocals
    Cardi B: Rap, Aggressive, Party, female vocals
    Imagine Dragons: Rock, Anthemic, Emotion
    Camila Cabello: Pop, Latin Jazz, Festive, female vocals
    Harry Styles: Pop, Rock, Groovy, male vocals
    Sam Smith: Soul, Emotional, Lounge, male vocals
    Lizzo: Pop, Funk, Empowering, female vocals
    Daft Punk: Electronic, Dance, Futuristic
    Gorillaz: Alternative Rock, Electronic, Unusual
    The Beatles: 60s British Pop, Classic, Rock
    Queen: Rock, Operatic, Theatrical, Male Vocals
    Led Zeppelin: Hard Rock, Blues Rock, Epic
    Pink Floyd: Rock, Progressive, Atmospheric
    The Rolling Stones: Rock, Blues Rock, Classic
    Bob Marley: Reggae, Peaceful, Soulful, male vocals
    Frank Sinatra: 1940s big band, Lounge Singer, male vocals
    Aretha Franklin: Soul, Gospel, Powerful, female vocals
    Whitney Houston: Pop, RnB, Emotional, female vocals
    Stevie Wonder: Soul, Funk, Joyful, male vocals
    The Chainsmokers: EDM, Dance, Party
    Nicki Minaj: Rap, Danceable, Bold, female vocals
    Green Day: Punk Rock, Aggressive, Youthful
    Nirvana: Grunge, Dark, Raw, Male Vocals
    Amy Winehouse: Soul, Jazz, Torch-Lounge, female vocals
    Linkin Park: Rock, Nu Metal, Emotional
    Aerosmith: Rock, Hard Rock, Classic
    Bon Jovi: Rock, Anthem, Stadium
    Billy Joel: Pop, Rock, Storytelling, male vocals
    Phil Collins: Pop, Rock, Emotional, soundtrack, male vocals
    Genesis: Rock, Progressive, Art
    The Eagles: Rock, Country Rock, Harmonious
    The Doors: Rock, Psychedelic, Mysterious
    Janis Joplin: Rock, Blues Rock, Raw Emotion, female vocals
    Jimi Hendrix: Rock, Psychedelic, Guitar Virtuoso, male vocals
    The Who: Rock, Hard Rock, Theatrical
    Black Sabbath: Heavy Metal, Doom
    Iron Maiden: Heavy Metal, Epic, Theatrical
    Judas Priest: Heavy Metal, Power, Leather
    Motorhead: Heavy Metal, Rock’n’Roll, Aggressive
    Slayer: Thrash Metal, Aggressive, Dark
    Ozzy Osbourne: Heavy Metal, Dark, Theatrical, male vocals
    Skrillex: Dubstep, Electronic, Intense, male vocals
    Calvin Harris: EDM, Dance, Festive, male vocals
    Avicii: EDM, Melodic, Euphoric, male vocals
    Arctic Monkeys: Indie Rock, Garage, Cool
    Tame Impala: Psychedelic Rock, Dreamy, Mellifluous
    The Strokes: Indie Rock, Cool, Raw
    Vampire Weekend: Indie Rock, Eclectic, Upbeat
    Kings of Leon: Rock, Emotional, Raw
    The Killers: Rock, Synthpop, Anthemic, male vocals
    System of a Down: Metal, Political, Eccentric
    Radiohead: Alternative Rock, Experimental, Atmospheric
    Foo Fighters: Rock, Alternative, Energetic
    Muse: Rock, Progressive, Theatrical
    Tool: Progressive Metal, Dark, Complex
    Rage Against the Machine: Rap Metal, Political, Aggressive
    Pearl Jam: Grunge, Rock, Emotional
    Soundgarden: 90s Grunge, Heavy, Dark
    Alice in Chains: Grunge, Dark, Melodic
    Sigur Rós: Post-Rock, Ethereal, Atmospheric, Icelandic
    Björk: Alternative, Experimental, Unusual, female vocals
    Enya: New Age, Ethereal, Calm, female vocals
    Deadmau5: Electronic, House, Progressive
    Marshmello: EDM, Dance, Happy
    Zedd: EDM, Dance Pop, Energetic, male vocals
    The XX: Indie Pop, Minimal, Atmospheric
    Lana Del Rey: Pop, Sadcore, Cinematic, female vocals
    Kacey Musgraves: Country, Pop, Mellifluous, female vocals
    St. Vincent: Art Rock, Eclectic, Unusual, female vocals
    Childish Gambino: HipHop, Funk, Thoughtful, male vocals
    SZA: RnB, Neo Soul, Emotional, female vocals
    Frank Ocean: RnB, Soulful, Introspective, male vocals
    Tyler, The Creator: HipHop, Eclectic, Unusual, male vocals
    Solange: RnB, Soul, Artistic, female vocals
    Brockhampton: HipHop, Alternative, Collective
    Janelle Monáe: Funk, RnB, Sci-Fi, female vocals
    Mac DeMarco: Indie Pop, Slacker Rock, Chill, male vocals
    Rufus Du Sol: Electronic, Dance, Atmospheric
    Bon Iver: Indie Folk, Ethereal, Intimate, male vocals
    Florence + The Machine: Indie Rock, Dramatic, Ethereal
    Jack White: Rock, Blues, Raw, male vocals
    Gary Clark Jr.: Blues Rock, Soulful, Gritty, male vocals
    Leon Bridges: Soul, RnB, Retro, male vocals
    Brittany Howard: Rock, Soul, Powerful, female vocals
    Alabama Shakes: Rock, Blues Rock, Soulful
    Glass Animals: Psychedelic Pop, Groovy, Eclectic
    Portugal, The Man: Alternative Rock, Psychedelic, Catchy
    FKA Twigs: RnB, Electronic, Avant-Garde, female vocals
    The National: Indie Rock, Melancholy, Introspective
    MGMT: Psychedelic Pop, Electronic, Playful
    Empire of the Sun: Electronic, Pop, Theatrical
    Grimes: Art Pop, Electronic, Experimental, female vocals
    James Blake: Electronic, Soul, Minimalist, male vocals
    The War on Drugs: Indie Rock, Heartland Rock, Melodic
    Sufjan Stevens: Indie Folk, Baroque Pop, Intimate, male vocals
    Bonobo: Downtempo, Electronic, Ambient
    Caribou: Electronic, Psychedelic, Dance
    Four Tet: Electronic, Ambient, Textural
    Jamie xx: Electronic, House, Minimal
    Nicolas Jaar: Electronic, Experimental, Atmospheric, male vocals
    Flying Lotus: Electronic, Experimental HipHop, Fusion, male vocals
    Thundercat: Funk, Jazz, Experimental, male vocals
    Kamasi Washington: Jazz, Fusion, Epic, male vocals
    Massive Attack: Trip Hop, Dark, Atmospheric
    Portishead: Trip Hop, Dark, Cinematic
    Aphex Twin: IDM, Electronic, Experimental, male vocals
    Boards of Canada: IDM, Downtempo, Nostalgic
    Burial: Dubstep, Ambient, Mysterious
    J Dilla: HipHop, Soulful, Experimental, male vocals
    MF DOOM: HipHop, Abstract, Lyrical, male vocals
    Kendrick Lamar: HipHop, Conscious, Lyrical, male vocals
    Blink-182: emo pop rock, male vocals
    Green Day: Punk Rock, Aggressive, Youthful
    Phoebe Bridgers: Bedroom, grungegaze, catchy, psychedelic, acoustic tape recording, female vocals
    Also, try these fun and unique styles:
    Uplifting atmospheric worship ballad with ethereal vocals and sweeping orchestral arrangements
    Live music, heavy metal with solo guitar, symphonic elements, and aggressive power vocals
    Bedroom-produced grungegaze, catchy, psychedelic, with acoustic tape recording and lo-fi aesthetics
    Rapid-fire rap, 140 bpm, deep bass beats, aggressive delivery in a minor key, creating high tension
    Chillwave electronic, ambient textures, slow-tempo, reverb-heavy vocals, and a dreamy synth backdrop
    Futuristic cyberpunk EDM, high-energy beats, distorted synth lines, and neon-lit, dystopian themes
    Acoustic folk, storytelling lyrics, warm vocal harmonies, fingerstyle guitar, and soft percussion
    Vintage jazz lounge, classic standards, smooth trumpet solos, upright bass, and sultry female vocals
    Baroque pop, intricate melodies, orchestral arrangements, harpsichord flourishes, and poetic lyrics
    Glam rock revival, flamboyant performance, glittery costumes, catchy hooks, and guitar solos
    Sultry RnB, smooth beats, seductive vocals, late-night vibes, and lush production
    Dark ambient, atmospheric soundscapes, slow-moving textures, and an unsettling, eerie mood
    Tropical house, upbeat, sun-kissed melodies, steel drums, breezy vocals, and a laid-back rhythm
    Psychedelic funk, groovy bass lines, wah-wah guitars, trippy effects, and energetic brass sections
    Epic cinematic scores, sweeping orchestral movements, heroic themes, and stirring emotional peaks
    Minimal techno, repetitive beats, subtle progression, hypnotic rhythms, and a deep, underground feel
    Indie surf rock, jangly guitars, beachy vibes, carefree vocals, and upbeat, sunny melodies
    Soulful gospel choir, powerful lead vocals, uplifting messages, organ accompaniment, and handclaps
    Aggressive trap metal, distorted 808s, screamed vocals, chaotic energy, and mosh-pit inducing breakdowns
    Contemporary classical piano, emotive compositions, dynamic range, and nuanced performance
    Gypsy jazz, acoustic guitars, fast-paced swing rhythms, violin solos, and a lively, festive atmosphere
    Dream pop, ethereal vocals, shimmering guitars, lush synths, and a sense of nostalgic longing
    Balkan electro swing, energetic brass ensembles, electronic beats, folk melodies, and infectious dance rhythms
    Hardcore punk, fast tempos, political lyrics, raw vocals, and a DIY ethos
    Space ambient, cosmic soundscapes, slow-evolving textures, and a sense of infinite exploration
    punk rock, ska punk, rock, rap, indie pop
    gregorian chorale, choir, carried singing, epic, majestic, ecclesiastical
    math rock, J-pop, mutation funk, bounce drop, dubstep, edm, 160bpm,
    anime opening, heavy metal, male vocal
    80's,post-punk, punk, Retrowave,slow
    Pentatonic Scale, Modern Classic, Game Music, Guzheng & Piano & Chinese Drum & Cello, Slow, Sad, Mellow
    80s pop, creepy, synth
    """



    output = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    )
    output = output.choices[0].message.content
    output = output.replace("START", "").replace("END", "" ).strip()
    punctuation_to_remove = [":", "!", ";", "."]  # Add any other punctuation as needed
    lyrics_punctuation_to_remove = [":", ";",]  # Add any other punctuation as needed

    for char in punctuation_to_remove:
        output = output.replace(char, "")  # Replace with an empty string or space

    if len(output) > 120:
        output = output[:120]

    title = generate_lyrics_by_prompt({
        "prompt": output,
    })
    title = title['title']

    lyrics_system_message = f"""
    You are an advanced Lyric Generator AI  with a tailored template to produce lyrics using precisely 1000 characters for songs that typically consist of two verses and one chorus, with each section having around 8 lines. This format should accommodate a song duration of up to 2 minutes depending on the BPM and genre. 

    IMPORTANT:
    You have to use precicely 1000 characters to craft the lyrics for the song including metatags and lyrics.
    Begin with 'START' and end with 'END' to ensure your output can be easily identified.
    Use square brackets for the Metatags like: [Verse]

    The lyrics you generate must:
    - Reflect the song's tempo and emotional dynamics by accurately translating emotional metrics into compelling, narrative-driven lyrics.
    - Avoid simplistic rhyming or generic patterns that could misalign with the desired genre. Adapt your style to ensure the lyrics enhance the musical composition.
    - Include a Point of View (POV) that can be abstract or from inanimate objects, introduce conflicts, and detailed imagery to enrich the narrative depth.
    - Utilize metatags like [Verse], [Chorus], [Pre-Chorus], and [Bridge] to structure the song. These should guide the flow and ensure that each section is distinct in rhythm and mood. The verse should set up the narrative, the chorus should act as a memorable hook, and the pre-chorus should build tension leading into the chorus.

    Additionally:
    - Manipulate syllable count, line lengths, and rhythmic patterns to suit the song's BPM and style. This will avoid monotonous structures and help differentiate verses from choruses.
    - Employ strategic pauses, punctuation, and potential ad-libs to vary the pace and inject dynamic shifts in the song.
    - Consider using instrumental tags like [Instrumental Interlude] or [Percussion Break] to suggest breaks in lyrics which can be used to emphasize musical shifts or thematic changes.
    - Consider using instrument solo tags like [Guitar Solo], [Piano Interlude], [Drum Solo], [Saxophone Solo] please make informed decsions in picking the instrument based on the song genre and style you can use these to guide the instrumental breaks in the song. These can be used to showcase musical prowess or add emotional depth to the composition.

    The lyrics should start with a strong thematic line and build up towards a high-energy chorus that aligns with the overall emotional tone of the song. Remember, while AI can start the process, a human touch can refine these elements to better fit the musical context. Your output should be adaptable, allowing for further human edits to perfect the song's lyrical and musical harmony.

    Implement these guidelines to craft lyrics that not only tell a story but also complement the musicality and intended emotional impact of the song within a precise, two-minute framework.
    """

    lyrics_prompt = f"""
    Craft lyrics for a song at {rounded_bpm} BPM in the genre of {desired_genre} using precisely 1000 characters The song should express emotions of Attention, Engagement, Relaxation, Interest, and Stress. Here are the emotional metrics to guide your lyric composition:

    Attention: {emotion_values['Attention']}%, 
    Engagement: {emotion_values['Engagement']}%, 
    Excitement: {emotion_values['Excitement']}%, 
    Relaxation: {emotion_values['Relaxation']}%, 
    Interest: {emotion_values['Interest']}%, 
    Stress: {emotion_values['Stress']}%, 
    Here is the title of the song: {title}
    Here is the song description to inspire your lyrics: {output}

    IMPORTANT:
    You have to use precicely 1000 characters to craft the lyrics for the song including metatags and lyrics.
    Begin with 'START' and end with 'END' to ensure your output can be easily identified.
    Use square brackets for the Metatags like: [Verse]

    Please use a selection of metatags like [Short Instrumental Intro], [Verse], [Chorus], [Catchy Hook], [Short Instrumental Intro], [Pre-Chorus], and [Bridge], [melodic interlude], [Percussion Break], [Outro], [Refrain], [Big Finish], [End], [Fade Out], [Fade to End] to structure the song you can add descriptive Style Words to metatags to guide how the lyrics should be sung
    like [Sad Verse] or [Happy Chorus] you can also use musical terms to influence the genre like [Rapped Verse] or [Powerpop Chorus]. The lyrics should be narrative-driven, avoiding simplistic rhyming patterns.
    Also Style vocals can be used as song-section metatags like: [Female Narrator], [Diva Solo], [Gospel Choir], [Primal Scream], [Rap Verse]
    An instrumental ‘break’ can replace a verse standing as its own section, or might be a short bridge in the music. These seem to work best when only one is used at a time, but adding commas inside the prompt may work. Experiment!
    Prompt examples include:

    [Break]
    [Instrumental Interlude]
    [Melodic Bass]
    [Percussion Break]
    [Syncopated Bass]
    [Fingerstyle Guitar Solo]
    [Build]
    [Bass Drop]

    Be experimental and creative with your song structure, lyrics, and metatags to create a compelling narrative that complements the musical composition.

    Please structure the song as follows:
    - Verse 1: Introduce the setting and/or characters, building up the narrative tension.
    - Chorus: A catchy, emotional pivot that highlights the main theme of enjoying life despite its hurdles.
    - Verse 2: Deepen the narrative with personal reflection or a twist in the story.
    - Final Chorus: Repeat with an added layer of intensity or a slight variation to emphasize the song’s message.

    Ensure the lyrics are precise, with each section clearly defined and aligning with the overall song structure. The total lyric content should not exceed the length suitable for a 2-minute performance, considering the BPM and emotional intensity.
    """


    lyrics_output = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": lyrics_system_message},
            {"role": "user", "content": lyrics_prompt}
        ]
    )

    lyrics_output = lyrics_output.choices[0].message.content
    lyrics_output = lyrics_output.replace("START", "").replace("END", "" ).strip()

    for char in lyrics_punctuation_to_remove:
        lyrics_output = lyrics_output.replace(char, "")  # Replace with an empty string or space

    if len(lyrics_output) > 1240:
        lyrics_output = lyrics_output[:1200]

    print(title)

    print(output)  # Display the generated description
    print(lyrics_output)
    print(title)

    max_attempts = 60  # The maximum number of times to check if the audio is ready
    attempt_interval = 5  # The number of seconds to wait between each attempt

    data = custom_generate_audio({
        "prompt": lyrics_output,
        "tags": output,
        "title": title,
        "make_instrumental": False,
        "wait_audio": False,
        "mv": "chirp-v3-5"
    })
    print(data)
    if data:
        ids = ','.join([clip['id'] for clip in data])
        print(f"Generated song IDs: {ids}")
        song_counter = 1

        for attempt in range(max_attempts):
            song_data = get_audio_information(ids)
            image_information = get_image_information(ids)

            streaming_clips = [clip for clip in song_data if clip['status'] == 'streaming']

            if len(streaming_clips) == len(song_data):
                threads = []
                download_folder = 'downloads'  # Folder where files should be moved post-download
                os.makedirs('images', exist_ok=True)
                os.makedirs(download_folder, exist_ok=True)  # Ensure the download folder exists

                for clip in streaming_clips:
                    audio_url = clip['audio_url']
                    image_url = clip['image_url']
                    if audio_url:
                        new_title = f"{title}{song_counter}.mp3"  # Create a new title for each song
                        destination_path = os.path.join(download_folder, f"downloaded_song_{clip['id']}.mp3")
                        print(f"Preparing to download audio for {clip['id']} from {audio_url}")

                        download_image(image_url, title=title, image_counter=song_counter)  # Ensure image naming consistency

                        t = threading.Thread(target=download_file_from_stream,
                                             args=(audio_url, destination_path, new_title))
                        threads.append(t)
                        t.start()
                        song_counter += 1  # Increment to ensure unique titles

                # Wait for all threads to complete
                for t in threads:
                    t.join()
                print("All downloads completed and files moved.")
                break
            else:
                print(f"Attempt {attempt + 1}: Waiting for all audio to be ready...")
                time.sleep(attempt_interval)
    else:
        print("Failed to generate songs or no IDs returned.")

    delete_file(emotion_file_path)
    delete_file(genre_file_path)

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)  # Explicitly exit with 0 on success
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Exit with a non-zero code to indicate error

