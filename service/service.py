from flask import flash
import os
from model.entity import *
from DB import db, query


class UserService:

    def get_user_by_id(self, id):
        users = query(User).filter(User.id == id).one_or_none()
        return users

    def get_user_id_by_email(self, email):
        id = query(User.id).filter(User.user_email == email).one_or_none()
        return id

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
            # with open('data/ml-1m/users.dat', 'a') as f:
            #     f.write(f'{new_user.id}::F::20::15::02460')
            #     print('6666666')
            flash("Register succeed!")
            return user.id

    def user_modify(self, id, sex, name, sign, picture):
        store_user = self.get_user_by_id(id)
        if name:
            store_user.user_name = name
        if sex:
            store_user.user_gender = sex
        if sign:
            store_user.user_signature = sign
        if picture:
            print(type(picture), '\n', picture)
        db.session.commit()
        flash("Modify succeed!")

    def password_modify(self, user, password):
        user = self.get_user_by_id(user.id)
        user.password = password
        db.session.commit()
        print("Modify succeed!")

    def get_all_user(self):
        users = query(User).filter(True).order_by(User.id)
        return users


# class BillService:
#
#     def add_bill(self, bill):
#         user = query(User).filter(User.id == bill.user_id).one_or_none()
#         if user:
#             user.total_cost += bill.transaction_amount
#             if user.total_cost >= 1:
#                 user.vip = 1
#             db.session.add(bill)
#             db.session.commit()
#             flash(f"交易成功,{user.user_name}")
#             print("add a bill")
#         else:
#             print("there is error in create_bill")
#
#
#     def get_bills(self, user=None, id=None):
#         if user:
#             bills = query(Bill).filter(Bill.user_id == user.id).order_by(Bill.bill_date).all()
#         elif id:
#             bills = query(Bill).filter(Bill.id == id).order_by(Bill.bill_date).all()
#         else:
#             bills = None
#         return bills


# class User_logService:
#
#     def add_log(self, ):




class CommentService:

    def add_comment(self, user_id, content, music_id):
        print('begin')
        new_comment = Comment(user_id=user_id, content=content, music_id=music_id)
        print('end')
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






class MusicService:

    def get_all(self):
        return query(Music.id).all()

    #根据名字查询歌曲
    def get_music_by_name(self, name):
        musics = query(Music.id).filter(Music.music_name.like('%' + name + '%')).all()
        return musics

    def search_musicname(self, name):
        '''
        返回音乐名字，用于搜索提示
        :param name:
        :return: top 7 the matched the name
        '''
        music_name = query(Music.music_name).filter(Music.music_name.like('%'+name+'%')).all()
        return music_name[0:7]

    def get_all_by_id(self, id):
        temp = self.get_music_by_id(id)
        if temp == None:
            print(f"Not found the music by the music id: {id}")
            return {}
        musician_name = MusicianService.get_musician_by_id(temp.musician_id).name
        tags = TagService.get_music_tag(id)
        #tags = ";".join(tags)
        music = {
            "music_id": str(id),
            "music_name": temp.music_name,
            "musician_name": musician_name,
            "music_lyric": temp.lyric,
            "album_name": temp.album_name,
            "music_picture": temp.picture,
            #"Tags": tags
        }
        return music

    def get_music_by_musician_id(self, id_li):
        if id_li == []:
            return []
        musics = []
        for id in id_li:
            musics += query(Music).filter(Music.musician_id == id).all()
        return musics

    #根据id查询歌曲
    def get_music_by_id(self, id):
        music = query(Music).filter(Music.id == id).one_or_none()
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

    def get_music_by_albmu_name(self, name):
        musics = query(Music).filter(Music.album_name == name).all()
        return musics



class MusicianService:

    #按id查询
    def get_musician_by_id(self, id):
        musician = query(Musician).filter(Musician.id == id).order_by(Musician.id).one_or_none()
        return musician

    def get_musician_id_by_name(self, name):
        '''
        返回一个实例列表
        :param name:
        :return:
        '''
        musician = query(Musician.id).filter(Musician.name.like('%' + name + '%')).order_by(Musician.name).all()
        return musician


    def search_the_musicianname(self, name):
        '''
        返回一个列表的前7个，来用于搜索提示
        :param name:
        :return:top 7 of the matched name
        '''
        musician_names = query(Musician).filter(Musician.name.like('%'+name+'%')).order_by(Musician.name).all()
        return musician_names[0:7]

    #修改图片
    def change_picture(self, musician):
        new_musician = self.get_musician_by_id(musician.id)
        new_musician.music_picture = musician.music_picture
        db.session.commit()


class CollectService:

    # 获取该用户的所有收藏音乐
    def get_collection_by_userid(self, user_id):
        temp = query(Collect).filter(Collect.user_id == user_id).order_by(Collect.id).all()
        collections = []
        Music = MusicService
        Musician = MusicianService
        for col in temp:
            music = Music.get_music_by_id(col.music_id)
            collections += [{
                "music_id": music.id,
                "music_name": music.music_name,
                "musician_name": Musician.get_musician_by_id(music.musician_id).name,
                "album": music.album_name
            }]
        return collections

    def get_collection_by_music_user(self, user_id, music_id):
        collections = query(Collect).filter(Collect.user_id == user_id and Collect.music_id == music_id)
        return collections

    def add_music(self, user_id, music_id):
        one_collection = self.get_collection_by_music_user(user_id, music_id).one_or_none()
        if one_collection:
            flash("You have collected this music")
        else:
            flash("Add succeed!")
            db.session.add(one_collection)
            db.session.commit()

    def delete_collection(self, user_id, music_id):
        collections = self.get_collection_by_music_user(user_id, music_id)
        if collections:
            flash("Delete succeed!")
            db.session.delete(collections)
            db.session.commit()
        else:
            flash("You have not collect the music!")


class TagService:

    def get_music_tag(self, music_id):
        tags = query(Tag).filter(Tag.music_id == music_id).all()
        return tags

    def if_in(self, music_id, tag_name):
        tag = query(Tag).filter(Tag.music_id == music_id and Tag.tag_name == tag_name)
        if tag:
            return True
        else:
            return False

    def add_tag(self, music_id, tag_name):
        if not self.if_in(music_id, tag_name):
            tag = Tag(tag_name=tag_name, music_id=music_id)
            db.session.add(tag)
            db.session.commit()
            return 1
        else:
            print("The music already have this tag!")
            return 0

UserService = UserService()
MusicService = MusicService()
MusicianService = MusicianService()
TagService = TagService()
CollectService = CollectService()
CommentService = CommentService()
# BillService = BillService()
