# PSI - 1. úloha

K řešení byl použit jazyk Python se základní knihovnou `socket` pro práci s BSD sockety. Program lze spustit pomocí příkazu `python3 server.py`, čímž se spustí TCP server na adrese `127.0.0.1:8080`.

### Popis funkcí:

### `main()`
Vstupní bod programu, spustí TCP server na portu 8080 a obsluhuje požadavky.

### `get_route_table()`
1. Načte směrovací tabulku z `/proc/net/route`
2. Vytvoří dictionary pro každý záznam tabulky
3. Převede zápis IPv4 adres do čitelné formy pomocí `hex_to_ipv4()`
4. Dekóduje FLAGS pomocí `decode_flags()` do čitelné formy
5. Vytvoří HTML tabulku s potřebnými daty

### `hex_to_ipv4()`
Převede hexadecimální zápis IPv4 adresy do standardního zápisu po oktetech. Je potřeba správné pořadí bytů (little endian) - 1. byte = 4. oktet, 2. byte = 3. oktet...

### `decode_flags()`
Z FLAGů záznamu směrovací tabulky dekóduje jednotlivé příznaky do čitelného řetězce.
