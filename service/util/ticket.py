from datetime import datetime

from service.db.database import database
from service.model.ticket import ticket_table
from service.schema import ticket as ticket_schema
from sqlalchemy import desc, func, select


async def create_ticket(ticket: ticket_schema.TicketModel):
    query = (
        ticket_table.insert()
        .values(
            first_name=ticket.first_name,
            last_name=ticket.last_name,
            username=ticket.username,
            from_id=ticket.from_id,
            to_id=ticket.to_id,
            content=ticket.content,
            status=ticket.status,
            created_at=datetime.now(),
        )
        .returning(
            ticket_table.c.id,
            ticket_table.c.first_name,
            ticket_table.c.last_name,
            ticket_table.c.username,
            ticket_table.c.from_id,
            ticket_table.c.to_id,
            ticket_table.c.content,
            ticket_table.c.status,
            ticket_table.c.created_at,
        )
    )
    ticket = await database.fetch_one(query)

    # Convert to dict and add user_name key to it
    ticket = dict(zip(ticket, ticket.values()))
    return ticket


async def get_ticket(ticket_id: int):
    query = (
        select(
            [
                ticket_table.c.id,
                ticket_table.c.first_name,
                ticket_table.c.last_name,
                ticket_table.c.username,
                ticket_table.c.from_id,
                ticket_table.c.to_id,
                ticket_table.c.content,
                ticket_table.c.status,
                ticket_table.c.created_at,
            ]
        )
        .select_from(ticket_table)
        .where(ticket_table.c.id == ticket_id)
    )
    return await database.fetch_one(query)


async def get_tickets(page: int):
    max_per_page = 100
    offset1 = (page - 1) * max_per_page
    query = (
        select(
            [
                ticket_table.c.id,
                ticket_table.c.first_name,
                ticket_table.c.last_name,
                ticket_table.c.username,
                ticket_table.c.from_id,
                ticket_table.c.to_id,
                ticket_table.c.content,
                ticket_table.c.status,
                ticket_table.c.created_at,
            ]
        )
        .select_from(ticket_table)
        .order_by(desc(ticket_table.c.created_at))
        .limit(max_per_page)
        .offset(offset1)
    )
    return await database.fetch_all(query)


async def get_tickets_count():
    query = select([func.count()]).select_from(ticket_table)
    return await database.fetch_val(query)


async def update_ticket(ticket_id: int, ticket: ticket_schema.TicketModel):

    query = (
        ticket_table.update()
        .where(ticket_table.c.id == ticket_id)
        .values(
            from_id=ticket_table.c.from_id,
            to_id=ticket_table.c.to_id,
            status=ticket.status,
            created_at=ticket_table.c.created_at,
        )
        .returning(
            ticket_table.c.id,
            ticket_table.c.first_name,
            ticket_table.c.last_name,
            ticket_table.c.username,
            ticket_table.c.from_id,
            ticket_table.c.to_id,
            ticket_table.c.content,
            ticket_table.c.status,
            ticket_table.c.created_at,
        )
    )
    ticket = await database.fetch_one(query)

    # Convert to dict and add user_name key to it
    ticket = dict(zip(ticket, ticket.values()))
    return ticket


async def delete_tickets(from_id: str):
    query = ticket_table.delete().where(from_id == ticket_table.c.from_id)
    return await database.execute(query)