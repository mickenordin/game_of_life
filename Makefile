env:
	test -e .env || virtualenv .env -p python3
	. ./.env/bin/activate \
		&& pip install -r requirements.txt

game: env
	test -e .env || virtualenv .env -p python3
	. ./.env/bin/activate \
		&& pip install -r requirements.txt \
		&& python -u game.py

clean:
	rm -rf .env
