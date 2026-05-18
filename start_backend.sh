#!/bin/bash
cd /var/www/hash-identifier/backend
source venv/bin/activate
export FLASK_ENV=production
export DATABASE_URL=postgresql://hashuser:HashPass123!@localhost:5432/hashdb
python3 -c "from app import create_app; app = create_app(); app.run(host='127.0.0.1', port=5000)"
