## Solution 1
Первая функция более читаема и более быстрая по сравнению со второй\
Вторая функция использует другой подход к решению задачи определения чётности числа,\
она использует последний знак двоичного представления числа, который в свою очередь\
может быть либо 0, либо 1, что в переводе в десятичную систему означает 0 или 1,\
а так как двоичные числа представляются в виде 1 2 4 8 16 32 и т.д., единственный способ\
сделать число нечётным, это использовать первый знак, поэтому функция отрабатывает корректно,\
но данный подход более затратен к времени и памяти.
## Solution 2
### FIFO cycle buffer на основе массива
Моя реализация подразумевает выделение ограниченного диапазона памяти,\
который хранит ссылки на значения массива, что вносит некоторую\
абстрагированность относительно других способов реализации.\
С точки зрения читаемости такой код менее дружелюбен,\
так как необходимо учитывать расположение указателей (чтобы они не вышли за пределы списка).
### FIFO cycle buffer на основе связного списка
Такая реализация более читаема и поддерживаема по сравнению с прошлой.\
Я считаю её поведение более предсказуемым, так как сама суть связного списка\
подразумевает его упорядоченность.
### Сравнение
<strong>Память:</strong> 2 способ для хранения указатели для каждого элемента связного списка,\
в то время как 1 способ использует только для крайних элементов.\
<strong>Время:</strong> с помощью стресс тестов получил следующие результаты:
1) Массив - Time: 37.853026390075684
2) Связн. список - Time: 36.296998739242554

Таким образом, учитывая погрешность и характеристики процессора, можно сказать,\
что второй способ работает немного быстрее.
### P.S.
Можно переписать первый способ для увеличения читаемости, но теряя в абстрагированности,\
за счёт отказа от указателей. В таком новом виде он будет напоминать связный список,\
но данные будут находиться в одном месте. Я не стал реализовывать такой способ,\
но в случае необходимости я бы использовал библиотеку heapq.
# Solution 3
Первый алгоритм, который мне пришёл в голову это merge sort. Основой которого является\
рекурсия, разделяющая существующий массив на более маленькие подмассивы и сортирующая их.\
Я считаю этот алгоритм одним из самых быстрых, так как его временная сложность O(n*log n)\
и она постоянна, вне зависимости от длины массива.