
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import hashlib
import json

app = FastAPI(title="AyurChain Backend", description="Blockchain-based Botanical Traceability System API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (use database in production)
users = {}
batches = {}
products = []
chain = []

# Models
class User(BaseModel):
    name: str
    role: str  # collector, processor, lab, manufacturer

class Batch(BaseModel):
    id: str
    herbName: str
    collector: str
    qty: float
    unit: str
    lat: float
    lng: float
    notes: str
    stage: str  # collected, processing, testing, certified, formulated, failed
    collectedAt: str
    processingLogs: List[dict] = []
    labResults: Optional[dict] = None
    productId: Optional[str] = None

class Product(BaseModel):
    id: str
    batchId: str
    herbName: str
    name: str
    form: str
    size: int
    expiry: Optional[str] = None
    mfr: str
    geo: str
    collector: str
    active: float
    createdAt: str
    qrData: str

class Block(BaseModel):
    index: int
    ts: str
    data: dict
    prevHash: str
    hash: str

# Helper functions
def hash_data(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def add_block(data):
    prev_hash = chain[-1].hash if chain else "0" * 64
    ts = datetime.utcnow().isoformat()
    block_data = {"type": data.get("type"), **data}
    block_hash = hash_data({"data": block_data, "ts": ts, "prevHash": prev_hash})
    block = Block(
        index=len(chain),
        ts=ts,
        data=block_data,
        prevHash=prev_hash,
        hash=block_hash
    )
    chain.append(block)
    return block

# Initialize with genesis block
add_block({"type": "GENESIS", "msg": "AyurChain system initialised"})

# API Endpoints
@app.post("/login")
def login(user: User):
    user_id = hash_data(user.name + user.role)
    users[user_id] = user.dict()
    return {"user_id": user_id, "user": user}

@app.get("/batches")
def get_batches():
    return list(batches.values())

@app.post("/batches")
def create_batch(batch: Batch):
    if batch.id in batches:
        raise HTTPException(status_code=400, detail="Batch ID already exists")
    batches[batch.id] = batch.dict()
    add_block({
        "type": "COLLECTION",
        "batchId": batch.id,
        "herb": batch.herbName,
        "collector": batch.collector,
        "geo": f"{batch.lat}N,{batch.lng}E",
        "qty": f"{batch.qty}{batch.unit}"
    })
    return batch

@app.put("/batches/{batch_id}")
def update_batch(batch_id: str, batch: Batch):
    if batch_id not in batches:
        raise HTTPException(status_code=404, detail="Batch not found")
    batches[batch_id] = batch.dict()
    # Add block based on update type
    if batch.stage == "processing":
        add_block({
            "type": "PROCESSING",
            "batchId": batch_id,
            "herb": batch.herbName,
            "stage": batch.processingLogs[-1]["stage"] if batch.processingLogs else "Updated",
            "by": batch.processingLogs[-1]["by"] if batch.processingLogs else "System"
        })
    elif batch.labResults:
        add_block({
            "type": "LAB_RESULT",
            "batchId": batch_id,
            "result": "PASS" if batch.labResults["passed"] else "FAIL",
            "heavyMetals": f"{batch.labResults['heavyMetals']}ppm",
            "activeCompound": f"{batch.labResults['activeCompound']}%",
            "tester": batch.labResults["testedBy"]
        })
    return batch

@app.get("/products")
def get_products():
    return products

@app.post("/products")
def create_product(product: Product):
    products.append(product.dict())
    add_block({
        "type": "FORMULATION",
        "productId": product.id,
        "batchId": product.batchId,
        "herb": product.herbName,
        "product": product.name,
        "form": product.form,
        "size": product.size,
        "mfr": product.mfr,
        "geo": product.geo
    })
    return product

@app.get("/chain")
def get_chain():
    return chain

@app.get("/chain/{index}")
def get_block(index: int):
    if index >= len(chain):
        raise HTTPException(status_code=404, detail="Block not found")
    return chain[index]

@app.post("/reset")
def reset_data():
    global users, batches, products, chain, batchNum
    users = {}
    batches = {}
    products = []
    chain = []
    batchNum = 4
    # Re-add genesis block
    add_block({"type": "GENESIS", "msg": "AyurChain system initialised"})
    return {"message": "All data reset successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
