import uvicorn
from fastapi import FastAPI

from src.Users import router as auth_router
from src.Airports import router as airports_router
from src.Flights import router as flights_router

from database import engine, Base




app = FastAPI()



@app.get("/")
def read_root():
    return {"message": "http://127.0.0.1:8000/docs"}
# def get_profile(current_user: dict = Depends(get_current_user)):
#    username = current_user.get('sub')
#    if not username:
#        raise HTTPException(status_code=400, detail="Invalid token payload: 'sub' claim is missing")
#    return {"username": username}



Base.metadata.create_all(bind=engine)


# Incluir as rotas
app.include_router(auth_router.router, prefix="/users", tags=["users"])
app.include_router(airports_router.router, prefix="/airports", tags=["airports"])
app.include_router(flights_router.router, prefix="/flights", tags=["flights"])
# Iniciar a aplicação
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)