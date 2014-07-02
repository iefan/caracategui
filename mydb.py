# sqlalchemy.__version__ = 0.94

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:stcl@localhost:3306/cataract?charset=utf8",  echo=True)
Base = declarative_base()
# coding=utf8
# mydb.Base.metadata.create_all(mydb.engine) 创建数据表

class User(Base):
    """docstring for User"""
    __tablename__ = "users"

    id          = Column(Integer, primary_key=True)
    username    = Column(String(50))
    password    = Column(String(50))
    unitname    = Column(String(50))
    email       = Column(String(50))

    def __repr__(self):
        return "<User(username='%s', password='%s', unitname='%s', email='%s')>" % (
            self.username, self.password, self.unitname, self.email)

def test():
    # ed_user = User(username='ed', unitname='中国', password='edspassword', email="a@a.com")
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # session.add(ed_user)
    # our_user = session.query(User).filter_by(username='ed').first()
    # print(our_user)

    # session.add_all([
    #         User(username='wendy', unitname='Wendy Williams', password='foobar'),
    #         User(username='mary', unitname='Mary Contrary', password='xxg527'),
    #         User(username='fred', unitname='Fred Flinstone', password='blah')])
    # print(session.dirty)
    # ed_user.password = "123"
    # print(session.dirty)
    # print(session.new)
    # print("-------------------------")
    # session.commit()

    ed_user.username = "AAAAAAA"
    fake_user = User(username='fakeuser', unitname='Invalid', password='12345')
    session.add(fake_user)
    session.query(User).filter(User.username.in_(['AAAAAAA', 'fakeuser'])).all()
    session.rollback()
    print(ed_user.username)
    print(fake_user in session)

if __name__ == "__main__":
    #ed_user = User(name=’ed’, fullname=’Ed Jones’, password=’edspassword’)
    test()
