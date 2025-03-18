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

std::vector<int> kmp_algorithm(std::string text, std::string pattern) {
    std::vector<int> prefix = prefixFunc(pattern);

    std::cout << "Полученные значения префикс функции для каждого символа паттерна:" << std::endl;
    for (int i = 0; i < prefix.size(); ++i) {
        std::cout << pattern[i] << " ";
    }
    std::cout << std::endl;

    for (int i = 0; i < prefix.size(); ++i) {
        std::cout << prefix[i] << " ";
    }
    std::cout << std::endl << std::endl;

    int ptrPattern = 0;
    int ptrText = 0;
    std::vector<int> answer;

    std::cout << "\033[31m" << "Вычисление вхождений" << "\033[0m" << std::endl << std::endl;

    while (ptrText < text.size()) {
        while (ptrPattern > 0 && text[ptrText] != pattern[ptrPattern]) {
            std::cout << "ptrPattern > 0 и символы " << pattern[ptrText] << "(" << ptrText << ") и " << pattern[ptrPattern] << "(" << ptrPattern << ") различны" << std::endl;
            std::cout << "ptrPattern заменяется на предыдущее значение массива префикс-значений == " << prefix[ptrPattern - 1] << std::endl << std::endl;
            ptrPattern = prefix[ptrPattern - 1];
        }

        if (text[ptrText] == pattern[ptrPattern]) {
            std::cout << "Символы на позициях текста (" << ptrText << ") и паттерна (" << ptrPattern << ") совпали" << std::endl;

            if (ptrPattern == pattern.size() - 1) {
                std::cout << "Полное совпадение шаблону в интервале {" << ptrText - (pattern.size() - 1) << ":" << ptrText << "}" << std::endl;
                answer.push_back(ptrText - (pattern.size() - 1));
                std::cout << "ptrPattern перемещается в " << prefix[ptrPattern] << std::endl;
                ptrPattern = prefix[ptrPattern];
            } else {
                std::cout << "ptrPattern увеличивается на 1" << std::endl;                
                ++ptrPattern;
            }
            
            std::cout << "ptrText увеличивается на 1" << std::endl << std::endl;
            ++ptrText;
            continue;
        }

        std::cout << "Символы на позициях текста (" << ptrText << ") и паттерна (" << ptrPattern << ") различны" << std::endl;
                
        if (ptrPattern == 0) {
            std::cout << "Начало паттерна не совпало с текущей позицией в тексте. ptrText увеличивается на 1." << std::endl << std::endl;
            ++ptrText;
            continue;
        }
    }

    return answer;
}

int main() {
    std::string pattern, text;

    std::cout << "Введи паттерн:" << std::endl;
    std::cin >> pattern;

    std::cout << "Введи текст:" << std::endl;
    std::cin >> text;
    std::cout << std::endl;

    std::vector<int> answer = kmp_algorithm(text, pattern);
    
    if (answer.size() == 0) {
        std::cout << -1 << std::endl;
        std::cout << "Вхождений не обнаружено." << std::endl;
        return 0;
    }

    std::cout << "Полученные вхождения:" << std::endl;
    for (int i = 0; i < answer.size(); ++i) {
        if (i == answer.size() - 1) {
            std::cout << answer[i];
            continue;
        }
        std::cout << answer[i] << ","; 
    }
    std::cout << std::endl << std::endl;

    for (int i = 0; i < text.size(); ++i) {
        int flag = 1;
        for (int j = 0; j < answer.size(); ++j) {
            if (i >= answer[j] && i < answer[j] + pattern.size()) {
                std::cout << "\033[31m" << text[i] << "\033[0m";
                flag = 0;
                break;
            }    
        }
        if (flag) {
            std::cout << text[i];
        }
    }
    std::cout << std::endl;
}
