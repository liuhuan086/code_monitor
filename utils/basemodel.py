# encoding: utf-8

from django.db import models
from django.db.models import Q


class TimestampMixin(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BasicMethodMixin(models.Model):
    VALID = True
    INVALID = False

    status = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True

    @classmethod
    def all(cls):
        return cls.objects.filter(status=cls.VALID).all()

    @classmethod
    def new(cls, fields):
        return cls.objects.create(**fields)

    @classmethod
    def get(cls, id):
        return cls.objects.filter(id=id, status=cls.VALID).first()

    @classmethod
    def mget(cls, ids):
        if not ids:
            return []
        return cls.objects.filter(id__in=ids, status=cls.VALID).all()

    @classmethod
    def _gen_condition(cls, key_value_dict):
        conditions = []
        for key, value in key_value_dict.items():
            item = {}
            if isinstance(value, (list, tuple, set)):
                search_key = key + '__in'
                item[search_key] = value
                conditions.append(Q(**item))
            elif isinstance(value, dict):
                for _key, _value in value.items():
                    item = {}
                    if _key == '>':
                        search_key = key + '__gt'
                    elif _key == '>=':
                        search_key = key + '__gte'
                    elif _key == '<':
                        search_key = key + '__lt'
                    elif _key == '<=':
                        search_key = key + '__lte'
                    else:
                        raise ValueError
                    item[search_key] = value
                    conditions.append(Q(**item))
            else:
                item[key] = value
                conditions.append(Q(**item))
        return conditions

    @classmethod
    def mget_by(cls, key_value_dict, order_by=None, asc=True):
        conditions = cls._gen_condition(key_value_dict)
        conditions.append(Q(status=cls.VALID))
        q = cls.objects.filter(*conditions)
        if order_by:
            q = q.order_by(getattr(cls, order_by).asc() if asc else getattr(cls, order_by).desc())
        return q.all()

    @classmethod
    def mget_by_exclude(cls, key_value_dict, exclude_dict, order_by=None, asc=True):
        conditions = cls._gen_condition(key_value_dict)
        conditions.append(Q(status=cls.VALID))
        ex_conditions = cls._gen_condition(exclude_dict)
        q = cls.objects.filter(*conditions).exclude(*ex_conditions)
        if order_by:
            q = q.order_by(getattr(cls, order_by).asc() if asc else getattr(cls, order_by).desc())
        return q.all()

    @classmethod
    def mget_by_offset_limit(cls, key_value_dict, offset, limit, order_by=None, asc=True):
        """list must at first in Q"""
        conditions = cls._gen_condition(key_value_dict)
        conditions.append(Q(status=cls.VALID))
        offset = int(offset)
        limit = int(limit)
        q = cls.objects.filter(*conditions)
        if order_by:
            q = q.order_by(getattr(cls, order_by).asc() if asc else getattr(cls, order_by).desc())
        return q.count(), q.all()[offset:offset+limit]

    @classmethod
    def get_by(cls, key_value_dict):
        conditions = cls._gen_condition(key_value_dict)
        conditions.append(Q(status=cls.VALID))
        return cls.objects.filter(*conditions).first()

    def set_invalid(self):
        self.status = self.INVALID
        self.save()
