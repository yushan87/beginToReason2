SET_CODE = """Facility BeginToReason;
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
    found_break = False
    student_code = ""
    i = 0
    while i < len(SET_CODE) - 10:
        #print("First loop")
        j = 0
        while j < 10:
            #print("Second loop")
            print(ord(SET_CODE[i]))
            print(ord(SET_CODE[i + j]))
            if SET_CODE[i] != SET_CODE[i + j]:
                #print("Unequal chars")
                found_break = False
                i += 1
                j += 1
                break
            else:
                #print("Equals chars")
                found_break = True
                j += 1
                continue

        if found_break and j == 10:
            #print("Found break")
            student_code = SET_CODE[0: i]
            k = 0
            while k < len(answers):
                #print("Answers while loop")
                student_code += answers[k]
                k += 1
            student_code += SET_CODE[i + 1: len(SET_CODE)]
            break

        i += 1

    print(student_code)

test()
