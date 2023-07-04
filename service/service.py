from flask import flash
from model.entity import *
from DB import db, query


class UserService:

    def get_user_by_id(self, id):
        users = query(User).filter(User.id == id).one_or_none()
        return users

    def get_user_by_email(self, email):
        user = query(User).filter(User.user_email == email).one_or_none()
        return user

    def query_signature_by_id(self, id):
        user = self.get_user_by_id(id)
        return user.user_signatue

    def user_register(self, user):
        new_user = self.get_user_by_email(user.user_email).one_or_none()
        if new_user != None:
            return 0
        elif new_user.email != None:
            new_user.name = new_user.email.split('@')[0]
            db.session.add(new_user)
            db.session.commit()
            flash("Register succeed!")
            return user.id

    def user_modify(self, user):
        store_user = self.get_user_by_id(user.id)
        if user.user_name:
            store_user.user_name = user.user_name
        if user.gender:
            store_user.gender = user.gender
        if user.user_signature:
            store_user = user.user_signature
        if user.user_picture:
            store_user.user_picture = user.user_picture
        db.session.commit()
        flash("Modify succeed!")

    def password_modify(self, user, password):
        user = self.get_user_by_id(user.id)
        user.password = password
        db.session.commit()
        print("Modify succeed!")

    def get_all_user(self):
        users = query(User).order_by(User.id).all()
        return users


class BillService():

    def add_bill(self, bill):
        user = query(User).filter(User.id == bill.user_id).one_or_none()
        if user:
            user.total_cost += bill.transaction_amount
            if user.total_cost >= 1:
                user.vip = 1
            db.session.add(bill)
            db.session.commit()
            flash(f"交易成功,{user.user_name}")
            print("add a bill")
        else:
            print("there is error in create_bill")


    def get_bills(self, user=None, id=None):
        if user:
            bills = query(Bill).filter(Bill.user_id == user.id).order_by(Bill.bill_date)
        elif id:
            bills = query(Bill).filter(Bill.id == id).order_by(Bill.bill_date)
        else:
            bills = None
        return bills


# class User_logService:
#
#     def add_log(self, ):


