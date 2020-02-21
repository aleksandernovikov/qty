from django.db.models import Sum, Q, Count
from django.test import TestCase

from app.models import Warehouse, Item, WarehouseItemCount


class TestApp(TestCase):
    fixtures = ['app']

    def test_sum(self):
        min_qty = 3
        wh_info = Item.get_warehouses_with_enough_items_quantity(
            item_id=1,
            min_qty=min_qty
        )
        print(wh_info.query)
        """
        SELECT 
            "app_warehouseitemcount"."id", 
            "app_warehouseitemcount"."warehouse_id", 
            "app_warehouse"."id", 
            "app_warehouse"."title" 
        FROM 
            "app_warehouseitemcount" 
        INNER JOIN 
            "app_warehouse" 
        ON 
            ("app_warehouseitemcount"."warehouse_id" = "app_warehouse"."id") 
        WHERE 
            ("app_warehouseitemcount"."count" >= 3 AND "app_warehouseitemcount"."item_id" = 1)
        """
        wh_info = wh_info.annotate(all_qty=Sum('count'))
        print(wh_info.query)
        """
        SELECT 
            "app_warehouseitemcount"."id", 
            "app_warehouseitemcount"."warehouse_id", 
            SUM("app_warehouseitemcount"."count") AS "all_qty", 
            "app_warehouse"."id", "app_warehouse"."title" 
        FROM 
            "app_warehouseitemcount" 
        INNER JOIN 
            "app_warehouse" 
        ON 
            ("app_warehouseitemcount"."warehouse_id" = "app_warehouse"."id") 
        WHERE 
            ("app_warehouseitemcount"."count" >= 3 AND "app_warehouseitemcount"."item_id" = 1) 
        GROUP BY 
            "app_warehouseitemcount"."id", "app_warehouseitemcount"."warehouse_id", "app_warehouse"."id", "app_warehouse"."title"
        """

    def test_aggregate(self):
        count_gte_min_qty = Sum('count', filter=Q(count__gte=3))

        qs = WarehouseItemCount.objects.aggregate(
            all_qty=count_gte_min_qty
        )
        print(qs)
