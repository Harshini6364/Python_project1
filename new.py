import pandas as pd
import os
CSV_FILE="students.csv"
try:
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE)>0:
        df=pd.read_csv(CSV_FILE,encoding="utf-8")
    else:
        df=pd.DataFrame(columns=["Roll_No","Name","Branch","Year","Gender","Age","Attendance_%","Mid1_Marks","Mid2_Marks","Quiz_Marks","Final_Marks"])
except pd.errors.ParserError:
    print("CSV file is corrupted")
    df=pd.DataFrame(columns=["Roll_No","Name","Branch","Year","Gender","Age","Attendance_%","Mid1_Marks","Mid2_Marks","Quiz_Marks","Final_Marks"])
def add_student():
    global df
    try:
        roll_no=int(input("Enter a roll no: "))
        if roll_no<=0:
            raise ValueError("Negative roll number is not allowed.")
            return df
        elif roll_no in df["Roll_No"].values:
            print("Roll number rejected.") 
            return df
    except ValueError:
        print("Roll number is not valid.")
        return df
    name=input("Enter name: ")
    branch=input("Enter branch: ")
    year=int(input("Enter year: "))
    gender=input("Enter gender: ")
    age=int(input("Enter age: "))
    attendance=float(input("Enter attendance-%: "))
    
    if not (0<=attendance<=100):
        print("Attendance must be 0-100.")
        return 
    mid1_marks=int(input("Enter mid1 marks: "))
    if not (0<=mid1_marks<=30):
        print("Marks must be 0-30.")
        return 
    mid2_marks=int(input("Enter mid2 marks: "))
    if not (0<=mid2_marks<=30):
        print("Marks must be 0-30.")
        return 
    quiz_marks=int(input("Enter quiz marks: "))
    if not (0<=quiz_marks<=10):
        print("Marks must be 0-10.")
        return 
    final_marks=mid1_marks+mid2_marks+quiz_marks
    new_student={
        "Roll_No": roll_no,
        "Name": name,
        "Branch": branch,
        "Year": year,
        "Gender": gender,
        "Age": age,
        "Attendance_%": attendance,
        "Mid1_Marks": mid1_marks,
        "Mid2_Marks": mid2_marks,
        "Quiz_Marks": quiz_marks,
        "Final_Marks": final_marks
    }
    df=pd.concat([df, pd.DataFrame([new_student])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    print("Student added successfully!")
    return df     
def search_student():
    global df
    input_value=input("Enter Roll No or Name to search: ")
    if input_value.isdigit():
        try:
            roll_no=int(input_value)
            if roll_no<=0:
                raise ValueError("Negative roll number is not allowed.")
                return df
        except ValueError:
            print("Roll number is not valid.")
            return df
        mask=df["Roll_No"]==int(input_value)
        result=df[mask]
        print(result)
    else:
        result=df[df["Name"].str.contains(input_value,case=False,na=False)]
        print(result)
def update_student():
    global df
    try:
        roll_no=int(input("Enter a roll no to update: "))
        if roll_no<=0:
            raise ValueError("Negative roll number is not allowed.")
            return df
    except ValueError:
        print("Roll number is not valid.")
        return df
    if roll_no in df["Roll_No"].values:
        choice=input("Enter field to update(marks,attendance): ").strip().lower()
        if choice=="marks":
            col=input("Enter which marks to update(Mid1_Marks/Mid2_Marks/Quiz_Marks): ").strip().lower()
            if col not in ["mid1_marks","mid2_marks","quiz_marks"]:
                print("Invalid marks type")
                return df
            elif col=="mid1_marks":
                col="Mid1_Marks"
            elif col=="mid2_marks":
                col="Mid2_Marks"
            elif col=="quiz_marks":
                col="Quiz_Marks"
        elif choice=="attendance":
                col="Attendance_%"
        else:
             print("Invalid choice")
             return df
        old_value=df.loc[df["Roll_No"]==roll_no, col].values[0]
        print(f"Old value: {old_value}")
        new_value=float(input(f"Enter new {col}: "))
        confirm=input(f"Confirm updating {col} from {old_value} to {new_value}? (yes/no): ").strip().lower()
        if confirm=="yes":
            df.loc[df["Roll_No"]==roll_no, col]=new_value
            df.to_csv(CSV_FILE, index=False)
            print("Record updated successfully!")
        else:
            print("Update cancelled.")
    else:
        print("Roll number not found.")
def delete_student():
    global df
    roll_no=int(input("Enter a roll no: "))
    if roll_no not in df["Roll_No"].values:
        print(f"Roll No {roll_no} not found.")
        return df
    confirm=input("Do you want to delete this record? (Yes/No): ").strip().lower()
    if confirm!="yes":
        print("Deletion cancelled.")
        return df
    deleted_record=df[df["Roll_No"]==roll_no]
    df=df[df["Roll_No"]!=roll_no]
    df.to_csv(CSV_FILE,index=False)
    print(f"Student with Roll No {roll_no} deleted from {CSV_FILE}.")
    deleted_file="students_deleted.csv"
    deleted_record.to_csv(deleted_file,index=False)
    print(f"Deleted record moved to {deleted_file}.")
def assign_grade(marks):
    if marks>=60:
        return "A"
    elif marks>=50:
        return "B"
    elif marks>=40:
        return "C"
    else:
        return "D"
def generate_report():
    branch=input("Enter branch: ")
    year=int(input("Enter year: "))
    class_df=df[(df["Branch"]==branch)&(df["Year"]==year)]
    if class_df.empty:
        print(f"No records found for Branch={branch},Year={year}.")
        return
    class_df["Grade"]=class_df["Final_Marks"].apply(assign_grade)
    total_students=len(class_df)
    class_avg=class_df["Final_Marks"].mean()
    highest_scorer=class_df['Final_Marks'].idxmax()
    lowest_scorer=class_df['Final_Marks'].idxmin()
    grade_distribution=class_df["Grade"].value_counts().to_dict()
    print("Parent-Teacher Meeting Report")
    print(f"Branch: {branch}, Year: {year}")
    print("-"*40)
    print(f"Total Students : {total_students}")
    print(f"Class Average  : {class_avg:.2f}")
    print("Highest Scorer : ",class_df.loc[highest_scorer,"Name"])
    print("Lowest Scorer  : ",class_df.loc[lowest_scorer,"Name"])
    print("Grade Distribution : ")
    for grade, count in grade_distribution.items():
        print(f"{grade}→{count} students")
    export=True
    if export:
        highest=class_df.loc[highest_scorer,"Name"]
        lowest=class_df.loc[lowest_scorer,"Name"]
        report_filename="report_IT_2.csv"
        report={
            "Total Students": [total_students],
            "Class Average": [class_avg],
            "Highest Scorer": [highest],
            "Lowest Scorer": [lowest],
            **{f"Grade_{g}": [c] for g, c in grade_distribution.items()}
        }
        pd.DataFrame(report).to_csv(report_filename, index=False)
        print(f"Report exported to {report_filename}")
    return class_df
def bulk_import():
    global df
    import_errors="import_errors.csv"
    new_file="new_students.csv"
    if not os.path.exists(new_file):
        print("File not found")
    else:
        df=pd.read_csv(new_file,encoding="utf-8",on_bad_lines='skip')
    errors=[]
    dup_mask=df['Roll_No'].duplicated(keep='first')
    valid_rows=[]
    #existing_rolls=set()
    for idx,row in df.iterrows():
        line_no=idx+2  
        roll=row.get('Roll_No')
        name=row.get('Name')
        if pd.isna(roll) or str(roll).strip() == "":
            errors.append({"line": line_no, "error": "Roll_No missing or blank", "row": row.to_dict()})
            continue
        if dup_mask.iloc[idx]:
            errors.append({"line": line_no, "error": "Duplicate Roll_No in import file", "row": row.to_dict()})
            continue
        if pd.isna(name) or str(name).strip() == "":
            errors.append({"line": line_no, "error": "Name missing or blank", "row": row.to_dict()})
            continue
        valid_rows.append(row.to_dict())
        #existing_rolls.add(str(roll).strip())
    valid_df=pd.DataFrame(valid_rows)
    error_df=pd.DataFrame(errors)
    if not error_df.empty:
        error_df.to_csv(import_errors,index=False)
    print("Valid rows to import:")
    print(valid_df)
    print("Error rows (see import_errors.csv):")
    print(error_df)
def sort():
    file_name="sorted_students.csv"
    choice=input("Enter marks or attendance:").strip().lower()
    if choice=="marks":
        sorted_marks=df.sort_values("Final_Marks",ascending=False)
        print("The sorted order of final marks: ",sorted_marks)
        sorted_marks.to_csv(file_name,index=False)
    elif choice=="attendance":
        threshold_value=int(input("Enter the threshold vaue: "))
        filtered_attendance=df[df["Attendance_%"]<threshold_value]
        print("The filtered students by attendance: ",filtered_attendance)
        filtered_attendance.to_csv(file_name,index=False)
    else:
        print("Invalid choice")
def main():
    while True:
        print("Student Management System")
        print("1.Add Student")
        print("2.Search Student")
        print("3.Update Student")
        print("4.Delete Student")
        print("5.Summarized Report")
        print("6.Sorting")
        print("7.Bulk import")
        print("8.Exit")
        choice=int(input("Enter option: "))
        match choice:
            case 1:
                add_student()
            case 2:
                search_student()
            case 3:
                update_student()
            case 4:
                delete_student()
            case 5:
                generate_report()
            case 6:
                sort()
            case 7:
                bulk_import()
            case _:
                print("Invalid choice.")
if __name__ == "__main__":
    main()