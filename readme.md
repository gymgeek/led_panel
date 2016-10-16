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
lince. Rozvržení tlačítek bude následující:

  Párování Wiimote 1                Had           Přednastavený text 1
  --------------------------------- ---------- -- ----------------------
  Párování Wiimote 2                Tetris        Přednastavený text 2
  Kalibrace infrapera (Wiimote 2)   2048          Přednastavený text 3
  Cancel                            Kreslení      Přednastavený text 4

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

<span id="_o77yxkeuano5" class="anchor"></span>Bude zavoláno po ukončení
druhého vlákna s *gameLogic*.

<span id="_96cxoyjf5ope" class="anchor"></span>

<span id="_a0lzfbu1iswz" class="anchor"></span>

<span id="_lxhnfynpca7a" class="anchor"></span>

<span id="_bgpfcyo27xm0" class="anchor"></span>

<span id="_j80lllkxbdbv" class="anchor"></span>

### 2.2.2 Návrh herní třídy

<span id="_iv8qz7frz7jz" class="anchor"></span>**import** threading

<span id="_mbjgc878l4o6" class="anchor"></span>**import** time

<span id="_do06c2gtylmm" class="anchor"></span>

<span id="_9ldqyu9d8kj7" class="anchor"></span>**class** Game
(threading.Thread):

<span id="_czjuypvr4oit" class="anchor"></span> **def**
\_\_init\_\_(self):

<span id="_sa45fnyl9q3c" class="anchor"></span>
threading.Thread.\_\_init\_\_(self)

<span id="_8yzpdydfg5wb" class="anchor"></span> self.running = False

<span id="_dhjlmziyerhb" class="anchor"></span>

<span id="_v8wvzhzhrxto" class="anchor"></span> **def** prepare(self,
svetelny\_panel, wiimote1, wiimote2, infrapen):

<span id="_uietoqd768uo" class="anchor"></span> self.svetelny\_panel =
svetelny\_panel

<span id="_7q9q589800pv" class="anchor"></span> self.wiimote1 = wiimote1

<span id="_qmaf3leqili6" class="anchor"></span> self.wiimote2 = wiimote2

<span id="_v1im3o41tq07" class="anchor"></span> self.infrapen = infrapen

<span id="_pre8yidqmcis" class="anchor"></span> **print**(**"Preparing
necessary ingredients..."**)

<span id="_jd58n7fzvdoc" class="anchor"></span> self.count = 0

<span id="_fx3nckknp9fj" class="anchor"></span>

<span id="_qrkij0mj3jje" class="anchor"></span> **def**
start\_game(self):

<span id="_lv4siexvzex" class="anchor"></span> self.running = True

<span id="_fz0612xa1vm9" class="anchor"></span> **print**(**"Starting
the game..."**)

<span id="_if6rv1ashdw5" class="anchor"></span> *\# This starts the
parallel thread (self.run() method is called)*

<span id="_8z7lp3iulbi" class="anchor"></span> self.start()

<span id="_whtco0rcggs5" class="anchor"></span>

<span id="_vqtahy95mu6r" class="anchor"></span> **def**
stop\_game(self):

<span id="_c6ojslwagn89" class="anchor"></span> self.running = False

<span id="_plrtzf1iud1p" class="anchor"></span> *\# Wait for the game to
be ended*

<span id="_n2u4qjgfx8ec" class="anchor"></span> time.sleep(1)

<span id="_6zmta7n8bpfy" class="anchor"></span> *\# Now, some other game
can be started*

<span id="_f6z3xur0d8te" class="anchor"></span>

<span id="_g4yibcb0uwtm" class="anchor"></span> **def** run(self):

<span id="_1roqqor0kupq" class="anchor"></span> *\# This method should
never be called manually, this runs in parallel thread and is executed
by &lt;thread&gt;.start() call*

<span id="_m1ca2mpu6rqa" class="anchor"></span> self.gameloop()

<span id="_1uhv8hnauaar" class="anchor"></span>

<span id="_jhjp62u3n9yt" class="anchor"></span> **def** gameloop(self):

<span id="_8iyk64rklaa4" class="anchor"></span> *\# This gameloop must
be end-able by setting self.running variable to False*

<span id="_5i9yjke74uv6" class="anchor"></span>

<span id="_t5f7xepys813" class="anchor"></span> **while** self.running:

<span id="_mxczeldt6tjf" class="anchor"></span> *\# Game logic here
please*

<span id="_d5ykudb7kld4" class="anchor"></span> **print**(self.count)

<span id="_rr6042m0wdlg" class="anchor"></span> self.count += 1

<span id="_8ljxf5453pt0" class="anchor"></span> time.sleep(1)

<span id="_2cy3odko999g" class="anchor"></span>

<span id="_z2epp2y0dymz" class="anchor"></span>

<span id="_sc7nf9h5g7vd" class="anchor"></span>*\# For example, game
could be run from the main service like this *

<span id="_p9hxf1yyvq38" class="anchor"></span>svetelny\_panel,
wiimote1, wiimote2, infrapen = None, None, None, None

<span id="_mjiloiuxlsin" class="anchor"></span>

<span id="_54fg2hurw0l0" class="anchor"></span>button =
checkForButtonPush()

<span id="_x8lj4v1de2l2" class="anchor"></span>

<span id="_rdto5tr9vyss" class="anchor"></span>ChosenGame = \[Game,
Game2, Game3\]\[button\]

<span id="_edn390zggty8" class="anchor"></span>*\# Run the chosen game*

<span id="_hibxqq7srg1d" class="anchor"></span>currentGame =
ChosenGame()

<span id="_4eurth3kgcbo"
class="anchor"></span>currentGame.prepare(svetelny\_panel, wiimote1,
wiimote2, infrapen)

<span id="_n0fzhlt7v3u3" class="anchor"></span>*\# run the game*

<span id="_kqeu862vxwq" class="anchor"></span>currentGame.start\_game()

<span id="_l7843vrdknz8" class="anchor"></span>*\# Meanwhile do
something else*

<span id="_uhck1uwy7qg7" class="anchor"></span>*\# Doing something
else...*

<span id="_ea7dy1k5gqtp" class="anchor"></span>*\# Doing something
else...*

<span id="_uipwax7n69oh" class="anchor"></span>*\# Doing something
else...*

<span id="_lhu2v6e4lj2x" class="anchor"></span>*\# It is time to end the
game now*

<span id="_b5eoa49tl0i4" class="anchor"></span>*\# Stop the game*

<span id="_722lnbrrzpef" class="anchor"></span>currentGame.stop\_game()

<span id="_xn422nqgj49c" class="anchor"></span>

<span id="_cijxbsy4vx0g" class="anchor"></span>

<span id="_eyoeutzftmnu" class="anchor"></span>

<span id="_gjdgxs" class="anchor"></span>
