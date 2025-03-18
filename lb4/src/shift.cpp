#include <iostream>
#include <string>
#include <vector>

std::vector<int> prefixFunc(std::string pattern) {
    std::vector<int> prefix;
    for (int i = 0; i < pattern.size(); ++i) {
        prefix.push_back(0);
    }

    int ptr2 = 0;

    std::cout << "\033[31m" << "Расчёт префикс-функции" << "\033[0m" << std::endl << std::endl;
    std::cout << "prefix[0] == 0 по условию" << std::endl << std::endl;

    for (int ptr1 = 1; ptr1 < prefix.size(); ++ptr1) {
        while (ptr2 > 0 && pattern[ptr1] != pattern[ptr2]) {
            std::cout << "ptr2 > 0 и символы " << pattern[ptr1] << "(" << ptr1 << ") и " << pattern[ptr2] << "(" << ptr2 << ") различны" << std::endl;
            std::cout << "ptr2 заменяется на предыдущее значение массива префикс-значений == " << prefix[ptr2 - 1] << std::endl << std::endl;
            ptr2 = prefix[ptr2 - 1];
        }

        if (pattern[ptr1] == pattern[ptr2]) {
            std::cout << "Символы на позициях (" << ptr1 << ") и (" << ptr2 << ") совпали" << std::endl;
            std::cout << "ptr2 увеличивается на 1" << std::endl;
            ++ptr2;
            std::cout << "prefix[" << ptr1 << "] == " << ptr2 << std::endl;
            prefix[ptr1] = ptr2;
            std::cout << "ptr1 увеличивается на 1" << std::endl << std::endl;
            continue;
        }

        std::cout << "Символы на позициях (" << ptr1 << ") и (" << ptr2 << ") различны" << std::endl;
        std::cout << "prefix[" << ptr1 << "] == 0" << std::endl;
        prefix[ptr1] = 0;
            std::cout << "ptr1 увеличивается на 1" << std::endl << std::endl;
    }

    return prefix;
}

int shift_algorithm(std::string a, std::string b) {
    if (a == b) {
        std::cout << "Строки равны" << std::endl;
        return 0;
    }

    if (a.size() != b.size()) {
        std::cout << "Размеры строк различны" << std::endl;
        return -1;
    }

    std::vector<int> prefix = prefixFunc(a);

    std::cout << "Полученные значения префикс функции для каждого символа паттерна:" << std::endl;
    for (int i = 0; i < a.size(); ++i) {
        std::cout << a[i] << " ";
    }
    std::cout << std::endl;

    for (int i = 0; i < a.size(); ++i) {
        std::cout << prefix[i] << " ";
    }
    std::cout << std::endl << std::endl;

    int ptrA = 0;

    std::cout << "\033[31m" << "Вычисление сдвига" << "\033[0m" << std::endl << std::endl;

    for (int ptrB = 0; ptrB < b.size() * 2; ++ptrB) {
        while (ptrA > 0 && a[ptrA] != b[ptrB % b.size()]) {
            std::cout << "ptrA > 0 и символы " << a[ptrA] << "(" << ptrA << ") и " << b[ptrB % b.size()] << "(" << ptrB << ") различны" << std::endl;
            std::cout << "ptrA заменяется на предыдущее значение массива префикс-значений == " << prefix[ptrA - 1] << std::endl << std::endl;
            ptrA = prefix[ptrA - 1];
        }

        if (a[ptrA] == b[ptrB % b.size()]) {
            if (ptrB >= b.size()) {
                std::cout << "Символы на позициях (" << ptrA << ") и (" << ptrB % b.size() << ") - по модулю длины, совпали" << std::endl;
            } else {
                std::cout << "Символы на позициях (" << ptrA << ") и (" << ptrB % b.size() << ") совпали" << std::endl;
            }

            if (ptrA == a.size() - 1) {
                std::cout << "Полное совпадение" << std::endl << std::endl;
                return (b.size()*2 - (ptrB + 1)) % b.size();
            }

            std::cout << "ptrA увеличивается на 1" << std::endl;
            std::cout << "ptrB увеличивается на 1" << std::endl << std::endl;
            ++ptrA;
            continue;
        }
        std::cout << "Символы на позициях (" << ptrA << ") и (" << ptrB % b.size() << ") различны" << std::endl;
        std::cout << "ptrB увеличивается на 1" << std::endl << std::endl;

    }

    return -1;
}

int main() {
    std::string a, b;
    
    std::cout << "Введи строку A:" << std::endl;
    std::cin >> a;

    std::cout << "Введи строку B:" << std::endl;
    std::cin >> b;
    std::cout << std::endl;
    
    int answer = shift_algorithm(a, b);

    if (answer == -1) {
        std::cout << -1 << std::endl;
        std::cout << "B не является циклическим сдвигом A" << std::endl;
        return 0;
    }

    std::cout << "Смещение на " << answer  << std::endl;

    for (int i = 0; i < a.size(); ++i) {
        if (i < answer) {
            std::cout << "\033[31m" << a[i] << "\033[0m";
        } else {
            std::cout << "\033[34m" << a[i] << "\033[0m";
        }
    }
    std::cout << std::endl;
}
