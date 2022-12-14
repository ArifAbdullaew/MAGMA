# Размер блока 4 байта
# Поскольку в алгоритме используются 32-битные блоки 
#(в виде так называемых двоичных векторов), для начала определим этот самый блок:
BLOCK_SIZE =  4

# Сложение двух двоичных векторов по модулю 2
# Каждый байт первого вектора ксорится с соответствующим
#байтом второго вектора, и результат пишется в третий (выходной) вектор:
def GOST_Magma_Add(a,b,c):
	for i in range(BLOCK_SIZE):
		c[i] = a[i]^b[i]
        
# Сложение двух двоичных векторов по модулю 32
#Два исходных 4-байтовых вектора представляются как два 32-битных числа,
#далее они складываются, переполнение, если оно появляется, отбрасывается:
def GOST_Magma_Add_32(a,b,c):
	internal = 0
	for i in range(3,-1,-1):
		internal = a[i]+b[i]+(internal>>8)
		c[i] = internal&0xff

# Нелинейное биективное преобразование (преобразование T)
# Используется следующая таблица перестановок
Pi = [[1,7,14,13,0,5,8,3,4,15,10,6,9,12,11,2],[8,14,2,5,6,9,1,12,15,4,11,0,13,10,3,7],[5,13,15,6,9,2,12,10,11,7,8,1,4,3,14,0],[7,15,5,10,8,1,6,13,0,9,3,14,11,4,2,12],[12,8,2,1,13,4,15,6,7,0,10,5,3,14,9,11],[11,3,5,8,2,15,10,13,14,1,7,4,12,9,6,0],[6,8,2,3,9,10,5,12,1,14,4,7,11,13,0,15],[12,4,6,2,10,5,11,9,14,8,13,7,0,3,15,1]]

# Поскольку в тексте стандарта (по неведомой традиции) нулевой байт пишется в конце,
#а последний в начале, то для корректной работы программы строки таблицы необходимо
#записывать в обратном порядке, а не так, как изложено в стандарте.
def GOST_Magma_T(in_data,out_data):
	for i in range(4):
		# Извлекаем первую 4-битную часть байта
		first_part_byte = (in_data[i]&0xf0)>>4
		# Извлекаем вторую 4-битную часть байта
		sec_part_byte = (in_data[i]&0x0f)
		# Выполняем замену в соответствии с таблицей подстановок
		first_part_byte = Pi[i*2][first_part_byte]
		sec_part_byte = Pi[i*2+1][sec_part_byte]
		# «Склеиваем» обе 4-битные части обратно в байт
		out_data[i] = (first_part_byte << 4) | sec_part_byte
# Развертывание ключей
# Для зашифровывания и расшифровывания нам нужно тридцать два итерационных 32-битных ключа, которые получаются из исходного 256-битного.
iter_key = [[0 for j in range(4)] for i in range(32)]
# Здесь развёртываем сам ключ.
def GOST_Magma_Expand_Key(key):
	for i in range(4):
		iter_key[0][i] = key[i]
	for i in range(4):
		iter_key[1][i] = key[i+4]
	for i in range(4):
		iter_key[2][i] = key[i+8]
	for i in range(4):
		iter_key[3][i] = key[i+12]
	for i in range(4):
		iter_key[4][i] = key[i+16]
	for i in range(4):
		iter_key[5][i] = key[i+20]
	for i in range(4):
		iter_key[6][i] = key[i+24]
	for i in range(4):
		iter_key[7][i] = key[i+28]
	for i in range(4):
	# Здесь снова 2 повтора
		iter_key[8][i] = key[i]
	for i in range(4):
		iter_key[9][i] = key[i+4]
	for i in range(4):
		iter_key[10][i] = key[i+8]
	for i in range(4):
		iter_key[11][i] = key[i+12]
	for i in range(4):
		iter_key[12][i] = key[i+16]
	for i in range(4):
		iter_key[13][i] = key[i+20]
	for i in range(4):
		iter_key[14][i] = key[i+24]
	for i in range(4):
		iter_key[15][i] = key[i+28]
	for i in range(4):
		iter_key[16][i] = key[i]
	for i in range(4):
		iter_key[17][i] = key[i+4]
	for i in range(4):
		iter_key[18][i] = key[i+8]
	for i in range(4):
		iter_key[19][i] = key[i+12]
	for i in range(4):
		iter_key[20][i] = key[i+16]
	for i in range(4):
		iter_key[21][i] = key[i+20]
	for i in range(4):
		iter_key[22][i] = key[i+24]
	for i in range(4):
		iter_key[23][i] = key[i+28]
	# А здесь байты записываются в обратном порядке
	for i in range(4):
		iter_key[24][i] = key[i+28]
	for i in range(4):
		iter_key[25][i] = key[i+24]
	for i in range(4):
		iter_key[26][i] = key[i+20]
	for i in range(4):
		iter_key[27][i] = key[i+16]
	for i in range(4):
		iter_key[28][i] = key[i+12]
	for i in range(4):
		iter_key[29][i] = key[i+8]
	for i in range(4):
		iter_key[30][i] = key[i+4]
	for i in range(4):
		iter_key[31][i] = key[i]

# Преобразование g
# Это преобразование включает в себя сложение правой части блока
#с итерационным ключом по модулю 32, нелинейное биективное преобразование
#и сдвиг влево на одиннадцать разрядов:
def GOST_Magma_g(k,a,out_data):
	internal = [0 for i in range(4)]
	# Складываем по модулю 32 правую половину блока с итерационным ключом
	GOST_Magma_Add_32(a,k,internal)
	# Производим нелинейное биективное преобразование результата
	GOST_Magma_T(internal,internal)
	# Преобразовываем четырехбайтный вектор в одно 32-битное число
	out_data_32 = internal[0]
	out_data_32 = (out_data_32<<8)+internal[1]
	out_data_32 = (out_data_32<<8)+internal[2]
	out_data_32 = (out_data_32<<8)+internal[3]
	# Циклически сдвигаем все влево на 11 разрядов
	out_data_32 = (out_data_32<<11)|(out_data_32>>21)
	# Преобразовываем 32-битный результат сдвига обратно в 4-байтовый вектор
	out_data[3] = out_data_32&0xFF
	out_data[2] = (out_data_32>>8)&0xFF
	out_data[1] = (out_data_32>16)&0xFF
	out_data[0] = (out_data_32>>24)&0xFF

# Преобразование G
# Это преобразование представляет собой одну итерацию цикла зашифровывания 
#или расшифровывания (с первой по тридцать первую). Включает в себя преобразование g,
#сложение по модулю 2 результата преобразования g с правой половиной блока
#и обмен содержимым между правой и левой частью блока
def GOST_Magma_G(k,a,out_data):
	a_0 = [0 for i in range(4)] # Правая половина блока
	a_1 = [0 for i in range(4)] # Левая половина блока
	G = [0 for i in range(4)]
	# Делим 64-битный исходный блок на две части
	for i in range(4):
		a_0[i] = a[4+i]
		a_1[i] = a[i]
	# Производим преобразование g
	GOST_Magma_g(k,a_0,G)
	# Ксорим результат преобразования g с левой половиной блока
	GOST_Magma_Add(a_1,G,G)
	for i in range(4):
		# Пишем в левую половину значение из правой
		a_1[i] = a_0[i]
		# Пишем результат GOST_Magma_Add в правую половину блока
		a_0[i] = G[i]
	# Сводим правую и левую части блока в одно целое
	for i in range(4):
		out_data[i] = a_1[i]
		out_data[4+i] = a_0[i]

# Финальное преобразование G
# Это последняя (тридцать вторая) итерация цикла зашифровывания
# или расшифровывания. От простого преобразования G отличается
#отсутствием обмена значениями между правой и левой частью исходного блока
def GOST_Magma_G_Fin(k,a,out_data):
	a_0 = [0 for i in range(4)] # Правая половина блока
	a_1 = [0 for i in range(4)] # Левая половина блока
	G = [0 for i in range(4)]
	# Делим 64-битный исходный блок на две части
	for i in range(4):
		a_0[i] = a[4+i]
		a_1[i] = a[i]
	# Производим преобразование g
	GOST_Magma_g(k,a_0,G)
	# Ксорим результат преобразования g с левой половиной блока
	GOST_Magma_Add(a_1,G,G)
	# Пишем результат GOST_Magma_Add в левую половину блока
	for i in range(4):
		a_1[i]=G[i]
	# Сводим правую и левую части блока в одно целое
	for i in range(4):
		out_data[i] = a_1[i]
		out_data[4+i] = a_0[i]
# Зашифрорываем
# шифрование производится путем тридцати двух итераций, 
#с первой по тридцать первую с применением преобразования G
# и тридцать вторую с применением финального преобразования G
def GOST_Magma_Encript(blk,out_blk):
	# Первое преобразование G
	GOST_Magma_G(iter_key[0],blk,out_blk)
	# Последующие (со второго по тридцать первое) преобразования G
	for i in range(1,31):
		GOST_Magma_G(iter_key[i],out_blk,out_blk)
	# Последнее (тридцать второе) преобразование G
	GOST_Magma_G_Fin(iter_key[31],out_blk,out_blk)

# Расшифровываем
# Расшифровывание выполняется аналогично зашифровыванию
# с использованием итерационных ключей в обратном порядке
def GOST_Magma_Decript(blk,out_blk):
	# Первое преобразование G с использованием тридцать второго итерационного ключа
	GOST_Magma_G(iter_key[31],blk,out_blk)
	# Последующие (со второго по тридцать первое) преобразования G (итерационные ключи идут в обратном порядке)
	for i in range(30,0,-1):
		GOST_Magma_G(iter_key[i],out_blk,out_blk)
	# Последнее (тридцать второе) преобразование G с использованием первого итерационного ключа
	GOST_Magma_G_Fin(iter_key[0],out_blk,out_blk)

# Вводим ключ
# Открываем файл с ключом
file_key = open("key.txt","r")
# Считываем ключ в виде строки
key_raw = file_key.read(64)
# Закрываем файл
file_key.close()
# Создаём массив для ключа
key = [0 for i in range(32)]
# Проверяем размер считанных данных
if (len(key_raw)==64):
	# Здесь переводим строку в числовые значения для ключа
	for i in range(32):
		# Читаем по два символа шестнадцатиричное число
		tmp = key_raw[i*2]+key_raw[i*2+1]
		# Переводим в обычное число
		key[i] = int(tmp,16)
else:
	# Если размер не верен, то устанавливаем ключ по умолчанию
	print("Warning: unknown format key.txt. Set default key")
	key = [0xff,0xee,0xdd,0xcc,0xbb,0xaa,0x99,0x88,0x77,0x66,0x55,0x44,0x33,0x22,0x11,0x00,0xf0,0xf1,0xf2,0xf3,0xf4,0xf5,0xf6,0xf7,0xf8,0xf9,0xfa,0xfb,0xfc,0xfd,0xfe,0xff]
	print("Default key: ",key)

# Запускаем функцию для развёртывания ключа
GOST_Magma_Expand_Key(key)
# Открываем файлы
# Первый открываем на чтение
file_hand = open("test.txt","rb")
# Второй и третий открываем на записывать
# Во втором будет зашифрованная информация 256-битным ключом
# В Третьем будет расшифрованная информация
file_hand2 = open("test2.txt","wb")
file_hand3 = open("test3.txt","wb")
# Читаем файлы, зашифровываем и записываем
# Весь массив мы считываем по 8 байт сразу в двоичном виде
# Читаем первые 8 символов
data_byte = file_hand.read(8)
while data_byte:
	# Переводим тип bytes в тип list
	# Теперь в data будет содержаться список с номерами байтов
	data = list(data_byte)
	# Проверяем, чтобы длина была равна восьми
	# Если не 8, то в конец дописываем пробелы
	if len(data)!=8:
		data1 = [32 for i in range(8)]
		for i in range(len(data)):
			data1[i] = data[i]
		data = data1.copy()
	# Создаём массив выходных данных такого же размера
	# В out_data будет записано зашифрованные значения в список
	out_data = data.copy()
	# Производим зашифровку
	GOST_Magma_Encript(data,out_data)
	# Создаём out_data2 для расшифровки
	out_data2 = out_data.copy()
	# Копируем в data2 зашифрованный список со значениями
	data2 = out_data.copy()
	# Расшифровываем
	GOST_Magma_Decript(data2,out_data2)
	# Переводим список числовых значений в байты для записи в файл
	out_data_byte = bytes(out_data)
	out_data_byte2 = bytes(out_data2)
	# Записываем в файл байтовые переменные
	file_hand2.write(out_data_byte)
	file_hand3.write(out_data_byte2)
	# Читаем из файла следующие 8 байт
	data_byte = file_hand.read(8)
	# Снова переводим в список числовых значений
	data = list(data_byte)
# Закрываем файлы
file_hand.close()
file_hand2.close()
file_hand3.close()
