from django.db import models


class Warehouse(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class WarehouseItemCount(models.Model):
    item = models.ForeignKey('Item', on_delete=models.DO_NOTHING, related_name='stocks')
    warehouse = models.ForeignKey('Warehouse', on_delete=models.DO_NOTHING, related_name='stocks')
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.item} at {self.warehouse}'


class Item(models.Model):
    title = models.CharField(max_length=30)
    availability = models.ManyToManyField('Warehouse', through='WarehouseItemCount')

    def __str__(self):
        return self.title

    @staticmethod
    def get_warehouses_with_enough_items_quantity(item_id, min_qty):
        qs = WarehouseItemCount.objects.select_related(
            'warehouse'
        ).filter(
            item_id=item_id,
            count__gte=min_qty
        ).only('warehouse')
        return qs
