# Blockchain Attendance Makefile

.PHONY: compile deploy run_backend run_frontend start clean status

compile:
	@echo "========================================="
	@echo "🛠️ Compiling Truffle Solidity Smart Contracts..."
	@echo "========================================="
	cd blockchain && npx truffle compile

deploy: compile
	@echo "========================================="
	@echo "🚀 Deploying Smart Contract to Ganache..."
	@echo "========================================="
	cd backend && .\venv\Scripts\python deploy.py

run_backend:
	@echo "========================================="
	@echo "📡 Starting Backend Flask API..."
	@echo "========================================="
	cd backend && .\venv\Scripts\python app.py

run_frontend:
	@echo "========================================="
	@echo "🌐 Starting Frontend Web Server on port 8080..."
	@echo "========================================="
	cd frontend && python -m http.server 8080

start: deploy
	@echo "========================================="
	@echo "🎉 Running both servers in the background..."
	@echo "========================================="
	start "Blockchain Attendance API (Port 5000)" cmd /k "cd backend && call .\venv\Scripts\python app.py"
	start "Blockchain Attendance Web (Port 8080)" cmd /k "cd frontend && python -m http.server 8080"

clean:
	@echo "🧹 Cleaning compile artifacts..."
	if exist blockchain\build rmdir /s /q blockchain\build
	if exist backend\attendance_gps_log.json del /f /q backend\attendance_gps_log.json
