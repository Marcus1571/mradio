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
	cd screenshots && for h in player favorites all-stations; do \
		qlmanage -t -s 2600 -o . $$h.html >/dev/null 2>&1; \
		mv $$h.html.png $$h.png; \
	done

.PHONY: install uninstall check test smoke screens