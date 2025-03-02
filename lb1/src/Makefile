SOURCES = $(wildcard sources/*.cpp)
OBJECTS = $(patsubst sources/%.cpp,sources/%.o,$(SOURCES))
CC = g++
CFLAGS = -Wall -Wextra -std=c++17
LDFLAGS = -lm

all: backtracking

backtracking: $(OBJECTS)
	$(CC) $(OBJECTS) $(LDFLAGS) -o backtracking && rm -rf sources/*.o

sources/%.o : sources/%.cpp
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf sources/*.o backtracking