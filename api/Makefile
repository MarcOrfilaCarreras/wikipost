FLASK_APP = wsgi.py
FLASK_APP_PORT = 8080
TEST_INTEGRATION_DIR = test/integration

install:
	@echo "\n🔧 Installing dependencies..."
	@pip install -r requirements.txt > /dev/null 2>&1 || { echo "❌ Failed to install dependencies"; exit 1; }

run-integration-tests:
	@echo "\n🔬 Running integration tests..."
	@rm -f app.log db.sqlite
	@echo "Starting integration tests..."
	@sleep 5
	@find $(TEST_INTEGRATION_DIR) -name "*.py" | sort | while read file; do \
		echo "\n➡️  Running test: $$file"; \
		python3 $$file || { echo "❌ Integration test $$file failed"; exit 1; }; \
	done

run-flask:
	@echo "\n🚀 Starting Flask app on port $(FLASK_APP_PORT)..."
	@nohup python3 $(FLASK_APP) > app.log 2>&1 &
	@echo "Flask app started in the background. Logs are being saved to app.log."

kill-flask:
	@echo "\n💥 Killing Flask app running on port $(FLASK_APP_PORT)..."
	@if lsof -t -i:$(FLASK_APP_PORT) > /dev/null; then \
		kill -9 $(shell lsof -t -i:$(FLASK_APP_PORT)); \
		echo "Flask app on port $(FLASK_APP_PORT) killed."; \
	else \
		echo "No Flask app running on port $(FLASK_APP_PORT) to kill."; \
	fi

test: install run-flask run-integration-tests kill-flask
