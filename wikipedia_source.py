import wikipedia
import nltk
wikipedia.set_lang("es")

results = wikipedia.search("luz salgado")
if len(results) < 1:
    raise Exception("invalid query person search")

focus = results[0]

page = wikipedia.page(focus)

tokens = nltk.tokenize.sent_tokenize(page.content, language="es")
print(tokens)


