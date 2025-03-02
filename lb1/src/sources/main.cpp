#include "../include/Table.hpp"

#include <iostream>

int main() {
    int n;
    std::cin >> n;
    if (n < 2 || n > 20) {
        std::cout << "Invalid input: n should be between 2 and 20." << std::endl;
        return 0;
    }
    
    Table table(n);
    if (n % 2 == 0) {
        table.setEvenPreset();
    } else if (isPrime(n)) {
        table.setPrimePreset();
    } else {
        table.setCompositePreset();
    }

    table.printCanvas();
    table.printSquares();

    return 0;
}
