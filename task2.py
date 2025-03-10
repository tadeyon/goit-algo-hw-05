import re

def generator_numbers(text: str):
    pattern = r'(?<= )-?\d+(?:\.\d+)?(?= )' # regular expression that finds number written with dot and separated with spaces
    for match in re.finditer(pattern, text):
        yield float(match.group())

def sum_profit(text: str, func: callable):
    return sum(func(text))