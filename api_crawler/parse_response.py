import json
import xml.etree.ElementTree as ET


def parse_encounters(xml_text):
    encounters = []
    try:
        root = ET.fromstring(xml_text)
        rows = root.findall(".//row")
        for row in rows:
            unbilled_raw = row.findtext("ClaimReq")
            unbilled = True if unbilled_raw == "0" else False
            encounter = {
                "encounterID": row.findtext("encounterID"),
                "physicianid": row.findtext("doctorID"),
                "practiceid": row.findtext("facilityId"),
                "Facility name": row.findtext("FacName"),
                "providerfirstname": row.findtext("ufname"),
                "providerlastname": row.findtext("ulname"),
                "unbilled": unbilled,
                "date":row.findtext("date")
            }
            encounters.append(encounter)
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
    return encounters


def parse_encounter_detail(xml_text):
    try:
        root = ET.fromstring(xml_text)
        encounter_elem = root.find(".//encounter")
        enc_lock_raw = encounter_elem.findtext("encLock")
        if enc_lock_raw == "1":
            chart_lock_status = "Lock"
        else:
            chart_lock_status = "Unlock"

        # Parse data in tag <encounter>
        return {
            "chart_lock_status": chart_lock_status,
            "visitType": encounter_elem.findtext("visitType"),
            "encounterdate": encounter_elem.findtext("date"),
            "id": encounter_elem.findtext("encounterId"),
            "patientId": encounter_elem.findtext("patientId"),
            "remarks": encounter_elem.findtext("reason"),
            "sourceencounterid": encounter_elem.findtext("ResourceId"),
        }



    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
        return {}
    except AttributeError as e:
        print(f"Tag not found error: {e}")
        return {}


def parse_logs_from_encounter(xml_text):
    try:
        root = ET.fromstring(xml_text)
        logs = root.findall(".//log")
        if len(logs) >= 2:
            second_log = logs[1]
            return {
                "createdate": second_log.findtext("date"),

            }
        else:
            return {"error": "Not found the second log"}
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
        return {}


def get_total_count_status(xml_text):
    try:
        root = ET.fromstring(xml_text)
        total_count = int(root.findtext(".//totalCount").strip())
        status_flag = total_count >= 1  # True if total count > 1

        return {
            "isdeleted": str(status_flag)
        }
    except Exception as e:
        print(f"XML parsing status error: {e}")
        return {}


def get_visit_des(json_data):
    results = []
    for item in json_data["data"]:
        visit_code = item["visitcode"]
        visit_desc = item["visitcodedesc"]

        results.append((visit_code, visit_desc))
    return results



def extract_dx_info(response_text):
    try:
        data = json.loads(response_text)
        dx_list = data.get("DxList", {}).get("Dx", [])
        result = []
        for dx_item in dx_list:
            code = dx_item.get("dxItemCode")
            if code and code != 'N/A':
                result.append(code)
        return result
    except json.JSONDecodeError:
        print("Error: JSON invalid.")
        return []


def get_patient_id_from_xml(xml_text):
    try:
        # Parse XML
        root = ET.fromstring(xml_text)

        # Tìm đến thẻ <id> (bất kể namespace)
        # Tìm tất cả thẻ "id" trong toàn bộ XML, và lấy thẻ đầu tiên
        id_element = root.find(".//id")

        if id_element is not None:
            return id_element.text
        else:
            return None
    except ET.ParseError as e:
        print("Lỗi khi parse XML:", e)
        return None