


#  Guía Completa: Cómo Jugar Yu-Gi-Oh! Forbidden Memories - Minimax

## Integrantes

- Juan David Garcia Arroyave
- Juan Jose Hincapie Tascon
- Sebastian Zacipa Martinez

## Objetivo del Juego

**¡Reduce los LP (Life Points) de tu oponente a 0 o menos!**

### Estados de los LP:
- **LP > 4000**:  Excelente (ventaja clara)
- **LP 2000-4000**:  Peligroso (equilibrado)
- **LP < 2000**:  Crítico (en riesgo de perder)

---

##  Las 3 Acciones Disponibles (Solo UNA por Turno)

### 1️ INVOCAR (Summon)
**Cómo hacerlo:**
- Haz clic en **1 sola carta** de tu mano (se marca en amarillo)
- Presiona el botón **"Invocar"**
- La carta aparece en tu campo

**Efecto:**
- Pone el monstruo en el campo
- Puedes atacar con él en tus próximos turnos
- Máximo 5 monstruos en el campo

**Estrategia:**
- Invoca monstruos débiles primero para "probar" la defensa del rival
- Guarda los monstruos fuertes para fusionarlos

---

### 2️ FUSIONAR (Fusion)
**Cómo hacerlo:**
- Haz clic en **2 cartas diferentes** de tu mano (ambas se marcan en amarillo)
- Presiona el botón **"Fusionar"**
- Aparece una carta nueva y más fuerte

**Efectos:**
- Las 2 cartas desaparecen (van al cementerio)
- Se crea 1 carta nueva más poderosa
- La carta nueva aparece en tu campo

**Ejemplo de Fusiones:**
```
Dragón Blanco (3000 ATK) + Mago Oscuro (2500 ATK) 
= Dragón Supremo (3200 ATK) 
```

**Estrategia:**
- Fusion cuando tengas cartas débiles en mano
- Busca crear monstruos > 2500 ATK
- Ahorra fusiones poderosas para momentos críticos

---

### 3️ ATACAR (Attack)
**Cómo hacerlo:**

**Opción A - Atacar monstruo enemigo:**
1. Haz clic en **tu monstruo** (se marca en amarillo)
2. Haz clic en un **monstruo enemigo**
3. Se realiza la batalla automáticamente

**Opción B - Ataque Directo:**
1. Haz clic en **tu monstruo**
2. Presiona **"Atacar directo"** (solo si la IA NO tiene monstruos)
3. Los LP del rival reciben daño directo

**Cálculo de Batalla:**
```
Si TU ATK > ENEMIGO DEF:
  Daño = TU ATK - ENEMIGO DEF
  Se resta de LP del enemigo
  El monstruo enemigo se destruye

Si TU ATK < ENEMIGO DEF:
  Daño = ENEMIGO DEF - TU ATK
  Se resta de TUS LP
  Tu monstruo se destruye

Si TU ATK = ENEMIGO DEF:
  Ambos monstruos se destruyen (sin daño a LP)
```

**Ejemplos de Batalla:**
```
Tu Dragón (ATK 3000) vs Mago Enemigo (DEF 2100)
→ Daño = 3000 - 2100 = 900
→ -900 LP al enemigo 

Tu Guerrero (ATK 1800) vs Bestia Enemiga (DEF 2000)
→ Daño = 2000 - 1800 = 200
→ -200 LP a TI 
→ Tu monstruo se destruye
```

**Estrategia:**
- Siempre compara ATK con DEF del enemigo
- Ataca solo si ganas la batalla
- Usa ataque directo cuando el enemigo no tenga defensa
- Sacrifica monstruos débiles si necesitas ganar tiempo

---

##  ¿Por Qué No Puedo Fusionar?

###  Razones Comunes:

**1. "No tienes 2 cartas seleccionadas"**
- Solución: Haz clic en EXACTAMENTE 2 cartas de tu mano
- Ambas deben marcarse en amarillo
- Si haces clic en una tercera, se deselecciona

**2. "Las 2 cartas no tienen fusión"**
- Solución: No todas las cartas se pueden fusionar
- Solo ciertos pares crean nuevas cartas
- Revisa el panel "Mazos Visibles" → "GUIA_FUSIONES.md"

**3. "No tienes espacio en el campo"**
- Solución: Ya tienes 5 monstruos (máximo)
- Destruye un monstruo primero (atacando)
- O invoca con una carta después

**4. "Ya usaste tu acción"**
- Solución: Solo UNA acción por turno
- Si ya invocaste o atacaste, no puedes fusionar
- Espera al siguiente turno

---

##  Flujo de un Turno

```
1. INICIO DE TURNO
   ↓
2. ELIGE UNA ACCIÓN (solo una):
   • INVOCAR (1 carta)
   • FUSIONAR (2 cartas)
   • ATACAR (tus monstruos atacan)
   • O: Presiona "Fin de turno" (sin hacer nada)
   ↓
3. TURNO TERMINA AUTOMÁTICAMENTE
   ↓
4. LA IA JUEGA
   • La IA elige su mejor acción
   • Tú ves sus monstruos y acciones
   ↓
5. VUELVE A TU TURNO
   • Se te da 1 carta nueva de tu mazo
   ↓
6. REPETIR hasta que alguien llegue a 0 LP
```

---

##  Estrategia Para Ganar

###  Fase 1: Establecimiento (Turnos 1-3)
```
✓ Invoca monstruos débiles
✓ Aprende la defensa del enemigo
✓ Guarda las cartas fuertes
✓ Observa qué cartas trae el rival
```

###  Fase 2: Presión (Turnos 4-6)
```
✓ Fusiona tus monstruos débiles
✓ Crea monstruos > 2500 ATK
✓ Ataca si ganas la batalla
✓ Reduce LP del enemigo lentamente
```

###  Fase 3: Ofensiva (Turnos 7+)
```
✓ Crea los monstruos más fuertes
✓ Ataca directo si el enemigo no tiene defensa
✓ Asegúrate cada daño
✓ Aplasta al enemigo con ventaja
```

---

##  Cartas Recomendadas para Empezar

###  MÁS FUERTES (ATK > 3000):
- **Dragón Emperador** (3800 ATK) - Definitivamente gana
- **Dragón Blanco** (3000 ATK) - Sólido
- **Dragón Definitivo** (3500 ATK) - Muy bueno
- **Dragón Supremo** (3200 ATK) - Fusión poderosa

###  BUENAS (ATK 2200-2800):
- **Dragón Rojo** (2600 ATK)
- **Leviatán** (2800 ATK)
- **Guerrero Dragón** (2200 ATK)
- **Caballero Dragón** (2400 ATK)

###  DÉBILES (ATK < 2000):
- **Guerrero Novato** (900 ATK) - Usa para fusionar
- **Dragón Bebé** (1200 ATK) - Material de fusión
- **Bestia Feroz** (1700 ATK) - Defensivo

---

##  Tips y Trucos

###  Tip 1: Revisa los Mazos Visibles
- Panel derecho muestra todas las cartas que vienen
- Planifica tus movimientos sabiendo qué cartas llegarán
- La IA también ve esto (información perfecta)

###  Tip 2: Usa Fusiones Estratégicamente
- No fusiones todo de una vez
- Guarda cartas para el momento crítico
- Algunas fusiones son muy poderosas (Dragón Emperador)

###  Tip 3: Ataque es la Mejor Defensa
- Si atacas primero, controlabas el ritmo
- Mantén monstruos fuertes en el campo
- Crea oportunidades de ataque directo

###  Tip 4: Sacrificio Inteligente
- A veces es mejor que tu monstruo pierda
- Especialmente si da mucho daño al enemigo
- Piensa en los próximos 2-3 turnos

###  Tip 5: Observa la IA
- La IA usa Minimax (algoritmo inteligente)
- Siempre elige la mejor opción
- Aprende de sus movimientos

---

##  Probabilidad de Ganar

| Situación | Probabilidad |
|-----------|-------------|
| Tienes 5000 LP, rival 3000 |  80% ganar |
| Tienes 3000 LP, rival 5000 |  50% ganar |
| Tienes 1000 LP, rival 5000 |  10% ganar |

**Conclusión:** Mantén tu LP alto y ataca constantemente.

---

##  Errores Comunes

| Error | Problema | Solución |
|-------|----------|----------|
| Invoco y ataco en el mismo turno | Pierdo turno | Solo UNA acción |
| Intento fusionar 3 cartas | No funciona | Solo 2 cartas |
| Ataco con desventaja (900 ATK vs 2000 DEF) | Pierdo LP | Calcula antes |
| Dejo vacío el campo | La IA ataca directo | Siempre ten defensa |
| Quemo todas las fusiones | No tengo poder | Usa fusiones lentamente |

---

##  Controles Rápidos

```
ACCIÓN          | CÓMO HACERLO
----------------|----------------------------------------
Invocar         | Clic 1 carta → Botón "Invocar"
Fusionar        | Clic 2 cartas → Botón "Fusionar"
Atacar Monstruo | Clic tu monstruo → Clic enemigo
Atacar Directo  | Clic tu monstruo → Botón "Atacar directo"
Pasar Turno     | Botón "Fin de turno"
Reiniciar       | Botón "Jugar de nuevo" (cuando termina)
```

---

##  Puntuación (¿Cómo Medir Mi Rendimiento?)

| Resultado | Puntuación |
|-----------|-----------|
| Ganas |  (5/5) |
| Pierdes con < 1000 LP diferencia |  (4/5) |
| Pierdes con 1000-3000 LP diferencia |  (3/5) |
| Pierdes por mucha diferencia |  (2/5) |
| Pierdes sin entender por qué |  (1/5) |

---

##  Próximo Nivel: Estrategia Avanzada

1. **Minimax Analysis**: La IA elige moves óptimos
2. **Perfect Information**: Ambos ven todas las cartas
3. **Decision Tree**: Cada movimiento afecta el futuro
4. **Resource Management**: Usa fusiones eficientemente
5. **Position Control**: Mantén ventaja siempre

---

¡Ahora estás listo para jugar! 

**Recuerda:** 
- Solo UNA acción por turno
- Reduce los LP del rival a 0 para ganar
- Planifica usando los mazos visibles
- ¡Buena suerte! 
