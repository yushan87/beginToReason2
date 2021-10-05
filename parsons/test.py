setCode = """Facility BeginToReason;
    uses Integer_Ext_Theory;

    Operation Main();
    Procedure
        Var I, J, K: Integer;
        Read(I);
        Read(J);

	
	K := J;
	If I &gt;= K then
		K := I;
	end;






































        Confirm K &gt;= #I;
end BeginToReason;"""


answers = ["end;", "If I &gt;= K then", "K := I;", "K := J;"]

def test():
    breakLoop = False
    studentCode = ""
    i = 0
    while i < len(setCode) - 10 and not breakLoop:
        j = 0
        while j < len(answers):
            if (setCode[i: i + len(answers[j])] == answers[j]):
                studentCode = setCode[0: i - 1]
                k = 0
                while k < len(answers):
                    studentCode = studentCode + answers[k]
                    i = i + len(answers[k])
                    k += 1
                studentCode = studentCode + setCode[i + len(answers[k - 1]): len(setCode)]

                breakLoop = True
                break
            j += 1
        i += 1

    print(studentCode)

test()