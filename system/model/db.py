from sqlalchemy import Table, Column, Integer, String, BLOB, MetaData, create_engine
engine = create_engine('sqlite:///college.db', echo=True)
meta = MetaData()





