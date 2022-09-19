last = []
names = [[], []]

with open('last.txt', 'r') as f:
    for line in f:
        last.append(line.strip())

with open('male-names.txt', 'r', encoding='utf-8') as f:
    for line in f:
        names[0].append(line.strip())

with open('female-names.txt', 'r', encoding='utf-8') as f:
    for line in f:
        names[1].append(line.strip())

gcodes = ['M', 'F']


jobs = [
    'Training Manager', 'Product Specialist I', 'Software Engineer I', 'IT Business Analyst', 
    'Software Developer', 'Project Manager', 'Deployment Manager', 'Software Engineer II',
    'Corporate Consultant', 'Development Intern', 'Software Engineer', 'Staff Accountant', 'Web Developer I', 
    'Technical Writer', 'Account Manager', 'Human Resource', 'Account Executive'
]

companies = [['9JT', 'MIE'], ['3EJ', 'NMC'], ['ZZ9', 'Contractors']]

departments = [
    'BlueHive', 'BlueHive Development', 'BlueHive Sales & Business Dev', 
    'Data Center', 'Development', 'EH Customer Success', 'EH Deployment', 
    'EH Development', 'EH HQ', 'EH Marketing', 'EH Product Management', 
    'EH Project Management', 'EH Sales', 'Enterprise Health', 'Help Desk', 
    'Marketing', 'MIE DevOps', 'MIE Finance and Accounting', 'MIE Headquarters', 
    'MIE Human Resource', 'MIE IT HQ', 'MIE Project Management', 
    'MIE Security & Risk Assessment', 'MIE Software Engineering', 
    'MIE Software Engineering HQ', 'MIE Systems Engineering', 'MIE Tech Support', 
    'NoMoreClipboard', 'Webchart', 'WebChart Customer Success', 'WebChart Sales & Business Dev'
]

states = [
    ['Alabama', 'AL'], ['Alaska', 'AK'], ['Arizona', 'AZ'], ['Arkansas', 'AR'], 
    ['California', 'CA'], ['Colorado', 'CO'], ['Connecticut', 'CT'], ['Delaware', 'DE'], 
    ['District of Columbia', 'DC'], ['Florida', 'FL'], ['Georgia', 'GA'], ['Hawaii', 'HI'], 
    ['Idaho', 'ID'], ['Illinois', 'IL'], ['Indiana', 'IN'], ['Iowa', 'IA'], ['Kansas', 'KS'], 
    ['Kentucky', 'KY'], ['Louisiana', 'LA'], ['Maine', 'ME'], ['Maryland', 'MD'], 
    ['Massachusetts', 'MA'], ['Michigan', 'MI'], ['Minnesota', 'MN'], ['Mississippi', 'MS'], 
    ['Missouri', 'MO'], ['Montana', 'MT'], ['Nebraska', 'NE'], ['Nevada', 'NV'], ['New Hampshire', 'NH'], 
    ['New Jersey', 'NJ'], ['New Mexico', 'NM'], ['New York', 'NY'], ['North Carolina', 'NC'], 
    ['North Dakota', 'ND'], ['Ohio', 'OH'], ['Oklahoma', 'OK'], ['Oregon', 'OR'], ['Pennsylvania', 'PA'], 
    ['Rhode Island', 'RI'], ['South Carolina', 'SC'], ['South Dakota', 'SD'], ['Tennessee', 'TN'], 
    ['Texas', 'TX'], ['Utah', 'UT'], ['Vermont', 'VT'], ['Virginia', 'VA'], ['Washington', 'WA'], 
    ['West Virginia', 'WV'], ['Wisconsin', 'WI'], ['Wyoming', 'WY']
]

add_suffix = ['Avenue', 'Road', 'Street', 'Lane', 'Way', 'Place']

notification_types = [
    'worker.legal-address.change', 
    'worker.legal-name.change', 
    'worker.preferred-name.change',
    'worker.hire', 
    'worker.terminate', 
    'worker.reports-to.modify'
]

notification_templates = [
    {
        "data": {
            "eventContext": {
                "worker": {
                    "associateOID": None
                }
            },
            "output": {
                "worker": {
                    "associateOID": None,
                    "person": {
                        "legalAddress": {
                            "lineOne": None,
                            "cityName": None,
                            "countrySubdivisionLevel1": {
                                "codeValue": None,
                                "shortName": None
                            },
                            "postalCode": None
                        }
                    }
                }
            }
        },
        "eventID": None,
        "eventNameCode": {
            "codeValue": "worker.legal-address.change"
        }
    },
    {
        "data": {
            "eventContext": {
                "worker": {
                    "associateOID": None
                }
            },
            "output": {
                "worker": {
                    "associateOID": None,
                    "person": {
                        "legalName": {
                            "familyName1": None
                        }
                    }
                
                }
            }
        },
        "eventID": None,
        "eventNameCode": {
            "codeValue": "worker.legal-name.change"
        }
    },
    {
        "data": {
            "eventContext": {
                "worker": {
                    "associateOID": None
                }
            },
            "output": {
                "worker": {
                    "associateOID": None,
                    "person": {
                        "legalName": {
                            "nickName": None
                        }
                    }
                }
            }
        },
        "eventID": None,
        "eventNameCode": {
            "codeValue": "worker.preferred-name.change"
        }
    },
    {
        "data": {
            "eventContext": {
                "worker": {
                    "associateOID": None
                }
            },
            "output": {
                "worker": {
                    
                }
            }
        },
        "eventID": None,
        "eventNameCode": {
            "codeValue": "worker.hire"
        }
    },
    {
        "data": {
            "eventContext": {
                "worker": {
                    "associateOID": None
                }
            },
            "output": {
                "worker": {
                    "associateOID": None,
                    "workerStatus": {
                        "statusCode": {
                            "codeValue": "Terminated"
                        }
                     }  
                }
            }
        },
        "eventID": None,
        "eventNameCode": {
            "codeValue": "worker.terminate"
        }
    },
    {
        "data": {
            "eventContext": {
                "worker": {
                    "associateOID": None
                }
            },
            "output": {
                "worker": {
                    "associateOID": None,
                    "reportsTo": {
                        "associateOID": None, 
                        "reportsToWorkerName": {
                            "givenName": None,
                            "familyName1": None
                        }   
                    },
                
                }
            }
        },
        "eventID": None,
        "eventNameCode": {
            "codeValue": "worker.reports-to.modify"
        }
    }
]