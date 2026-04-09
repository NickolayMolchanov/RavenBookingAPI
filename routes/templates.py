from fastapi import APIRouter, Request, Depends, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Hotel, Room

templates_router = APIRouter(prefix="/pages",tags=["templates"])
templates = Jinja2Templates(directory="templates")

@templates_router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="base.html")

@templates_router.get("/index", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@templates_router.get("/hotels-list", response_class=HTMLResponse)
async def get_hotels(
    request: Request,
    search: str | None = None,
    country: str | None = None,
    sort: str | None = None,
    page: int = 1,
    per_page: int = 20,
    session: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * per_page
    query = select(Hotel).offset(offset).limit(per_page)

    if search:
        query = query.where(Hotel.name.ilike(f"%{search}%"))

    if country:
        query = query.where(Hotel.country == country)

    if sort == "name":
        query = query.order_by(Hotel.name.asc())


    result = await session.execute(query)
    hotels = result.scalars().all()

    count_result = await session.execute(select(Hotel))
    total = len(count_result.scalars().all())
    total_pages = (total + per_page - 1) // per_page


    return templates.TemplateResponse(
        "hotels.html",
        {
            "request": request,
            "hotels": hotels,
            "search": search,
            "country": country,
            "page": page,
            "total_pages": total_pages,
        }
    )

@templates_router.get("/hotels-list/{hotel_id}", response_class=HTMLResponse)
async def hotel_detail(
        request: Request,
        hotel_id: int,
        sort: str | None = None,
        session: AsyncSession = Depends(get_db)
):
    hotel_result = await session.execute(select(Hotel).where(Hotel.id == hotel_id))
    hotel = hotel_result.scalar_one_or_none()
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")

    query = select(Room).where(Room.hotel_id == hotel_id)

    if sort == "price_asc":
        query = query.order_by(Room.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Room.price.desc())

    result = await session.execute(query)
    rooms = result.scalars().all()

    return templates.TemplateResponse(
        "hotel_detail.html",
        {
            "request": request,
            "hotel": hotel,
            "rooms": rooms,
        }
    )