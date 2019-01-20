import re
pattern = re.compile(u"[\u4e00-\u9fa5_a-zA-Z0-9]+")
word = [' ','你号 ','.','你']
def word_compile(n):
    return bool(re.search(pattern, n))
result = filter(word_compile, word)
print(list(result))
