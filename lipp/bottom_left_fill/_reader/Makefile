LEX = flex
YACC = bison -y
YFLAGS = -d
CFLAGS = -g
LDFLAGS = -lfl
objects = blf_scan.o blf_parse.o blf_parse_impl.o tree.o

blf_reader: blf_reader.o $(objects)
	$(CC) -o $@ $^ $(LDFLAGS)

blf_scan.o: blf_scan.l blf_parse.o
blf_parse.o: blf_parse.y

.PHONY: clean
clean: $(objects) blf_reader.o blf_reader y.tab.h
	rm -f $^
