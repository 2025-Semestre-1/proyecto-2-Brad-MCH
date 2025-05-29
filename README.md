# Proyecto #2 | Taller de programación GR61

## Tecnológico de Costa Rica

## Información del estudiante

- **Nombre:** Bradly Morgan Ching
- **Carné:** 2025064803

## _Estado del proyecto:_ Superior

## [Link del video](https://drive.google.com/drive/folders/1DSjk3d-U89M-o8fpGWbkbJq-r29UgEao?usp=sharing)

# Documentación

## Manual de usuario

Al iniciar el programa y clickearse el botón de jugar, se le pedirá al usuario ingresar su usuario y contraseña. Si tiene un usuario registrado, puede tocar al botón de iniciar sesión, de lo contrario, una vez ingresados los datos, puede presionar al botón de registrarse para crear un nuevo usuario y iniciar el juego

Una vez en la pantalla del juego inicial, este empezará pausado, para iniciar el juego puede tocar el botón de iniciar juego o tocar la tecla de espacio o escape

Un requerimiento era que se debían agregar obstaculos al juego, sin embargo, habiendo probado varias veces el juego con obstaculos, me dí cuenta que la matriz del juego no es lo suficientemente grande para que los obstaculos le sumen dificultad al juego sin restarle jugabilidad. Es por esto que añadí un cheat code para desactivarlos. Puede hacerlo si mantiene apretado o presiona 3 veces seguidas la tecla de borrar (retroceso)

Para pausar puede presionar el botón de pausar o las teclas de escape o espacio

Para moverse puede utilizar las flechas direccionales, pero la flecha de arriba rota la figura; también puede utilizar las teclas wasd para estos propositos. Adicionalmente, puede utilizar la tecla R para rotar.

El botón de guardar y salir guarda la partida y sale del programa

Al perder, el botón de salir, guarda la partida (Solo información de puntaje, porque el usuario perdio) y sale del programa. El botón de guardar y salir hace lo mismo. Adicionalmente el botón de volver a jugar hace lo mismo, pero en lugar de salir del programa, reinicia la partida.

## Descripción del problema

Se debía realizar un Tetris tradicional, con el añadido de obstaculos, ranking y velocidad progresiva

## Diseño del programa

Como me es habitual, no pude evitar añadir cosas extras al programa. Se dijo que el programa debe de ser capáz de guardar las partidas, pero el programa también tiene un ranking entonces no sería justo que otra persona pueda entrar a la partida de otro y hacerlo perder si tiene un puntaje alto, entonces decidí diseñar un sistema de login.

Además, agregué algunos efectos visuales extras, como que los bloques del borde se vuelven verdes por un instante cuando el jugador consigué romper una fila y tambien se vuelven azules cuando el juego está en pausa.

Las indicaciones requerian que crearamos una matriz que sirviera como representación visual de los juegos guardados, sin embargo, en el desarrollo me dí cuenta que esta matriz no servía para poder desarrollar la lógica del juego, entonces estas matrices se guardan en matrices_profe y para la lógica del juego se utilizan otras matrices las cuales están guardadas en data_partidas

El juego se desarrolla en una matriz y las figuras están formadas por bloques individuales. Esto para universalizar la lógica de rotación y creación de figuras, de está forma, contando las combinaciones de colores, existen 40 figuras diferentes que pueden aparecer. Descubrí que si se tiene el eje de rotación de una figura en una matríz, la rotación de sus bloques sigue un patron definido dependiendo de su posición cardinal, entonces solo debí programar 8 casos distintos y definir los ejes centrales de las 8 figuras, y eso bastó para poder rotar cualquier figura.

## Librerias usadas

- PIL, para manejo de imagenes
- Random, para eventos aleatorios
- Time, para hacer debbouncers

## Análisis de resultados

Se logró concluir con todos los objetivos que se pidió para este proyecto, incluyendo los objetivos extras; además, se logró añadir con éxito las funcionalidades extras que se mencionaron anteriormente

## Conclusión

Creo que aprendí bastante con la realización de este programa. No me gusta la libreria TKinter porque es muy limitada y usualmente es muy dificil hacer una GUI atractiva y moderna sin tener que complicarse añadiendo funciones extras que no existen por defecto, pero como este programa se basa en un juego retro, decidí aplicar un estilo minimalista y así no tuve muchos problemas.
