def test_gui():
    import Barnes_Hut.gui.DisplayArea as DA
    DA.__nose()

def test_object_generator():
    import Barnes_Hut.stellar_objects.ObjectGenerator as Og
    Og.__nose()

def test_config_loader():
    import Barnes_Hut.gui.ConfigChecker as CC
    CC.__nose()

if __name__ == '__main__':
    test_config_loader()
    #test_object_generator()