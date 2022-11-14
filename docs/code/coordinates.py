


import ananimlib as al

def main():
    coord_snip1()
    al.play_movie()



def coord_snip1():
    
    
    nat = Native()


    al.Animate(
        al.AddAnObject(nat),
        al.Wait(1.0)
    )



class Native(al.CompositeAnObject):
    
    
    def __init__(self):
        super().__init__()
        grid = al.CoordGrid(
            screen_size   = [10,8],
            grid_size     = [10,8],
            major_spacing = [1,1],
            minor_spacing = [0.2,0.2],
            offset = [0,0]
        )
        
        grid.opacity = 0.25
    
    
        box = al.Rectangle(
            size = [1.0,1.0],
            pen  = al.Pen(
                stroke_color   = "#FFFFFF",
                stroke_opacity = 1.0,
                stroke_width   = 3.0,
                fill_color     = "#cda448",
                fill_opacity   = 1.0
            )
        )
        
        self.add_anobject(grid)
        self.add_anobject(box)
        

if __name__=="__main__":
    main()