CC=c++
CFLAGS=-Wall
OBJS=char_category locale function by_ref algorithms predicate
OBJS+=lambda overload_fn cast doxygen struct class virtual
OBJS+=functor search find_if replace_if exception noexcept
OBJS+=function_template class_template template_special
OBJS+=custom_comparator test_debug

# in this makefile, latter script will appear later
clean:
	rm -rf *.o
	rm -rf $(OBJS) debug.txt

char_category: char_category.o
	$(CC) char_category.cpp $(CFLAGS) -o $@


locale: locale.o
	$(CC) locale.cpp $(CFLAGS) -o $@

function: function.o
	$(CC) function.cpp $(CFLAGS) -o $@

by_ref: by_ref.o
	$(CC) by_ref.cpp $(CFLAGS) -o $@

algorithms: algorithms.o
	$(CC) algorithms.cpp $(CFLAGS) -o $@

predicate: predicate.o
	$(CC) predicate.cpp $(CFLAGS) -o $@
	
lambda: lambda.o
	$(CC) lambda.cpp $(CFLAGS) -o $@
	
overload_fn: overload_fn.o
	$(CC) overload_fn.cpp $(CFLAGS) -o $@

cast: cast.o
	$(CC) cast.cpp $(CFLAGS) -o $@

doxygen: doxygen.o
	$(CC) doxygen.cpp $(CFLAGS) -o $@

struct: struct.o
	$(CC) struct.cpp $(CFLAGS) -o $@

class: class.o
	$(CC) class.cpp $(CFLAGS) -o $@

virtual: virtual.o
	$(CC) virtual.cpp $(CFLAGS) -o $@

functor: functor.o
	$(CC) functor.cpp $(CFLAGS) -o $@

search: search.o
	$(CC) search.cpp $(CFLAGS) -o $@

find_if: find_if.o
	$(CC) find_if.cpp $(CFLAGS) -o $@

replace_if: replace_if.o
	$(CC) replace_if.cpp $(CFLAGS) -o $@

exception: exception.o
	$(CC) exception.cpp $(CFLAGS) -o $@

noexcept: noexcept.o
	$(CC) noexcept.cpp $(CFLAGS) -o $@

function_template: function_template.o
	$(CC) function_template.cpp $(CFLAGS) -o $@

class_template: class_template.o
	$(CC) class_template.cpp $(CFLAGS) -o $@

template_special: template_special.o
	$(CC) template_special.cpp $(CFLAGS) -o $@

custom_comparator: custom_comparator.o
	$(CC) custom_comparator.cpp $(CFLAGS) -o $@

test_debug: test_debug.o debug.o
	$(CC) test_debug.cpp debug.cpp $(CFLAGS) -o $@
