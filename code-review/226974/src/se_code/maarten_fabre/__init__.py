# Taken from the comment by [Maarten Fabre](https://codereview.stackexchange.com/users/123200/maarten-fabr%c3%a9)
# https://codereview.stackexchange.com/questions/226970/printing-a-list-as-a-b-c-using-python/226974#comment441720_226976
def display(flavours):
    print(', '.join(flavours), end='.\n')
