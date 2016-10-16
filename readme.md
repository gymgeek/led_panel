1. Světelný panel
=================

1.1 Třídy světelného panelu
---------------------------

### 1.1.1 svetelnypanel

Aktuálně používaná třída

…

### 1.1.2 wiimote

Aktuálně používaná třída

…

### 1.1.3 infrapen

Třída pro práci s infraperem.

#### 1.1.3.1 \_\_init\_\_(self,wiimote):

Počáteční inicializace, dostane objekt wiimote použitého jako
infrakamera

#### 1.1.3.2 calibrate(self):

Zkalibruje infrapero jak tomu bylo doposud. Běží v paralelním vlákně,
které je zastavitelné metodou cancelCalibration.

#### 1.1.3.3 cancelCalibration(self):

Pokud bude při kalibraci zavolána tato metoda, , kalibrace se přeruší.
Využití např. pokud už je jasné, že wiimote je špatně natočen a
kalibraci nebude možné dokončit, půjde zrušit stiskem cancel na
ovládacím menu.

#### 1.1.3.4 getCord(self,timeout=0.5):

Vrátí souřadnice kliknutí infrapera na panel. Pokud dojde ke kliknutí
pod panel, bude vrácena záporná Y souřadnice. Pokud nedošlo ke kliknutí,
vrátí None. Doba čekání na kliknutí je určena parametrem timeout
v sekundách, nejvýše však 0.5 sekundy, aby to zde nezůstalo viset při
ukončení hry.

*return (x, y)*

2. Panel menu
=============

Jeden skript, nejlépe fungující jako service, obstarávající hlavní
ovládání. Přes druhou sériovou linku komunikace s Arduinem s připojeným
4x4 LED matrixem a 4x4 klávesnicí. Menu bude zajiěťovat párování obou
wiimote i konfiguraci infrapera. Všechny hry budou naimportovatelné jako
objekt, v parametru dostane obejkt wiimote a světelného panelu.

2.1 Fungování HW menu
---------------------

HW menu sestává ze 16 tlačítek, každé s LEDkou, oboje zapojené jako 4x4
matrix. Ovládání bude zajišťovat Arduino, komunikace s BBB po sériové
lince. Tlačíka jsou značena abecedně, odshora dolu, zleva doprava. Rozvržení tlačítek bude následující:

| 1. sloupec |  2. sloupec | 3. sloupec | 4. sloupec | 
|---|---|---|---|
| A: Párování Wiimote 1                | B: Had     | C:      | D: Přednastavený text 1 |
| E: Párování Wiimote 2                | F: Tetris  | G:      | H: Přednastavený text 2 |
| I: Kalibrace infrapera (Wiimote 2)   | J: 2048    | K:      | L: Přednastavený text 3 |
| M: Cancel                            | N: Kreslení| O:      | P: Přednastavený text 4 |

Při spárovaném Wiimote bude LEDka svítit, při odpojeném bude zhasnutá.
Pokud bude prováděna kalibrace nebo párování, LEDka bude blikat. Po
první kalibraci infrapera se rozsvítí i jeho LEDka.

Ledka aktuálně aktivované hry (včetně přednastavených textů) bude
svítit, ostatní zhasnuté. Tlačítkem cancel se zruší aktuální hra a na
panelu se pustí nějaké demo (něco jako XYmatrix example z knihovny
FastLED pro Arduino). Změna hry bude možná i stisknutím tlačítka hry,
bez nutnosti ukončovat aktuální hru tlačítkem cancel.

2.2Fungování SW menu
--------------------

Bude se jednat o dvouvláknovou aplikaci. Jedno vlákno bude zajišťovat
komunikaci s HW menu a na základě toho pouštět jednotlivé hry v druhém
vlákně.

### 2.2.1 Třída samotné hry.

Třída hry bude obsahovat následující funkce a proměnné, kterými bude
ovladatelná. Před spuštěním se vždy vybraná třída hry uloží do proměnné
*currentGame*, na kterou se budou volat dané metody, tudíž je nezbytné
je následující metody implementovat, i pokud nejsou potřeba.

#### 2.2.1.1 prepare(self svetelnypanel, wiimote1, wiimote2, infrapen):

Zavolá se před spuštěním hry. V parametrech jsou předány třídy
svetelnypanel a infrapen a objekty obou wiimote.

#### 2.2.1.2 startGame(self):

Funkce obstarávající herní logiku, bude zavolána hned po *prepare*.
Bude/Musí obsahovat nekonečnou smyčku, která poběží v druhém vlákně, ale
smyčka musí být přerušitelná pomocí *isActive*

#### 2.2.1.3 isActive

Těsně před zavoláním *startGame* bude nastavena na True. Pokud bude
třeba hru ukončit, nastaví se na False, to bude signál pro smyčku
*startGame* aby se přerušila. Hra by se měla ukončit nejpozději za jednu
vteřinu, poté bude vlákno *startGame* násilně ukončeno a připraveno
spuštění další hry.

#### 2.2.1.4 terminate(self):

Bude zavoláno po ukončení
druhého vlákna s *gameLogic*.


### 2.2.2 Návrh herní třídy
Blueprint ednotlivých tříd [jsou dostupné zde](https://github.com/gymgeek/led_panel/tree/master/source/BBB/blueprints)
