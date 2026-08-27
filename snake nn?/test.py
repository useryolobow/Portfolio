import random
n = random.randint(0,100000)
class Solution(object):
    def romanToInt(self, s):
        operations = {"I": 1, "X": 10, "V": 5, "L":50, "C": 100, "D": 500, "M": 1000}
        chars = list(s)
        result = 0
        for i in range(len(s)):
            num = 0
            if i > 0 and operations[s[i-1]] < operations[s[i]]:
                num = operations[s[i]] - operations[s[i-1]]
            elif i < len(s)-1 and operations[s[i]] < operations[s[i+1]]:
                pass
            else:
                num = operations[s[i]]
            result += num
        return result

thing = Solution()
print(thing.romanToInt("IV"))