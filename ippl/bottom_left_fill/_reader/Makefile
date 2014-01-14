FLEX = flex
BISON = bison
BFLAGS = -vd
CFLAGS = -g
LDFLAGS = -lfl
objects = scan.lex.o parse.tab.o parse_impl.o parse_util.o

reader: libreader.a reader.o
	$(CC) -o $@ reader.o libreader.a

libreader.a: $(objects)
	$(AR) rcs $@ $^

scan.lex.o: scan.lex.c parse.tab.o
parse.tab.o: parse.tab.c scan.lex.h

scan.lex.c: scan.l
	$(FLEX) -o scan.lex.c $^
parse.tab.c: parse.y
	$(BISON) $(BFLAGS) $^

.PHONY: clean
clean: $(objects) reader.o reader libreader.a
	rm -f $^
	rm -f scan.lex.h
	rm -f scan.lex.c
	rm -f parse.tab.h
	rm -f parse.tab.c
	rm -f parse.output
