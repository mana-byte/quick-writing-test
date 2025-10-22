# Project Setup Guide

https://github.com/user-attachments/assets/1821129d-e1d2-482f-9e4f-c9c42f1624f7

## Backend Setup

### Prerequisites
- Docker and Docker Compose installed.
- Python installed (compatible with FastAPI).

### Steps
1. Clone the repository to your local machine:
   ```bash
   git clone <repository-url>
   cd devweb/back_jeu
   ```

2. Start the PostgreSQL database using Docker:
   ```bash
   docker-compose up -d
   ```
   This will set up a PostgreSQL database with the following environment:
   - `POSTGRES_USER`: mana
   - `POSTGRES_PASSWORD`: pswd
   - `POSTGRES_DB`: pg_db
   - Accessible on port `8898` locally.

   Now we need to initialize the database
   ```bash
   python3 src/db/init.db.py
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI application:
   ```bash
   fastapi run src/backend/api.py
   ```

---

## Frontend Setup

### Prerequisites
- Node.js and npm installed.

### Steps
1. Navigate to the frontend directory:
   ```bash
   cd devweb/front_jeu
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   # Or
   npm run dev
   ```


