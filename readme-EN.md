This document is currently being translated. Please be patient
======================


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

#### 1.1.3.1 `__init__(self,wiimote):`

Počáteční inicializace, dostane objekt wiimote použitého jako
infrakamera

#### 1.1.3.2 `calibrate(self):`

Zkalibruje infrapero jak tomu bylo doposud. Běží v paralelním vlákně,
které je zastavitelné metodou cancelCalibration.

#### 1.1.3.3 `cancelCalibration(self):`

Pokud bude při kalibraci zavolána tato metoda, , kalibrace se přeruší.
Využití např. pokud už je jasné, že wiimote je špatně natočen a
kalibraci nebude možné dokončit, půjde zrušit stiskem cancel na
ovládacím menu.

#### 1.1.3.4 `getCord(self,timeout=0.5):`

Vrátí souřadnice kliknutí infrapera na panel. Pokud dojde ke kliknutí
pod panel, bude vrácena záporná Y souřadnice. Pokud nedošlo ke kliknutí,
vrátí None. Doba čekání na kliknutí je určena parametrem timeout
v sekundách, nejvýše však 0.5 sekundy, aby to zde nezůstalo viset při
ukončení hry.

`return (x, y)`

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

2.2 SW menu
--------------------

Service-like app, which takes care of pairing wiimotes, communication with HW menu and starting games in paraler thread.


### 2.2.1 Class of individual game

Class of the game must have implemented following methods, which will be used to controll the game. Class of current game will be saved in variable `currentGame`. All methods will be called every time, so it's necessary to implement them, even if they are not needed

#### 2.2.1.1 `prepare(self, led_panel, wiimote1, wiimote2, infrapen):`

Will be called before the game will launch. Instations of led_panel, infrapen and both wiimotes are passed in arguments.

#### 2.2.1.2 `start_game(self):`

Funkce, kterou se pouští hra. Je zavolána hned po `prepare`. Po zavolání se 
nastaví stav proměnné, která řídi běh hry na True (`self.running = True`) a pustí 
se paralelní vlákno (zavoláním `self.start()`) s herní logikou (veškerá herní logika je 
implementována v metodě `self.gameloop(self)`), které běží tak dlouho, dokud
proměná `self.running` není False.


#### 2.2.1.3 `self.running`

Kritická proměná ovládající běh hry. Těsně před zavoláním `start_game`
bude nastavena na True. Pokud bude třeba hru ukončit, nastaví se na False, 
to bude signál pro smyčku herní logiky v `self.gameloop()`, aby se přerušila. 
Hra by se měla ukončit nejpozději za jednu vteřinu, poté bude vlákno hry 
násilně ukončeno a připraveno spuštění další hry.

#### 2.2.1.4`stop_game(self):`

Metoda, kterou se stopuje hra. Nastaví hodnotu proměné `self.running` na False,
tím ukončí běh herní smyčky v `self.gameloop()`.


Herní třída musí mimo výše zmíněné metody implementovat ještě rozhraní `threading.Thread`,
je tedy třeba implementovat metodu `run(self)`, která se spouští v paralelním vlákně,
a jež bude pouštět herní smyčku. Dále je třeba v konstruktoru herní třídy spustit
konstruktor třídy ze které herní třída dědí (`threading.Thread.__init__(self)`).


### 2.2.2 Návrh herní třídy
Blueprint jednotlivých tříd [jsou dostupné zde](https://github.com/gymgeek/led_panel/tree/master/source/BBB/blueprints)

### 2.2.3 Sériová komunikace s HW menu
Pro označení jednotlivých tlačítek se používají byty v hodnotě 65-80, tj. ASCII hodnoty pro písmena A-P. Pokud dojde ke stisknutí tlačítka na menu, odešle Arduino po sériové lince odpovídající znak. Pokud je ze strany BBB požadováno rozsvícení LEDky, jsou do Arduina po sériové lince poslány dva znaky - jeden označuje LEDku příslušného tlačítka, druhý stav.

| Příkaz | Stav |
| ------ | ---- |
| A      | Zhasnuto |
| B      | Rozsvíceno |
| C      | Blikání s frekvencí 2Hz |

Například pro rozsvícení LEDky u tlačítka N je potřeba odeslat `NB`, tj byty `78,66`










