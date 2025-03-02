#pragma once

#include "Square.hpp"

#include <vector>
#include <queue>

class Table {
    private:
        std::vector<std::vector<int>> canvas;
        int n;
        std::vector<Square> squares;

    public:
        Table(int n);

        Coordinate findEmpty();
        bool isPossibleToInsert(Coordinate coordinate, int currentSize);
        void insertSquare(Coordinate coordinate, int currentSize);

        void setEvenPreset();
        void setPrimePreset();
        void setCompositePreset();

        Table backtracking();
        Table scaler(int multiplier);

        void printIteration(int iteration);
        void printCanvas();
        void printSquares();

        std::vector<std::vector<int>> getCanvas() const;
        int getN() const;
        std::vector<Square> getSquares() const;
};
