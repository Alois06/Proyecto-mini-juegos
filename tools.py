def prediction(rect, vx, vy, a, x_end, obs) -> tuple :

    obstacles = []
    obstacles_obj = []
    for ob in obs :
        obstacles.append(ob.rect)
        obstacles_obj.append(ob)

    k_stop = 0

    while k_stop < 50 : 

        if rect.right < x_end :

            k_stop += 1

            if rect.top <= 0 or rect.bottom >= 720: 
                vy *= -1

            if rect.left <= 0 or rect.right >= 1080 :
                vx *= -1

            if rect.collidelist(obstacles) >= 0 :
                for obstacle in obstacles : 

                    if rect.colliderect(obstacle) :

                        #Touche le haut ou le bas d'un obstacle
                        if (rect.left > obstacle.left and rect.right < obstacle.right):
                            if rect.top > obstacle.top and rect.top < obstacle.bottom :
                                vy *= -1
                            elif rect.bottom > obstacle.top and rect.bottom < obstacle.bottom : 
                                vy *= -1
                        
                        #Touche le côté gauche ou droite d'un obstacle
                        if rect.top > obstacle.top and rect.bottom < obstacle.bottom : 
                            if rect.left > obstacle.left and rect.left < obstacle.right :
                                vx *= -1
                            elif rect.right > obstacle.left and rect.right < obstacle.right : 
                                vx *= -1

            rect.x += vx*a
            rect.y += vy*a

        else : 
            break

    return (rect.center, vx, vy)

#fonction qui permet de trouver la coordonnée y future
def find_y(point, abs_x, vx, vy) -> float :
    coeff_a = vy/vx
    ord_y = coeff_a*(abs_x - point[0]) + point[1]
    return ord_y

#compare la différence d'abscisse et la différence d'ordonnée pour établir dans quel sens se fait la déviation 
#(dans le cas d'un angle notamment)
def compare_impact(dx, dy, vx, vy) :
    if dx > dy : 
        vy *= -1
    elif dy > dx :
        vx *= -1

    return  [vx, vy]