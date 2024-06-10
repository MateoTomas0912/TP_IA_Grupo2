from simpleai.search import SearchProblem, astar, greedy

def jugar(frascos, dificil=False):
    """
    Resuelve el juego Sort Em All.

    Args:
        frascos: Una tupla de tuplas, donde cada tupla interna representa un frasco
                 y cada elemento de la tupla interna es el color de un cuarto del frasco,
                 ordenados de abajo hacia arriba.
        dificil: Un booleano indicando si se trata de un caso difícil.

    Returns:
        Una lista de tuplas, donde cada tupla representa un movimiento en el juego.
        Cada tupla contiene dos números: el frasco de origen y el frasco de destino.
    """
    class SortEmAllProblem(SearchProblem):
        def cost(self, state1, action, state2):
            return 1

        def is_goal(self, state):
            color_en_frascos = {}
            for frasco in state:
                if len(frasco) > 0:
                    # Verificar si todos los valores en el frasco son iguales
                    if len(set(frasco)) != 1:
                        return False
                    # Verificar si el color ya está en otro frasco
                    color = frasco[0]
                    if color in color_en_frascos:
                        return False
                    color_en_frascos[color] = True
            return True

        def actions(self, state):
            actions = []
            num_frascos = len(state)
            for i in range(num_frascos):
                if len(state[i]) == 4 and len(set(state[i])) == 1:
                    continue
                for j in range(num_frascos):
                    if i != j and state[i] and (not state[j] or (state[i][-1] == state[j][-1] and len(state[j]) < 4)):
                        if len(state[j]) < 4:
                            actions.append((i+1, j+1))
            return actions

        def result(self, state, action):
            new_state = [list(frasco) for frasco in state]

            origen, destino = action
            origen -= 1
            destino -= 1

            color = new_state[origen][-1]  # Color en el cuarto superior del frasco origen
            dest_frasco = new_state[destino]  # Frasco destino

            # Mover todos los cuartos del mismo color al frasco destino
            for cuarto in reversed(new_state[origen]):
                if cuarto == color and len(dest_frasco) < 4:
                    dest_frasco.append(color)
                    new_state[origen].pop()
                else:
                    break

            return tuple(tuple(frasco) for frasco in new_state)

        def heuristic(self, state):
            # Heurística: número de frascos incompletos o con colores mezclados
            frascos_incompletos = 0
            for frasco in state:
                if frasco and (len(frasco) != 4 or len(set(frasco)) != 1):
                    frascos_incompletos += 1
            return frascos_incompletos

    problema = SortEmAllProblem(frascos)
    if dificil:
        resultado = greedy(problema, graph_search=True)
    else:
        resultado = astar(problema, graph_search=True)

    if resultado:
        pasos = []
        for paso,_ in resultado.path():
            pasos.append(paso)
        return pasos[1:]
    else:
        return []  # No se encontró solución


# Ejemplo de uso
if __name__ == "__main__":
    pasos = jugar(
        frascos=(
            ("verde", "azul", "rojo", "naranja"),
            ("azul", "rosa", "naranja"),
            ("rosa", "celeste", "verde", "verde"),
            ("rosa", "rojo", "celeste", "celeste"),
            ("rojo", "azul", "lila"),
            ("verde", "naranja", "celeste", "rojo"),
            ("azul", "naranja", "rosa"),
            ("lila", "lila", "lila"),
            (),
        ),
        dificil=True,

    )
    for paso in pasos:
        print(paso)
