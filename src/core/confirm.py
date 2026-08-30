def confirm():
    answer = input("Do you want to continue? [Y/n] ").strip().lower()
    #'Sim' and 's' ae from portuguese
    if answer in ["", "y", "yes", "sim", "s"]:
        return True
    return False