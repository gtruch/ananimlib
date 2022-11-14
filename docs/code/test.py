


def main():

    file = 'tutorial_snip5.py'
    
    with open(file) as f:
        stuff = f.read()
        exec(stuff,globals())

main()





