import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class World_rus(Base):
    __tablename__ = "world_rus"

    id = sq.Column(sq.Integer, primary_key=True)
    translate = sq.Column(sq.String(length=40), unique=True)
    part_speech = sq.Column(sq.String(length=40), unique=False)
    target_word = sq.Column(sq.String(length=40), unique=True)

class User(Base):
    __tablename__ = "user"

    id = sq.Column(sq.Integer, primary_key=True)
    name_user = sq.Column(sq.String(length=40), unique=False)

class World_user(Base):
    __tablename__ = "world_user"


    id = sq.Column(sq.Integer, primary_key=True)
    id_world_rus = sq.Column(sq.Integer, sq.ForeignKey("world_rus.id"), nullable=False)
    # course = relationship(Course, back_populates="homeworks")
    world_rus = relationship(World_rus, backref="world_user")
    id_name_user = sq.Column(sq.Integer, sq.ForeignKey("user.id"), nullable=False)
    # course = relationship(Course, back_populates="homeworks")
    name_user = relationship(User, backref="world_user")





def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def creation_obj():
    # создание объектов
    translate_world1 = World_rus(translate="Мир", part_speech = "сущ.", target_word="Peace")
    name_user1 =  User(name_user= None)
    print(translate_world1.id)
    world_user1 = World_user(world_rus=translate_world1, name_user= name_user1)


    session.add(translate_world1)
    session.add(name_user1)
    session.add(world_user1)
    session.commit()  # фиксируем изменения

    translate_world2 = World_rus(translate="Машина", part_speech = "сущ.", target_word="Car")
    world_user2 = World_user(world_rus=translate_world2, name_user=name_user1)


    session.add(translate_world2)
    session.add(world_user2)
    session.commit()  # фиксируем изменения


    translate_world3 = World_rus(translate="Небо", part_speech="сущ.",target_word="Sky")
    world_user3 = World_user(world_rus=translate_world3, name_user=name_user1)

    session.add(translate_world3)
    session.add(world_user3)

    session.commit()  # фиксируем изменения


    translate_world4 = World_rus(translate="Красный", part_speech="сущ.", target_word="Red")
    world_user4 = World_user(world_rus=translate_world4, name_user=name_user1)

    session.add(translate_world4)
    session.add(world_user4)

    session.commit()  # фиксируем изменения


    translate_world5 = World_rus(translate="Серый", part_speech="сущ.",target_word="Grey")
    world_user5 = World_user(world_rus=translate_world5, name_user=name_user1)

    session.add(translate_world5)
    session.add(world_user5)
    session.commit()  # фиксируем изменения


    translate_world6 = World_rus(translate="Стол", part_speech="сущ.", target_word="Table")
    world_user6 = World_user(world_rus=translate_world6, name_user=name_user1)

    session.add(translate_world6)
    session.add(world_user6)
    session.commit()  # фиксируем изменения


    translate_world7 = World_rus(translate="Мяч", part_speech="сущ.", target_word="Ball")
    world_user7 = World_user(world_rus=translate_world7, name_user=name_user1)

    session.add(translate_world7)
    session.add(world_user7)

    session.commit()  # фиксируем изменения


    translate_world8 = World_rus(translate="Собака", part_speech="сущ.", target_word="Dog")
    world_user8 = World_user(world_rus=translate_world8, name_user=name_user1)

    session.add(translate_world8)
    session.add(world_user8 )

    session.commit()  # фиксируем изменения


    translate_world9 = World_rus(translate="Мы", part_speech="сущ.", target_word="We")
    world_user9 = World_user(world_rus=translate_world9, name_user=name_user1)
    session.add(translate_world9)
    session.add(world_user9)

    session.commit()  # фиксируем изменения


    translate_world10 = World_rus(translate="Мама", part_speech="сущ.", target_word="Mother")
    world_user10 = World_user(world_rus=translate_world10, name_user=name_user1)
    session.add(translate_world10)
    session.add(world_user10)

    session.commit()  # фиксируем изменения


def del_obj():

    # удаление объектов
    session.query(World_user).delete()
    session.commit()  # фиксируем изменения

    session.query(User).delete()
    session.commit()  # фиксируем изменения

    session.query(World_rus).delete()
    session.commit()  # фиксируем изменения



if __name__ == "__main__":
    DSN = "postgresql://postgres:pslocalhost:5432/netology_bd"
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)

    # сессия
    Session = sessionmaker(bind=engine)
    session = Session()
    creation_obj()
    #del_obj()





    session.commit()  # фиксируем изменения

    session.close()