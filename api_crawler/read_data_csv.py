import csv


def read_acc_numbers_from_csv(file_path):
    acc_numbers = []
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        if 'Acc #' not in reader.fieldnames:
            raise Exception("column 'Acc #' not found")
        for row in reader:
            acc_numbers.append(row['Acc #'])
    return acc_numbers
