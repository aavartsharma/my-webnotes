import package as pk

if(__name__ == "__main__"):
    pk.InzliteDataBase()   
    main_root = pk.tk.Tk()
    if(pk.check_platform() == "Android"):
        pk.show_welcome_android_page(main_root)
    else:
        
        pk.show_welcome_page(main_root)
