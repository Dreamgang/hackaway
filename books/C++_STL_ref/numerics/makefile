CXX=g++
CXXFLAGS=-g -std=c++14 -Wall
ALL_TARGET=q_cmath q_complex q_ratio q_random q_valarray

q_cmath: q_cmath.o
	${CXX} ${CXXFLAGS} q_cmath.cpp -o $@

q_complex: q_complex.o
	${CXX} ${CXXFLAGS} q_complex.cpp -o $@

q_ratio: q_ratio.o
	${CXX} ${CXXFLAGS} q_ratio.cpp -o $@

q_random: q_random.o
	${CXX} ${CXXFLAGS} q_random.cpp -o $@

q_valarray: q_valarray.o
	${CXX} ${CXXFLAGS} q_valarray.cpp -o $@

clean:
	rm -rf *.o 
	rm -rf ${ALL_TARGET}