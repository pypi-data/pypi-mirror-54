from sqlalchemy import create_engine, MetaData, text
from contextlib import contextmanager


class Dict(dict):
    def __getattribute__(self, item):
        return object.__getattribute__(self, item)

    def __getattr__(self, item):
        if item not in self.keys():
            return None
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, item):
        del self[item]


class DB(object):

    def __init__(self, e):
        self.engine = e
        self.connection = self.engine.connect()

    @contextmanager
    def session(self):
        work = self.connection.begin()
        tables = MetaData(bind=self.engine, reflect=True).tables
        try:
            connection = Connection(self.connection, tables)
            yield connection
            work.commit()
        except Exception as e:
            work.rollback()

    def query_one(self, s, session=None, **kwargs):
        if session:
            return session.query_one(s, **kwargs)
        with self.session() as session:
            return session.query_one(s, **kwargs)

    def query_page(self, s, session=None, **kwargs):
        if session:
            return session.query_page(s, **kwargs)
        with self.session() as session:
            return session.query_page(s, **kwargs)

    def query(self, s, session=None, **kwargs):
        if session:
            return session.query(s, **kwargs)
        with self.session() as session:
            return session.query(s, **kwargs)

    def add(self, t, d, session=None):
        if session:
            return session.add(t, d)
        with self.session() as session:
            return session.add(t, d)

    def update(self, t, d, session=None):
        if session:
            return session.update(t, d)
        with self.session() as session:
            return session.update(t, d)

    def delete(self, t, d, session=None):
        if session:
            return session.delete(t, d)
        with self.session() as session:
            return session.delete(t, d)

    def execute(self, s, session=None, **kwargs):
        if session:
            return session.execute(s, **kwargs)
        with self.session() as session:
            return session.execute(s, **kwargs)


class Connection(object):

    def __init__(self, sa_con, tables):
        self.sa_on = sa_con
        self.tables = tables

    def query_one(self, s, **kwargs):
        rs = self._query(s, **kwargs)
        try:
            return next(rs)
        except StopIteration:
            return None

    def query(self, s, **kwargs):
        rs = self._query(s, **kwargs)
        return list(rs)

    def query_page(self, s, page=1, limit=20, **kwargs):
        s = s + f" limit {int(limit)} offset {int(page) - 1}"
        rs = self._query(s, **kwargs)
        return list(rs)

    def add(self, t, d):
        t = self._check_table(t, d)
        rs = self._execute(t.insert(), **d)
        p = dict()
        for k, v in zip(t.primary_key, rs.inserted_primary_key):
            p[k.name] = v
        p.update(d)
        return p

    def delete(self, t, d):
        t = self._check_table(t, d)
        t, p = self._check_primary(t, d)
        s = t.delete().where(t.c[p.name] == d[p.name])
        return self._execute(s)

    def update(self, t, d):
        t = self._check_table(t, d)
        t, p = self._check_primary(t, d)
        s = t.update().where(t.c[p.name] == d[p.name]).values(d)
        return self._execute(s)

    def execute(self, s, **kwargs):
        return self._execute(s, **kwargs)

    def _check_table(self, t, d):
        if t not in self.tables:
            raise Exception(f"Not found table '{t}'!")
        if not isinstance(d, dict):
            raise Exception(f"Data must be dict-like!")

        return self.tables[t]

    @classmethod
    def _check_primary(cls, t, d):

        if not len(t.primary_key) == 1:
            raise Exception("Primary length must be 1 !")

        for p in t.primary_key:
            if p.name in d.keys():
                return t, p
        else:
            raise Exception(f"Miss primary key !")

    def _execute(self, s, **kwargs):
        rs = self.sa_on.execute(s, **kwargs)
        return rs

    def _query(self, s, **kwargs):
        rs = self.sa_on.execute(text(s), **kwargs)
        col = rs.keys()

        def to_dict(row):
            r = Dict()
            for k, v in zip(col, row):
                r[k] = v
            return r

        return (to_dict(row) for row in rs)
