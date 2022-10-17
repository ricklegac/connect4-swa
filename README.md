<b>
John von Neumann es el creador del teorema minimax, quien dio la siguiente noción de lo que era un juego
Un juego es una situación conflictiva en la que uno debe tomar una decisión sabiendo
que los demás también toman decisiones, y que el resultado del conflicto se determina, de
algún modo, a partir de todas las decisiones realizadas.</b>

<h1><u><b>Minimax:</b></u></h1>
La función minimax en connect4.py  implementa una búsqueda minimax depth-limited. Como el juego se puede jugar entre dos IA o un IA vs un jugador humano, aquí el IA 1 se trata como el jugador MAX y el IA 2 o Humano como el jugador MIN. Como no es factible buscar en todo el árbol del juego, nuestro código ha limitado la búsqueda a una profundidad arbitraria mediante el uso de la GUI. 
Las hojas de su arbol minimax se evalua con la funcion proporcionada para tratarlas como nodos terminales (vea utils.utils).
