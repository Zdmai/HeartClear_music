from model.entity import *
from DB import db, query


class UerService:

    def get_user_by_id(self, id):
        user = query(User).filter_by(id=id).one_or_none()
        return user

    def get_user_by_email(self, email):
        user = query(User).filter_by(user_email=email).one_or_none()
        return user

    def user_register(self, user):
        new_user = self.get_user_by_email(user.user_email).one_or_none()
        if new_user != None:
            return 0
        else:
            db.session.add()
            db.session.commit()
            return user.id


