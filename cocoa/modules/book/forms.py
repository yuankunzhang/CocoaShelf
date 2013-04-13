# -*- coding: utf-8 -*-
from flask.ext.wtf import TextField, IntegerField, \
     TextAreaField, DateField, FileField, SelectField, \
     FloatField, Required, ValidationError

from cocoa.helpers.wtf import Form, DictField
from .consts import Currency, Binding
from .models import Book

def book_not_exist():
    message = u'这本书已经存在'

    def _check(form, field):
        book = Book.query.get_by_isbn(field.data)
        if book is not None:
            raise ValidationError(message)

    return _check


class BookAddForm(Form):

    isbn = TextField(u'ISBN', [
        Required(message=u'必填'),
        book_not_exist(),
    ], id=u'book-isbn', description=u'10位或13位isbn号')

    cover = FileField(u'封面', id=u'book-cover')

    title = TextField(u'书名', [
        Required(message=u'必填'),
    ], id=u'book-title')

    subtitle = TextField(u'副标题', id=u'book-subtitle')
    orititle = TextField(u'原作名', id=u'book-orititle')

    author = DictField(u'作者', [
        Required(message=u'必填'),
    ], id=u'book-publisher', description=u'使用英文逗号作为分隔符')

    translator = DictField(u'译者',
        id=u'book-translator', description=u'使用英文逗号作为分隔符')

    publisher = TextField(u'出版社', [
        Required(),
    ], id=u'book-publisher')

    pubdate = DateField(u'出版日期', format='%Y-%m-%d',
        id=u'book-publisher')

    price = FloatField(u'定价', [
        Required(message=u'必填'),
    ], id=u'book-price')

    currency = SelectField(u'货币类型', choices=[
        (Currency.CNY.value, Currency.CNY.text),
        (Currency.USD.value, Currency.USD.text),
    ], coerce=int, default=Currency.CNY.value, id=u'book-currency')

    binding = SelectField(u'装帧', choices=[
        (Binding.PAPERBACK.value, Binding.PAPERBACK.text),
        (Binding.HARDCOVER.value, Binding.HARDCOVER.text),
    ], coerce=int, default=Binding.PAPERBACK.value, id=u'book-binding')

    pages = IntegerField(u'页码', [
    ], id=u'book-pages')

    summary = TextAreaField(u'内容简介', id=u'book-summary')
    author_intro = TextAreaField(u'作者简介', id=u'book-author-intro')
