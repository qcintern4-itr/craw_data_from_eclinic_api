import os
from api_crawler.data_collector import *
from api_crawler.read_data_csv import read_acc_numbers_from_csv

def merge_df_csv(from_date, to_date, csv_file_path):
    file_path = os.path.abspath(csv_file_path)
    patient_ids_raw = read_acc_numbers_from_csv(file_path)
    df_acc_no = pd.DataFrame(patient_ids_raw, columns=["acc_no"])

    patient_ids_converted_acc = get_patient_id(patient_ids_raw)
    df_encounter = get_table_encounter(patient_ids_converted_acc, from_date, to_date)
    df_encounter_detail = get_table_encounter_detail(df_encounter)
    df_log = get_table_log(df_encounter_detail)
    df_status_del = get_table_status_del(df_encounter_detail, from_date, to_date)
    df_visit_type = get_table_visit_type()
    df_dx_info = get_table_dx_info(df_encounter_detail)

    # merge to csv
    df_merged = pd.concat([df_encounter_detail, df_encounter.drop("encounterID", axis=1), df_log, df_status_del, df_dx_info, df_acc_no], axis=1)
    if "visitType" in df_merged.columns and "visit type code" in df_visit_type.columns:
        df_merged = pd.merge(df_merged, df_visit_type, left_on='visitType', right_on='visit type code', how='left')


    column_order = [
        "id","patientId","acc_no","chart_lock_status","createdate","visitType","visit type name",
        "encounterdate","isdeleted","physicianid","practiceid","Facility name","providerfirstname","providerlastname",
        "remarks","sourceencounterid","unbilled","icd_code_10"]

    df_sorted = df_merged[column_order]

    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    output_dir = os.path.join(parent_dir, "output")

    # create if not exist
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "encounter.csv")
    df_sorted.to_csv(output_path, index=False)


