import time

from data_collector import get_table_2, get_table_1, get_table_3, get_table_4, get_table_5, get_table_6
from read_data_csv import read_acc_numbers_from_csv
import os



file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "patientid_10_4_25.csv"))
patient_ids = read_acc_numbers_from_csv(file_path)


from_date = "4/10/2025"
to_date = "4/10/2025"



# Table 2 - cần đầu tiên
table_2 = get_table_2(patient_ids, from_date, to_date)
table_2.to_csv("encounters_data.csv", index=False)

# Table 1
table_1 = get_table_1(table_2)
table_1.to_csv("encounters_detail.csv", index=False)

# Table 3
table_3 = get_table_3(table_1)
table_3.to_csv("logs_data.csv", index=False)

# Table 4
table_4 = get_table_4(table_1, from_date, to_date)
table_4.to_csv("status_data.csv", index=False)

# Table 5

table_5 = get_table_5()
table_5.to_csv("visit_data.csv", index=False)

# talbe 6
table_6 = get_table_6(table_1)
table_6.to_csv("dx_info.csv", index=False)


