def check_allergy_risk(user_allergies, ingredients):
    allergies        = [str(a).lower().strip() for a in user_allergies]
    ingredient_list  = [str(i).lower().strip() for i in ingredients]
    for allergy in allergies:
        for ingredient in ingredient_list:
            if allergy and allergy in ingredient:
                return True
    return False
