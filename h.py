from deep_translator import GoogleTranslator
to_translate = 'I want to translate this text'
translated = GoogleTranslator(source='auto', target='de').translate(to_translate)
# outpout -> Ich möchte diesen Text übersetzen
print(translated)