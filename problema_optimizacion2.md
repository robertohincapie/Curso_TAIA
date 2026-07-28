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
C_{S,i}\,z_{Sij}
+
\sum_{\substack{a,b\in\mathcal U\\a\neq b}}
C_{ab}\,z_{abj}
+
\sum_{i\in\mathcal U}
C_{i,F}\,z_{iFj}
\Bigg)
\end{aligned}
\]

sujeto a

\[
\begin{aligned}
&
\sum_{j\in\mathcal D}
\sum_{k\in\tau_i}
x_{ijk}
=
1,
&&
\forall i\in\mathcal U,
\\[2mm]
&
\sum_{k\in\tau_i}
x_{ijk}
\le
u_j,
&&
\forall i\in\mathcal U,\;
\forall j\in\mathcal D,
\\[2mm]
&
\sum_{h\in\mathcal H}
y_{jh}
=
u_j,
&&
\forall j\in\mathcal D,
\\[2mm]
&
x_{ijk}
\le
\sum_{\substack{
h\in\mathcal H\\
h\le k\\
k+c_i-1\le h+H-1}}
y_{jh},
&&
\forall i,j,\;
k\in\tau_i,
\\[2mm]
&
\sum_{i\in\mathcal U}
z_{Sij}
=
u_j,
&&
\forall j\in\mathcal D,
\\[2mm]
&
\sum_{i\in\mathcal U}
z_{iFj}
=
u_j,
&&
\forall j\in\mathcal D,
\\[2mm]
&
z_{Sij}
+
\sum_{\substack{a\in\mathcal U\\a\neq i}}
z_{aij}
=
\sum_{k\in\tau_i}
x_{ijk},
&&
\forall i,j,
\\[2mm]
&
z_{iFj}
+
\sum_{\substack{b\in\mathcal U\\b\neq i}}
z_{ibj}
=
\sum_{k\in\tau_i}
x_{ijk},
&&
\forall i,j,
\\[2mm]
&
t_b
\ge
t_a
+
c_a
+
\delta_{ab}
-
M_T(1-z_{abj}),
&&
\forall j,\;
a\neq b,
\\[2mm]
&
t_i
\ge
q_j
+
\delta_{S,i}
-
M_T(1-z_{Sij}),
&&
\forall i,j,
\\[2mm]
&
t_i+c_i+\delta_{i,F}
\le
q_j+H
+
M_T(1-z_{iFj}),
&&
\forall i,j,
\\[2mm]
&
u_j
\ge
u_{j+1},
&&
j=1,\ldots,n-1,
\\[2mm]
&
x_{ijk},
u_j,
y_{jh},
z_{abj},
z_{Sij},
z_{iFj}
\in
\{0,1\}.
\end{aligned}
\]