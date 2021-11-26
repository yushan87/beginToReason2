setCode = """Facility BeginToReason;
    uses Integer_Ext_Theory;

    Operation Main();
    Procedure
        Var I, J, K: Integer;
        Read(I);
        Read(J);

	
	
    


    






































        Confirm K &gt;= #I;
end BeginToReason;"""


answers = ["end;", "If I &gt;= K then", "K := I;", "K := J;"]

def test():
    foundBreak = False
    studentCode = ""
    i = 0
    while i < len(setCode) - 10:
        #print("First loop")
        j = 0
        while j < 10:
            #print("Second loop")
            print(ord(setCode[i]))
            print(ord(setCode[i + j]))
            if setCode[i] != setCode[i + j]:
                #print("Unequal chars")
                foundBreak = False
                i += 1
                j += 1
                break
            else:
                #print("Equals chars")
                foundBreak = True
                j += 1
                continue
            
            

        if foundBreak and j == 10:
            #print("Found break")
            studentCode = setCode[0: i]
            k = 0
            while k < len(answers):
                #print("Answers while loop")
                studentCode += answers[k]
                k += 1
            studentCode += setCode[i + 1: len(setCode)]
            break
        
        i += 1

    print(studentCode)

test()