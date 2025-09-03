.PHONY: backend frontend lib_utils ingest-pipeline success

all: ingest-pipeline backend frontend lib_utils success

ingest-pipeline:
	@echo "▶️  Execute ingest-pipeline..."
	$(MAKE) -C ingest-pipeline all

backend:
	@echo "▶️  Execute api-service..."
	$(MAKE) -C api-service all

frontend:
	@echo "▶️  Execute frontend..."
	$(MAKE) -C frontend all

lib_utils:
	@echo "▶️  Execute lib_utils..."
	$(MAKE) -C lib_utils all


success:
	@echo "==========================="
	@echo "✅ Monorepo build success!"
	@echo "==========================="
