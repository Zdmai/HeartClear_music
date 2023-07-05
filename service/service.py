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




class CommentService:

    def add_comment(self, user_id, content, music_id):
        new_comment = Comment(user_id=user_id, content=content, music_id=music_id)
        db.session.add(new_comment)
        db.session.commit()
        print("评论添加成功")

    def delete_comment(self, comment_id):
        comment_to_delete = Comment.query.filter(Comment.id == comment_id).first()
        if comment_to_delete:
            db.session.delete(comment_to_delete)
            db.session.commit()
            print("评论删除成功")
        else:
            print("找不到要删除的评论")

    # def get_comment_by_user_and_movie(self, user_id, movie_id):
    #     comments = query(Comment).filter(Comment.user_id == user_id, Comment.movie_id == movie_id).all()
    #     if comments:
    #         for comment in comments:
    #             print(f"评论：{comment.content}")
    #     else:
    #         print("找不到评论")

    def get_comment_by_music_id(self, music_id):
        '''
        :param music_id:
        :return: A list of the comment of that music
        '''
        comments = query(Comment).filter(Comment.music_id == music_id).order_by(Comment.comment_date)
        return comments






class MusicService():

    #根据名字查询歌曲
    def get_music_by_name(self, name):
        musics = query(Music).filter(name in Music.music_name).all()
        return musics

    def search_musicname(self, name):
        '''
        返回音乐名字，用于搜索提示
        :param name:
        :return: top 7 the matched the name
        '''
        music_name = query(Music.music_name).filter(name in Music.music_name).all()
        return list(music_name)[0:7]

    #根据id查询歌曲
    def get_music_by_id(self, id):
        music = query(Music).filter(Music.id == id).order_by(Music.id).one_or_none()
        return music

    #添加歌曲
    def add_music(self, music):
        one_music = self.get_music_by_name(music.id).one_or_none()
        if one_music:
            return 0
        else:
            db.session.add(music)
            db.session.commit()
            return '添加成功'

    #修改歌曲信息
    def update_music(self, music):
        one_music = self.get_music_by_id(music.id)
        one_music.music_name = music.music_name
        db.session.commit()



class MusicianService():

    #按id查询
    def get_musician_by_id(self, id):
        musician = query(Musician).filter(Musician.id == id).order_by(Musician.id)
        return musician

    def get_musician_by_name(self, name):
        '''
        返回一个实例列表
        :param name:
        :return:
        '''
        musician = query(Musician).filter(name in Musician.name).order_by(Musician.name).all()
        return musician

    def search_the_musicianname(self, name):
        '''
        返回一个列表的前7个，来用于搜索提示
        :param name:
        :return:top 7 of the matched name
        '''
        musician_names = query(Musician).filter(name in Musician.name).order_by(Musician.name)
        return list(musician_names)[0:7]

    #修改图片
    def change_picture(self, musician):
        new_musician = self.get_musician_by_id(musician.id)
        new_musician.music_picture = musician.music_picture
        db.session.commit()


class CollectService():

    def get_collection_by_id(self, user_id):
        collection = query(Collect).filter(Collect.user_id == user_id).order_by(Collect.id).one_or_none()
        return collection


    def add_music(self, music):
        one_collection = self.get_collection_by_id(music.id)
        if one_collection:
            flash("You have collected this music")
            return 0
        else:
            db.session.add(one_collection)
            db.session.commit()

    def delete_collection(self, collection):
        db.session.delete(collection)
        db.session.commit()