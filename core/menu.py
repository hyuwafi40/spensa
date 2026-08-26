from django.urls import reverse, NoReverseMatch
from core.access import is_authenticated
from core.utils.constants import JobChoices


class MenuItem:
    def __init__(self, name, label, url_name, icon, roles):
        self.name = name
        self.label = label
        self.url_name = url_name
        self.icon = icon
        self.roles = roles
        try:
            self.url = reverse(f"core:{url_name}")
        except NoReverseMatch:
            self.url = "#"


class MenuCategory:
    def __init__(self, name, label, icon, items):
        self.name = name
        self.label = label
        self.icon = icon
        self.items = items


ALL_ROLES = [
    JobChoices.DEVELOPER,
    JobChoices.ADMINISTRATOR,
    JobChoices.TEACHER,
    JobChoices.STUDENT,
]

MENU = [
    MenuCategory(
        name="home",
        label="Home",
        icon="fa-house",
        items=[
            MenuItem(
                "dashboard_developer",
                "Dashboard Developer",
                "dashboard_developer",
                "fa-gauge",
                [JobChoices.DEVELOPER],
            ),
            MenuItem(
                "dashboard_administrator",
                "Dashboard Administrator",
                "dashboard_administrator",
                "fa-gauge",
                [JobChoices.ADMINISTRATOR],
            ),
            MenuItem(
                "dashboard_teacher",
                "Dashboard Teacher",
                "dashboard_teacher",
                "fa-gauge",
                [JobChoices.TEACHER],
            ),
            MenuItem(
                "dashboard_student",
                "Dashboard Student",
                "dashboard_student",
                "fa-gauge",
                [JobChoices.STUDENT],
            ),
            MenuItem("profile", "Profil", "profile", "fa-user", ALL_ROLES),
            MenuItem(
                "teacher_journal",
                "Jurnal Guru",
                "teacher_journal",
                "fa-book-journal-whills",
                [JobChoices.TEACHER],
            ),
            MenuItem(
                "student_journal",
                "Jurnal Siswa",
                "student_journal",
                "fa-book-journal-whills",
                [JobChoices.STUDENT],
            ),
        ],
    ),
    MenuCategory(
        name="academic",
        label="Akademik",
        icon="fa-school",
        items=[
            MenuItem(
                "academic_year",
                "Tahun Ajaran",
                "academic_year",
                "fa-calendar-days",
                [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR],
            ),
            MenuItem(
                "term",
                "Semester",
                "term",
                "fa-calendar-week",
                [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR],
            ),
            MenuItem(
                "subject",
                "Mata Pelajaran",
                "subject",
                "fa-book",
                [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR],
            ),
            MenuItem(
                "classroom",
                "Kelas",
                "classroom",
                "fa-door-open",
                [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR],
            ),
        ],
    ),
    MenuCategory(
        name="active_management",
        label="Manajemen Aktif",
        icon="fa-toggle-on",
        items=[
            MenuItem(
                "active_year",
                "Tahun Ajaran Aktif",
                "active_year",
                "fa-calendar-check",
                [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR],
            ),
            MenuItem(
                "active_subject",
                "Mata Pelajaran Aktif",
                "active_subject",
                "fa-list-check",
                [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR],
            ),
            MenuItem(
                "active_classroom",
                "Kelas Aktif",
                "active_classroom",
                "fa-chalkboard-user",
                [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR],
            ),
        ],
    ),
    MenuCategory(
        name="learning_teacher",
        label="Pembelajaran Guru",
        icon="fa-chalkboard",
        items=[
            MenuItem(
                "teacher_material",
                "Materi",
                "teacher_material",
                "fa-folder-open",
                [JobChoices.TEACHER],
            ),
            MenuItem(
                "teacher_assignment",
                "Tugas",
                "teacher_assignment",
                "fa-pen-to-square",
                [JobChoices.TEACHER],
            ),
            MenuItem(
                "teacher_question_bank",
                "Bank Soal",
                "teacher_question_bank",
                "fa-database",
                [JobChoices.TEACHER],
            ),
            MenuItem(
                "teacher_quiz",
                "Kuis",
                "teacher_quiz",
                "fa-clipboard-question",
                [JobChoices.TEACHER],
            ),
            MenuItem(
                "teacher_grade_report",
                "Laporan Nilai",
                "teacher_grade_report",
                "fa-chart-line",
                [JobChoices.TEACHER],
            ),
        ],
    ),
    MenuCategory(
        name="learning_student",
        label="Pembelajaran Siswa",
        icon="fa-graduation-cap",
        items=[
            MenuItem(
                "student_material",
                "Materi",
                "student_material",
                "fa-folder-open",
                [JobChoices.STUDENT],
            ),
            MenuItem(
                "student_assignment",
                "Tugas",
                "student_assignment",
                "fa-pen-to-square",
                [JobChoices.STUDENT],
            ),
            MenuItem(
                "student_practice",
                "Latihan Soal",
                "student_practice",
                "fa-file-circle-question",
                [JobChoices.STUDENT],
            ),
            MenuItem(
                "student_quiz",
                "Kuis",
                "student_quiz",
                "fa-clipboard-question",
                [JobChoices.STUDENT],
            ),
            MenuItem(
                "student_grade_report",
                "Laporan Nilai",
                "student_grade_report",
                "fa-chart-line",
                [JobChoices.STUDENT],
            ),
        ],
    ),
    MenuCategory(
        name="assessment",
        label="Penilaian",
        icon="fa-clipboard-list",
        items=[
            MenuItem(
                "assessment_daily",
                "Penilaian Harian",
                "assessment_daily",
                "fa-calendar-day",
                [JobChoices.TEACHER],
            ),
            MenuItem(
                "assessment_midterm",
                "Penilaian Tengah Semester",
                "assessment_midterm",
                "fa-calendar-days",
                [JobChoices.TEACHER],
            ),
            MenuItem(
                "assessment_final",
                "Penilaian Akhir Semester",
                "assessment_final",
                "fa-calendar-check",
                [JobChoices.TEACHER],
            ),
            MenuItem(
                "ledger", "Leger Nilai", "ledger", "fa-table-list", [JobChoices.TEACHER]
            ),
        ],
    ),
    MenuCategory(
        name="homeroom",
        label="Wali Kelas",
        icon="fa-users",
        items=[
            MenuItem(
                "homeroom_students",
                "Siswa Bimbingan",
                "homeroom_students",
                "fa-user-graduate",
                [JobChoices.TEACHER],
            ),
            MenuItem(
                "homeroom_grade_recap",
                "Rekap Nilai",
                "homeroom_grade_recap",
                "fa-chart-bar",
                [JobChoices.TEACHER],
            ),
            MenuItem(
                "homeroom_download",
                "Unduh Nilai",
                "homeroom_download",
                "fa-download",
                [JobChoices.TEACHER],
            ),
        ],
    ),
    MenuCategory(
        name="settings",
        label="Pengaturan",
        icon="fa-gear",
        items=[
            MenuItem(
                "user_account",
                "Akun Pengguna",
                "user_account",
                "fa-user-gear",
                [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR],
            ),
            MenuItem("brand", "Brand", "brand", "fa-tags", [JobChoices.DEVELOPER]),
            MenuItem(
                "school",
                "Sekolah",
                "school",
                "fa-building-columns",
                [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR],
            ),
            MenuItem(
                "backup_restore",
                "Cadangkan & Pulihkan",
                "backup_restore",
                "fa-cloud-arrow-up",
                [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR],
            ),
            MenuItem(
                "log_activity",
                "Log Aktivitas",
                "log_activity",
                "fa-list-ul",
                [JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR],
            ),
        ],
    ),
]


def get_menus_for_user(user):
    if not is_authenticated(user):
        return []
    user_role = getattr(user, "job", None)
    if not user_role:
        return []
    menus = []
    for category in MENU:
        items = [item for item in category.items if user_role in item.roles]
        if items:
            menus.append(
                MenuCategory(category.name, category.label, category.icon, items)
            )
    return menus
