# OEIS A354427 no tiene otros términos por debajo de 10^11

<!-- explicacion -->
**¿No sos del tema? Esto está explicado desde cero, sin dar nada por sabido:**
[English](https://jorgell23-sys.github.io/de-koninck-cycle-primes/) · [Español](https://jorgell23-sys.github.io/de-koninck-cycle-primes/es/)

<!-- hallazgo:que -->
## Qué se encontró

Los primos p ≤ 10^11 para los que hay primos q, r con q | p+1, r | q²+q+1 y
p | r²+r+1 (OEIS A354427) son exactamente 3, 13, 19, 631, 1794067711 y
10855016833. Que los dos últimos eran términos ya se sabía; que no hay nada
entre ellos ni por debajo de 10^11, no.

<!-- hallazgo:enunciado -->
## El enunciado

Para todo primo p ≤ 10^11: p está en A354427 **si y sólo si**
p ∈ {3, 13, 19, 631, 1794067711, 10855016833}. Por lo tanto a(5) = 1794067711,
a(6) = 10855016833, y a(7) > 10^11 si existe. La cota anterior era 2^24.

<!-- hallazgo:ejemplo -->
## El caso más chico, hecho a mano

    631 + 1        = 632  = 2³ · 79
    79² + 79 + 1   = 6321 = 3 · 7² · 43
    43² + 43 + 1   = 1893 = 3 · 631        → vuelve a 631

y para a(5): 1794067711 + 1 = 2⁸·23·31·9829, 9829² + 9829 + 1 = 3·439·73363,
73363² + 73363 + 1 = 3·1794067711.

<!-- hallazgo:prueba -->
## Por qué es cierto

Se examinaron los 4.118.054.813 primos menores que 10^11. Un lema (RESULT.md
§2) abarata cada uno: si el testigo r es mayor que p, el cofactor (q²+q+1)/r es
menor que p y congruente con (q²+q+1)·ρ² módulo p, con ρ una raíz cúbica de la
unidad módulo p; así una división reemplaza a factorizar q²+q+1. Si r < p, r es
ρ misma. Dos algoritmos que no comparten nada con el lema dan los mismos
testigos en los rangos que cubren, y cada testigo se confirma con enteros
exactos.

<!-- hallazgo:comprobar -->
## Comprobalo vos

```
python verify.py
```

imprime `PASS` en cada uno de sus <!-- checks -->46<!-- /checks --> controles y
`N passed, 0 failed`; sin dependencias. `python verify.py --deep` además
repite segmentos al azar de la búsqueda, y `python src/search.py 100000000000`
la repite entera.

<!-- hallazgo:nodice -->
## Qué NO dice

Nada por encima de 10^11, ni si la secuencia es finita. No descubre a(5) ni
a(6) (lo hizo Yamada, en el comentario de OEIS): muestra que antes de ellos no
hay nada. Dos algoritmos independientes cubren p ≤ 8589934589; por encima, uno
solo, demostrado y muestreado. No toca A355298.

---

## Archivos

| | |
|---|---|
| [RESULT.md](RESULT.md) | el enunciado, el lema con su prueba, la búsqueda, los controles cruzados y los límites (en inglés) |
| [PRIOR_ART.md](PRIOR_ART.md) | qué se buscó, dónde, y el control positivo |
| `verify.py` | cada afirmación, comprobada; sólo biblioteca estándar |
| `src/cycle_primes.py` | la definición y el lema, en Python simple |
| `src/search.py` | la búsqueda entera (numba opcional) |
| `data/terms.json`, `data/blocks/` | los testigos y el registro de la búsqueda, un archivo por 10^9 |
| `docs/` | la explicación para no iniciados, en inglés y en español |

## Autor

**Jorge Ellena Godoy**

## Cómo se produjo

System design and research direction are the author's. The mathematical
results were produced by an automated system (Claude, Anthropic) under that
direction. All computations were verified by two independent implementations
and cross-checked against published work. The author is responsible for the
correctness of everything published here.
