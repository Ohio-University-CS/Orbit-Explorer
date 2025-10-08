# Compiler
CXX = g++
CXXFLAGS = -std=c++17 -I"src/cspice/include"

# Library
LDFLAGS = -L"src/cspice/lib" -l:cspice.a -lm

# Target
TARGET = a
SRC = src/main.cpp src/CelestialEvents.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET) $(LDFLAGS)

clean:
	rm -f $(TARGET)
