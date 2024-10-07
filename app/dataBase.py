from tortoise import Tortoise, run_async

async def init():
    await Tortoise.init(
        db_url="sqlite://database.db",  
        modules={"models": ["app.models"]} 
    )
    
    await Tortoise.generate_schemas()

async def close():
    await Tortoise.close_connections()

# run_async 进行测试
if __name__ == "__main__":
    run_async(init())

