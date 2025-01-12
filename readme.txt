8/1/2025
WhipSplash Hotel - An Agent-Powered LLM App 

This is a PoC which demonstrates how we can use Pydantic AI, AWS Bedrock, FastAPI, and Postgres to create an agentic LLM app that allows users to use
hotel services (book rooms, change reservations, ask about services) through a simple chat interface. 

room types: single, double, suite

services: room service, room service with hot meal, wake up call, late check in, hot water, electricity

--- 
to run locally:

1. run the postgres container using the scrip in db/start_postgres.SessionSchema

2. uv run alembic upgrade head

3. uv run uvicorn main:app --host 0.0.0.0 --port 8080 --reload 

4. in the ui folder, run 'npm run dev'