
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from API.schemas import CheckIMEI
from imei_checker.check_imei import check_imei


app = FastAPI(title='API CheckIMEI')


@app.post("/api/check-imei")
async def handle_message(request: CheckIMEI):
    """Обрабатывает запрос на проверку IMEI.
       Args:
           request (CheckIMEI): Запрос с токеном и IMEI.
       Raises:
           HTTPException: Если возникает ошибка при проверке IMEI.
       Returns:
           JSONResponse: Ответ с результатами проверки IMEI.
       """
    try:
        response = check_imei(token_api=request.token, imei=request.imei)
    except HTTPException as e:
        print(f"Ошибка - {e}")
    return JSONResponse(content=response.json())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

