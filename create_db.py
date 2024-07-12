import sqlite3

connection = sqlite3.connect('orders_data.db')
cursor = connection.cursor()
cursor.executescript("""
create table user (
user_id integer primary key autoincrement,
name text not null,
email text not null);

create table orders (
order_id integer primary key autoincrement,
user_id integer not null,
status text not null check (status in ('accepted', 'delivery', 'finalised')) default 'accepted',
foreign key (user_id) references user (user_id));

create table product (
product_id integer primary key autoincrement,
description text not null,
price real not null);

create table order_product_relationship (
order_product_relationship_id integer primary key autoincrement,
order_id integer not null,
product_id integer not null,
foreign key (order_id) references orders (order_id),
foreign key (product_id) references product (product_id));
""")
connection.commit()
connection.close()
