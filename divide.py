import bs4
import random
import requests
import sys

if len(sys.argv) != 2:
    print('Usage: python ' + sys.argv[0] + ' <minimum_group_size>')
    sys.exit(1)

try:
    minimum_group_size = int(sys.argv[1])
except ValueError:
    print("Error: minimum_group_size must be an integer.")
    sys.exit(1)

URL = 'https://www.novacare.no/menneskene'

response = requests.get(URL)
soup = bs4.BeautifulSoup(response.text, 'html.parser')
employee_tags = soup.select('li h2')
# The first and last name are separate nodes, so join them with a space
employees = [tag.get_text(' ', strip=True) for tag in employee_tags]
employees = [name for name in employees if name]

if not employees:
    print(f'Error: found no employees at {URL}. Has the page markup changed?')
    sys.exit(1)

random.shuffle(employees)

employee_count = len(employees)
group_count = employee_count // minimum_group_size
extra_persons = employee_count % minimum_group_size
group_sizes = [minimum_group_size] * group_count

# Distribute extra persons
for index in range(extra_persons):
    group_sizes[index % len(group_sizes)] += 1

start_index = 0

# Print groups
for i, size in enumerate(group_sizes):    
    print(f'\nGruppe {i+1} ({size} personer):')

    end_index = start_index + size
    current_group = employees[start_index:end_index]

    for person in current_group:
        print(f"- {person}")
       
    start_index = end_index
    print()