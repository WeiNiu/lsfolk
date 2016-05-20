class A():
    z=0
    def __init__(self):
        self.z=10
#    @staticmethod
    def summation(self, x,y):
        return self.z+x+y*2

class B():
    
    def getS(self,x,y):
        b=A()
        return b.summation(x,y)
    
a=A()
print a.summation(5,2)
c=B()
print c.getS(5,2)
name_split=['TEXAsAggies','KobeBrant']
new=[]
for text in name_split:
    words=""
    prev_letter=text[0]
    word_length = len(text)
    words += prev_letter
    for i in range(1, len(text)):
        cur_letter = text[i]
        if cur_letter.isupper() and prev_letter.islower():
            words += ' '
        words += cur_letter
        prev_letter = cur_letter
    words = words.split(' ')
    print words
    for word in words:
        new.append(word.lower())
    #new+=' '
print new    
