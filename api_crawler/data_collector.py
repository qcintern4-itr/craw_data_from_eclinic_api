from api_crawler.parse_response import *
import requests
import pandas as pd
import json
from api_crawler.get_cookies_token import get_token_and_cookies
import config
import time, random

timestamp = int(time.time() * 1000)
rnd2 = random.random()
session = requests.Session()

auth = get_token_and_cookies()
cookies_val = auth["cookies"]
token_val = auth["token"]

def get_cookies():
    return {
        "JSESSIONID": cookies_val["JSESSIONID"],
        "ApplicationGatewayAffinityCORS": cookies_val["ApplicationGatewayAffinityCORS"],
        "ApplicationGatewayAffinity": cookies_val["ApplicationGatewayAffinity"],
        "SL_GWPT_Show_Hide_tmp": "1",
        "SL_G_WPT_TO": "vi",
        "SL_wptGlobTipTmp": "1"
    }


def get_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "x-csrf-token": token_val,
        "Accept": "application/xml, application/json",
        # "Accept-Encoding": "identity",
    }

def convert_acc_to_patient_id(acc_no_num):
    # URL
    url = f"{config.BASE_URL}/catalog/xml/getPatients.jsp"

    # params
    params = {
        "sessionDID": config.SESSION_DID,
        "TrUserId": config.TR_USER_ID,
        "Device": "webemr",
        "ecwappprocessid": 0,
        "rnd2": rnd2,
        "timestamp": timestamp,
        "clientTimezone": config.CLIENT_TIMEZONE
    }

    # Form data
    patient_obj = {
        "AccountNo": acc_no_num,
        "primarySearchValue": acc_no_num,
        "device": "webemr",
        "callFromScreen": "PatientSearch",
        "action": "Patient",
        "SearchBy": "AccountNo"
    }

    response = session.post(url, params=params, data=patient_obj, cookies=get_cookies(), headers=get_headers())

    if response.status_code == 200:
        patient_id = get_patient_id_from_xml(response.text)
        return patient_id


def get_patient_id(patient_ids):
    for i, pid in enumerate(patient_ids):
        if not pid.isdigit():
            converted_id = convert_acc_to_patient_id(pid)
            if converted_id:
                patient_ids[i] = converted_id  # update right that position
    return patient_ids



def get_table_encounter(patient_list, from_date, to_date):
    # URL
    url = f"{config.BASE_URL}/catalog/xml/getPtEncounters.jsp"

    # params
    params = {
        "PatientId": None,
        "FacilityId": 0,
        "LogView": "true",
        "EncOptions": 0,
        "DelOptions": 0,
        "ProviderId": 0,
        "UnlockedEnc": 0,
        "fromDate": from_date,
        "toDate": to_date,
        "ICDItemId": 0,
        "strDeviceType": "webemr",
        "CaseId": 0,
        "CaseTypeId": 0,
        "ecwVisitStatusFlag": "true",
        "blockedEncounterFlagRequest": "true",
        "includeConfidentialInfo": "true",
        "excludeBlockedEncounter": "false",
        "counter": 0,
        "MAXCOUNT": 50,
        "callingfor": "PATIENT_HUB_ENCOUNTER_LOOKUP",
        "IncludeEncCount": 1,
        "sessionDID": config.SESSION_DID,
        "TrUserId": config.TR_USER_ID,
        "Device": "webemr",
        "ecwappprocessid": 0,
        "rnd2": rnd2,
        "timestamp": timestamp,
        "clientTimezone": config.CLIENT_TIMEZONE
    }

    # session = requests.Session()
    all_encounters = []

    for patient_id in patient_list:
        params["PatientId"] = patient_id
        response = session.post(url, params=params, cookies=get_cookies(), headers=get_headers())
        if response.status_code == 200:
            encounters = parse_encounters(response.text)
            for enc in encounters:
                all_encounters.append(enc)

    df = pd.DataFrame(all_encounters)
    return df




def set_table_encounter_detail(encounter_id):
    # URL
    url = f"{config.BASE_URL}/catalog/xml/getValuesForEnctrId.jsp"

    # params
    params = {
        "encounterId": encounter_id,
        "addPtDetails": "true",
        "sessionDID": config.SESSION_DID,
        "TrUserId": config.TR_USER_ID,
        "Device": "webemr",
        "ecwappprocessid": "0",
        "rnd2": rnd2,
        "timestamp": timestamp,
        "clientTimezone": config.CLIENT_TIMEZONE,
        "_": "1744278198672",
        "gd": "e5e084e46d422c4b3ca2fa3aec4b35ee0366eb2f49cd7544046fad06890a47b0"
    }

    # create session and send request
    response = session.get(url, params=params, cookies=get_cookies(), headers=get_headers())

    # check status code
    if response.status_code == 200:
        data = parse_encounter_detail(response.text)
        return data
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


def get_table_encounter_detail(df_table_2):
    result = []
    for _, row in df_table_2.iterrows():
        data = set_table_encounter_detail(row["encounterID"])
        if data:
            result.append(data)
    return pd.DataFrame(result)


def set_table_log(encounter_id):
    url = f"{config.BASE_URL}/catalog/xml/getLogs.jsp"

    params = {
        "EncounterId": encounter_id,
        "sessionDID": config.SESSION_DID,
        "TrUserId": config.TR_USER_ID,
        "Device": "webemr",
        "ecwappprocessid": "0",
        "rnd2": rnd2,
        "timestamp": timestamp,
        "clientTimezone": config.CLIENT_TIMEZONE
    }
    # create session and send request
    response = session.post(url, params=params, headers=get_headers(), cookies=get_cookies())
    # check status code
    if response.status_code == 200:
        data = parse_logs_from_encounter(response.text)
        return data

    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


def get_table_log(df_table_1):
    result = []
    for _, row in df_table_1.iterrows():
        log = set_table_log(row["id"])
        if log:
            result.append(log)
    return pd.DataFrame(result)


def set_table_status_del(patient_id, from_date, to_date):
    url = f"{config.BASE_URL}/catalog/xml/getPtEncounters.jsp"

    params = {
        "PatientId": patient_id,
        "FacilityId": "0",
        "LogView": "true",
        "EncOptions": "0",
        "DelOptions": "1",
        "ProviderId": "0",
        "UnlockedEnc": "0",
        "fromDate": from_date,
        "toDate": to_date,
        "ICDItemId": "0",
        "strDeviceType": "webemr",
        "CaseId": "0",
        "CaseTypeId": "0",
        "ecwVisitStatusFlag": "true",
        "blockedEncounterFlagRequest": "true",
        "includeConfidentialInfo": "true",
        "excludeBlockedEncounter": "false",
        "counter": "0",
        "MAXCOUNT": "50",
        "callingfor": "PATIENT_HUB_ENCOUNTER_LOOKUP",
        "IncludeEncCount": "1",
        "sessionDID": config.SESSION_DID,
        "TrUserId": config.TR_USER_ID,
        "Device": "webemr",
        "ecwappprocessid": "0",
        "rnd2": rnd2,
        "timestamp": timestamp,
        "clientTimezone": config.CLIENT_TIMEZONE
    }

    # create session and send request
    response = session.post(url, params=params, cookies=get_cookies(), headers=get_headers())
    # check status code
    if response.status_code == 200:
        data = get_total_count_status(response.text)
        return data

    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


def get_table_status_del(df_table_1, from_date, to_date):
    result = []
    for _, row in df_table_1.iterrows():
        status = set_table_status_del(row["patientId"], from_date, to_date)
        if status:
            result.append(status)
    return pd.DataFrame(result)


def get_table_visit_type():
    url = f"{config.BASE_URL}/webemr/menu/schedule/visitTypeCostConfigController.jsp"

    params = {
        "Action": "GET_LIST",
        "sessionDID": config.SESSION_DID,
        "TrUserId": config.TR_USER_ID,
        "Device": "webemr",
        "ecwappprocessid": "0",
        "rnd2": rnd2,
        "timestamp": timestamp,
        "clientTimezone": config.CLIENT_TIMEZONE
    }

    # create session and send request
    # session = requests.session()
    response = session.post(url, data=params, cookies=get_cookies(), headers=get_headers())

    if response.status_code == 200:
        json_dict = json.loads(response.text)
        data = get_visit_des(json_dict)
        df = pd.DataFrame(data, columns=["visit type code", "visit type name"])
        return df

    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


def set_table_dx_info(patient_id, encounter_id):
    url = f"{config.BASE_URL}/webemr/labs/LabsRequestHandler.jsp"

    params = {
        "sessionDID": config.SESSION_DID,
        "TrUserId": config.TR_USER_ID,
        "Device": "webemr",
        "ecwappprocessid": "0",
        "rnd2": rnd2,
        "timestamp": timestamp,
        "clientTimezone": config.CLIENT_TIMEZONE
    }

    quick_search_obj = {
        "sContext": "PNScreen",
        "qsMarginTop": -2,
        "nPatientId": patient_id,
        "nTrUserId": config.TR_USER_ID,
        "nEncounterId": encounter_id,
        "nDxItemId": 0,
        "sActionType": ""
    }

    # Form data
    data = {
        "QuickSearchFilterObj": json.dumps(quick_search_obj),
        "sRequestFrom": "qsDirective",
        "sRequestType": "loadQuickSearchData"
    }

    # create session and send request
    # session = requests.session()
    response = session.post(url, params=params, data=data, cookies=get_cookies(), headers=get_headers())

    if response.status_code == 200:
        dx_infor = extract_dx_info(response.text)
        return dx_infor

    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


def get_table_dx_info(df_table_1):
    result = []
    for _, row in df_table_1.iterrows():
        dx_info = set_table_dx_info(row["patientId"], row["id"])  # Trả về list các dxItemCode (string)
        if dx_info:
            merged_dx_codes = ", ".join(dx_info)
        else:
            merged_dx_codes = ""
        result.append({"icd_code_10": merged_dx_codes})

    return pd.DataFrame(result)



