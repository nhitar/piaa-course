#pragma once

#include <iostream>
#include <math.h>

struct Coordinate {
    int x;
    int y;

    bool operator==(const Coordinate& other) const {
        return x == other.x && y == other.y;
    }

    bool operator!=(const Coordinate& other) const {
        return !(*this == other);
    }
};

inline int isPrime(int n) {
    for (int i = 2; i < int(sqrt(n)) + 1; i++) {
        if (n % i == 0) return 0;        
    }
    return 1;
}

inline int getDivs(int n) {
    for (int i = 2; i < int(sqrt(n)) + 1; i++) {
        if (n % i == 0) {
            return i;
        }      
    }
    throw std::invalid_argument("Error: Number is prime.");
}
