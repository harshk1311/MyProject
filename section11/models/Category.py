from db import db

class CategoryModel(db.Model) :
    __tablename__ = 'categories'
    cid = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(80))

    def __init__ (self,cid,cname):
        self.cid=cid
        self.cname=cname
    
    def json(self):
        return{
            'cid':self.cid,
            'cname':self.cname
        }
    
    @classmethod 
    def find_by_name(cls,cname):
        cls.query.filter_by(cname=cname).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()


    def save_to_db(self) :
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

