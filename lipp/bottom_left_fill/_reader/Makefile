FLEX = flex
BISON = bison
BFLAGS = -d
CFLAGS = -g
LDFLAGS = -lfl
objects = scan.lex.o parse.tab.o parse_impl.o

reader: $(objects) reader.o
	$(CC) -o $@ $^ $(LDFLAGS)

scan.lex.o: scan.lex.c parse.tab.o parse.h
scan.lex.c: scan.l
	$(FLEX) -o $@ $^
parse.tab.o: parse.tab.c parse.h
parse.tab.c: parse.y
	$(BISON) $(BFLAGS) $^

.PHONY: clean
clean: $(objects) reader.o reader
	rm -f $^
	rm -f scan.lex.h
	rm -f scan.lex.c
	rm -f parse.tab.h
	rm -f parse.tab.c
