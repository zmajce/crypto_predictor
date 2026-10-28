run-dev:
	uv run --env-file live.settings.env python run.py

build:
	docker build -f Dockerfile -t candles .

run: build
	docker run -it \
		--network redpanda_network \
		--env-file live.settings.env \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		candles
