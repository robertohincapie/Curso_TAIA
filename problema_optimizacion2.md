# Variables a considerar y conjuntos

## Ranuras de tiempo: 
Se supone que el tiempo está partido en ranuras de duración $\Delta t$, que representan intervalos de tiempo así. Si por ejemplo, $\Delta t=10 min$, entonces, tenemos diferentes tiempos, la ranura representada por diferentes valores de k: 

| Número del intervalor: k | Tiempo real | Representación |
|--------|------|---------|
| 1    | 6:00 am   | $t_1$  |
| 2    | 6:10 am   | $t_2$  |
| 3    | 6:20 am   | $t_3$  |
| $\ldots$    | $\ldots$   | $\ldots$  |
| 144    | 5:50 am   | $t_{144}$  |

Lo anterior, suponiendo 10 minutos y un tiempo total de 24 horas que resultaría en 144 ranuras de tiempo

Conjunto de tiempos o ranuras: $\mathbf{T}=\{1, 2, \ldots, k, \ldots, K\}$, indicando que $t_k$ representa a una de las $K$ ranuras.

## Usuarios: 

Conjunto de Usuarios: $\mathbf{U}=\{1, 2, \ldots,i, \ldots,m\}$, indicando que $u_i$ representa a uno de $m$ usuarios. 

## Doctores: 
Conjunto de doctores: $\mathbf{D}=\{1, 2, \ldots, j, \ldots, n\}$, indicando que $d_j$ representa a uno de $n$ doctores.

## Variables de decisión: 

$x_{i,j,k}$ Variable binaria que tiene un valor de 1 si el médico $j$ atiende al usuario $i$, comenzando en la ranura de tiempo $k$. 

$u_j$ Variable binaria que tiene un valor de 1 si el médico $j$ está activo en el turno. En nuestro caso, suponemos algo: Es necesario atender a todos los pacientes, pero podemos disminuir el número de médicos que necesitemos. 

$y_{j,k}$ Variable binaria que tiene un valor de 1 si el médico $j$ inicia su atención en la ranura de tiempo $k$.

$
t_i=\sum_{j\in\mathcal D}\sum_{k\in\tau_i}k\,x_{ijk}
$ es la ranura en la que inicia el servicio del paciente $i$

$
q_j=\sum_{h\in\mathcal H}h\,y_{jh}
$ es la ranura de inicio de la jornada del médico \(j\).

$z_{a,b,j}$ Variable binaria que tiene un valor de 1 si el médico $j$ sale de atender al usuario $a$ y luego pasa a atender al usuario $b$. Existen dos "Usuarios" ficticios que son el usuario $S$ que corresponde al inicio de la jornada y el usuario $T$ que corresponde al final de la jornada.  

## Parámetros del problema: 

### Servicios de los usuarios: 

El servicio del usuario $i$ está determinado por 3 cantidades
- $a_i$ La ranura de tiempo en que el servicio puede comenzar, no antes de ese tiempo. 
- $b_i$ La ranura de tiempo en que el servicio puede terminar como máximo. El usuario debe ser atendido entre $a_i$ y $b_i$. 
- $c_i$ La duración del servicio en tiempo dado por el número de ranuras necesarias. 

### Retrazos de movilidad: 

Si un médico se tiene que desplazar desde un usuario $i_1$ hasta la ubicación de un usuario $i_2$, se toma un tiempo $\delta_{i_1, i_2}$. Esta matriz está calculada para todos los pares posibles de usuarios y no es necesariamente simétrica. Esto aplica también para $i_1=S$ y para $i_2=T$. 

### Costos de desplazamiento

Si un médico se tiene que desplazar desde un usuario $i_1$ hasta la ubicación de un usuario $i_2$, esto tiene un cost $C_{i_1, i_2}$. Este costo aplica también para $i_1=S$ y para $i_2=T$. 

$C^{med}$ corresponde al costo de un médico por cumplir el turno. 

## Formulación matemática



El problema de optimización puede formularse como

\[
\begin{aligned}
\min \quad
&
C^{\text{med}}
\sum_{j\in\mathcal D}u_j
+
\sum_{j\in\mathcal D}
\Bigg(
\sum_{i\in\mathcal U}
C_{S,i}\,z_{S,i,j}
+
\sum_{\substack{a,b\in\mathcal U\\a\neq b}}
C_{a,b}\,z_{a,b,j}
+
\sum_{i\in\mathcal U}
C_{i,F}\,z_{i,F,j}
\Bigg)
\end{aligned}
\]

sujeto a

\[
\begin{aligned}
&i.\;
\sum_{j\in\mathcal D}
\sum_{k\in\tau_i}
x_{i,j,k}
=
1,
&&
\forall i\in\mathcal U,
\\[2mm]
&ii.\;
\sum_{k\in\tau_i}
x_{i,j,k}
\le
u_j,
&&
\forall i\in\mathcal U,\;
\forall j\in\mathcal D,
\\[2mm]
&
iii.\;\sum_{k\in\mathcal T}
y_{j,k}
=
u_j,
&&
\forall j\in\mathcal D,
\\[2mm]
&
iv.\;x_{i,j,k}
\le
\sum_{\substack{
s\in\mathcal T\\
s\le k\\
k+c_i-1\le s+\beta-1}}
y_{j,h},
&&
\forall i\in\mathcal U,\;
\forall j\in\mathcal D,\;
\forall k\in\tau_i,
\\[2mm]
&
v.\;\sum_{i\in\mathcal U}
z_{S,i,j}
=
u_j,
&&
\forall j\in\mathcal D,
\\[2mm]
&
vi.\;\sum_{i\in\mathcal U}
z_{i,F,j}
=
u_j,
&&
\forall j\in\mathcal D,
\\[2mm]
&
vii.\;z_{S,i,j}
+
\sum_{\substack{a\in\mathcal U\\a\neq i}}
z_{a,i,j}
=
\sum_{k\in\tau_i}
x_{i,j,k},
&&
\forall i\in\mathcal U,\;
\forall j\in\mathcal D,\;

\\[2mm]
&
viii.\;z_{i,F,j}
+
\sum_{\substack{b\in\mathcal U\\b\neq i}}
z_{i,b,j}
=
\sum_{k\in\tau_i}
x_{i,j,k},
&&
\forall i\in\mathcal U,\;
\forall j\in\mathcal D,\;
\\[2mm]
&
ix.\;t_b
\ge
t_a
+
c_a
+
\delta_{a,b}
-
M_T(1-z_{a,b,j}),
&&
\forall j\in\mathcal D,\;
\forall a\in\mathcal U,\;
\forall b\in\mathcal U,\;
a\neq b,
\\[2mm]
&
x.\;
t_i
\ge
q_j
+
\delta_{S,i}
-
M_T(1-z_{S,i,j}),
&&
\forall i\in\mathcal U,\;
\forall j\in\mathcal D,\;
\\[2mm]
&
xi.\;t_i+c_i+\delta_{i,F}
\le
q_j+\beta
+
M_T(1-z_{i,F,j}),
&&
\forall i\in\mathcal U,\;
\forall j\in\mathcal D,\;
\\[2mm]
&
u_j
\ge
u_{j+1},
&&
j=1,\ldots,n-1,
\\[2mm]
&
x_{i,j,k},
u_j,
y_{j,h},
z_{a,b,j},
z_{S,i,j},
z_{i,F,j}
\in
\{0,1\}.
\end{aligned}
\]

## Heurística constructiva secuencial para un número dado de médicos

En esta sección se describe una heurística constructiva para obtener una solución factible del problema cuando se fija un número máximo de médicos disponibles, denotado por \(n\). La heurística fue diseñada para ser llamada como `heuristic(n)`, de modo que el usuario pueda probar sucesivamente con \(n=1,2,3,\ldots\) hasta encontrar el menor valor de \(n\) para el cual existe una solución factible.

La heurística **no resuelve** el modelo exacto anterior por optimización matemática, sino que construye una solución de manera secuencial siguiendo una regla de prioridad y una regla de asignación temprana.

## Objetivo de la heurística

Dado un valor fijo de \(n\):

- determinar si es posible atender a todos los pacientes con a lo sumo \(n\) médicos,
- construir explícitamente la asignación de pacientes a médicos,
- fijar el tiempo de inicio de atención de cada paciente,
- identificar cuáles médicos quedan realmente activos,
- y calcular el costo total de la solución construida.

El propósito principal es evaluar factibilidad con distintos valores de \(n\), y en caso de factibilidad obtener también el costo de la solución generada.

## Conjuntos y parámetros utilizados

La heurística utiliza los mismos conjuntos y parámetros del modelo:

- \(\mathcal U=\{1,2,\ldots,m\}\): conjunto de pacientes.
- \(\mathcal D=\{1,2,\ldots,n\}\): conjunto de médicos disponibles para la corrida de la heurística.
- \(\mathcal T=\{1,2,\ldots,K\}\): conjunto de ranuras de tiempo.
- \(a_i\): primera ranura en la que puede iniciar la atención del paciente \(i\).
- \(b_i\): última ranura en la que debe haber terminado la atención del paciente \(i\).
- \(c_i\): duración, en número de ranuras, de la atención del paciente \(i\).
- \(\delta_{i_1,i_2}\): tiempo de desplazamiento en ranuras entre \(i_1\) e \(i_2\).
- \(C_{i_1,i_2}\): costo de desplazamiento entre \(i_1\) e \(i_2\).
- \(H\): longitud máxima del turno de un médico.
- \(\beta\): número máximo de ranuras consecutivas que puede trabajar un médico.
- \(C^{med}\): costo fijo de activar un médico.

Además, para cada paciente \(i\), se define:

\[
\tau_i=\{k\in\mathcal T:\; a_i\le k \le b_i-c_i+1\},
\]

es decir, \(\tau_i\) es el conjunto de ranuras factibles de inicio de atención del paciente \(i\).

## Idea central de la heurística

La heurística sigue dos principios:

1. **Orden de prioridad de pacientes.**  
   Los pacientes se procesan de forma ascendente según el primer instante factible de su ventana, esto es, según el valor mínimo de \(\tau_i\), equivalente a \(a_i\).  
   En caso de empate, se prioriza el paciente con menor amplitud de ventana factible, es decir, con menor valor de \(|\tau_i|\). Si el empate persiste, se puede desempatar por \(b_i\) y luego por el índice \(i\).

2. **Asignación lo más temprano posible.**  
   Cuando se procesa un paciente \(i\), se intenta ubicarlo en el **primer médico disponible** y en la **ranura más temprana posible** dentro de \(\tau_i\), respetando factibilidad temporal, desplazamientos y duración máxima del turno.

En consecuencia, la heurística es una regla de tipo:

- **primero los pacientes más urgentes en términos de inicio temprano de ventana**, y
- **cada paciente se ubica tan pronto como sea posible**.

## Estado de cada médico durante la construcción

Para cada médico \(j\), la heurística mantiene la siguiente información:

- la lista ordenada de pacientes ya asignados al médico \(j\),
- el primer paciente atendido por el médico \(j\),
- el último paciente atendido por el médico \(j\),
- la ranura de inicio de su turno,
- la ranura de finalización de la última atención asignada.

Un médico \(j\) está inicialmente **inactivo**.  
Un médico se **activa** únicamente cuando se le asigna su primer paciente. Antes de eso, el médico no tiene turno iniciado.

## Regla de activación del médico

Si un médico \(j\) no tiene pacientes asignados y se decide asignarle por primera vez el paciente \(i\) en la ranura \(k\), entonces:

- el médico \(j\) pasa a estar activo,
- su turno se considera iniciado en la ranura
  \[
  q_j = k,
  \]
- el primer paciente de su ruta es \(i\),
- y la primera atención del médico comienza exactamente cuando inicia su turno.

Esto es consistente con la idea de que **el médico no se activa antes de atender al primer paciente**.

## Regla de factibilidad para asignar un paciente a un médico

Supóngase que se está procesando un paciente \(i\) y se quiere evaluar si puede ser asignado al médico \(j\).

### Caso 1: el médico \(j\) aún no ha sido activado

Si el médico no tiene pacientes previos, entonces el paciente \(i\) puede comenzar en cualquier ranura:

\[
k\in \tau_i.
\]

Como la heurística utiliza asignación temprana, se selecciona el menor valor posible:

\[
k_i=\min \tau_i.
\]

### Caso 2: el médico \(j\) ya tiene pacientes asignados

Sea \(a(j)\) el último paciente asignado al médico \(j\).  
Sea \(t_{a(j)}\) la ranura de inicio de atención de ese último paciente.  
Entonces, la atención de \(a(j)\) finaliza en:

\[
t_{a(j)} + c_{a(j)}.
\]

Después, el médico necesita desplazarse desde \(a(j)\) hasta el nuevo paciente \(i\), lo que toma \(\delta_{a(j),i}\) ranuras. Por tanto, el nuevo paciente \(i\) no puede empezar antes de:

\[
t_{a(j)} + c_{a(j)} + \delta_{a(j),i}.
\]

En consecuencia, un inicio \(k\in\tau_i\) es factible para el médico \(j\) si cumple:

\[
k \ge t_{a(j)} + c_{a(j)} + \delta_{a(j),i}.
\]

Adicionalmente, si el médico \(j\) inició su turno en la ranura \(q_j\), entonces toda atención asignada debe quedar dentro de las \(\beta\) ranuras máximas de turno. Por tanto, también se exige:

\[
k + c_i \le q_j + \beta.
\]

La heurística elige el **menor** valor \(k\in\tau_i\) que satisfaga ambas desigualdades.

## Regla de asignación secuencial

Para cada paciente \(i\), una vez fijado su orden de procesamiento, se prueban los médicos en el orden:

\[
1,2,\ldots,n.
\]

El procedimiento es:

1. Se intenta asignar el paciente \(i\) al médico 1 en la ranura factible más temprana.
2. Si no existe una ranura factible con el médico 1, se intenta con el médico 2.
3. Se continúa del mismo modo con los médicos 3, 4, etc.
4. Si algún médico \(j\) admite al paciente \(i\), la asignación se fija de inmediato y ya no se prueban los médicos restantes.
5. Si ningún médico entre \(1\) y \(n\) puede recibir al paciente \(i\), la heurística termina y declara la solución como **no factible** para ese valor de \(n\).

Esta es una heurística constructiva voraz: una vez hecha una asignación, esta no se reconsidera más adelante.

## Definición formal de solución factible heurística

Para un valor dado de \(n\), la solución construida por la heurística se considera **factible** si logra asignar todos los pacientes \(i\in\mathcal U\) a algún médico \(j\in\{1,\ldots,n\}\) y a una ranura de inicio \(k_i\in\tau_i\), cumpliendo simultáneamente:

1. cada paciente es asignado exactamente una vez;
2. si dos pacientes consecutivos \(a\) e \(b\) son atendidos por el mismo médico, entonces:
   \[
   t_b \ge t_a + c_a + \delta_{a,b};
   \]
3. para cada médico activo \(j\), todas sus atenciones quedan dentro del turno iniciado en \(q_j\), es decir:
   \[
   t_i + c_i \le q_j + \beta
   \]
   para todo paciente \(i\) asignado a dicho médico.

Si al menos un paciente no puede ser asignado bajo estas reglas, la salida de la heurística es **no factible**.

## Cálculo del costo de la solución heurística

Si la heurística encuentra una solución factible, el costo total se calcula como:

\[
\text{Costo total}
=
\sum_{j\in\mathcal D^{act}} C^{med}
+
\sum_{j\in\mathcal D^{act}} \text{Costo de ruta del médico } j,
\]

donde \(\mathcal D^{act}\subseteq\mathcal D\) es el conjunto de médicos que fueron activados.

Para cada médico activo \(j\), si su secuencia de pacientes es:

\[
(i_1,i_2,\ldots,i_r),
\]

entonces su costo de ruta es:

\[
C_{S,i_1}
+
\sum_{\ell=1}^{r-1} C_{i_\ell,i_{\ell+1}}
+
C_{i_r,T}.
\]

Por tanto, el costo total completo de la solución heurística es:

\[
\text{Costo total}
=
\sum_{j\in\mathcal D^{act}} C^{med}
+
\sum_{j\in\mathcal D^{act}}
\left(
C_{S,i_1^{(j)}}
+
\sum_{\ell=1}^{r_j-1} C_{i_\ell^{(j)},i_{\ell+1}^{(j)}}
+
C_{i_{r_j}^{(j)},T}
\right).
\]

En la implementación actual, los costos \(C_{S,i}\) y \(C_{i,T}\) se consideran de acuerdo con los valores definidos en los datos del problema.

## Salida esperada de `heuristic(n)`

La función `heuristic(n)` debe devolver, como mínimo, la siguiente información:

- si la solución es factible o no;
- el costo total de la solución, si es factible;
- el número de médicos activos realmente utilizados;
- la asignación de cada paciente a un médico;
- el tiempo de inicio de atención de cada paciente;
- la secuencia de pacientes atendidos por cada médico activo.

De manera complementaria, puede generarse una visualización tipo diagrama de Gantt que muestre:

- la franja temporal del turno activo de cada médico,
- y los bloques de tiempo ocupados por cada paciente dentro de dicho turno.

## Algoritmo en pseudocódigo

```text
Heuristic(n)

Entrada:
    - Número máximo de médicos disponibles n
    - Conjuntos y parámetros del problema

Salida:
    - Indicador de factibilidad
    - Costo total, si existe solución factible
    - Asignaciones construidas

1. Ordenar los pacientes i en forma ascendente según min(tau_i).
2. En caso de empate, ordenar por menor |tau_i|.
3. Inicializar los n médicos como inactivos y sin pacientes.
4. Para cada paciente i en el orden calculado:
5.     asignado <- Falso
6.     Para j = 1 hasta n:
7.         Si el médico j está inactivo:
8.             Buscar el menor k en tau_i.
9.         Si el médico j ya está activo:
10.            Sea a(j) el último paciente del médico j.
11.            Buscar el menor k en tau_i tal que
                   k >= t_a(j) + c_a(j) + delta_a(j),i
                y
                   k + c_i <= q_j + beta.
12.        Si dicho k existe:
13.            Asignar el paciente i al médico j en la ranura k.
14.            Si j estaba inactivo, fijar q_j = k.
15.            Actualizar el último paciente del médico j.
16.            asignado <- Verdadero
17.            Salir del ciclo sobre médicos.
18.    Si asignado = Falso:
19.        Retornar "No factible".
20. Calcular el costo fijo de médicos activados.
21. Calcular el costo de desplazamiento de cada ruta construida.
22. Retornar "Factible" y el costo total.
```

## Observaciones importantes

1. La heurística es sensible al orden de procesamiento de los pacientes.  
   Al tratarse de un método voraz, una mala decisión temprana puede impedir una solución factible posterior, incluso si tal solución existe.

2. La factibilidad heurística para un valor \(n\) **no implica** optimalidad en costo.  
   La heurística solo garantiza que construyó una solución que respeta sus reglas de asignación, no que sea la mejor posible.

3. La no factibilidad heurística para un valor \(n\) **no prueba** necesariamente que el problema exacto sea infactible con ese mismo número de médicos.  
   Solo indica que **esta heurística**, bajo su orden y su regla de asignación temprana, no logró construir una solución.

4. El uso principal del procedimiento es explorar el menor número de médicos con el que la heurística logra una solución factible de manera rápida y comprensible.
