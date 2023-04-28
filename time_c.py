#!/usr/bin/python3

def timeConversion(s):
    if "PM" in s:
        s=s.replace("PM"," ")
        t= s.split(":")
        if t[0] != '12':
            t[0]=str(int(t[0])+12)
            s= (":").join(t)
        return s
    else:
        s = s.replace("AM"," ")
        t= s.split(":")
        if t[0] == '12':
            t[0]='00'
            s= (":").join(t)
        return s

if __name__ == "__main__":
    print(timeConversion("12:20PM"))
