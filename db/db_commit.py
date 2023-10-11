from db.database import SessionLocal, engine
from sqlalchemy.orm import sessionmaker
from db import models

from datetime import datetime






# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class StatiscticCommit:
    count = 0
    all_count = 0
    # Session = sessionmaker(bind=engine)
    # db = Session()

    @staticmethod
    def commit():
        # StatiscticCommit.db.commit()
        ...

    @staticmethod
    def update(statistic,balance):
        Session = sessionmaker(bind=engine)
        db = Session()
        obj = db.query(models.Statistic).filter_by(id=statistic.id).first()
        obj.updated_at = datetime.now()
        obj.balance = balance
        StatiscticCommit.count += 1
        StatiscticCommit.all_count += 1

        db.commit()
        # if StatiscticCommit.count >= 10:
        #     StatiscticCommit.count = 0
        #     db.commit()
        #     print(StatiscticCommit.all_count)
        #     # StatiscticCommit.db.flush()
        db.close()
        # obj = StatiscticCommit.db.query(models.Statistic).filter_by(id=statistic.id).first()
        # obj.updated_at = datetime.now()
        # obj.balance = balance
        # StatiscticCommit.count += 1

        # if StatiscticCommit.count >= 100:
        #     StatiscticCommit.count = 0
        #     StatiscticCommit.db.commit()
        #     # StatiscticCommit.db.flush()
