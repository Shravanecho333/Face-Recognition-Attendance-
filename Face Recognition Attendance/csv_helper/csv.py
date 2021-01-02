from datetime import datetime

FILENAME = 'attendance.csv'


def initialize_csv():
    f = open(FILENAME, 'w')
    f.write('NAME,TIME')
    f.close()


def mark_attendance(name):
    with open(FILENAME, 'r+') as f:
        # we need to read beforehand so we don't write students twice
        names = set()
        for line in f:
            names.add(line.split(',')[0].strip())
        if name not in names:
            now = datetime.now().strftime("%H:%M:%S")
            f.writelines(f'\n{name},{now}')


def prepare_final_report(all_students):
    all_students = set(all_students)
    with open(FILENAME, 'r+') as f:
        for line in f:
            # don't consider the students that are already here
            student = line.split(',')[0].strip()
            if student in all_students:
                all_students.remove(student)

        # report the ones that are not here
        f.write("\n")
        for student in all_students:
            # absent students
            f.writelines(f'\n{student},00:00:00')
