LEX = flex
YACC = bison -y
YFLAGS = -d
LDFLAGS = -lfl
objects = blf_scan.o blf_parse.o blf_parse_impl.o _queue.o _tree.o

blf_reader: $(objects)
	$(CC) -o $@ $^ $(LDFLAGS)

blf_scan.o: blf_scan.l blf_parse.o
blf_parse.o: blf_parse.y

.PHONY: clean
clean: $(objects) blf_reader
	rm -f $^
