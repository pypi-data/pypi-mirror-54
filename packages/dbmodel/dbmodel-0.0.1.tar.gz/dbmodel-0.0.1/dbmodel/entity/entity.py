#-*- coding: utf-8 -*-

__private_methods__ = ["toJSON", "toDB"]

from dbmodel.entity.datatype import *
from dbmodel.entity.status import EntityStatus
from dbmodel.utils.inflector import Inflector, Portugues

class Entity(object):

    def __init__(self, context=None, **kw):
        try:
            self.__context__ = context
            self.__commit__ = []
            self.__status__ = EntityStatus.created
            self.__table__ = Inflector(Portugues).tableize(self.__class__.__name__)
            filled = False
            for item in self.__dir__():
                if not item.startswith("__") and item not in __private_methods__:
                    self.__dict__["__%s"%item] = self.__getattribute__(item)
                    if self.__dict__["__%s"%item].name and not self.__dict__["__%s"%item].type:
                        self.__dict__["__%s"%item].type = getattr(__import__('model.{0}'.format(self.__dict__["__%s"%item].name.lower()), fromlist=[self.__dict__["__%s"%item].name]), self.__dict__["__%s"%item].name)
                    self.__dict__[item] = None if self.__dict__["__%s"%item].__class__.__name__ != "ObjectList" else ListType(context=self, type=self.__dict__["__%s"%item].type)
                    if item in kw:
                        filled = True
                        self.__setattr__(item, kw[item])
                        del kw[item]
                    elif "%s.%s"%(self.__table__,item) in kw:
                        filled = True
                        self.__setattr__(item, kw["%s.%s"%(self.__table__,item)])
                        del kw["%s.%s"%(self.__table__,item)]
            if len(kw) > 0:
                filled = True
                self.__setrelattr__(**kw)
            if self.__context__ and filled:
                self.__status__ = EntityStatus.filled
        except Exception as e:
            raise e

    def __setrelattr__(self, **kw):
        relation_kw = {item.split(".")[0]: {value[0].split(".")[1]:value[1] for value in kw.items() if item.split(".")[0] in value[0]} for item in sorted(kw) if "." in item and not "%s."%self.__table__ in item}
        for _table, _data in relation_kw.items():
            if self.__dict__["__%s"%_table].__class__.__name__ == "Object" or isinstance(_data, list):
                self.__setattr__(_table, _data)
            if self.__dict__["__%s"%_table].__class__.__name__ == "ObjectList" and isinstance(_data, dict):
                self.__setattr__(_table, [_data])

    def __setattr__(self, item, value):
        try:
            if not item.startswith("__"):
                if hasattr(self, "__%s"%item):
                    self.__status__ = EntityStatus.modified
                    field = self.__getattribute__("__%s"%item)
                    if field.type and field.__class__.__name__ is "ObjectList" and isinstance(value, list):
                        for item_list in value:
                            if isinstance(item_list, dict):
                                self.__dict__[item].append(field.type(context=self, **item_list))
                            if isinstance(item_list, field.type):
                                item_list.__context__ = self
                                self.__dict__[item].append(item_list)
                    else:
                        if field.type and isinstance(value, dict):
                            field.value = field.type(context=self, **value)
                        else:
                            if field.type and field.__class__.__name__ is "Object":
                                value.__context__ = self
                            field.value = value
                        self.__dict__[item] = field.value

                    if self.__context__:
                        object_exit = [obj for obj in self.__context__.__commit__ if all([getattr(obj, pk) == self.__dict__[pk] for pk in self.__primary_key__])]
                        if len(object_exit)==0:
                            self.__context__.__commit__.append(self)
                        else:
                            object_exit[0] = self
                else:
                    raise Exception("%s field does not exist"%item)
            else:
                super().__setattr__(item, value)
        except Exception as e:
            raise e

    def toJSON(self, encode=False):
        try:
            return {k: CustomEncoder(v, self.__getattribute__("__%s"%k), encode) if encode else v if not hasattr(v, "toJSON") else v.toJSON() for k, v in self.__dict__.items() if not k.startswith("__") and v is not None }
        except Exception as e:
            raise e

    def toDB(self):
        try:
            return {k: v for k, v in self.__dict__.items() if not k.startswith("__") and v is not None and not hasattr(v, "toJSON")}
        except Exception as e:
            raise e

def CustomEncoder(item, datatype, encode=False):
	try:
		if hasattr(item, "toJSON"):
			return item.toJSON(encode)
		if isinstance(item, decimal.Decimal):
			return float(item)
		if isinstance(item, datetime.datetime):
			return item.strftime("%d/%m/%Y %H:%M:%S")
		if isinstance(item, bytes):
			return item.decode('utf-8')
		return item
	except Exception as e:
		raise e
