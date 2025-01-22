from config.directories import BASE_DIRECTORY


def init_firebase(storage_bucket: str):
    import firebase_admin
    from firebase_admin import credentials

    cred = credentials.Certificate(f"{BASE_DIRECTORY}/key.json")
    firebase_admin.initialize_app(cred, {'storageBucket': storage_bucket})