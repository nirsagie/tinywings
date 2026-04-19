class State:
    @staticmethod
    def get_as_array(env):
        """ הופך את נתוני המשחק למערך מספרים עבור ה-AI """
        # כרגע מחזיר רק את הגובה והמיקום
        return [env.bird_x, env.bird_y]