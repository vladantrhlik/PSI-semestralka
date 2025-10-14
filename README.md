# PSI - 1. úloha

K řešení byl použit jazyk Python se základní knihovnou `socket` pro práci s BSD sockety. Program lze spustit pomocí příkazu `python3 server.py`, čímž se spustí TCP server na adrese `127.0.0.1:8080`.

### Popis funkcí:

- `main()` - vstupní bod programu, spustí TCP server a obsluhuje požadavky

- `get_route_table()` - načte směrovací tabulku z `/proc/net/route` a vytvoří HTML tabulku s potřebnými daty

- `decode_flags()` - z FLAGů záznamu směrovací tabulky dekóduje jednotlivé příznaky do čitelného řetězce

- `hex_to_ipv4()` - převede hexadecimální zápis IPv4 adresy do standardního zápisu po oktetech; je potřeba správné pořadí bytů - 1. byte = 4. oktet, 2. byte = 3. oktet...
