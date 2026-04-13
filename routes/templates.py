from fastapi import APIRouter, Request, Depends, status, HTTPException, Query, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from collections import defaultdict
from starlette.responses import RedirectResponse

from core.security import verify_password, create_access_token
from database import get_db
from models import Hotel, Room, User


templates_router = APIRouter(prefix="/pages",tags=["templates"])
templates = Jinja2Templates(directory="templates")

@templates_router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="base.html")

@templates_router.get("/index", response_class=HTMLResponse)
async def home(request: Request, session: AsyncSession = Depends(get_db)):
    result = await session.execute(
        select(Hotel.country, Hotel.city).distinct()
    )
    data = result.all()
    countries = defaultdict(list)
    for country, city in data:
        if city not in country:
            countries[country].append(city)

    countries_sorted = dict(
        sorted(
            {
                country: sorted(cities)
                for country, cities in countries.items()
            }.items()
        )
    )
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "countries": countries_sorted,
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

@templates_router.get("/hotels-list", response_class=HTMLResponse)
async def hotels_search(
        request: Request,
        q: str = Query(None, alias="search"),
        city: str = Query(None),
        sort: str = Query(None),
        page: int = 1,
        per_page: int = 20,
        session: AsyncSession = Depends(get_db),
):

    offset = (page - 1) * per_page
    result = await session.execute(
        select(Hotel.country, Hotel.city).distinct()
    )
    data = result.all()

    countries = defaultdict(list)

    for c, ct in data:
        if ct not in countries[c]:
            countries[c].append(ct)

    countries_sorted = dict(
        sorted(
            {
                c: sorted(cities)
                for c, cities in countries.items()
            }.items()
        )
    )

    filters = []

    if city:
        filters.append(Hotel.city == city)

    if q:
        search = f"%{q}%"
        filters.append(
            or_(
                Hotel.name.ilike(search),
                Hotel.description.ilike(search),
                Hotel.address.ilike(search),
            )
        )

    stmt = select(Hotel)
    count_stmt = select(func.count(Hotel.id))

    if filters:
        stmt = stmt.where(*filters)
        count_stmt = count_stmt.where(*filters)

    total = (await session.execute(count_stmt)).scalar()
    total_pages = (total + per_page - 1) // per_page

    stmt = stmt.offset(offset).limit(per_page)

    result = await session.execute(stmt)
    hotels = result.scalars().all()

    return templates.TemplateResponse(
        "hotels.html",
        {
            "request": request,
            "hotels": hotels,
            "search": q,
            "selected_city": city,
            "sort": sort,
            "countries": countries_sorted,
            "page": page,
            "total_pages": total_pages,
        }
    )

@templates_router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@templates_router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@templates_router.post("/register", response_class=HTMLResponse)
async def register(
        request: Request,
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        password2: str = Form(...),
        session: AsyncSession = Depends(get_db),
):
    if password != password2:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Пароли не совпадают", "email": email}
        )

    existing = await session.execute(
        select(User).where(User.email == email)
    )

    if existing.scalar_one_or_none():
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Пользователь с таким Email уже существует", "email": email}
        )

    user = User(
        username=username,
        email=email,
        hashed_password=password,
    )

    session.add(user)
    await session.commit()

    return RedirectResponse("/pages/login", status_code=status.HTTP_303_SEE_OTHER)

@templates_router.post("/login", response_class=HTMLResponse)
async def login(
        request: Request,
        email: str = Form(...),
        password: str = Form(...),
        session: AsyncSession = Depends(get_db),
):
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Неверный пароль или почтовый ящик",
                "email": email,

            }
        )

    token = create_access_token({"sub": str(user.id)})

    response = RedirectResponse("/pages/index", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
    )

    return response