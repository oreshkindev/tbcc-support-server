from service.schema.ticket import TicketDetailsModel, TicketModel
from service.schema.user import User
from service.util import user as user_util
from service.util import ticket as ticket_util
from service.util.dependencies import get_current_user
from service.util.websocket import manager as manager
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.post(
    "", response_model=TicketDetailsModel, status_code=201, name="create ticket"
)
async def create_ticket(
    ticket: TicketModel, current_user: User = Depends(get_current_user)
):
    ticket = await ticket_util.create_ticket(ticket)
    return ticket


@router.get("")
async def get_tickets(page: int = 1, current_user: User = Depends(get_current_user)):
    total_cout = await ticket_util.get_tickets_count()
    ticket = await ticket_util.get_tickets(page)
    return {"total_count": total_cout, "results": ticket}


@router.get("/{ticket_id}", response_model=TicketDetailsModel, name="get ticket by id")
async def get_ticket(ticket_id: int, current_user: User = Depends(get_current_user)):
    return await ticket_util.get_ticket(ticket_id)


@router.put("/{ticket_id}", response_model=TicketDetailsModel)
async def update_ticket(
    ticket_id: int, ticket: TicketModel, current_user: User = Depends(get_current_user)
):
    ticket = await ticket_util.update_ticket(ticket_id, ticket)

    await manager.broadcast([ticket])

    return ticket


@router.delete("/{from_id}", name="remove ticket by id")
async def delete_tickets(from_id: int, current_user: User = Depends(get_current_user)):

    await ticket_util.delete_tickets(from_id)
    await user_util.update_user_stats(current_user["id"])

    # return all tickets from ticket_util
    tickets = await ticket_util.get_tickets(page=1)
    await manager.broadcast(tickets)