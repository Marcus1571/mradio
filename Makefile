PREFIX ?= $(HOME)/.local/bin

install:
	./install.sh

uninstall:
	rm -f $(PREFIX)/mradio

check:
	python3 -m py_compile mradio
	bash -n install.sh

test:
	python3 test_mradio.py

smoke:
	python3 mradio --version
	python3 mradio --help

screens:
	cd screenshots && swiftc -O shot.swift -o shot && \
		./shot player player.png && ./shot fav favorites.png && ./shot all all-stations.png

.PHONY: install uninstall check test smoke screens