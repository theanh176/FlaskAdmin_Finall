from hospital.models import Receipt, ReceiptDetails, Medicine, db, Customer, ClinicalRecords, Disease
from sqlalchemy import func
from sqlalchemy.sql.functions import count

def get_receiptDetails():
    return ReceiptDetails.query.all()

def get_all_detail():
    return db.session.query(Receipt.created_date, Customer.name, func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price).label("TotalPrice"))\
        .join(Receipt, Receipt.id == ReceiptDetails.receipt_id)\
        .join(Customer, Customer.id == Receipt.patient_id).group_by(ReceiptDetails.receipt_id, Customer.name).all()

# def get_receipt_detail(id_patient):
#     return db.session.query(Medicine.name, ReceiptDetails.medicine_id, ReceiptDetails.quantity, ReceiptDetails.unit_price)\
#         .join(Receipt, Receipt.id == ReceiptDetails.receipt_id).join(Medicine, Medicine.id == ReceiptDetails.medicine_id)\
#         .filter(Receipt.patient_id == id_patient).all()

def get_name_receipt_detail(name_patient):
    return db.session.query(Medicine.name, ReceiptDetails.medicine_id, ReceiptDetails.quantity, ReceiptDetails.unit_price, Receipt.created_date)\
        .join(Receipt, Receipt.id == ReceiptDetails.receipt_id).join(Medicine, Medicine.id == ReceiptDetails.medicine_id)\
        .join(Customer, Customer.id == Receipt.patient_id)\
        .filter(Customer.name == name_patient).all()


def get_stats_by_date(date1=None, date2=None):
    stats = db.session.query(Disease.name, count(ClinicalRecords.patient_id).label("count_di")).join(Disease, Disease.id == ClinicalRecords.disease_id)

    if date1:
        stats = stats.filter(ClinicalRecords.checked_date.__ge__(date1))

    if date2:
        stats = stats.filter(ClinicalRecords.checked_date.__le__(date2))

    return stats.group_by(ClinicalRecords.disease_id).all()
