from flask_admin.babel import lazy_gettext
from flask_admin.contrib.sqla import ModelView, filters
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla.filters import BaseSQLAFilter
from flask_admin.contrib.sqla.filters import *
from flask_admin.model.filters import BaseFilter
from flask_login import current_user, logout_user
from flask import redirect, request
from sqlalchemy import func

from hospital.models import Assistant, Policy, Patient, Medicine, Time, Books, ClinicalRecords, Disease, Question, Advisory, ReceiptDetails, Receipt
from hospital import db, admin

from flask_appbuilder.charts.views import DirectByChartView
from flask_appbuilder.models.sqla.interface import SQLAInterface

import utils

class PolyModel(ModelView):
    excluded_form_columns = ('type',)

    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class DoctorModelView(PolyModel):
    can_export = True


class AssistantModelView(PolyModel):
    can_export = True

class QuestionModelView(AuthenticatedView):
    can_export = True

class AdvisoryModelView(AuthenticatedView):
    can_export = True

class PolicyModelView(AuthenticatedView):
    can_export = True


class MedicineModelView(AuthenticatedView):
    can_export = True


class PatientModelView(AuthenticatedView):
    can_export = True


class TimeModelView(AuthenticatedView):
    can_export = True


class ClinicalRecordsModelView(AuthenticatedView):
    can_export = True

class ReceiptDetailsModelView(AuthenticatedView):
    can_export = True

class ReceiptModelView(AuthenticatedView):
    can_export = True

class ListBookView(AuthenticatedView):
    can_edit = False
    can_create = False
    can_delete = False

    # column_searchable_list = ('booked_date',)
    column_filters = ('booked_date',)

class BookModelView(AuthenticatedView):
    can_export = True


class DiseaseModelView(AuthenticatedView):
    can_export = True

class OderView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/oderMedicine.html")

    def is_accessible(self):
        return current_user.is_authenticated

class InformationView1(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/profileAdmin.html")

    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

class AllDetailsModelView(BaseView):
    @expose("/")
    def index(self):
        detail = utils.get_all_detail()
        return self.render("admin/oderMedicine.html", detail=detail)

    def is_accessible(self):
        return current_user.is_authenticated

class StatsView(BaseView):
    @expose("/")
    def index(self):
        date1 = request.args.get("date_start")
        date2 = request.args.get("date_end")
        stats = utils.get_stats_by_date(date1=date1, date2=date2)
        if stats:
            mes = "co du lieu"
            return self.render("admin/stats.html", stats=stats, mes=mes)
        else:
            mes = "chua co du lieu"
            return self.render("admin/stats.html", stats=stats, mes=mes)

    def is_accessible(self):
        return current_user.is_authenticated

class GetDetailView(BaseView):
    @expose("/")
    def index(self):
        name = request.args.get("namepatient")
        getDetail = utils.get_name_receipt_detail(name)
        if getDetail:
            mes = "co du lieu"
            return self.render("admin/receiptDetail.html", getDetail=getDetail, mes=mes)
        else:
            mes = "chua co du lieu"
            return self.render("admin/receiptDetail.html", getDetail=getDetail, mes=mes)

    def is_accessible(self):
        return current_user.is_authenticated

admin.add_view(TimeModelView(Time, db.session, name="Thoi gian"))
admin.add_view(MedicineModelView(Medicine, db.session, name="Danh sach thuoc", category='Danh sách'))
admin.add_view(PatientModelView(Patient, db.session, name="Danh sach benh nhan", category='Danh sách'))
admin.add_view(AssistantModelView(Assistant, db.session, name="Danh sach nhân viên", category='Danh sách'))
admin.add_view(ListBookView(Books, db.session, name="Danh sach dat lich", endpoint='ListBooks', category='Danh sách'))
admin.add_view(ClinicalRecordsModelView(ClinicalRecords, db.session, name="Nhập bệnh", endpoint="Record", category='Khám bệnh'))
admin.add_view(ReceiptModelView(Receipt, db.session, name="Chọn bác sĩ", category='Khám bệnh'))
admin.add_view(ReceiptDetailsModelView(ReceiptDetails, db.session, name="Lấy thuốc", category='Khám bệnh'))

admin.add_view(AllDetailsModelView(name="Hóa Đơn", category="Khám bệnh"))
admin.add_view(GetDetailView(name="Chi tiết hóa đơn", category="Khám bệnh"))

admin.add_view(QuestionModelView(Question, db.session, name="Câu hỏi", category='Q&A'))
admin.add_view(AdvisoryModelView(Advisory, db.session, name="Trả lời", category='Q&A'))
admin.add_view(PolicyModelView(Policy, db.session, name="Quy dinh"))
admin.add_view(DiseaseModelView(Disease, db.session, name="Loại bệnh"))
admin.add_view(BookModelView(Books, db.session, name="Book"))
admin.add_view(StatsView(name="Bao cao thang", category="Statistics"))
admin.add_view(InformationView1(name="ProfileAd", endpoint='Information1', category='Profile'))
admin.add_view(LogoutView(name="Dang xuat", endpoint='Logout', category='Profile'))




