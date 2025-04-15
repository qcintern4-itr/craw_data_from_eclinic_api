import pandas as pd
from export_tables import *

df_encounter_details = table_1
df_encounter = table_2.drop("encounterID", axis=1)
df_log = table_3
df_status = table_4
df_visit = table_5


df_dx_code = table_6

# merge df
df_merged = pd.concat([df_encounter_details, df_encounter, df_log, df_status, df_dx_code], axis=1)

# mapping visitType → visit description
if "visitType" in df_merged.columns and "visit type code" in df_visit.columns:
    df_merged = pd.merge(df_merged, df_visit, left_on='visitType', right_on='visit type code', how='left')

# order column
column_order = [
    "chart_lock_status",
    "createdate",
    "visitType",
    "visit type name",
    "encounterdate",
    "id",
    "isdeleted",
    "patientId",
    "physicianid",
    "practiceid",
    "Facility name",
    "providerfirstname",
    "providerlastname",
    "remarks",
    "sourceencounterid",
    "unbilled",
    "icd_code_10"
]

df_sorted = df_merged[column_order]

df_sorted.to_csv("encounter_sorted.csv", index=False)
