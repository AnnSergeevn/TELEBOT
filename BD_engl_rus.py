import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class World_rus(Base):
    __tablename__ = "world_rus"

    id = sq.Column(sq.Integer, primary_key=True)
    translate = sq.Column(sq.String(length=40), unique=True)
    part_speech = sq.Column(sq.String(length=40), unique=False)

class World_engl(Base):
    __tablename__ = "world_engl"

    id = sq.Column(sq.Integer, primary_key=True)
    target_word = sq.Column(sq.String(length=40), unique=True)
    id_world_rus = sq.Column(sq.Integer, sq.ForeignKey("world_rus.id"), nullable=False)
    # course = relationship(Course, back_populates="homeworks")
    world_rus = relationship(World_rus, backref="world_engl")



class Add_world(Base):
    __tablename__ = "add_world"

    id = sq.Column(sq.Integer, primary_key=True)
    add_world = sq.Column(sq.String(length=40), unique=True)

class Add_trans_world(Base):
    __tablename__ = "add_trans_world"

    id = sq.Column(sq.Integer, primary_key=True)
    target_add_word = sq.Column(sq.String(length=40), unique=True)
    id_add_world = sq.Column(sq.Integer, sq.ForeignKey("add_world.id"), nullable=False)
    # course = relationship(Course, back_populates="homeworks")
    add_world = relationship(Add_world, backref="add_trans_world")

def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def creation_obj():
    # создание объектов
    translate_world1 = World_rus(translate="Мир", part_speech = "сущ.")
    new_add_world1 = Add_world(add_world="Мышь")
    new_add_trans_world1 = Add_trans_world(target_add_word="Mouse", add_world=new_add_world1)
    engl_translate_world1 = World_engl(target_word="Peace", world_rus=translate_world1)
    print(translate_world1.id)


    session.add(translate_world1)
    session.add(new_add_world1)
    session.add(new_add_trans_world1)
    session.add(engl_translate_world1)

    session.commit()  # фиксируем изменения

    translate_world2 = World_rus(translate="Машина", part_speech = "сущ.")
    engl_translate_world2 = World_engl(target_word="Car", world_rus=translate_world2)
    print(translate_world2.id)


    session.add(translate_world2)
    session.add(engl_translate_world2)

    session.commit()  # фиксируем изменения


    translate_world3 = World_rus(translate="Небо", part_speech="сущ.")
    engl_translate_world3 = World_engl(target_word="Sky", world_rus=translate_world3)
    print(translate_world3.id)


    session.add(translate_world3)
    session.add(engl_translate_world3)

    session.commit()  # фиксируем изменения


    translate_world4 = World_rus(translate="Красный", part_speech="сущ.")
    engl_translate_world4 = World_engl(target_word="Red", world_rus=translate_world4)
    print(translate_world4.id)


    session.add(translate_world4)
    session.add(engl_translate_world4)

    session.commit()  # фиксируем изменения


    translate_world5 = World_rus(translate="Серый", part_speech="сущ.")
    engl_translate_world5 = World_engl(target_word="Grey", world_rus=translate_world5)
    print(translate_world5.id)


    session.add(translate_world5)
    session.add(engl_translate_world5)

    session.commit()  # фиксируем изменения


    translate_world6 = World_rus(translate="Стол", part_speech="сущ.")
    engl_translate_world6 = World_engl(target_word="Table", world_rus=translate_world6)
    print(translate_world6.id)


    session.add(translate_world6)
    session.add(engl_translate_world6)

    session.commit()  # фиксируем изменения


    translate_world7 = World_rus(translate="Мяч", part_speech="сущ.")
    engl_translate_world7 = World_engl(target_word="Ball", world_rus=translate_world7)
    print(translate_world7.id)


    session.add(translate_world7)
    session.add(engl_translate_world7)

    session.commit()  # фиксируем изменения


    translate_world8 = World_rus(translate="Собака", part_speech="сущ.")
    engl_translate_world8 = World_engl(target_word="Dog", world_rus=translate_world8)
    print(translate_world8.id)


    session.add(translate_world8)
    session.add(engl_translate_world8)

    session.commit()  # фиксируем изменения


    translate_world9 = World_rus(translate="Мы", part_speech="сущ.")
    engl_translate_world9 = World_engl(target_word="We", world_rus=translate_world9)
    print(translate_world9.id)


    session.add(translate_world9)
    session.add(engl_translate_world9)

    session.commit()  # фиксируем изменения


    translate_world10 = World_rus(translate="Мама", part_speech="сущ.")
    engl_translate_world10 = World_engl(target_word="Mother", world_rus=translate_world10)
    print(translate_world10.id)


    session.add(translate_world10)
    session.add(engl_translate_world10)

    session.commit()  # фиксируем изменения


def del_obj():

    # удаление объектов
    session.query(Add_world).delete()
    session.commit()  # фиксируем изменения

    session.query(World_engl).delete()
    session.commit()  # фиксируем изменения

    session.query(World_rus).delete()
    session.commit()  # фиксируем изменения



if __name__ == "__main__":
    DSN = "postgresql://postgres:post@localhost:5432/netology_bd"
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)

    # сессия
    Session = sessionmaker(bind=engine)
    session = Session()
    creation_obj()
    #del_obj()





    session.commit()  # фиксируем изменения

    session.close()