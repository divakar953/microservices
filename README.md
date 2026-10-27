# Microservices E-Commerce Platform

An event driven e-commerce platform built with microservices architecture. The application separates inventory management and payment processing into isolated services that communicate asynchronously using Redis Streams, ensuring high availability and fault tolerance.

## Architecture

* **Frontend:** React (Bootstrapped with Create React App)
* **Inventory Service:** Python / FastAPI
* **Payment Service:** Python / FastAPI
* **Database & Message Broker:** Redis & Redis OM
* **Package Management:** `uv` (Python) and `npm` (Node.js)

## Prerequisites

* Python 3.14+
* [uv](https://github.com/astral-sh/uv) installed
* Node.js and npm installed
* A running Redis instance (local or Redis Cloud)

## Setup and Installation

**1. Clone the repository and install dependencies**
From the root directory of the project, install the Python dependencies using `uv`:
```bash
uv sync
```

**2. Environment Configuration**
Copy the example environment file and fill in your Redis credentials:
```bash
cp .env.example .env
```
Ensure your `.env` file contains your actual `REDIS_HOST`, `REDIS_PORT`, and `REDIS_PASSWORD`.

**3. Frontend Setup**
Navigate to the frontend directory and install the Node modules:
```bash
cd frontend
npm install
```

## Running the Application

Because this is a microservices architecture utilizing background workers for event processing, you will need to run multiple services simultaneously across separate terminal windows.

**Terminal 1: Inventory API**
```bash
cd inventory
uv run uvicorn main:app --port 8000 --reload
```

**Terminal 2: Inventory Consumer**
```bash
cd inventory
uv run python consumer.py
```

**Terminal 3: Payment API**
```bash
cd payment
uv run uvicorn main:app --port 8001 --reload
```

**Terminal 4: Payment Consumer**
```bash
cd payment
uv run python consumer.py
```

**Terminal 5: Frontend React App**
```bash
cd frontend
npm start
```
