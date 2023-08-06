import logging

from isc_common.models.base_ref import BaseRefManager, BaseRefQuerySet, BaseRef

logger = logging.getLogger(__name__)


class Status_launchQuerySet(BaseRefQuerySet):
    def delete(self):
        return super().delete()

    def create(self, **kwargs):
        return super().create(**kwargs)

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class Status_launchManager(BaseRefManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'description': record.description,
        }
        return res

    def get_queryset(self):
        return Status_launchQuerySet(self.model, using=self._db)


class Status_launch(BaseRef):
    objects = Status_launchManager()

    def __str__(self):
        return f"ID:{self.id}, code: {self.code}, name: {self.name}, description: {self.description}"

    class Meta:
        verbose_name = 'Статусы запусков'
