# Quick writting test

https://github.com/user-attachments/assets/1821129d-e1d2-482f-9e4f-c9c42f1624f7

## Backend Setup

### Prerequisites

- Docker and Docker Compose installed.
- Python installed (compatible with FastAPI).

### Steps

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/mana-byte/quick-writing-test.git
    cd devweb/back_jeu
    ```

2. Start the whole backend using Docker:
   ```bash
   docker-compose up -d
   ```

---

## Frontend Setup

### Prerequisites

- Node.js and npm installed.
- A Mistral API key to put into Type.jsx or in env variables at MISTRAL_API_KEY

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
