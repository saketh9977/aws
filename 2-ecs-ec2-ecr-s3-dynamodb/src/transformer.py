
from src.utils import (
    get_cur_timestamp_str,
    print_
)

def get_transformed_response(res_list):

    out = []

    for res in res_list:

        if len(res) == 0:
            return out

        po_list = res[0].get('PostOffice', [])
        if len(po_list) == 0:
            return out

        for po_dict in po_list:
            pin_code = po_dict.get('Pincode', '')
            area_name = po_dict.get('Name', '')
            circle = po_dict.get('Circle', '')
            district = po_dict.get('District', '')
            state = po_dict.get('State', '')
            country = po_dict.get('Country', '')
            timestamp = get_cur_timestamp_str()

            out.append({
                'pin_code': pin_code,
                'timestamp': timestamp,
                'area_name': area_name,
                'circle': circle,
                'district': district,
                'state': state,
                'country': country
            })

        # print_(f"transfomer: transformed data = {out}")

    return out
