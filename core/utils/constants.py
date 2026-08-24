from django.db import models


class JobChoices(models.TextChoices):
    DEVELOPER = "developer", "Developer"
    ADMINISTRATOR = "administrator", "Administrator"
    TEACHER = "teacher", "Teacher"
    STUDENT = "student", "Student"


class GenderChoices(models.TextChoices):
    MALE = "male", "Laki-laki"
    FEMALE = "female", "Perempuan"


class ReligionChoices(models.TextChoices):
    ISLAM = "islam", "Islam"
    CHRISTIAN = "christian", "Kristen"
    CATHOLIC = "catholic", "Katolik"
    HINDU = "hindu", "Hindu"
    BUDDHA = "buddha", "Buddha"
    KONGHUCU = "konghucu", "Konghucu"


class ClassLevelChoices(models.TextChoices):
    CLASS_1 = "1", "Kelas 1"
    CLASS_2 = "2", "Kelas 2"
    CLASS_3 = "3", "Kelas 3"
    CLASS_4 = "4", "Kelas 4"
    CLASS_5 = "5", "Kelas 5"
    CLASS_6 = "6", "Kelas 6"
    CLASS_7 = "7", "Kelas 7"
    CLASS_8 = "8", "Kelas 8"
    CLASS_9 = "9", "Kelas 9"
    CLASS_10 = "10", "Kelas 10"
    CLASS_11 = "11", "Kelas 11"
    CLASS_12 = "12", "Kelas 12"


class SubjectChoices(models.TextChoices):
    MATEMATIKA = "matematika", "Matematika"
    BAHASA_INDONESIA = "bahasa_indonesia", "Bahasa Indonesia"
    BAHASA_INGGRIS = "bahasa_inggris", "Bahasa Inggris"
    IPA = "ipa", "IPA"
    IPS = "ips", "IPS"
    PPKN = "ppkn", "PPKn"
    SENI_BUDAYA = "seni_budaya", "Seni Budaya"
    PENJASKES = "penjaskes", "Penjaskes"
    INFORMATIKA = "informatika", "Informatika"
    AGAMA = "agama", "Agama"
    LAINNYA = "lainnya", "Lainnya"


class SchoolTypeChoices(models.TextChoices):
    SD = "sd", "SD"
    SMP = "smp", "SMP"
    SMA = "sma", "SMA"
    SMK = "smk", "SMK"
    MI = "mi", "MI"
    MTS = "mts", "MTs"
    MA = "ma", "MA"
    LAINNYA = "lainnya", "Lainnya"


class SchoolStatusChoices(models.TextChoices):
    NEGERI = "negeri", "Negeri"
    SWASTA = "swasta", "Swasta"


class AccreditationChoices(models.TextChoices):
    A = "a", "A"
    B = "b", "B"
    C = "c", "C"
    UNGGUL = "unggul", "Unggul"
    BAIK = "baik", "Baik"
    BELUM_TERAKREDITASI = "belum_terakreditasi", "Belum Terakreditasi"


class TermChoices(models.TextChoices):
    GANJIL = "ganjil", "Ganjil"
    GENAP = "genap", "Genap"


class QuestionTypeChoices(models.TextChoices):
    MULTIPLE_CHOICE = "MC", "Pilihan Ganda"
    ESSAY = "ES", "Esai"
    TRUE_FALSE = "TF", "Benar/Salah"
    SHORT_ANSWER = "SA", "Jawaban Singkat"


class DifficultyChoices(models.TextChoices):
    EASY = "Easy", "Mudah"
    MEDIUM = "Medium", "Sedang"
    HARD = "Hard", "Sulit"


class AssignmentTypeChoices(models.TextChoices):
    INDIVIDUAL = "Individual", "Individu"
    GROUP = "Group", "Kelompok"


class AssignmentStatusChoices(models.TextChoices):
    DRAFT = "Draft", "Draf"
    PUBLISHED = "Published", "Diterbitkan"
    CLOSED = "Closed", "Ditutup"


class SubmissionStatusChoices(models.TextChoices):
    SUBMITTED = "Submitted", "Terkumpul"
    RETURNED = "Returned", "Dikembalikan"
    GRADED = "Graded", "Dinilai"


class QuizStatusChoices(models.TextChoices):
    DRAFT = "Draft", "Draf"
    PUBLISHED = "Published", "Diterbitkan"
    CLOSED = "Closed", "Ditutup"


class JournalActivityChoices(models.TextChoices):
    CREATE = "create", "Membuat"
    UPDATE = "update", "Memperbarui"
    DELETE = "delete", "Menghapus"
    SUBMIT = "submit", "Mengumpulkan"
    GRADE = "grade", "Menilai"
    RETURN = "return", "Mengembalikan"
    PUBLISH = "publish", "Menerbitkan"
    ATTEMPT = "attempt", "Mengerjakan"
    VIEW = "view", "Melihat"
    LOGIN = "login", "Masuk"
    LOGOUT = "logout", "Keluar"


class JournalModuleChoices(models.TextChoices):
    MATERIAL = "material", "Materi"
    ASSIGNMENT = "assignment", "Tugas"
    ASSIGNMENT_SUBMISSION = "assignment_submission", "Pengumpulan Tugas"
    QUESTION_BANK = "question_bank", "Bank Soal"
    QUESTION = "question", "Soal"
    QUIZ = "quiz", "Kuis"
    QUIZ_ATTEMPT = "quiz_attempt", "Percobaan Kuis"
    GRADE = "grade", "Nilai"
    SCHOOL = "school", "Sekolah"
    BRAND = "brand", "Brand"
    PROFILE = "profile", "Profil"
    OTHER = "other", "Lainnya"


class LogLevelChoices(models.TextChoices):
    DEBUG = "debug", "Debug"
    INFO = "info", "Info"
    WARNING = "warning", "Warning"
    ERROR = "error", "Error"
    CRITICAL = "critical", "Critical"


TEACHER_LIMIT = {"job": JobChoices.TEACHER}
STUDENT_LIMIT = {"job": JobChoices.STUDENT}
