# ������ ����� 4 �����
# ��������� � ��������� ������������ 32-������ ����� 
#(� ���� ��� ���������� �������� ��������), ��� ������ ��������� ���� ����� ����:
BLOCK_SIZE =  4

# �������� ���� �������� �������� �� ������ 2
# ������ ���� ������� ������� �������� � ���������������
#������ ������� �������, � ��������� ������� � ������ (��������) ������:
def GOST_Magma_Add(a,b,c):
	for i in range(BLOCK_SIZE):
		c[i] = a[i]^b[i]
        
# �������� ���� �������� �������� �� ������ 32
#��� �������� 4-�������� ������� �������������� ��� ��� 32-������ �����,
#����� ��� ������������, ������������, ���� ��� ����������, �������������:
def GOST_Magma_Add_32(a,b,c):
	internal = 0
	for i in range(3,-1,-1):
		internal = a[i]+b[i]+(internal>>8)
		c[i] = internal&0xff

# ���������� ���������� �������������� (�������������� T)
# ������������ ��������� ������� ������������
Pi = [[1,7,14,13,0,5,8,3,4,15,10,6,9,12,11,2],[8,14,2,5,6,9,1,12,15,4,11,0,13,10,3,7],[5,13,15,6,9,2,12,10,11,7,8,1,4,3,14,0],[7,15,5,10,8,1,6,13,0,9,3,14,11,4,2,12],[12,8,2,1,13,4,15,6,7,0,10,5,3,14,9,11],[11,3,5,8,2,15,10,13,14,1,7,4,12,9,6,0],[6,8,2,3,9,10,5,12,1,14,4,7,11,13,0,15],[12,4,6,2,10,5,11,9,14,8,13,7,0,3,15,1]]

# ��������� � ������ ��������� (�� ��������� ��������) ������� ���� ������� � �����,
#� ��������� � ������, �� ��� ���������� ������ ��������� ������ ������� ����������
#���������� � �������� �������, � �� ���, ��� �������� � ���������.
def GOST_Magma_T(in_data,out_data):
	for i in range(4):
		# ��������� ������ 4-������ ����� �����
		first_part_byte = (in_data[i]&0xf0)>>4
		# ��������� ������ 4-������ ����� �����
		sec_part_byte = (in_data[i]&0x0f)
		# ��������� ������ � ������������ � �������� �����������
		first_part_byte = Pi[i*2][first_part_byte]
		sec_part_byte = Pi[i*2+1][sec_part_byte]
		# ���������� ��� 4-������ ����� ������� � ����
		out_data[i] = (first_part_byte << 4) | sec_part_byte
# ������������� ������
# ��� �������������� � ��������������� ��� ����� �������� ��� ������������ 32-������ �����, ������� ���������� �� ��������� 256-�������.
iter_key = [[0 for j in range(4)] for i in range(32)]
# ����� ����������� ��� ����.
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
	# ����� ����� 2 �������
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
	# � ����� ����� ������������ � �������� �������
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

# �������������� g
# ��� �������������� �������� � ���� �������� ������ ����� �����
#� ������������ ������ �� ������ 32, ���������� ���������� ��������������
#� ����� ����� �� ����������� ��������:
def GOST_Magma_g(k,a,out_data):
	internal = [0 for i in range(4)]
	# ���������� �� ������ 32 ������ �������� ����� � ������������ ������
	GOST_Magma_Add_32(a,k,internal)
	# ���������� ���������� ���������� �������������� ����������
	GOST_Magma_T(internal,internal)
	# ��������������� �������������� ������ � ���� 32-������ �����
	out_data_32 = internal[0]
	out_data_32 = (out_data_32<<8)+internal[1]
	out_data_32 = (out_data_32<<8)+internal[2]
	out_data_32 = (out_data_32<<8)+internal[3]
	# ���������� �������� ��� ����� �� 11 ��������
	out_data_32 = (out_data_32<<11)|(out_data_32>>21)
	# ��������������� 32-������ ��������� ������ ������� � 4-�������� ������
	out_data[3] = out_data_32&0xFF
	out_data[2] = (out_data_32>>8)&0xFF
	out_data[1] = (out_data_32>16)&0xFF
	out_data[0] = (out_data_32>>24)&0xFF

# �������������� G
# ��� �������������� ������������ ����� ���� �������� ����� �������������� 
#��� ��������������� (� ������ �� �������� ������). �������� � ���� �������������� g,
#�������� �� ������ 2 ���������� �������������� g � ������ ��������� �����
#� ����� ���������� ����� ������ � ����� ������ �����
def GOST_Magma_G(k,a,out_data):
	a_0 = [0 for i in range(4)] # ������ �������� �����
	a_1 = [0 for i in range(4)] # ����� �������� �����
	G = [0 for i in range(4)]
	# ����� 64-������ �������� ���� �� ��� �����
	for i in range(4):
		a_0[i] = a[4+i]
		a_1[i] = a[i]
	# ���������� �������������� g
	GOST_Magma_g(k,a_0,G)
	# ������ ��������� �������������� g � ����� ��������� �����
	GOST_Magma_Add(a_1,G,G)
	for i in range(4):
		# ����� � ����� �������� �������� �� ������
		a_1[i] = a_0[i]
		# ����� ��������� GOST_Magma_Add � ������ �������� �����
		a_0[i] = G[i]
	# ������ ������ � ����� ����� ����� � ���� �����
	for i in range(4):
		out_data[i] = a_1[i]
		out_data[4+i] = a_0[i]

# ��������� �������������� G
# ��� ��������� (�������� ������) �������� ����� ��������������
# ��� ���������������. �� �������� �������������� G ����������
#����������� ������ ���������� ����� ������ � ����� ������ ��������� �����
def GOST_Magma_G_Fin(k,a,out_data):
	a_0 = [0 for i in range(4)] # ������ �������� �����
	a_1 = [0 for i in range(4)] # ����� �������� �����
	G = [0 for i in range(4)]
	# ����� 64-������ �������� ���� �� ��� �����
	for i in range(4):
		a_0[i] = a[4+i]
		a_1[i] = a[i]
	# ���������� �������������� g
	GOST_Magma_g(k,a_0,G)
	# ������ ��������� �������������� g � ����� ��������� �����
	GOST_Magma_Add(a_1,G,G)
	# ����� ��������� GOST_Magma_Add � ����� �������� �����
	for i in range(4):
		a_1[i]=G[i]
	# ������ ������ � ����� ����� ����� � ���� �����
	for i in range(4):
		out_data[i] = a_1[i]
		out_data[4+i] = a_0[i]
# �������������
# ���������� ������������ ����� �������� ���� ��������, 
#� ������ �� �������� ������ � ����������� �������������� G
# � �������� ������ � ����������� ���������� �������������� G
def GOST_Magma_Encript(blk,out_blk):
	# ������ �������������� G
	GOST_Magma_G(iter_key[0],blk,out_blk)
	# ����������� (�� ������� �� �������� ������) �������������� G
	for i in range(1,31):
		GOST_Magma_G(iter_key[i],out_blk,out_blk)
	# ��������� (�������� ������) �������������� G
	GOST_Magma_G_Fin(iter_key[31],out_blk,out_blk)

# ��������������
# ��������������� ����������� ���������� ��������������
# � �������������� ������������ ������ � �������� �������
def GOST_Magma_Decript(blk,out_blk):
	# ������ �������������� G � �������������� �������� ������� ������������� �����
	GOST_Magma_G(iter_key[31],blk,out_blk)
	# ����������� (�� ������� �� �������� ������) �������������� G (������������ ����� ���� � �������� �������)
	for i in range(30,0,-1):
		GOST_Magma_G(iter_key[i],out_blk,out_blk)
	# ��������� (�������� ������) �������������� G � �������������� ������� ������������� �����
	GOST_Magma_G_Fin(iter_key[0],out_blk,out_blk)

# ������ ����
# ��������� ���� � ������
file_key = open("key.txt","r")
# ��������� ���� � ���� ������
key_raw = file_key.read(64)
# ��������� ����
file_key.close()
# ������ ������ ��� �����
key = [0 for i in range(32)]
# ��������� ������ ��������� ������
if (len(key_raw)==64):
	# ����� ��������� ������ � �������� �������� ��� �����
	for i in range(32):
		# ������ �� ��� ������� ����������������� �����
		tmp = key_raw[i*2]+key_raw[i*2+1]
		# ��������� � ������� �����
		key[i] = int(tmp,16)
else:
	# ���� ������ �� �����, �� ������������� ���� �� ���������
	print("Warning: unknown format key.txt. Set default key")
	key = [0xff,0xee,0xdd,0xcc,0xbb,0xaa,0x99,0x88,0x77,0x66,0x55,0x44,0x33,0x22,0x11,0x00,0xf0,0xf1,0xf2,0xf3,0xf4,0xf5,0xf6,0xf7,0xf8,0xf9,0xfa,0xfb,0xfc,0xfd,0xfe,0xff]
	print("Default key: ",key)

# ��������� ������� ��� ������������ �����
GOST_Magma_Expand_Key(key)
# ��������� �����
# ������ ��������� �� ������
file_hand = open("test.txt","rb")
# ������ � ������ ��������� �� ����������
# �� ������ ����� ������������� ���������� 256-������ ������
# � ������� ����� �������������� ����������
file_hand2 = open("test2.txt","wb")
file_hand3 = open("test3.txt","wb")
# ������ �����, ������������� � ����������
# ���� ������ �� ��������� �� 8 ���� ����� � �������� ����
# ������ ������ 8 ��������
data_byte = file_hand.read(8)
while data_byte:
	# ��������� ��� bytes � ��� list
	# ������ � data ����� ����������� ������ � �������� ������
	data = list(data_byte)
	# ���������, ����� ����� ���� ����� ������
	# ���� �� 8, �� � ����� ���������� �������
	if len(data)!=8:
		data1 = [32 for i in range(8)]
		for i in range(len(data)):
			data1[i] = data[i]
		data = data1.copy()
	# ������ ������ �������� ������ ������ �� �������
	# � out_data ����� �������� ������������� �������� � ������
	out_data = data.copy()
	# ���������� ����������
	GOST_Magma_Encript(data,out_data)
	# ������ out_data2 ��� �����������
	out_data2 = out_data.copy()
	# �������� � data2 ������������� ������ �� ����������
	data2 = out_data.copy()
	# ��������������
	GOST_Magma_Decript(data2,out_data2)
	# ��������� ������ �������� �������� � ����� ��� ������ � ����
	out_data_byte = bytes(out_data)
	out_data_byte2 = bytes(out_data2)
	# ���������� � ���� �������� ����������
	file_hand2.write(out_data_byte)
	file_hand3.write(out_data_byte2)
	# ������ �� ����� ��������� 8 ����
	data_byte = file_hand.read(8)
	# ����� ��������� � ������ �������� ��������
	data = list(data_byte)
# ��������� �����
file_hand.close()
file_hand2.close()
file_hand3.close()
