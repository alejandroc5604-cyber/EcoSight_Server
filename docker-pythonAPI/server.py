import sqlite3
import uuid
import datetime
#setup the API for the interface website thing
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import uvicorn #type:ignore

data_path = "data/database.sql"
write_lock = asyncio.Lock()



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/BuildDatabase")
async def SetupDatabase():
    try:   
        async with write_lock: 
            print("Building database")
            connection = sqlite3.connect(data_path)
            cursor = connection.cursor()
            #cursor.execute("DROP TABLE IF EXISTS found_trash;")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS found_trash (
                    ID TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    date REAL NOT NULL,
                    confidence_score REAL NOT NULL,
                    image_path TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL
                )
            """)

            connection.commit()
            connection.close()
            return ("Success", None)
    except Exception as e:
        return ("Failed", str(e))
    

@app.get("/AddToDatabase")
async def AddToDatabase(Type:str, confidence_score:float, image_path:str, latitude:float, longitude:float):
    try:
        async with write_lock:
            connection = sqlite3.connect(data_path)
            cursor = connection.cursor()

            ID = str(uuid.uuid4())

            # timestamp in seconds
            date = datetime.datetime.now().timestamp()

            data = [
                ID,
                str(Type),
                float(date),
                float(confidence_score),
                str(image_path),
                float(latitude),
                float(longitude),
            ]

            cursor.execute("""
                INSERT INTO found_trash
                (ID, type, date, confidence_score, image_path, latitude, longitude)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, data)

            connection.commit()
            connection.close()
        return ("Success", None)
    except Exception as e:
        return ("Failed", str(e))

@app.get("/ReturnJSONData")
async def ReturnJSONData(limit:int | None) -> tuple:
    try:
        async with write_lock:
            connection = sqlite3.connect(data_path)
            cursor = connection.cursor()

            if limit is None:
                result = cursor.execute("""
                    SELECT ID, type, date, confidence_score, image_path
                    FROM found_trash
                    ORDER BY date DESC
                """).fetchall()
            else:
                result = cursor.execute("""
                    SELECT ID, type, date, confidence_score, image_path
                    FROM found_trash
                    ORDER BY date DESC
                    LIMIT ?
                """, (limit,)).fetchall()

            connection.close()
            return_data = {"FoundData": []}
            for ID, trash_type, date, confidence_score, image_path in result:
                    return_data["FoundData"].append({
                        "ID": ID,
                        "type": trash_type,
                        "date": date,
                        "confidence_score": confidence_score,
                        "image_path": image_path
                    })
            return ("Success", return_data)
    except Exception as e:
        return ("Failed", str(e))

async def tester_main():
    import random

    await SetupDatabase()

    for i in range(100):
        print("\033[A\033[2K", end="")
        print("\033[A\033[2K", end="")
        print(i)

        choice = random.choice(["plastic","metal","paper","glass"])

        result = await AddToDatabase(
            choice,
            random.randint(1, 10000) / 100,
            "Database",
            -1.2864, 
            36.8172
        )
        print(result)

    data = await ReturnJSONData(None)
    print(data)
    if data[0] != "Failed":
        for item in data[1]["FoundData"]:
            print(f"ID: {item['ID']} type: {item['type']} date: {item['date']} confidence_score: {item['confidence_score']}")
    else:
        print(data[1])


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    #asyncio.run(tester_main())