# -*- coding: utf-8 -*-
from sqlalchemy import func

from flask.ext.sqlalchemy import BaseQuery

from cocoa.extensions import db
from .consts import ColumnType

class ShelfQuery(BaseQuery):

    def check_columns(self, book):
        from .models import ColumnHave, ColumnRead, ColumnReading, \
            ColumnWish, ColumnLike

        in_columns = []
        not_in_columns = []

        result = db.session.query(
                ColumnHave.id.label('have'),
                ColumnRead.id.label('read'),
                ColumnReading.id.label('reading'),
                ColumnWish.id.label('wish'),
                ColumnLike.id.label('like')).\
             outerjoin(ColumnRead,
                ColumnHave.book_id==ColumnRead.book_id).\
             outerjoin(ColumnReading,
                ColumnHave.book_id==ColumnReading.book_id).\
             outerjoin(ColumnWish,
                ColumnHave.book_id==ColumnWish.book_id).\
             outerjoin(ColumnLike,
                ColumnHave.book_id==ColumnLike.book_id).\
             filter(ColumnHave.book==book).\
             filter(ColumnReading.finished_timestamp==None).\
             first()

        if result is None:
            not_in_columns = [x for x in ColumnType]
        else:
            for k in result.keys():
                if result.__dict__[k] is not None:
                    in_columns.append(ColumnType.from_name(k))
                else:
                    not_in_columns.append(ColumnType.from_name(k))

        return in_columns, not_in_columns

    def book_count(self, shelf_id):
        from .models import ColumnHave, ColumnRead, ColumnReading, \
            ColumnWish, ColumnLike
        
        have = ColumnHave.query.filter_by(shelf_id=shelf_id).count()
        read = ColumnRead.query.filter_by(shelf_id=shelf_id).count()
        reading = ColumnReading.query.filter_by(shelf_id=shelf_id).\
                    filter_by(finished_timestamp=None).count()
        wish = ColumnWish.query.filter_by(shelf_id=shelf_id).count()
        like = ColumnLike.query.filter_by(shelf_id=shelf_id).count()

        return {
            'have':     have,
            'read':     read,
            'reading':  reading,
            'wish':     wish,
            'like':     like,
        }
