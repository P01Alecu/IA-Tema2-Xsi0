import time
import copy
import pygame
import sys


ADANCIME_MAX=4


def elem_identice(lista):
	if(len(set(lista))==1) :
		return lista[0] if lista[0]!=Joc.GOL else False
	return False


class Joc:
	"""
	Clasa care defineste jocul. Se va schimba de la un joc la altul.
	"""
	JMIN=None
	JMAX=None
	GOL='#'
	NR_LINII=None
	NR_COLOANE=None
	scor_maxim=0
	def __init__(self, matr=None, NR_LINII=None, NR_COLOANE=None):
		#creez proprietatea ultima_mutare # (l,c)
		self.ultima_mutare=None

		if matr:
			#e data tabla, deci suntem in timpul jocului
			self.matr=matr 
		else:
			#nu e data tabla deci suntem la initializare
			self.matr= [[self.__class__.GOL] * NR_COLOANE for i in range(NR_LINII)]
		 
			if NR_LINII is not None:
				self.__class__.NR_LINII= NR_LINII
			if NR_COLOANE is not None:
				self.__class__.NR_COLOANE= NR_COLOANE
			
			######## calculare scor maxim ###########
			sc_randuri=(NR_COLOANE-3)*NR_LINII
			sc_coloane = (NR_LINII - 3)*NR_COLOANE
			sc_diagonale = (NR_LINII - 3) * (NR_COLOANE - 3) * 2
			self.__class__.scor_maxim = sc_randuri + sc_coloane + sc_diagonale

	

	def deseneaza_grid(self, coloana_marcaj=None, stare_curenta=None): # tabla de exemplu este ["#","x","#","0",......]
		"""
		Deseneaza grid

		Coloreaza cu rosu patratelele pierzatoare
		"""
		pozitii_pierzatoare = []
		if stare_curenta != None:
			if stare_curenta.tabla_joc.final():
				directii = [[(0, 1), (0, -1)], [(1, 1), (-1, -1)], [(1, -1), (-1, 1)], [(1, 0), (-1, 0)]]
				for dir in directii:
					pozitionare_temporar = []
					nr_mutari1 = 0
					nr_mutari2 = 0
					um1 = self.ultima_mutare # (l,c)
					um2 = self.ultima_mutare # (l,c)
					culoare = self.matr[um1[0]][um1[1]]
					while True:
						um1 = (um1[0] + dir[0][0], um1[1] + dir[0][1])
						if not 0 <= um1[0] < self.__class__.NR_LINII or not 0 <= um1[1] < self.__class__.NR_COLOANE:
							break
						if not self.matr[um1[0]][um1[1]] == culoare:
							break
						pozitionare_temporar.append(um1)
						nr_mutari1 += 1

					while True:
						um2 = (um2[0] + dir[1][0], um2[1] + dir[1][1])
						if not 0 <= um2[0] < self.__class__.NR_LINII or not 0 <= um2[1] < self.__class__.NR_COLOANE:
							break
						if not self.matr[um2[0]][um2[1]] == culoare:
							break
						pozitionare_temporar.append(um2)
						nr_mutari2 += 1

					if len(pozitionare_temporar) >= 2:
						pozitii_pierzatoare = pozitionare_temporar
						pozitii_pierzatoare.append(stare_curenta.tabla_joc.ultima_mutare)
						break


		for ind in range(self.__class__.NR_COLOANE*self.__class__.NR_LINII):
			linie=ind // self.__class__.NR_COLOANE # // inseamna div
			coloana=ind % self.__class__.NR_COLOANE

			if stare_curenta != None:
				simbol_pierzator = '0'
				if stare_curenta.tabla_joc.final() == '0':
					simbol_pierzator = 'x'
				else:
					simbol_pierzator = '0'
				if stare_curenta.tabla_joc.final() and len(pozitii_pierzatoare) > 0:
					for i in range(0, len(pozitii_pierzatoare)):
						if linie == pozitii_pierzatoare[i][0] and coloana == pozitii_pierzatoare[i][1]:
							culoare=(255,0,0)
							break
						else:
							culoare=(255,255,255)
				else:
					culoare=(255,255,255)

			else:
				#altfel o desenez cu alb
				culoare=(255,255,255)

			pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind]) #alb = (255,255,255)
			if self.matr[linie][coloana]=='x':
				self.__class__.display.blit(self.__class__.x_img,(coloana*(self.__class__.dim_celula+1),linie*(self.__class__.dim_celula+1)))
			elif self.matr[linie][coloana]=='0':
				self.__class__.display.blit(self.__class__.zero_img,(coloana*(self.__class__.dim_celula+1),linie*(self.__class__.dim_celula+1)))
		pygame.display.update()			

	@classmethod
	def jucator_opus(cls, jucator):
		return cls.JMAX if jucator==cls.JMIN else cls.JMIN


	@classmethod
	def initializeaza(cls, display, NR_LINII=6, NR_COLOANE=7, dim_celula=100):
		cls.display=display
		cls.dim_celula=dim_celula
		cls.x_img = pygame.image.load('ics.png')
		cls.x_img = pygame.transform.scale(cls.x_img, (dim_celula,dim_celula))
		cls.zero_img = pygame.image.load('zero.png')
		cls.zero_img = pygame.transform.scale(cls.zero_img, (dim_celula,dim_celula))
		cls.celuleGrid=[] #este lista cu patratelele din grid
		for linie in range(NR_LINII):
			for coloana in range(NR_COLOANE):
				patr = pygame.Rect(coloana*(dim_celula+1), linie*(dim_celula+1), dim_celula, dim_celula)
				cls.celuleGrid.append(patr)

	def parcurgere(self, directie):
		um = self.ultima_mutare # (l,c)
		culoare = self.matr[um[0]][um[1]]
		nr_mutari = 0
		while True:
			um = (um[0] + directie[0], um[1] + directie[1])
			if not 0 <= um[0] < self.__class__.NR_LINII or not 0 <= um[1] < self.__class__.NR_COLOANE:
				break
			if not self.matr[um[0]][um[1]] == culoare:
				break
			nr_mutari += 1
		return nr_mutari
		
	def final(self):
		if not self.ultima_mutare: #daca e inainte de prima mutare
			return False
		directii = [[(0, 1), (0, -1)], [(1, 1), (-1, -1)], [(1, -1), (-1, 1)], [(1, 0), (-1, 0)]]
		um = self.ultima_mutare
		rez = False
		for per_dir in directii:
			len_culoare = self.parcurgere(per_dir[0]) + self.parcurgere(per_dir[1]) + 1 # +1 pt chiar ultima mutare
			if len_culoare >= 3:
				rez = self.matr[um[0]][um[1]]

		if(rez):
			if rez == 'x':
				return '0'
			if rez == '0':
				return 'x'
			return rez
			
		elif all(self.__class__.GOL not in x for x in self.matr):
			return 'remiza'
		else:
			return False

	def mutari(self, jucator):
		l_mutari=[]
		for j in range(self.__class__.NR_COLOANE):
			last_poz = None
			if self.matr[0][j] != self.__class__.GOL:
				continue
			for i in range(self.__class__.NR_LINII):
				if self.matr[i][j]!=self.__class__.GOL:
						last_poz = (i-1,j)
						break			 
			if last_poz is None:
				last_poz = (self.__class__.NR_LINII-1, j)
			matr_tabla_noua = copy.deepcopy(self.matr)
			matr_tabla_noua[last_poz[0]][last_poz[1]] = jucator
			jn=Joc(matr_tabla_noua)
			jn.ultima_mutare=(last_poz[0],last_poz[1])
			l_mutari.append(jn)
		return l_mutari


	#linie deschisa inseamna linie pe care jucatorul mai poate forma o configuratie castigatoare
	#practic e o linie fara simboluri ale jucatorului opus
	def linie_deschisa(self,lista, jucator):
		jo=self.jucator_opus(jucator)
		#verific daca pe linia data nu am simbolul jucatorului opus
		if not jo in lista:
				#return 1
				return lista.count(jucator)
		return 0
			
	def linii_deschise(self, jucator):
		
		linii = 0
		for i in range(self.__class__.NR_LINII):
			for j in range(self.__class__.NR_COLOANE - 3):
				linii += self.linie_deschisa(self.matr[i][j:j + 4], jucator)
				
		for j in range(self.__class__.NR_COLOANE):
			for i in range(self.__class__.NR_LINII - 3):
				linii += self.linie_deschisa([self.matr[k][j] for k in range(i, i + 4)],jucator)

		# \
		for i in range(self.__class__.NR_LINII - 3):
			for j in range(self.__class__.NR_COLOANE - 3):
				linii += self.linie_deschisa([self.matr[i+k][j+k] for k in range(0, 4)],jucator)
		
		# /
		for i in range(self.__class__.NR_LINII-3):
			for j in range(3, self.__class__.NR_COLOANE):
				linii += self.linie_deschisa([self.matr[i+k][j-k] for k in range(0, 4)],jucator)
		
		return linii

	def estimeaza_scor(self, adancime):
		t_final=self.final()
		#if (adancime==0):
		if t_final==self.__class__.JMAX :
			return (self.__class__.scor_maxim+adancime)
		elif t_final==self.__class__.JMIN:
			return (-self.__class__.scor_maxim-adancime)
		elif t_final=='remiza':
			return 0
		else:
			return (self.linii_deschise(self.__class__.JMAX)- self.linii_deschise(self.__class__.JMIN))
			
	def sirAfisare(self):
		sir="  |"
		sir+=" ".join([str(i) for i in range(self.NR_COLOANE)])+"\n"
		sir+="-"*(self.NR_COLOANE+1)*2+"\n"
		sir+= "\n".join([str(i)+" |"+" ".join([str(x) for x in self.matr[i]]) for i in range(len(self.matr))])
		return sir

	def __str__(self):
		return self.sirAfisare()

	def __repr__(self):
		return self.sirAfisare()	
	
			

class Stare:
	"""
	Clasa folosita de algoritmii minimax si alpha-beta
	Are ca proprietate tabla de joc
	Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
	De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
	"""
	def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
		self.tabla_joc=tabla_joc
		self.j_curent=j_curent
		
		#adancimea in arborele de stari
		self.adancime=adancime	
		
		#scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
		self.scor=scor
		
		#lista de mutari posibile din starea curenta
		self.mutari_posibile=[]
		
		#cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
		self.stare_aleasa=None



	def mutari(self):		
		l_mutari=self.tabla_joc.mutari(self.j_curent)
		juc_opus=Joc.jucator_opus(self.j_curent)
		l_stari_mutari=[Stare(mutare, juc_opus, self.adancime-1, parinte=self) for mutare in l_mutari]

		return l_stari_mutari
		
	
	def __str__(self):
		sir= str(self.tabla_joc) + "(Juc curent:"+self.j_curent+")\n"
		return sir	
	def __repr__(self):
		sir= str(self.tabla_joc) + "(Juc curent:"+self.j_curent+")\n"
		return sir
	

			
""" Algoritmul MinMax """

def min_max(stare):
	
	if stare.adancime==0 or stare.tabla_joc.final() :
		stare.scor=stare.tabla_joc.estimeaza_scor(stare.adancime)
		return stare
		
	#calculez toate mutarile posibile din starea curenta
	stare.mutari_posibile=stare.mutari()

	#aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
	mutari_scor=[min_max(mutare) for mutare in stare.mutari_posibile]
	


	if stare.j_curent==Joc.JMAX :
		#daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
		stare.stare_aleasa=max(mutari_scor, key=lambda x: x.scor)
	else:
		#daca jucatorul e JMIN aleg starea-fiica cu scorul minim
		stare.stare_aleasa=min(mutari_scor, key=lambda x: x.scor)
	stare.scor=stare.stare_aleasa.scor
	return stare
	

def alpha_beta(alpha, beta, stare):
	if stare.adancime==0 or stare.tabla_joc.final() :
		stare.scor=stare.tabla_joc.estimeaza_scor(stare.adancime)
		return stare
	
	if alpha>beta:
		return stare #este intr-un interval invalid deci nu o mai procesez
	
	stare.mutari_posibile=stare.mutari()


	if stare.j_curent==Joc.JMAX :
		scor_curent=float('-inf')
		
		for mutare in stare.mutari_posibile:
			#calculeaza scorul
			stare_noua=alpha_beta(alpha, beta, mutare)
			
			if (scor_curent<stare_noua.scor):
				stare.stare_aleasa=stare_noua
				scor_curent=stare_noua.scor
			if(alpha<stare_noua.scor):
				alpha=stare_noua.scor
				if alpha>=beta:
					break

	elif stare.j_curent==Joc.JMIN :
		scor_curent=float('inf')
		
		for mutare in stare.mutari_posibile:
			
			stare_noua=alpha_beta(alpha, beta, mutare)
			
			if (scor_curent>stare_noua.scor):
				stare.stare_aleasa=stare_noua
				scor_curent=stare_noua.scor

			if(beta>stare_noua.scor):
				beta=stare_noua.scor
				if alpha>=beta:
					break
	stare.scor=stare.stare_aleasa.scor

	return stare
	

def afis_daca_final(stare_curenta):
	final=stare_curenta.tabla_joc.final()
	if(final):
		if (final=="remiza"):
			print("Remiza!")
		else:
			print("A castigat "+final)

		mutari_jucator = 0
		mutari_calculator = 0
		for i in stare_curenta.tabla_joc.matr:
			mutari_jucator += i.count(stare_curenta.tabla_joc.JMIN)
			mutari_calculator += i.count(stare_curenta.tabla_joc.JMAX)
		print("Jucatorul a facut {0} mutari, iar calculatorul a facut {1} mutari.".format(mutari_jucator, mutari_calculator))

		return True
		
	return False

class Buton:
	def __init__(self, display=None, left=0, top=0, w=0, h=0,culoareFundal=(53,80,115), culoareFundalSel=(89,134,194), text="", font="arial", fontDimensiune=16, culoareText=(255,255,255), valoare=""):
		self.display=display		
		self.culoareFundal=culoareFundal
		self.culoareFundalSel=culoareFundalSel
		self.text=text
		self.font=font
		self.w=w
		self.h=h
		self.selectat=False
		self.fontDimensiune=fontDimensiune
		self.culoareText=culoareText
		#creez obiectul font
		fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
		self.textRandat=fontObj.render(self.text, True , self.culoareText) 
		self.dreptunghi=pygame.Rect(left, top, w, h) 
		#aici centram textul
		self.dreptunghiText=self.textRandat.get_rect(center=self.dreptunghi.center)
		self.valoare=valoare

	def selecteaza(self,sel):
		self.selectat=sel
		self.deseneaza()
	def selecteazaDupacoord(self,coord):
		if self.dreptunghi.collidepoint(coord):
			self.selecteaza(True)
			return True
		return False

	def updateDreptunghi(self):
		self.dreptunghi.left=self.left
		self.dreptunghi.top=self.top
		self.dreptunghiText=self.textRandat.get_rect(center=self.dreptunghi.center)

	def deseneaza(self):
		culoareF= self.culoareFundalSel if self.selectat else self.culoareFundal
		pygame.draw.rect(self.display, culoareF, self.dreptunghi)	
		self.display.blit(self.textRandat ,self.dreptunghiText) 

class GrupButoane:
	def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10,left=0, top=0):
		self.listaButoane=listaButoane
		self.indiceSelectat=indiceSelectat
		self.listaButoane[self.indiceSelectat].selectat=True
		self.top=top
		self.left=left
		leftCurent=self.left
		for b in self.listaButoane:
			b.top=self.top
			b.left=leftCurent
			b.updateDreptunghi()
			leftCurent+=(spatiuButoane+b.w)

	def selecteazaDupacoord(self,coord):
		for ib,b in enumerate(self.listaButoane):
			if b.selecteazaDupacoord(coord):
				self.listaButoane[self.indiceSelectat].selecteaza(False)
				self.indiceSelectat=ib
				return True
		return False

	def deseneaza(self):
		#atentie, nu face wrap
		for b in self.listaButoane:
			b.deseneaza()

	def getValoare(self):
		return self.listaButoane[self.indiceSelectat].valoare


############# ecran initial ########################
def deseneaza_alegeri(display, tabla_curenta) :
	btn_alg=GrupButoane(
		top=30, 
		left=30,  
		listaButoane=[
			Buton(display=display, w=80, h=30, text="minimax", valoare="minimax"), 
			Buton(display=display, w=80, h=30, text="alphabeta", valoare="alphabeta")
			],
		indiceSelectat=1)
	btn_juc=GrupButoane(
		top=70, 
		left=30, 
		listaButoane=[
			Buton(display=display, w=35, h=30, text="x", valoare="x"), 
			Buton(display=display, w=35, h=30, text="zero", valoare="0")
			], 
		indiceSelectat=0)
	dificultate_joc=GrupButoane(
		top=110,
		left=30,
		listaButoane=[
			Buton(display=display, w=50, h=30, text="Usor", valoare="usor"), 
			Buton(display=display, w=50, h=30, text="Mediu", valoare="mediu"),
			Buton(display=display, w=50, h=30, text="Greu", valoare="greu")
			],
		indiceSelectat=0
	)
	ok=Buton(display=display, top=150, left=30, w=40, h=30, text="ok", culoareFundal=(155,0,55))
	btn_alg.deseneaza()
	btn_juc.deseneaza()
	dificultate_joc.deseneaza()
	ok.deseneaza()
	while True:
		for ev in pygame.event.get(): 
			if ev.type== pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif ev.type == pygame.MOUSEBUTTONDOWN: 
				pos = pygame.mouse.get_pos()
				if not btn_alg.selecteazaDupacoord(pos):
					if not btn_juc.selecteazaDupacoord(pos):
						if not dificultate_joc.selecteazaDupacoord(pos):
							if ok.selecteazaDupacoord(pos):
								display.fill((0,0,0)) #stergere ecran 
								tabla_curenta.deseneaza_grid()
								return btn_juc.getValoare(), btn_alg.getValoare(), dificultate_joc.getValoare()
		pygame.display.update()

def timpi_calculator(timpi_gandire):
	"""
	Aceasta functie calculeaza timpul minim, maxim si mediu de gandire al calculatorului
	timpi_gandire == lista timpilor de gandire (variabile int, in milisecunde) ai calculatorului pentru fiecare mutare

	returneaza valorile min, max, mediu, mediana in aceasta ordine
	"""
	min = sys.maxsize
	max = 0
	mediu = 0
	for i in timpi_gandire:
		if min > i:
			min = i
		if max < i:
			max = i
		mediu += i
	mediu = mediu / len(timpi_gandire)

	mediana = sorted(timpi_gandire)[int(len(timpi_gandire)/2)]
	return (min, max, mediu, mediana)

def selectie_valida(tabla_joc, linie, coloana, simbol):
	"""
	verifica daca selectia jucatorului este una valida 
	verificam daca avem un simbol vecin de acelasi fel 
	"""

	linie_min = 0
	linie_max = linie
	coloana_min = 0
	coloana_max = coloana
	if linie != 0:
		linie_min = linie - 1
	if linie != len(tabla_joc.matr) - 1:
		linie_max = linie + 1
	if coloana != 0:
		coloana_min = coloana - 1
	if coloana != len(tabla_joc.matr[0]) - 1:
		coloana_max = coloana + 1
	for i in range(linie_min, linie_max + 1):
		for j in range(coloana_min, coloana_max + 1):
			if tabla_joc.matr[i][j] == simbol:
				return True
	return False

def main():
	timp_start = int(round(time.time() * 1000)) #Timpul cand a fost pornit programul
	#setari interf grafica
	pygame.init()
	pygame.display.set_caption("Alecu Florin Gabriel: ex-jocuri-exemple-modificate")

	#Memoreaza daca este prima mutare pentru calculator/jucator
	prima_mutare_jucator = True
	prima_mutare_calculator = True

	#dimensiunea ferestrei in pixeli
	#nl=6
	#nc=7

	#nr = int(input())
	nr = 5
	nl = nr
	nc = nr

	w=50
	ecran=pygame.display.set_mode(size=(nc*(w+1)-1,nl*(w+1)-1))# N *w+ N-1= N*(w+1)-1
	Joc.initializeaza(ecran, NR_LINII=nl, NR_COLOANE=nc, dim_celula=w)

	#initializare tabla
	tabla_curenta=Joc(NR_LINII=nl,NR_COLOANE=nc)
	Joc.JMIN, tip_algoritm, dificultate = deseneaza_alegeri(ecran,tabla_curenta)
	print(Joc.JMIN, tip_algoritm)

	Joc.JMAX= '0' if Joc.JMIN == 'x' else 'x'


	print("Tabla initiala")
	print(str(tabla_curenta))
	
	#creare stare initiala
	stare_curenta=Stare(tabla_curenta,'x',ADANCIME_MAX)

	tabla_curenta.deseneaza_grid()

	t_inainte_jucator = int(round(time.time() * 1000)) #Preiau timpul de dinainte pentru jucator (se reseteaza dupa ce face calculatorul o mutare)

	timp_gandire_calculator = []

	while True :
		if (stare_curenta.j_curent==Joc.JMIN):
			for event in pygame.event.get():
				if event.type== pygame.QUIT:
					#iesim din program
					timp_final = int(round(time.time() * 1000)) #Timpul cand a fost inchis programul
					print("Programul a rulat timp de "+str(timp_final - timp_start)+" milisecunde.")
					pygame.quit()
					sys.exit()

				elif event.type == pygame.MOUSEBUTTONDOWN:
					
					pos = pygame.mouse.get_pos()#coordonatele cursorului la momentul clickului
					
					for np in range(len(Joc.celuleGrid)):
						
						if Joc.celuleGrid[np].collidepoint(pos):
							linie=np//Joc.NR_LINII
							coloana=np%Joc.NR_COLOANE
							
							#verifica daca se poate pune un simbol aici	
							if stare_curenta.tabla_joc.matr[linie][coloana] == Joc.GOL:
								t_dupa_jucator=int(round(time.time() * 1000)) #Preia timpul dupa ce s-a facut mutarea

								if prima_mutare_jucator:
									stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN
									stare_curenta.tabla_joc.ultima_mutare=(linie, coloana)
								elif selectie_valida(stare_curenta.tabla_joc, linie, coloana, Joc.JMIN):
									stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN
									stare_curenta.tabla_joc.ultima_mutare=(linie, coloana)
								else:
									continue
								prima_mutare_jucator = False

								#afisarea starii jocului in urma mutarii utilizatorului
								print("\nTabla dupa mutarea jucatorului")
								print(str(stare_curenta))
								
								stare_curenta.tabla_joc.deseneaza_grid(coloana_marcaj=coloana)
								#testez daca jocul a ajuns intr-o stare finala
								#si afisez un mesaj corespunzator in caz ca da
								#afisez timpii de gandire ai calculatorului
								if (afis_daca_final(stare_curenta)):
									stare_curenta.tabla_joc.deseneaza_grid(coloana_marcaj=coloana, stare_curenta=stare_curenta)
									min, max, medie, mediana = timpi_calculator(timp_gandire_calculator)
									print("Timpul minim de gandire al calculatorului: {0}\nTimpul maxim de gandire al calculatorului: {1}\nTimpul mediu de gandire al calculatorului: {2}\nTimpul median de gandire al calculatorului: {3}".format(min, max, medie, mediana))
									break
									
								print("Utilizatorul a \"gandit\" timp de "+str(t_dupa_jucator-t_inainte_jucator)+" milisecunde.") #Afisaza timpul de gandire al jucatorului

								#S-a realizat o mutare. Schimb jucatorul cu cel opus
								stare_curenta.j_curent=Joc.jucator_opus(stare_curenta.j_curent)


	
		#--------------------------------
		else: #jucatorul e JMAX (calculatorul)
			#Mutare calculator
			
			#preiau timpul in milisecunde de dinainte de mutare
			t_inainte=int(round(time.time() * 1000))
			if tip_algoritm=='minimax':
				stare_actualizata=min_max(stare_curenta)
			else: #tip_algoritm=="alphabeta"
				stare_actualizata=alpha_beta(-500, 500, stare_curenta)
			stare_curenta.tabla_joc=stare_actualizata.stare_aleasa.tabla_joc

			print("Tabla dupa mutarea calculatorului\n"+str(stare_curenta))

			#preiau timpul in milisecunde de dupa mutare
			t_dupa=int(round(time.time() * 1000))
			print("Calculatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")
			timp_gandire_calculator.append(t_dupa-t_inainte)

			stare_curenta.tabla_joc.deseneaza_grid()
			if (afis_daca_final(stare_curenta)):
				stare_curenta.tabla_joc.deseneaza_grid(coloana_marcaj=coloana, stare_curenta=stare_curenta)
				min, max, medie, mediana = timpi_calculator(timp_gandire_calculator)
				print("Timpul minim de gandire al calculatorului: {0}\nTimpul maxim de gandire al calculatorului: {1}\nTimpul mediu de gandire al calculatorului: {2}\nTimpul median de gandire al calculatorului: {3}".format(min, max, medie, mediana))
				break
				
			#S-a realizat o mutare. Schimb jucatorul cu cel opus
			stare_curenta.j_curent=Joc.jucator_opus(stare_curenta.j_curent)

			t_inainte_jucator = int(round(time.time() * 1000)) # Preiau timpul initial pentru jucator
	
if __name__ == "__main__" :
	main()

	while True :
		for event in pygame.event.get():
			if event.type== pygame.QUIT:
				pygame.quit()
				sys.exit()