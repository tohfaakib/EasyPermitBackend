import requests
import json
from pyairtable import Api
from settings import AppSettings

settings = AppSettings()

def geocoder_municipality_status(smartyAutoAddress, filtered_airtable_cities):
    url = "https://usgeocoder.com/api/get_info.php"
    params = {
        "address": f"{smartyAutoAddress['street_line']}", 
        "zipcode": smartyAutoAddress['zipcode'], 
        "authkey": settings.GEOCODER_AUTH_KEY, 
        "format": "json"
    }
    try:
        response = requests.get(url, params=params)
        data = json.loads(response.text)

        municipal_status = data['usgeocoder']['jurisdictions_info']['municipal']['municipal_status']

        if municipal_status == 'Match Found':
            municipal_name = data['usgeocoder']['jurisdictions_info']['municipal']['municipal_name']

            if municipal_name in filtered_airtable_cities:
                response = {
                    'data': {
                        'message': "Municipality Match Found and municipal_name(city) in airtable_cities",
                        'success': True
                    },
                }
                return response
            else:
                response = {
                    'data': {
                        'message': "Municipality Match Found but municipal_name(city) not in airtable_cities!",
                        'success': False
                    },
                }
                return response
            
        elif municipal_status == 'Un-incorporated':
            if '-' in filtered_airtable_cities:
                response = {
                    'data': {
                        'message': "Municipality Un-incorporated and - in airtable_cities.",
                        'success': True
                    },
                }
                return response
            else:
                response = {
                    'data': {
                        'message': "Municipality Un-incorporated and - not in airtable_cities.",
                        'success': False
                    },
                }
                return response

    except Exception as e:
        response = {
            'data': {
                'message': "Geocoder VPN is turned OFF.",
                'success': False
            },
        }
        return response

def airtable_county_check(smartyAutoAddress, smarty_county):
    api = Api(settings.AIRTABLE_TOKEN)
    table = api.table(settings.AIRTABLE_BASE_ID, settings.AIRTABLE_TABLE_ID)

    filter_formula = f"AND({{Allowed?}}=1, {{county}}='{smarty_county}')"

    # filter_formula = "{Allowed?}=1"
    filtered_airtable = table.all(formula=filter_formula)

    filtered_airtable_cities = [item['fields']['City'] for item in filtered_airtable]

    if len(filtered_airtable) > 0:
        return geocoder_municipality_status(smartyAutoAddress, filtered_airtable_cities)
    else:
        response = {
            'data': {
                'message': "Smarty county is not available in Airtable county.",
                'success': False
            },
        }
        return response

def smarty_residency_county(smartyAutoAddress):
    url = "https://us-street.api.smarty.com/street-address"
    params = {
        "auth-id": settings.SMARTY_AUTH_ID,
        "auth-token": settings.SMARTY_AUTH_TOKEN,
        "street": smartyAutoAddress['street_line'],
        "city": smartyAutoAddress['city'],
        "state": smartyAutoAddress['state']
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        res = response.json()
        
        try:
            residency = res[0]['metadata']['rdi'] if res else None
            county_name = res[0]['metadata']['county_name'] if res else None

            data = {
                "residency": residency,
                "county": county_name
            }
            return data
        except Exception as e:
            data = {
                "residency": str(e),
                "county": str(e)
            }
            return data
    else:
        print(f"Request failed with status code {response.status_code}")
        return None


def validate_address(smartyAutoAddress):
    if smartyAutoAddress['state'] == 'CA':
        rc = smarty_residency_county(smartyAutoAddress)

        if rc['residency'] == 'Residential':
            county_response = airtable_county_check(smartyAutoAddress, rc['county'])
            return county_response
        response = {
            'data': {
                'message': "Address is  not residential.",
                'success': False
            },
        }
        return response
    else:
        response = {
            'data': {
                'message': "Sorry! Service only available for california state",
                'success': False
            },
        }
        return response

