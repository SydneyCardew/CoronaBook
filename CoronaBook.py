r = requests.get('https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=newDeathsByDeathDate&format=csv')
tabledata = []
csv.register_dialect('data', delimiter=",", quoting=csv.QUOTE_NONE)  # creates a csv dialect that seperates on commas
with open(r) as csvfile:
    csvobject = csv.reader(csvfile, dialect='data')  # creates a csv object
    for row in csvobject:
        tabledata.append(row)
print tabledata
