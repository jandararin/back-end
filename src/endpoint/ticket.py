from fastapi import APIRouter, HTTPException
from model.data.ticket import Ticket, TicketDetail
from beanie import PydanticObjectId
from typing import List


ticketRouter = APIRouter()


@ticketRouter.get("/list", response_model=List[Ticket])
async def retrieve_ticket(
    # skip = 何件目のデータから取得するのか。デフォルトは0(最初から)
    skip: int = 0,
    # limit = データを取得する件数。デフォルト30
    limit: int = 30,
    # このパラメータが指定された際は、条件分岐する。
    userId: PydanticObjectId = None
):
    if (userId is None):
        # createAtの降順(最新順)でTicketのリストを返す
        return (
            await Ticket.find_all().skip(skip).limit(limit).sort(-Ticket.createdAt).to_list()
        )
    # userIDが指定されている場合
    else:
        # userIdでフィルタリングかつ、
        # createAtの降順(最新順)でTicketのリストを返す
        return (
            await Ticket.find_many({"authorUserId": userId}).sort(-Ticket.createdAt).skip(skip).limit(limit).to_list()
        )


@ticketRouter.post("", response_model=Ticket)
async def post_a_user(body: Ticket):
    await body.create()
    return body


# TicketDetailを返すと宣言(自動生成ドキュメントに反映される)
@ticketRouter.get("/detail", response_model=TicketDetail)
async def retrieve_ticket_and_replies(ticketId: PydanticObjectId):
    # チケットの情報を取得
    ticket = await Ticket.get(ticketId)
    # チケットの情報がないならエラー
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # リプライを全県取得
    replies = await Ticket.find_many({"referTicket": ticketId}).to_list()

    # TicketDetailにデータを当てはめる
    return TicketDetail(
        ticket=ticket,
        replies=replies
    )


@ticketRouter.patch("")
async def update_tcket(
    ticketId: PydanticObjectId,
    title: str = None,
    body: str = None
):
    # パラメータの存在確認
    # titleもbodyも未指定は、このAPIを通す意味がないのでエラー
    if (title is None and body is None):
        raise HTTPException(status_code=422, detail="bosy or title is required")
    # bodyがNoneでなく、bodyが空文字列の場合、エラーにする
    if (body is None):
        if (len(body) == 0):
            raise HTTPException(status_code=422, detail="body is required")
    ticket = await Ticket.get(ticketId)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # title、もしくはbodyの変更を反映する
    # 先程getしたデータを格納したticketのプロパティを
    # 直接変えるような書き方をする
    if (title is not None):
        ticket.title = title if len(title) != 0 else None
    if (body is not None):
        ticket.body = body
    # save_changes()で、変更したプロパティをDBに反映する
    await ticket.save_changes()
    return ticket
