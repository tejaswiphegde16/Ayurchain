# AyurChain — Blockchain Botanical Traceability System

## 🌿 Project Overview
AyurChain is a comprehensive blockchain-based system for tracking Ayurvedic herbs from collection to final product formulation. It integrates three main components:
- **Frontend (index.html, ayurchain.html)**: Web interface for the traceability system
- **Backend (backend.py)**: Flask API server handling authentication and data management

---

## 📁 File Structure
```
ayurchain/
├── index.html          # Landing/home page with project overview
├── ayurchain.html      # Main application dashboard & blockchain ledger
└── backend.py          # Flask backend API server
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7+ installed
- pip (Python package manager)
- Modern web browser

### Installation & Setup

#### 1. Install Python Dependencies
```bash
pip install flask flask-cors
```

#### 2. Start the Backend Server
```bash
cd c:\vs codes\ayurchain
python backend.py
```

You should see output like:
```
🌿 AyurChain Backend Server Starting...
📍 Navigate to http://localhost:5000/
📱 API Documentation available at http://localhost:5000/api/health
 * Running on http://localhost:5000
```

#### 3. Open the Frontend
- **Option A**: Open `index.html` in your web browser
  - Click "Explore the System" button to navigate to `ayurchain.html`
  
- **Option B**: Directly navigate to `ayurchain.html`

---

## 🔗 How Files Connect

### Frontend Flow
1. **index.html** serves as the landing page with:
   - Project overview and features
   - Navigation to the main application
   - Hero section with "Explore the System" button linking to `ayurchain.html`

2. **ayurchain.html** is the main application with:
   - User login (Field Collector, Processor, Lab Tester, Manufacturer)
   - Role-based dashboards
   - Blockchain ledger viewer
   - Connected to backend via JavaScript API calls

### Backend Integration
The backend (`backend.py`) provides REST API endpoints:

#### Authentication
- `POST /api/login` - User login with username and role
  ```json
  { "username": "John Doe", "role": "collector" }
  ```

#### Plant/Batch Management
- `POST /api/plant` - Create new plant record
  ```json
  { "plant_id": "BATCH-001", "name": "Ashwagandha", "species": "Withania somnifera", "location": "8.1774°N, 77.4347°E" }
  ```
- `GET /api/plant/<plant_id>` - Retrieve specific plant record
- `GET /api/plants` - Get all plant records

#### Health Check
- `GET /api/health` - Check backend status

---

## 💻 Usage Guide

### For Field Collectors
1. Log in with name and select "Field Collector" role
2. Navigate to "Log Collection" (📍)
3. Fill in herb details and GPS coordinates
4. Submit to blockchain - data syncs with backend

### For Processors
1. Log in as "Processing Unit"
2. View "Incoming Batches" (📥)
3. Update stage as processing progresses
4. Changes are recorded on blockchain and sent to backend

### For Lab Testers
1. Log in as "Lab Tester"
2. Enter test results for pending batches
3. System automatically determines PASS/FAIL based on AYUSH standards
4. Results saved to blockchain and backend

### For Manufacturers
1. Log in as "Manufacturer"
2. View certified batches ready for formulation
3. Create final products with QR codes
4. QR codes link to full provenance records

---

## 🔌 API Endpoints Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/login` | Authenticate user |
| GET | `/api/user/<username>` | Get user info |
| POST | `/api/plant` | Add plant record |
| GET | `/api/plant/<plant_id>` | Get plant by ID |
| GET | `/api/plants` | Get all plants |
| GET | `/api/health` | Health check |

---

## ✨ Key Features

✅ **Geo-Tagged Traceability** - GPS coordinates at collection point  
✅ **Immutable Blockchain Ledger** - Tamper-proof transaction history  
✅ **Role-Based Access Control** - Different views for each stakeholder  
✅ **QR Code Generation** - Consumer verification via product QR  
✅ **Smart Contract Enforcement** - Automatic AYUSH compliance checking  
✅ **Multi-Stakeholder Dashboard** - Real-time supply chain visibility  

---

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python Flask, Flask-CORS
- **Database**: In-memory (can integrate PostgreSQL/MongoDB)
- **Blockchain**: Simulated blockchain with hash-based integrity
- **Libraries**: QRCode.js for QR generation

---

## 📝 Demo Data

The system comes pre-loaded with sample batches:
- **BATCH-001**: Ashwagandha (certified)
- **BATCH-002**: Shatavari (processing)
- **BATCH-003**: Brahmi (testing)

---

## 🔐 Security Notes

⚠️ **Important**: This is a demo/educational system. For production use:
- Implement proper database (PostgreSQL, MongoDB)
- Add authentication tokens (JWT)
- Use HTTPS for API calls
- Implement proper access control (RBAC)
- Add audit logging
- Enable CORS properly with origin validation

---

## 📞 Support

For issues or questions:
1. Check backend logs in terminal
2. Verify API is running on `http://localhost:5000`
3. Check browser console for frontend errors (F12)
4. Ensure port 5000 is available

---

## 📄 License

Educational & Research Project
