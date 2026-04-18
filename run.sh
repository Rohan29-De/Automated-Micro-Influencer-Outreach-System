#!/bin/bash
echo "Starting Micro-Influencer Outreach System..."

# Start backend
cd webapp/backend && uvicorn main:app --reload --port 8000 &

# Start frontend
cd webapp/frontend && npm run dev &

echo "=========================================="
echo "✅ Backend: http://localhost:8000"
echo "✅ Frontend: http://localhost:5173"
echo "✅ API Docs: http://localhost:8000/docs"
echo "=========================================="

wait