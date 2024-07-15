from order_api_exception import OrderAPIException


# класс - интерфейс работы с бд sqlite
class Order:
    def __init__(self, db, order_id=None, user_id=None, status=None, product_ids=None):
        self.db = db
        self.order_id = order_id
        self.user_id = user_id
        self.status = status
        self.product_ids = product_ids

    # проверка данных на корректность
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

    # проверка данных на корректность перед обновлением статуса заказа
    def validate_before_update(self):
        if self.status is None:
            raise OrderAPIException(f'Поле "status" не должно быть пустым')
        if not isinstance(self.status, str):
            raise OrderAPIException(f'Поле "status" должно иметь тип int')
        statuses = ('accepted', 'delivery', 'finalised')
        if self.status not in statuses:
            raise OrderAPIException(f'Поле "status" должно быть одним из следующих значений:\n{statuses}')

    # создание записи в БД
    async def create(self):
        try:
            # запись данных в таблицу заказов
            cursor = await self.db.execute(
                'insert into orders (user_id) values (?);',
                (self.user_id, )
            )
            await self.db.commit()
            self.order_id = cursor.lastrowid
            await cursor.close()
            order_ids = [self.order_id] * len(self.product_ids)
            # запись данных в таблицу отношений заказов и продуктов
            cursor = await self.db.executemany(
                'insert into order_product_relationship (order_id, product_id) '
                'values (?, ?);', zip(order_ids, self.product_ids)
            )
            await self.db.commit()
            await cursor.close()
            return self.order_id
        except Exception as e:
            raise OrderAPIException(f'Не удалось сохранить данные в БД:\n{e}')

    # выдача данных о заказе из БД
    async def read(self):
        try:
            # запрос данных из таблицы заказов, а также данных о продуктов в заказе
            cursor = await self.db.execute("""
            select orders.user_id, orders.status, order_product_relationship.product_id from orders
            join order_product_relationship on orders.order_id = order_product_relationship.order_id
            where orders.order_id = ?""", (self.order_id, ))
            data = await cursor.fetchall()
            await cursor.close()
            self.user_id = data[0][0]
            self.status = data[0][1]
            self.product_ids = [data[i][2] for i in range(len(data))]
            return self.order_id
        except Exception as e:
            raise OrderAPIException(f'Не удалось найти данные в БД:\n{e}')

    # обновление статуса заказа в БД
    async def update(self):
        try:
            cursor = await self.db.execute(
                'update orders set status = ? where order_id = ?;', (self.status, self.order_id)
            )
            await self.db.commit()
            await cursor.close()
            return self.order_id
        except Exception as e:
            raise OrderAPIException(f'Не удалось обновить данные в БД:\n{e}')

    # формирование словаря из данных о заказе
    def to_dict(self):
        data = {
            'order_id': self.order_id,
            'user_id': self.user_id,
            'status': self.status,
            'product_ids': self.product_ids
        }
        return {k: v for k, v in data.items() if v is not None}
