PROG ?=
PREFIX ?= /usr/local
DESTDIR ?=
LIBDIR ?=
MANDIR ?=

all:
	@echo "This version of arch-wiki-docs and arch-wiki-lite requires some other packages:"
	@echo "         brew install ripgrep w3m newt dialog"
	@echo "         cargo install huniq"

install:
	@install -vd "$(PREFIX)/etc/dialog.d/"
	@install -vm755 lite/wiki-search "$(PREFIX)/bin/wiki-search"
	@install -vm755 lite/wiki-search-html "$(PREFIX)/bin/wiki-search-html"
	@install -vm655 lite/wiki-search.dialog.rc "$(PREFIX)/etc/dialog.d/wiki-search.dialog.rc"
	@echo
	@echo "arch-wiki-lite installed successfully"
	@echo
	@install -vd "$(PREFIX)/share/doc/arch-wiki/html"
	@install -vd "$(PREFIX)/share/doc/arch-wiki/text"
	@install -vm644 docs/text/* "$(PREFIX)/share/doc/arch-wiki/text"
	@tar -xzf docs/html.tar.gz -C "$(PREFIX)/share/doc/arch-wiki/html" --strip-components 1
	@echo
	@echo "arch-wiki-docs installed successfully"
	@echo

test:
	make -C tests
