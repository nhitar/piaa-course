#pragma once

#include "Utils.hpp"

class Square {
    private:
        Coordinate coordinate;
        int length;

    public:
        Square(Coordinate coordinate, int length) : coordinate(coordinate), length(length) {};

        Coordinate getCoordinate() const {
            return coordinate;
        }

        int getLength() const {
            return length;
        }
};
