oferentes=[[52,6,2],[33,10,3],[23,0,0],[17,2,0],[7,6,0],[7,10,0]]
acciones=10
precio_minimo=7
def subasta_publica(acciones, precio_minimo,oferentes):

    n = len(oferentes)
    # Matriz de memoria para la programación dinámica
    memo = [[None for j in range(acciones + 1)] for i in range(n + 1)]
    
    # Función recursiva auxiliar que implementa la programación dinámica
    def dp(i, j):
        # print("abrir")
        # Si ya se ha calculado este valor, devolverlo
        if memo[i][j] is not None:
            return memo[i][j]
        
        # Casos base
        if i == n:
            # Se acabaron las ofertas, solo se pueden comprar acciones al precio mínimo
            memo[i][j] = j * precio_minimo
            return memo[i][j]
        if j == 0:
            # No se quieren comprar acciones, el precio es 0
            memo[i][j] = 0
            return memo[i][j]
        
        # Comprobar si se puede aceptar la oferta actual
        oferta = oferentes[i]
        precio = oferta[0]
        maximo = oferta[1]
        minimo = oferta[2]
        
        max_acciones = min(j, maximo) # No se pueden comprar más acciones de las que ofrece la oferta o de las que quedan por vender
        min_acciones = min(j, minimo) # Se deben comprar al menos las acciones mínimas o las que quedan por vender
        
        # Si no se pueden comprar las acciones mínimas, se descarta la oferta
        if min_acciones > max_acciones:
            memo[i][j] = dp(i+1, j)
            return memo[i][j]
        
        # Calcular la ganancia si se acepta la oferta
        ganancia = precio * min_acciones + dp(i+1, j-min_acciones)
        
        
        # Probar a aceptar la oferta y otras ofertas
        for k in range(min_acciones+1, max_acciones+1):
            #print(precio*min_acciones)
            ganancia_k = precio * k + dp(i+1, j-k)
            if ganancia_k > ganancia:
                ganancia = ganancia_k
                
        
        # No aceptar la oferta y seguir probando otras ofertas
        ganancia_no = dp(i+1, j)
        if ganancia_no > ganancia:
            ganancia = ganancia_no
        
        memo[i][j] = ganancia
        
        return memo[i][j]
    
    # Llamada inicial a la función recursiva
    print(dp(0, acciones))

subasta_publica(acciones, precio_minimo, oferentes)