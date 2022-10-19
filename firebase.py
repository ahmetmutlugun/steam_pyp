import json
import os
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
if __name__ == "__main__":
    cred = credentials.Certificate(os.getcwd() + "/../firebase.json")
else:
    cred = credentials.Certificate(os.getcwd() + "/firebase.json")

# Initialize the app with a service account, granting admin privileges
f = open('config.json')
url = json.load(f)['firebase_url']
f.close()

firebase_admin.initialize_app(cred, {
    'databaseURL': url
})


# As an admin, the app has access to read and write all data, regradless of Security Rules


def set_item(items):
    update_dict = {}
    for i in items:
        name = str(i[0])
        name = name.replace(".", "(dot)")
        if i[1] is not None and 'success' in i[1]:
            i[1].pop("success")
        update_dict.update({name: i[1]})
    ref = db.reference("Items")
    ref.update(update_dict)
