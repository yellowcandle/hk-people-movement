.PHONY: data build dev deploy clean install validate

# Default: just show targets
help:
	@echo "Targets:"
	@echo "  install   Install node + python deps"
	@echo "  data      Refresh data/ from upstream sources (IMMD + HKIA) and rebuild aggregates"
	@echo "  validate  Check every number in master JSON has a source"
	@echo "  dev       Run Observable Framework dev server"
	@echo "  build     Build dashboard to dist/"
	@echo "  deploy    Deploy to Cloudflare Pages (requires wrangler login)"
	@echo "  clean     Remove dist/ and Observable cache"

install:
	npm install
	cd pipeline && python3 -m pip install -e .

data:
	python3 pipeline/fetch_immd.py
	python3 pipeline/fetch_hkia_window.py
	python3 pipeline/build_aggregates.py

validate:
	python3 pipeline/validate.py

dev:
	npm run dev

build: validate
	npm run build
	# Observable hashes static files into dist/_file/<path>.<hash>.<ext>;
	# copy the originals to dist/static/ so the @font-face URLs in <head>
	# resolve in production. (See `dev-fonts` for the dev-mode equivalent.)
	mkdir -p dist/static
	cp -R src/static/. dist/static/

deploy: build
	npm run deploy

fonts:
ifdef NOTO
	python3 pipeline/subset_font.py --source noto
else
	python3 pipeline/subset_font.py --source metrosung
endif

clean:
	rm -rf dist .observablehq/cache
