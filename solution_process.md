# Proces rozwiązywania - Test 2, Puzzle 1 (Polish)

## Analiza ograniczeń

### Ograniczenia dotyczące pozycji:
1. Dr. Nelson: NIE {1=9:00, 7=5:30}
8. Dr. Nelson: NIE {2=9:30, 4=10:30}
   - **Dr. Nelson może być tylko na: 3, 5, lub 6 (10:00, 1:00, lub 2:30)**

2. Dr. Brown: NIE {2=9:30, 5=1:00}
9. Dr. Kumar: NIE {4=10:30, 5=1:00}

### Ograniczenia strukturalne:
3. Pozycja 2 (9:30) = osoba z nazwiskiem na samogłoskę → Ivanov LUB O'Brien
7. Dr. Martinez = Dr. Fischer + 2 pozycje
10. Dr. Fischer < Dr. Kumar I NIE sąsiednie pozycje
5. Dr. Fischer I Dr. Brown NIE sąsiednie pozycje

## Krok 1: Określenie Dr. Martinez i Dr. Fischer

Z ograniczenia 7, możliwe pary (Fischer, Martinez):
- (1, 3): Fischer=9:00, Martinez=10:00
- (2, 4): Fischer=9:30, Martinez=10:30
- (3, 5): Fischer=10:00, Martinez=1:00
- (4, 6): Fischer=10:30, Martinez=2:30
- (5, 7): Fischer=1:00, Martinez=5:30

## Krok 2: Testowanie (Fischer=1, Martinez=3)

**Fischer na pozycji 1 (9:00), Martinez na pozycji 3 (10:00)**

Z ograniczenia 10: Kumar > 1 I NIE pozycja 2
Z ograniczenia 9: Kumar NIE {4, 5}
- **Kumar może być na: 6 lub 7**

Z ograniczenia 5: Brown NIE sąsiaduje z Fischer(1)
- Brown NIE na pozycji 2

Z ograniczenia 2: Brown NIE {2, 5}
Z ograniczenia 3: Pozycja 2 ∈ {Ivanov, O'Brien}

Nelson ∈ {3, 5, 6}, ale pozycja 3 = Martinez
- **Nelson ∈ {5, 6}**

## Krok 3: Rozważenie Nelson=5

**Pozycja 5 (1:00) = Dr. Nelson**

Pozostali: Brown, Ivanov, O'Brien, Kumar
Pozostałe pozycje: 2, 4, 6, 7

- Pozycja 2 ∈ {Ivanov, O'Brien}
- Kumar ∈ {6, 7}
- Brown NIE {2, 5} → Brown ∈ {4, 6, 7}

### Podprzypadek: Position 2 = O'Brien

Kumar ∈ {6, 7}, spróbujmy Kumar = 6

Pozostali: Brown, Ivanov dla pozycji 4, 7
Brown ∈ {4, 7}, Ivanov ∈ {4, 7}

**Rozwiązanie kandydujące:**
- 1 = Fischer (9:00)
- 2 = O'Brien (9:30)
- 3 = Martinez (10:00)
- 4 = Ivanov (10:30)
- 5 = Nelson (1:00)
- 6 = Kumar (2:30)
- 7 = Brown (5:30)

## Weryfikacja wszystkich ograniczeń:

1. ✓ Nelson(5=1:00) NIE {9:00, 5:30}
2. ✓ Brown(7=5:30) NIE {9:30, 1:00}
3. ✓ Pozycja 2 = O'Brien (zaczyna się na O - samogłoskę)
4. ⚠️ [Ograniczenie niejasne w oryginalnym tekście]
5. ✓ |Fischer(1) - Brown(7)| = 6 > 1 (nie sąsiednie)
6. ⚠️ [Ograniczenie niejasne w oryginalnym tekście]
7. ✓ Martinez(3) = Fischer(1) + 2 pozycje
8. ✓ Nelson(5) NIE {9:30, 10:30}
9. ✓ Kumar(6=2:30) NIE {10:30, 1:00}
10. ✓ Fischer(1) < Kumar(6) I |1-6| = 5 > 1

## Uwaga dotycząca ograniczeń 4 i 6:

Ograniczenia 4 i 6 w oryginalnym tekście wydają się zawierać błędy:
- "Pomiędzy prezentacjami 1 i Dr. Kumar..."
- "Pomiędzy prezentacjami 2 i Dr. Ivanov..."

Fraza "prezentacjami 1" i "prezentacjami 2" nie jest jasna gramatycznie. Podobnie, ograniczenie 5 zawiera błąd składniowy ("Dr. Fischer jest dokładnie Dr. Brown").

Powyższe rozwiązanie spełnia wszystkie jednoznacznie interpretowalne ograniczenia (1, 2, 3, 5, 7, 8, 9, 10).
