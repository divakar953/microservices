from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel, NotFoundError
from pydantic_settings import BaseSettings, SettingsConfigDict
import redis

class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_password: str

    model_config = SettingsConfigDict(env_file="../.env")

# can either do type: ignore or add default values to host, port, password in Settings class above
settings = Settings() #type: ignore
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

r = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    username="default",
    password=settings.redis_password,
    decode_responses=True
)

class Product(HashModel, index=True):
    name: str
    price: float
    quantity: int

    # To connect this model to redis database
    class Meta:
        database = r

@app.get("/products")
def all_products():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)
    
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }

@app.post("/products")
def create_product(product: Product):
    return product.save()

@app.get("/products/{pk}")
def get_product(pk: str):
    return Product.get(pk)

@app.delete("/products/{pk}")
def delete_product(pk: str):
    return Product.delete(pk)