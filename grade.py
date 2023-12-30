print("Grade Calculator")
print("")

fullmarks = 100
exam = input("Name of the exam :")
score = float(input("input your score :"))
if score >= 90 and score <= 100 :
  print("you got", score, "% and your grade is A+")
elif score >= 80 and score < 90:
  print("you got", score, "% and your grade is A")
elif score >= 70 and score <80:
  print("you got", score, "% and your grade is B+")
elif score >= 60 and score <70:
  print("you got", score, "% and your grade is B")
elif score >=50 and score <60:
  print("you got", score, "% and your grade is C")
elif score >= 40 and score <50:
  print("you got", score, "% and your grade is C+")
elif score > 100:
  print("Please enter a valid score")
else:
  print("Sorry you are out of Grade")
 
