import locale
print(f"Current locale: {locale.getlocale()}")
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    print(f"Set to en_US.UTF-8: {locale.getlocale()}")
    print(f"Test number: {74.5:n}")
    print(f"Test number f-string: {74.5:.1f}")
except Exception as e:
    print(f"Failed to set en_US.UTF-8: {e}")

try:
    locale.setlocale(locale.LC_ALL, 'en_US')
    print(f"Set to en_US: {locale.getlocale()}")
    print(f"Test number: {74.5:n}")
except Exception as e:
    print(f"Failed to set en_US: {e}")
