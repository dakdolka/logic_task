from fastapi import HTTPException
from sqlalchemy import text, insert, select, func, cast, Integer, and_, update
# from db.models import metadata_obj
from sqlalchemy.orm import aliased
from sqlalchemy.orm import joinedload, selectinload, contains_eager
from data.database import Base, async_engine, async_session_factory
from data.models import Info, OrdderConstructor, Order, pack
import pandas as pd


class Orm:
    @staticmethod
    async def create_all():
        async with async_engine.begin() as conn:
            async_engine.echo = False
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            print('tables created')
            
            async_engine.echo = True
    
    @staticmethod
    async def insert_or_upd_info(info):
        async with async_session_factory() as session:
            async_engine.echo = False
            info = info[['Наименование', 'Артикул', 'Упаковка высота (мм)', "Упаковка длина (см)", "Упаковка ширина (см)", "УПАКОВКА FBO (Общие)" ]]
            data = info.values.tolist()
            dop = []
            for i in range(len(data)):
                # print(data[i])
                # exit()
                if not pd.isna(data[i][1]):
                    data[i] = {
                        'id': data[i][1] ,
                        'name': data[i][0] if not pd.isna(data[i][0]) else '0',
                        'h': data[i][2] if not pd.isna(data[i][2]) else 0,
                        'w': data[i][4] if not pd.isna(data[i][4]) else 0,
                        'l': data[i][3] if not pd.isna(data[i][3]) else 0,
                        'is_packed': pack(data[i][5])
                    }
                    dop.append(data[i])
            data = dop
            temp_inf = await session.execute(select(Info.id))
            temp_inf = temp_inf.scalars().all()
            cnt = 0
            dop = []
            for row in data:
                # print(row)
                if row['id'] in dop and (row['id'] == 'insp' or row['id'] == 'sh' or row['id'] == 0 or row['id'] == '23362' or row['id'] == '11332' or row['id'] == 'sf1'):
                    # raise HTTPException(status_code=400, detail="В номенклатуре присутствуют повторяющиеся артикулы")
                    continue
                if row['id'] in temp_inf:
                    await session.execute(update(Info).where(Info.id == row['id']).values(**row))
                    dop.append(row['id'])
                else:
                    await session.execute(insert(Info).values(**row))
                    dop.append(row['id'])
            await session.commit()
            async_engine.echo = True
            
    @staticmethod
    async def insert_order(order):
        async with async_session_factory() as session:
            async_engine.echo = False
            order = order[['Артикул', 'Количество', 'Сумма с НДС']]
            order_id = await session.execute(func.count(Order.id))
            order_id = order_id.scalar() + 1
            await session.execute(insert(Order).values({'id': order_id}))
            await session.flush()
            data = order.values.tolist()
            for i in range(len(data)):
                data[i] = {
                    'order_id': order_id,
                    'info_id': data[i][0],
                    'amount': data[i][1],
                    'price': data[i][2]
            } 
            temp_inf = await session.execute(select(Info.id))
            temp_inf = temp_inf.scalars().all()
            print(temp_inf)
            for row in data:
                print(row)
                if row['info_id'] in temp_inf:
                    await session.execute(insert(OrdderConstructor).values(row))
            await session.commit()
            async_engine.echo = True
            return order_id
            
    
    
    @staticmethod
    async def calc_time_and_volume(order_id):
        async with async_session_factory() as session:
            query = (
                select(OrdderConstructor).where(OrdderConstructor.order_id == order_id).options(
                    selectinload(OrdderConstructor.info))
                )
            result = await session.execute(query)
            result = result.scalars().all()
            summ = 0
            #TODO объём считается так, а часы: 100л/ч - упаковка т.е. если товар упаковываемый - на него тратится время сверх, 200л/ч - сборка
            #в эксельке выводить товар: описание артикул, количество - габариты, литраж если есть, если нет - красным
            for row in result:
                summ += (row.info.h * row.info.w * row.info.l) * row.amount
            return (summ // 1000)
            
            
            