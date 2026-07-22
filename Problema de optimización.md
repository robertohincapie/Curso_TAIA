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

$x_{i,j,k} Variable binaria que tiene un valor de 1 si el médico $j$ atiende al usuario $i$, comenzando en la ranura de tiempo $k$. 

$y_j$ Variable binaria que tiene un valor de 1 si el médico $j$ está activo en el turno. En nuestro caso, suponemos algo: Es necesario atender a todos los pacientes, pero podemos disminuir el número de médicos que necesitemos. 

## Parámetros del problema: 

### Servicios de los usuarios: 

El servicio del usuario $i$ está determinado por 3 cantidades
- $a_i$ La ranura de tiempo en que el servicio puede comenzar, no antes de ese tiempo. 
- $b_i$ La ranura de tiempo en que el servicio puede terminar como máximo. El usuario debe ser atendido entre $a_i$ y $b_i$. 
- $c_i$ La duración del servicio en tiempo dado por el número de ranuras necesarias. 

### Retrazos de movilidad: 

Si un médico se tiene que desplazar desde un usuario $i_1$ hasta la ubicación de un usuario $i_2$, se toma un tiempo $\delta_{i_1, i_2}$. Esta matriz está calculada para todos los pares posibles de usuarios y no es necesariamente simétrica. 

## Formulación del problema: 

Para este caso suponemos una cantidad entera M que representa un número muy grande. Así mismo, los conjuntos $\mathbf{U}$, $\mathbf{D}$ y $\mathbf{T}$. Para un usuario $i$, definimos una variable auxiliar $\alpha_i^k$, binaria, que vale 1 si el tiempo $k$ es un inicio de atención posible para el usuario $i$, esto es, que si el servicio inicia en esa ranura de tiempo, va a respetar la ventana que el usuario requiere. $0$ si cae por fuera. 

$$\alpha_i^k = 1 \; si \; k \in \{a_i, a_i+1, \ldots, b_i-c_i+1\}$$

Esto permite definir el conjunto $\mathbf{\tau_i}=\{k\in \mathbf{T} | \alpha_i^k = 1\}$, que corresponde a todas las ranuras de tiempo posibles para el inicio del servicio. 


$$
\begin{aligned}
\min \quad & \sum_{j \in \mathbf{D}}{y_j}\\
\text{s.a.}\quad
&i)\;\sum_{j \in \mathbf{D}}\sum_{k \in \mathbf{\tau_i}}x_{i,j,k}==1, &&\forall i\in \mathbf{U},\\
&ii)\;x_{i,j,k}\leq \alpha_i^k \left( 1-\frac{1}{M}\sum_{\eta \in \mathbf{U} \setminus \{i\}}\sum_{s=k-c_\eta-\delta_{\eta,i}+1}^{k}x_{\eta,j,s} \right) , &&\forall i\in \mathbf{U},\forall j\in \mathbf{D},\forall k\in \mathbf{T},\\
&iii)\;\sum_{i \in \mathbf{U}}\sum_{k \in \mathbf{\tau_i}}x_{i,j,k}\leq M y_j, &&\forall j\in \mathbf{D},\\

\end{aligned}
$$

---

# Alternativas de escenarios a considerar, encontrando nuevas alternativas de optimización para definir. 

El proceso de la analítica prescriptiva busca plantear diferentes modelos que pueden ser alternativas interesantes respecto al problema original. 

Para este caso, propongo que analicemos 3 escenarios alternativos: 

## Separar la ciudad por regiones:

Esto es, definir n regiones (n es un parámetro por definir), donde los usuarios se organizan en n clusters por cercanía y el problema se tiene que resolver n veces, solucionando el número de ambulancias totales como la suma de las ambulancias por cada sector. 

## Separar los servicios por duraciones: 

Esto es, concentrar n tipos de servicio por la duración que tienen. Esto se refiere a si n=2, los servicios que duran hasta, solo como ejemplo, menos de 1 hora y los servicios que duran más de una hora. Si n=3, hay otras divisiones de duraciones. Se debe solucionar el número de ambulancias totales como la suma de las ambulancias por cada grupo de duraciones. 

## Hacer el modelo considerando algo similar a un planificador: 

Hacer un modelo que no tenga la condición extricta por la ventana, sino que la atención por fuera de la ventana tenga un costo adicional en el servicio y mientras 