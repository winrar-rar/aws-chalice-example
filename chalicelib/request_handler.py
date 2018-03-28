from chalicelib import db

def handle_get_all():
    return db.get_all()

def handle_get_company(company):
    return db.get_item(company)

def handle_post_item(data):
    return db.post_item(data)

def handle_put_item(company, data):
    return db.put_item(company, data)

def handle_delete_item(uuid):
    return db.delete_item(uuid)