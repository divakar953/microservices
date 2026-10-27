from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.requests import Request
from fastapi.background import BackgroundTasks
import redis, requests, time

class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_password: str

    model_config = SettingsConfigDict(env_file="../.env")

settings = Settings() #type: ignore
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

#this should be a different database - microservices should not share the same database
r = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    username="default",
    password=settings.redis_password,
    decode_responses=True
)

class Order(HashModel, index=True):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str # pending, completed, refunded

    class Meta:
        database = r

@app.get("/orders/{pk}")
def get_order(pk: str):
    return Order.get(pk)

@app.post("/orders")
async def create_order(request: Request, background_tasks: BackgroundTasks): 
    # we need only id and quantity from the request body, so we can use the Order model to validate the request body
    body = await request.json()

    req = requests.get("http://localhost:8000/products/%s" % body['id'])
    product = req.json()

    order = Order(
        product_id=body["id"],
        price=product["price"],
        fee=0.2*product["price"],
        total=1.2*product["price"],
        quantity=body["quantity"],
        status="pending"
    )
    order.save()

    background_tasks.add_task(order_completed, order)

    return order


def order_completed(order: Order):
    time.sleep(5) # simulating a long running task, like processing a payment
    order.status = "completed"
    order.save()
    r.xadd('order_completed', order.model_dump(), '*')


