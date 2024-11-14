from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Create a new API endpoint from a db.json file
@app.get("/db")

def get_db():
    data = json.load(open("db.json"))
    # Return the contents of the file
    return data

@app.get("/status")

def get_general_config():
    data = json.load(open("general_config.json"))
    return data

@app.get("/monitoring_data")
def get_monitoring_data():
    data = json.load(open("monitoring.json"))
    return data

@app.post("/personal-config")
async def post_personal_config(request: Request):
    try:
        data = await request.json()
        with open("personal_config.json", "w") as file:
            json.dump(data, file)
        return {"message": "Personal configuration saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/serial-debug")
def get_debug_serial():
    data = json.load(open("serial_debug.json"))
    return data

@app.delete("/personal-config")
def delete_status():
    with open("personal_config.json", "w") as file:
        json.dump({}, file)
    return {"message": "Status deleted successfully"}

@app.get("/protocols/mqtt")
async def get_protocols():
    data = json.load(open("protocols_mqtt.json"))
    return data

@app.put("/protocols/mqtt")
async def put_protocols(request: Request):
    try:
        data = await request.json()
        with open("protocols_mqtt.json", "w") as file:
            json.dump(data, file)
        return {"message": "Protocols saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/protocols/modbus")
async def get_protocols_modbus():
    data = json.load(open("protocols_modbus.json"))
    return data

@app.put("/protocols/modbus")
async def put_protocols_modbus(request: Request):
    try:
        data = await request.json()
        with open("protocols_modbus.json", "w") as file:
            json.dump(data, file)
        return {"message": "Protocols saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/firm-update")
async def post_firm_update(request: Request):
    print(await request.form())
    try:
        form = await request.form()
        file = form.get("file")
        
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
        
        if not file.filename.endswith(".bin"):
            raise HTTPException(status_code=400, detail="Only .bin files are allowed")
        
        file_location = f"./firmware/{file.filename}"
        
        with open(file_location, "wb") as f:
            f.write(await file.read())
        
        return {"message": "Firmware update started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)