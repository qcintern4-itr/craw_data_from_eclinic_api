import csv
import os
import  pandas as pd

def read_acc_numbers_from_csv(file_path):
    acc_numbers = []
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        if 'Acc #' not in reader.fieldnames:
            raise Exception("column 'Acc #' not found")
        for row in reader:
            acc_numbers.append(row['Acc #'])
    return acc_numbers


# file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "patientid_10_4_25.csv"))
# patient_ids_raw = read_acc_numbers_from_csv(file_path)
# # patient_ids_converted_acc = get_patient_id(patient_ids_raw)
# df_acc_no = pd.DataFrame(patient_ids_raw, columns=["acc_no"])
#
# df_acc_no.to_csv("test_acc_no.csv", index=False)