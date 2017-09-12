Meff = {1: {1: 0.9269526128488481}, 2: {1: 0.9326247864869996}, 6: {1: 0.834688897925986}, 8: {1: 0.9127754949570415}, 9: {1: 0.8568722374237003}, 10: {1: 0.6806167400881056}, 12: {1: 0.7867031551835157}, 13: {1: 0.9145299145299147}, 14: {1: 0.9494882064975523}, 15: {1: 0.9313725490196078}, 16: {1: 0.783356258596974}, 17: {1: 0.7403169014084506}}
teams = {1:'Michael Koester', 2:"Zach Haywood", 6:"Johal Baez", 8:"Eric Begens", 9:"Benjamin Burnstine", 10:"Matt Goldman", 12:"Eric Wilson", 13:"Daniel Wossenu", 14:"Mohamed Somji", 15:"Andrew Frost", 16:"Joshua Bautz", 17:"Michael Goldman"}

for keys in Meff:
    print teams[keys] +': %.2f'%(Meff[keys][1]*100)+ '%'

# for keys in Meff:
#     sum = 0
#     for keys2 in Meff[keys]:
#         sum +=Meff[keys][keys2]
#     sum = sum/13.0
#     print teams[keys] +': %.2f'%(sum*100)+ '%'


# TODO make this a method for ME