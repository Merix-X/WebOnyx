from search_string import SearchStringAsBool

def is_in_path(to_detect):
    booleen, string = SearchStringAsBool("databaze.txt", to_detect)
    string2 = string.split(to_detect)[-1].strip()
    if booleen:
        return string2
    elif booleen == False:
        return False