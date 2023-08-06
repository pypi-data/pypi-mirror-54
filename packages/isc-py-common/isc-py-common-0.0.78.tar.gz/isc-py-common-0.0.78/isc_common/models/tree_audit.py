import logging

from django.db.models.query import RawQuerySet

from isc_common.models.audit import AuditManager, AuditQuerySet

logger = logging.getLogger(__name__)


class TreeAuditModelQuerySet(AuditQuerySet):
    def delete(self):
        return super().delete()

    def create(self, **kwargs):
        return super().create(**kwargs)

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class TreeAuditModelManager(AuditManager):

    def get_descendants(self, id='id', limit=None, child_id='child_id', parent_id='parent_id', include_self=True) -> RawQuerySet:
        db_name = self.model._meta.db_table

        res = super().raw(f'''WITH RECURSIVE r AS (
                            SELECT *, 1 AS level
                            FROM {db_name}
                            WHERE {child_id if include_self else parent_id} = %s or %s is null

                            union all

                            SELECT {db_name}.*, r.level + 1 AS level
                            FROM {db_name}
                                JOIN r
                            ON {db_name}.{parent_id} = r.{child_id})

                        select * from r limit %s
                        ''', [id, id, limit])
        return res

    def get_descendants_count(self, id='id', limit=None, child_id='child_id', parent_id='parent_id', include_self=True) -> int:
        return len(self.get_descendants(id=id, limit=limit, child_id=child_id, parent_id=parent_id, include_self=include_self))

    def get_queryset(self):
        return TreeAuditModelQuerySet(self.model, using=self._db)


