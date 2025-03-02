#include "../include/Table.hpp"

Table::Table(int n) : n(n) {
    this->canvas = std::vector<std::vector<int>>();
    for (int i = 0; i < n; ++i) {
        this->canvas.push_back(std::vector<int>(n));
    }
    this->squares = std::vector<Square>();
};

Coordinate Table::findEmpty() {
    for (int y = 0; y < this->n; ++y) {
        for (int x = 0; x < this->n; ++x) {
            if (this->canvas[y][x] == 0) return Coordinate{x, y};
            x += this->canvas[y][x] - 1;
        }
    }
    return Coordinate{-1, -1};
}

bool Table::isPossibleToInsert(Coordinate coordinate, int currentSize) {
    if (coordinate.x + currentSize > this->n || coordinate.y + currentSize > this->n) return false;

    for (int y = coordinate.y; y < coordinate.y + currentSize; ++y) {
        for (int x = coordinate.x; x < coordinate.x + currentSize; ++x) {
            if (this->canvas[y][x] != 0) return false;
        }
    }
    return true;
}

void Table::insertSquare(Coordinate coordinate, int currentSize) {
    Square square = Square(coordinate, currentSize);
    for (int y = 0; y < currentSize; ++y) {
        this->canvas[coordinate.y + y][coordinate.x] = currentSize;
        this->canvas[coordinate.y + y][coordinate.x + currentSize - 1] = currentSize;
        
        this->canvas[coordinate.y][coordinate.x + y] = currentSize;
        this->canvas[coordinate.y + currentSize - 1][coordinate.x + y] = currentSize;
    }

    this->squares.push_back(square);
}

void Table::setEvenPreset() {
    clock_t time = clock();
    insertSquare({0, 0}, this->n/2);
    insertSquare({this->n/2, 0}, this->n/2);
    insertSquare({0, this->n/2}, this->n/2);
    insertSquare({this->n/2, this->n/2}, this->n/2);
    std::cout << "Total operations: 4" << std::endl;
    std::cout << "Time spend: " << (double)(clock() - time)/CLOCKS_PER_SEC << std::endl;
}

void Table::setPrimePreset() {
    clock_t time = clock();
    insertSquare({0, 0}, (this->n+1)/2);
    insertSquare({0, (this->n+1)/2}, (this->n)/2);
    insertSquare({(this->n+1)/2, 0}, (this->n)/2);
    *this = this->backtracking();
    std::cout << "Time spend: " << (double)(clock() - time)/CLOCKS_PER_SEC << std::endl;
}

void Table::setCompositePreset() {
    int div1 = getDivs(n);
    int div2 = n / div1;
    clock_t time = clock();
    Table smallerTable = Table(div1).backtracking();
    *this = smallerTable.scaler(div2);
    std::cout << "Time spend: " << (double)(clock() - time)/CLOCKS_PER_SEC << std::endl;
}

Table Table::backtracking() {
    std::queue<Table> q = std::queue<Table>();
    q.push(*this);
    int counter = 0;
    
    while (q.front().findEmpty() != Coordinate{-1, -1}) { // проверка на заполненность
        Table lead = q.front(); // копия первого стола в очереди
        Coordinate coordinate = lead.findEmpty(); // поиск пустого места

        for (int i = this->n - 1; i > 0; --i) { // перебор размеров квадрата для расстановки
            if (lead.isPossibleToInsert(coordinate, i)) { // проверка на возможность вставки
                Table current = lead;
                current.insertSquare(coordinate, i); // вставка квадрата
                
                if (current.findEmpty() == Coordinate{-1, -1}) { // проверка на заполненность стола
                    std::cout << "Total operations: " << counter << std::endl;
                    return current;
                }
                
                if (this->n < 10) {
                    current.printIteration(counter); // вывод промежуточного результата
                }
                q.push(current); // сохранение очередной расстановки
            }
            ++counter;
        }
        q.pop(); // удаление расстановки, которая дала все возможные разбиения
    }
    std::cout << "Total operations: " << counter << std::endl;
    return q.front();
}

Table Table::scaler(int multiplier) {
    Table newTable(this->getN() * multiplier);

    for (const auto& square : this->getSquares()) {
        int x = square.getCoordinate().x * multiplier;
        int y = square.getCoordinate().y * multiplier;
        int length = square.getLength() * multiplier;
        newTable.insertSquare({x, y}, length);
    }
    return newTable;
}

void Table::printIteration(int iteration) {
    std::cout << "Iteration " << iteration << std::endl;
    for (int y = 0; y < this->n; ++y) {
        for (int x = 0; x < this->n; ++x) {
            std::cout << this->getCanvas()[y][x] << " ";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

void Table::printCanvas() {
    int counter, size;
    for (int i = 0; i < this->n; ++i) { 
        counter = 1;
        for (int j = 0; j < this->n; ++j) {
            size = this->canvas[i][j];
            
            if (size == 0) {
                std::cout << "    ";
            } else if (size < 10) {
                if (this->canvas[i][j+1] == 0 || counter == size) {
                    std::cout << "\033[3" << canvas[i][j] % 7 << "m" << size << "   ";
                } else {
                    std::cout << "\033[3" << canvas[i][j] % 7 << "m" << size << "---";
                }
            } else {
                if (this->canvas[i][j+1] == 0 || counter == size) {
                    std::cout << "\033[3" << canvas[i][j] % 7 << "m" << size << "  ";
                } else {
                    std::cout << "\033[3" << canvas[i][j] % 7 << "m" << size << "--";
                }
            }

            ++counter;
            if (counter == size + 1)
                counter = 1;
        }
        std::cout << std::endl;
        
        for (int j = 0; j < this->n; ++j) {
            size = this->canvas[i][j];
            if (size == 0 || size == 1) {
                std::cout << "    ";
                continue;
            }
            if (i+1 == n || size != canvas[i+1][j] || ((i-size+1) >= 0 && (i+size) < n && canvas[i-size+1][j] == size && canvas[i+size][j] == size && (canvas[i][j-1] == size || canvas[i][j+1] == size))) {
                if (size > 2 && i-1 >= 0 && i+1 < n && canvas[i-1][j] == size && canvas[i+1][j] == size && ((j-1 >= 0 && canvas[i][j-1] == size && canvas[i+1][j-1] == 0) || (j+1 < n && canvas[i][j+1] == size && canvas[i+1][j+1] == 0))) {
                    std::cout << "\033[3" << canvas[i][j] % 7 << "m" << "|   ";
                } else {
                    std::cout << "\033[3" << canvas[i][j] % 7 << "m" << "    ";
                }
            } else {
                std::cout << "\033[3" << canvas[i][j] % 7 << "m" << "|   ";
            }
        }
        std::cout << "\033[0m" << std::endl;
    }
}

void Table::printSquares() {
    std::cout << this->squares.size() << std::endl;
    for (const auto& square : this->squares) {
        std::cout << square.getCoordinate().x << " " << square.getCoordinate().y << " " << square.getLength() << std::endl;
    }
}

std::vector<std::vector<int>> Table::getCanvas() const {
    return this->canvas;
}

int Table::getN() const {
    return this->n;
}

std::vector<Square> Table::getSquares() const {
    return this->squares;
}
