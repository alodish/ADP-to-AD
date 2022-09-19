import random
import string
from random_word import RandomWords
import json
from config import (
    names, 
    gcodes, 
    last, jobs, 
    companies, 
    departments, 
    states, 
    add_suffix, 
    notification_types, 
    notification_templates
)


r = RandomWords()


def generate_users(n):
    employees = {"workers": []}
    for i in range(n):
        w1 = ""
        w2 = ""

        while not w1:
            w1 = r.get_random_word(includePartOfSpeech="noun")
        w1 = w1.capitalize()

        while not w2:
            w2 = r.get_random_word(includePartOfSpeech="noun")
        w2 = w2.capitalize()

        aoid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

        lineOne = str(random.randrange(1, 99999)) + ' ' +  w1 + ' ' + random.choice(add_suffix)
        state = random.choice(states)
        list_idx = random.choice([0, 1])
        mgr_idx = random.choice([0, 1, 2])
        
        with open('managers.json', 'r') as mgr:
            manager = json.load(mgr)
            mgr.close()

        d = {
            "associateOID": aoid,
            "person": {
                "legalName": {
                    "givenName": random.choice(names[list_idx]),
                    "middleName": random.choice(["", random.choice(names[list_idx])]),
                    "familyName1": random.choice(last),
                    "nickName": random.choice(["", random.choice(names[list_idx])]),
                    "genderCode": {
                        "codeValue": gcodes[list_idx]
                    },
                },
                "legalAddress": {
                    "lineOne": lineOne,
                    "cityName": w2,
                    "countrySubdivisionLevel1": {
                        "codeValue": state[1],
                        "shortName": state[0]
                    },
                "countryCode": "US",
                "postalCode": random.randrange(10000, 99999)
            },
                "communication": {
                    "mobiles": [
                        {
                            "countryDialing": 1,
                            "areaDialing": random.randrange(300, 999),
                            "dialNumber": random.randrange(3000000, 9999999)
                        }
                    ]
                }
            },
            "workAssignments": [
                {
                    "homeOrganizationalUnits": [
                        {
                            "nameCode": {
                                    "shortName": random.choice(departments)
                                }
                        }
                    ],
                    "jobTitle": random.choice(jobs),
                    "reportsTo": {
                        "associateOID": manager['workers'][mgr_idx]['associateOID'],
                        "reportsToWorkerName": {
                            "givenName": manager['workers'][mgr_idx]['person']['legalName']['givenName'],
                            "familyName1": manager['workers'][mgr_idx]['person']['legalName']['familyName1']
                        }   
                    },
                    "payrollGroupCode": random.choices(companies, weights=[65, 10, 25])[0][0],
                }
            ],
            "workerDates":{
                "originalHireDate": '-'.join(
                    [
                        str(random.choice(range(2008, 2023))), 
                        str(random.choice(range(1,13))), 
                        str(random.choice(range(1, 28)))
                    ]
                )
            },
            "workerStatus": {
                "statusCode": {
                    "codeValue": "Active"
                }
            }
        }

        if not d['person']['legalName']['middleName']:
            d['person']['legalName'].pop('middleName', None)
    
        if not d['person']['legalName']['nickName']:
            d['person']['legalName'].pop('nickName', None)

        employees["workers"].append(d)

    return employees

def generate_events(n=5, event=False):
    notifications = []
    for _ in range(n):
        if event:
            notification_type = event
            template = notification_templates[notification_type.index(event)]
        else:
            event_qty = len(notification_types)
            current_event = random.choice(list(range(event_qty)))
            notification_type = notification_types[current_event]
            template = notification_templates[current_event]
        with open('dummies.json', 'r') as f:
            obj = json.load(f)
            worker_idx = random.choice(list(range(len(obj['workers']))))
            f.close()

        template['eventID']  = '-'.join(
            [
                ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)), 
                ''.join(random.choices(string.ascii_lowercase + string.digits, k=4)),
                ''.join(random.choices(string.ascii_lowercase + string.digits, k=4)),
                ''.join(random.choices(string.ascii_lowercase + string.digits, k=12)),
            ]
        ) 
        match notification_types.index(notification_type):
            case 0:
                w1 = ""
                w2 = ""

                while not w1:
                    w1 = r.get_random_word(includePartOfSpeech="noun")
                w1 = w1.capitalize()

                while not w2:
                    w2 = r.get_random_word(includePartOfSpeech="noun")
                w2 = w2.capitalize()
                lineOne = str(random.randrange(1, 99999)) + ' ' +  w1 + ' ' + random.choice(add_suffix)
                state = random.choice(states)
                zip_code = random.randrange(10000, 99999)
                mod_obj = obj['workers'][worker_idx]['person']['legalAddress']
                mod_obj['lineOne'] = lineOne
                mod_obj['cityName'] = w2
                mod_obj['countrySubdivisionLevel1']['codeValue'] = state[1]
                mod_obj['countrySubdivisionLevel1']['shortName'] = state[0]
                mod_obj['postalCode'] = zip_code
                obj['workers'][worker_idx]['person']['legalAddress'] = mod_obj
                notification = 'Legal Name changed for {} {} (associateOID: {}).'.format(
                    obj['workers'][worker_idx]['person']['legalName']['givenName'],
                    obj['workers'][worker_idx]['person']['legalName']['familyName1'],
                    obj['workers'][worker_idx]['associateOID']
                )
                notifications.append(notification)

                template['data']['eventContext']['worker']['associateOID'] = obj['workers'][worker_idx]['associateOID']
                template['data']['output']['worker']['associateOID'] = obj['workers'][worker_idx]['associateOID']
                template['data']['output']['worker']['person']['legalAddress']['lineOne'] = lineOne
                template['data']['output']['worker']['person']['legalAddress']['cityName'] = w2
                template['data']['output']['worker']['person']['legalAddress']['countrySubdivisionLevel1']['codeValue'] = state[1]
                template['data']['output']['worker']['person']['legalAddress']['countrySubdivisionLevel1']['shortName'] = state[0]
                template['data']['output']['worker']['person']['legalAddress']['postalCode'] = zip_code

            case 1:
                mod_obj = obj['workers'][worker_idx]['person']['legalName']
                mod_obj['familyName1'] = random.choice(last)
                obj['workers'][worker_idx]['person']['legalName']['familyName1'] = mod_obj['familyName1']
                notification = 'Last Name changed for {} {} (associateOID: {}).'.format(
                    obj['workers'][worker_idx]['person']['legalName']['givenName'],
                    obj['workers'][worker_idx]['person']['legalName']['familyName1'],
                    obj['workers'][worker_idx]['associateOID']
                )
                notifications.append(notification)

                template['data']['eventContext']['worker']['associateOID'] = obj['workers'][worker_idx]['associateOID']
                template['data']['output']['worker']['associateOID'] = obj['workers'][worker_idx]['associateOID']
                template['data']['output']['worker']['person']['legalName']['familyName1'] = mod_obj['familyName1']

            case 2:
                mod_obj = obj['workers'][worker_idx]['person']['legalName']
                mod_obj['nickName'] = random.choice(names[gcodes.index(mod_obj['genderCode']['codeValue'])])
                obj['workers'][worker_idx]['person']['legalName']['nickName'] = mod_obj['nickName']
                notification = 'Preferred Name changed for {} {} (associateOID: {}).'.format(
                    obj['workers'][worker_idx]['person']['legalName']['givenName'],
                    obj['workers'][worker_idx]['person']['legalName']['familyName1'],
                    obj['workers'][worker_idx]['associateOID']
                )
                notifications.append(notification)

                template['data']['eventContext']['worker']['associateOID'] = obj['workers'][worker_idx]['associateOID']
                template['data']['output']['worker']['associateOID'] = obj['workers'][worker_idx]['associateOID']
                template['data']['output']['worker']['person']['legalName']['nickName'] = mod_obj['nickName']

            case 3:
                new_worker = generate_users(1)
                mod_obj = new_worker['workers'][0]
                obj['workers'].append(mod_obj)
                notification = 'New Employee, {} {} (associateOID: {}), has been hired.'.format(
                    mod_obj['person']['legalName']['givenName'],
                    mod_obj['person']['legalName']['familyName1'],
                    mod_obj['associateOID']
                )
                notifications.append(notification)

                template['data']['eventContext']['worker']['associateOID'] = mod_obj['associateOID']
                template['data']['output']['worker'] = mod_obj

            case 4:
                mod_obj = obj['workers'][worker_idx]['workerStatus']['statusCode']
                mod_obj['codeValue'] = 'Terminated'
                obj['workers'][worker_idx]['workerStatus']['statusCode'] = mod_obj
                notification = 'Employee, {} {} (associateOID: {}), has been terminated.'.format(
                    obj['workers'][worker_idx]['person']['legalName']['givenName'],
                    obj['workers'][worker_idx]['person']['legalName']['familyName1'],
                    obj['workers'][worker_idx]['associateOID']
                )
                notifications.append(notification)

                template['data']['output']['worker']['associateOID'] = obj['workers'][worker_idx]['associateOID']
                template['data']['eventContext']['worker']['associateOID'] = obj['workers'][worker_idx]['associateOID']

            case 5:
                current_manager = obj['workers'][worker_idx]['workAssignments'][0]['reportsTo']['associateOID']
                with open('managers.json', 'r') as m:
                    mgr_obj = json.load(m)
                    m.close()
                
                managers = {}
                for i in range(len(mgr_obj['workers'])):
                    managers[mgr_obj['workers'][i]['associateOID']] = [
                        mgr_obj['workers'][i]['person']['legalName']['givenName'],
                        mgr_obj['workers'][i]['person']['legalName']['familyName1']
                    ]
                
                manager = random.choice(list(managers.keys()))
                while manager == current_manager:
                    manager = random.choice(list(managers.keys()))

                mod_obj = obj['workers'][worker_idx]['workAssignments'][0]['reportsTo']
                mod_obj['associateOID'] = manager
                mod_obj['reportsToWorkerName']['givenName'] = managers[manager][0]
                mod_obj['reportsToWorkerName']['familyName1'] = managers[manager][1]
                obj['workers'][worker_idx]['workAssignments'][0]['reportsTo'] = mod_obj
                obj['workers'][worker_idx]['associateOID'] 

                notification = 'Manager has been changed for {} {} (associateOID: {}).'.format(
                    obj['workers'][worker_idx]['person']['legalName']['givenName'],
                    obj['workers'][worker_idx]['person']['legalName']['familyName1'],
                    obj['workers'][worker_idx]['associateOID']
                )
                notifications.append(notification)

                template['data']['eventContext']['worker']['associateOID'] = obj['workers'][worker_idx]['associateOID']
                template['data']['output']['worker']['associateOID'] = obj['workers'][worker_idx]['associateOID']
                template['data']['output']['worker']['reportsTo'] = obj['workers'][worker_idx]['workAssignments'][0]['reportsTo']

        
        updated_object = json.dumps(obj, indent=4)
        with open('dummies.json', 'w') as d:
            d.write(updated_object)

        with open('notification_queue.json', 'r') as n:
            all_notification = json.load(n)
            n.close()

        all_notification['notifications'].append(template)

        with open('notification_queue.json', 'w') as n:
            n.write(json.dumps(all_notification, indent=4))
            n.close()

        
    return notifications

    