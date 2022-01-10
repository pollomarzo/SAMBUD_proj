import csv

# import csv file and only keep the ones referring to an entire region
with open('italian_population.csv') as csvfile:
    reader = csv.reader(csvfile)
    with open('italian_population_by_region.csv', 'w+') as newfile:
        writer = csv.writer(newfile)
        first_row = next(reader)
        first_row[0] = "NUTS2"
        # remove flag trash
        writer.writerow(first_row[:13])
        for row in reader:
            if len(row[0]) == 4 and row[5] == row[7] == row[9] == "totale":
                writer.writerow(
                    [row[0].replace("ITD", "ITH").replace("ITE", "ITI"), *  row[1:13]])
