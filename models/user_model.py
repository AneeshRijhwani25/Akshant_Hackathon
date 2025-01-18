def create_user_collection(db):
    user_schema = {
        'email': {"type": "string", "required": True},
        'password': {"type": "string", "required": True},
        'KYCStatus': {"type": "bool", "default": False},
        'Documents': {
            "panCardDetails": {
                'panCardNumber': {"type": "string"},
                'nameOnPanCard': {"type": "string"},
                'DateOfBirth': {"type": "string"}
            },
            "DrivingLicenceDetails": {
                'drivingLicenceNumber': {"type": "string"},
                'expDate': {"type": "string"},
                'DateofBirth': {"type": "string"},
                'nameOnDrivingLicence': {"type": "string"}
            }
        }
    }
    db.create_collection('users')
