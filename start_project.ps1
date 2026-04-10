Write-Host "Starting Placement Risk Modeling System..." -ForegroundColor Cyan

# Start Backend
Start-Process powershell -ArgumentList "python app/main.py" -NoNewWindow
Write-Host "Backend API starting on http://localhost:8000..." -ForegroundColor Green

# Wait a bit
Start-Sleep -Seconds 5

# Start Frontend
python -m streamlit run app/view.py
