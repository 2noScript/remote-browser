from sqlalchemy import create_engine, Column, Integer, String,JSON,Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///database.db", echo=True)

_Session = sessionmaker(bind=engine)
_session = _Session()

Base = declarative_base()

class BrowserDB(Base):
    __tablename__ = 'browser'
    id = Column(Integer, primary_key=True)
    identify = Column(String(40), unique=True)
    config = Column(JSON)
    is_running = Column(Boolean, default=False)

    @classmethod
    async def create(cls, identify: str, config: dict):
        browser = cls(identify=identify, config=config)
        _session.add(browser)
        _session.commit()
        return browser

    @classmethod
    async def get(cls, identify: str):
        return _session.query(cls).filter_by(identify=identify).first()

    @classmethod
    async def get_all(cls):
        return _session.query(cls).all()

    @classmethod
    async def update(cls, identify: str, config: dict={},is_running:bool=False):
        browser = await cls.get(identify)
        if browser:
            browser.config = {**browser.config, **config} 
            browser.is_running = is_running
            _session.commit()
            return browser
        return None
    @classmethod
    async def delete(cls, identify: str):
        browser = await cls.get(identify)
        if browser:
            _session.delete(browser)
            _session.commit()
            return True
        return False


class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True)



def init_database():
    Base.metadata.create_all(engine)
