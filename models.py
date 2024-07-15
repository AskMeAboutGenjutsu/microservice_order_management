from order_api_exception import OrderAPIException


class Order:
    def __init__(self, db, order_id=None, user_id=None, status=None, product_ids=None):
        self.db = db
        self.order_id = order_id
        self.user_id = user_id
        self.status = status
        self.product_ids = product_ids

    def validate(self):
        if self.user_id is None:
            raise OrderAPIException(f'Поле "user_id" не должно быть пустым')
        if not isinstance(self.user_id, int):
            raise OrderAPIException(f'Поле "user_id" должно иметь тип int')
        if self.product_ids is None:
            raise OrderAPIException(f'Поле "user_id" не должно быть пустым')
        if not isinstance(self.product_ids, list):
            raise OrderAPIException(f'Поле "product_ids" должно иметь тип список')
        if not all([isinstance(product_id, int) for product_id in self.product_ids]):
            raise OrderAPIException(f'Поле "product_ids" должно быть списком с элементами типа int')

    async def create(self):
        try:
            cursor = await self.db.execute(
                'insert into orders (user_id) values (?);',
                (self.user_id, )
            )
            await self.db.commit()
            self.order_id = cursor.lastrowid
            await cursor.close()
            order_ids = [self.order_id] * len(self.product_ids)
            cursor = await self.db.executemany(
                'insert into order_product_relationship (order_id, product_id) '
                'values (?, ?);', zip(order_ids, self.product_ids)
            )
            await self.db.commit()
            await cursor.close()
            return self.order_id
        except Exception as e:
            raise OrderAPIException(f'Не удалось сохранить данные в БД:\n{e}')

    async def get(self):
        cursor = await self.db.execute("""
        select orders.user_id, orders.status, order_product_relationship.product_id from orders
        join order_product_relationship on orders.order_id = order_product_relationship.order_id
        where orders.order_id = ?""", (self.order_id, ))
        data = await cursor.fetchall()
        self.user_id = data[0][0]
        self.status = data[0][1]
        self.product_ids = [data[i][2] for i in range(len(data))]
        await cursor.close()
        return

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'user_id': self.user_id,
            'status': self.status,
            'product_ids': self.product_ids
        }
