PREFIX ?= $(HOME)/.local/bin

install:
	./install.sh

uninstall:
	rm -f $(PREFIX)/mradio

check:
	python3 -m py_compile mradio
	bash -n install.sh

.PHONY: install uninstall check