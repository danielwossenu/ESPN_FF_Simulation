Meff = {1: {3: 0.9141378499176663}, 2: {3: 0.6669311329736592}, 6: {3: 0.9237995824634656}, 8: {3: 0.8805487053020963}, 9: {3: 0.6340512439658373}, 10: {3: 0.8839347276488161}, 12: {3: 0.8700290979631427}, 13: {3: 0.7571055684454756}, 14: {3: 0.9113101510361784}, 15: {3: 0.907784986098239}, 16: {3: 0.7728813559322034}, 17: {3: 0.7927031509121063}}
teams = {1:'Michael Koester', 2:"Zach Haywood", 6:"Johal Baez", 8:"Eric Begens", 9:"Benjamin Burnstine", 10:"Matt Goldman", 12:"Eric Wilson", 13:"Daniel Wossenu", 14:"Mohamed Somji", 15:"Andrew Frost", 16:"Joshua Bautz", 17:"Michael Goldman"}

for keys in Meff:
    print teams[keys] +': %.2f'%(Meff[keys][3]*100)+ '%'

# for keys in Meff:
#     sum = 0
#     for keys2 in Meff[keys]:
#         sum +=Meff[keys][keys2]
#     sum = sum/13.0
#     print teams[keys] +': %.2f'%(sum*100)+ '%'


# TODO make this a method for ME