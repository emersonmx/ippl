LEX = flex
YACC = bison -y
YFLAGS = -v -d
CFLAGS = -g
LDFLAGS = -lfl
objects = scan.o parse.o parse_impl.o

reader: reader.o $(objects)
	$(CC) -o $@ $^ $(LDFLAGS)

scan.o: scan.l parse.o
parse.o: parse.y

.PHONY: clean
clean: $(objects) reader.o reader
	rm -f $^
