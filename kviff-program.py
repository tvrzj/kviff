# Implementation of Greedy Algorithm for Interval Scheduling Maximization for KVIFF24 movies.
#   ___            __       
#  / _ | ___ __ __/ /_____ _
# / __ |(_-</ // /  '_/ _ `/
#/_/ |_/___/\_,_/_/\_\\_,_/ 
                                                      
import re
from datetime import datetime, timedelta

try:
    with open('MujProgram.txt', 'r', encoding='utf-8') as file:
        data = file.read()    
    lang='cs'
except:
    with open('MyProgramme.txt', 'r', encoding='utf-8') as file:
        data = file.read()
    lang='en'

# Extract films and their projection times based on inputted language
if lang == 'cs':
    film_pattern = re.compile(r'(.+?)\nRežie:.+?(\d{1,4}min.)\n.+?Projekce: (.+?)(?=\n\w|$)', re.DOTALL)
    projections_pattern = re.compile(r'(\d{1,2}\.\d{1,2}\. \d{1,2}:\d{2})')
else:
    film_pattern = re.compile(r'(.+?)\nDirector:.+?(\d{1,4}min.)\n.+?Screenings: (.+?)(?=\n\w|$)', re.DOTALL)
    projections_pattern = re.compile(r'(\d{1,2}\/\d{1,2} \d{1,2}:\d{2})')

length_pattern = re.compile(r'(\d+)min.')

films = film_pattern.findall(data)
film_projections = []

for film, length, projections in films:
    length_minutes = int(length_pattern.search(length).group(1))
    projection_times = projections_pattern.findall(projections)
    for projection in projection_times:
        if lang == 'cs':
            start_time = datetime.strptime(projection, '%d.%m. %H:%M')
        else:
            start_time = datetime.strptime(projection, '%d/%m %H:%M')
        end_time = start_time + timedelta(minutes=length_minutes)
        film_projections.append((film.strip(), start_time, end_time))

# Sort projections by end time
film_projections.sort(key=lambda x: x[2])

# Implement the interval scheduling algorithm with uniqueness constraint
max_films = []
seen_films = set()
unseen_films = set(film[0].strip() for film in films)

last_end_time = datetime.min

for film, start_time, end_time in film_projections:
    if film not in seen_films and start_time >= last_end_time:
        max_films.append((film, start_time, end_time))
        seen_films.add(film)
        last_end_time = end_time

unseen_films -= seen_films

# Print the selected projections
print("Films that will be possible to see:")
for film, start_time, end_time in max_films:
    if lang == 'cs':
        print(f"{film}: {start_time.strftime('%d.%m. %H:%M')} - {end_time.strftime('%d.%m. %H:%M')}")
    else:
        print(f"{film}: {start_time.strftime('%d.%m. %H:%M')} - {end_time.strftime('%d/%m %H:%M')}")

print(f'\nIn total: {len(max_films)}')

print("\nFilms that will not fit into the schedule:")
for film in unseen_films:
    print(f"{film}")