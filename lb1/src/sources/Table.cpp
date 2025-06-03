#include "../include/Table.hpp"
#include <iostream>
#include <queue>

Table::Table(int n) : n(n) {
    std::cout << "\033[1;34m1. Инициализация стола:\033[0m" << std::endl;
    std::cout << "  Создание стола размером " << n << "x" << n << std::endl << std::endl;
    this->canvas = std::vector<std::vector<int>>();
    for (int i = 0; i < n; ++i) {
        this->canvas.push_back(std::vector<int>(n));
    }
    this->squares = std::vector<Square>();
};

Coordinate Table::findEmpty() {
    for (int y = 0; y < this->n; ++y) {
        for (int x = 0; x < this->n; ++x) {
            if (this->canvas[y][x] == 0) {
                return Coordinate{x, y};
            }
            x += this->canvas[y][x] - 1;
        }
    }
    std::cout << "  Пустых координат не найдено\n" << std::endl;
    return Coordinate{-1, -1};
}

bool Table::isPossibleToInsert(Coordinate coordinate, int currentSize) {
    std::cout << "  Проверка возможности вставки квадрата размером " << currentSize 
              << " в позицию (" << coordinate.x << ", " << coordinate.y << ")" << std::endl;
    
    if (coordinate.x + currentSize > this->n || coordinate.y + currentSize > this->n) {
        std::cout << "  Квадрат выходит за границы стола\n" << std::endl;
        return false;
    }

    for (int y = coordinate.y; y < coordinate.y + currentSize; ++y) {
        for (int x = coordinate.x; x < coordinate.x + currentSize; ++x) {
            if (this->canvas[y][x] != 0) {
                std::cout << "  Обнаружено препятствие в позиции (" << x << ", " << y << ")\n" << std::endl;
                return false;
            }
        }
    }
    std::cout << "  Вставка возможна\n" << std::endl;
    return true;
}

void Table::insertSquare(Coordinate coordinate, int currentSize) {
    std::cout << std::endl << "\033[1;34mВставка квадрата:\033[0m" << std::endl;
    std::cout << "  Размер: " << currentSize << std::endl;
    std::cout << "  Позиция: (" << coordinate.x << ", " << coordinate.y << ")\n" << std::endl;
    
    Square square = Square(coordinate, currentSize);
    for (int y = 0; y < currentSize; ++y) {
        this->canvas[coordinate.y + y][coordinate.x] = currentSize;
        this->canvas[coordinate.y + y][coordinate.x + currentSize - 1] = currentSize;
        
        this->canvas[coordinate.y][coordinate.x + y] = currentSize;
        this->canvas[coordinate.y + currentSize - 1][coordinate.x + y] = currentSize;
    }

    this->squares.push_back(square);
    std::cout << "  Квадрат успешно добавлен\n" << std::endl;
}

void Table::setEvenPreset() {
    std::cout << "\033[1;34mУстановка предустановки для четного n:\033[0m" << std::endl;
    clock_t time = clock();
    std::cout << "  Вставка 4 квадратов размером " << this->n/2 << std::endl;
    insertSquare({0, 0}, this->n/2);
    insertSquare({this->n/2, 0}, this->n/2);
    insertSquare({0, this->n/2}, this->n/2);
    insertSquare({this->n/2, this->n/2}, this->n/2);
    std::cout << "  Всего операций: 4" << std::endl;
    std::cout << "  Затраченное время: " << (double)(clock() - time)/CLOCKS_PER_SEC << " сек\n" << std::endl;
}

void Table::setPrimePreset() {
    std::cout << "\033[1;34mУстановка предустановки для простого n:\033[0m" << std::endl;
    clock_t time = clock();
    std::cout << "  Вставка начальных квадратов" << std::endl;
    insertSquare({0, 0}, (this->n+1)/2);
    insertSquare({0, (this->n+1)/2}, (this->n)/2);
    insertSquare({(this->n+1)/2, 0}, (this->n)/2);
    *this = this->backtracking();
    std::cout << "  Затраченное время: " << (double)(clock() - time)/CLOCKS_PER_SEC << " сек\n" << std::endl;
}

void Table::setCompositePreset() {
    std::cout << "\033[1;34mУстановка предустановки для составного N:\033[0m" << std::endl;
    int div1 = getDivs(n);
    int div2 = n / div1;
    std::cout << "  Разложение N: " << n << " = " << div1 << " * " << div2 << std::endl;
    clock_t time = clock();
    std::cout << "  Построение стола для меньшего размера " << div1 << std::endl;
    Table smallerTable = Table(div1).backtracking();
    std::cout << "  Масштабирование стола в " << div2 << " раз" << std::endl;
    *this = smallerTable.scaler(div2);
    std::cout << "  Затраченное время: " << (double)(clock() - time)/CLOCKS_PER_SEC << " сек\n" << std::endl;
}

Table Table::backtracking() {
    std::cout << std::endl << "\033[1;34mЗапуск backtracking алгоритма:\033[0m" << std::endl;
    std::queue<Table> q = std::queue<Table>();
    q.push(*this);
    int counter = 0;
    
    while (q.front().findEmpty() != Coordinate{-1, -1}) {
        Table lead = q.front();
        Coordinate coordinate = lead.findEmpty();
        std::cout << "  Текущая пустая позиция: (" << coordinate.x << ", " << coordinate.y << ")" << std::endl;

        for (int i = this->n - 1; i > 0; --i) {
            if (lead.isPossibleToInsert(coordinate, i)) {
                Table current = lead;
                current.insertSquare(coordinate, i);
                
                if (current.findEmpty() == Coordinate{-1, -1}) {
                    std::cout << "\033[1;32mРешение найдено\033[0m" << std::endl;
                    std::cout << "  Всего операций: " << counter << std::endl;
                    return current;
                }
                
                if (this->n < 10) {
                    current.printIteration(counter);
                }
                q.push(current);
            }
            ++counter;
        }
        q.pop();
    }
    std::cout << "\033[1;35mРешение найдено!\033[0m" << std::endl;
    std::cout << "  Всего операций: " << counter << std::endl;
    return q.front();
}

Table Table::scaler(int multiplier) {
    std::cout << "\033[1;34mМасштабирование стола:\033[0m" << std::endl;
    std::cout << "  Множитель: " << multiplier << std::endl;
    std::cout << "  Новый размер: " << this->getN() * multiplier << "x" << this->getN() * multiplier << std::endl;
    
    Table newTable(this->getN() * multiplier);

    for (const auto& square : this->getSquares()) {
        int x = square.getCoordinate().x * multiplier;
        int y = square.getCoordinate().y * multiplier;
        int length = square.getLength() * multiplier;
        std::cout << "  Масштабирование квадрата: (" << square.getCoordinate().x << ", " << square.getCoordinate().y 
                  << ", " << square.getLength() << ") -> (" << x << ", " << y << ", " << length << ")" << std::endl;
        newTable.insertSquare({x, y}, length);
    }
    
    std::cout << "  Масштабирование завершено\n" << std::endl;
    return newTable;
}

void Table::printIteration(int iteration) {
    std::cout << "\033[1;34mИтерация " << iteration << ":\033[0m" << std::endl;
    for (int y = 0; y < this->n; ++y) {
        for (int x = 0; x < this->n; ++x) {
            std::cout << this->getCanvas()[y][x] << " ";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

void Table::printCanvas() {
    std::cout << "\033[1;34mВизуализация квадратов:\033[0m" << std::endl;
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
    std::cout << std::endl;
}

void Table::printSquares() {
    std::cout << "\033[1;34mСписок квадратов:\033[0m" << std::endl;
    std::cout << "  Всего квадратов: " << this->squares.size() << std::endl;
    for (const auto& square : this->squares) {
        std::cout << "  Квадрат: (" << square.getCoordinate().x << ", " << square.getCoordinate().y 
                  << "), размер: " << square.getLength() << std::endl;
    }
    std::cout << std::endl;
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