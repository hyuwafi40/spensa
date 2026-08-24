from .account import CustomUserAdmin
from .brand import BrandAdmin, SchoolAdmin
from .academic import (
    YearAdmin,
    TermAdmin,
    SubjectAdmin,
    ClassroomAdmin,
    ActiveYearAdmin,
    ActiveSubjectAdmin,
    ActiveClassroomAdmin,
    ActiveStudentAdmin,
)
from .learning import (
    MaterialAdmin,
    AssignmentAdmin,
    AssignmentSubmissionAdmin,
    QuestionBankAdmin,
    QuestionAdmin,
    AnswerOptionAdmin,
    QuizAdmin,
    QuizAttemptAdmin,
)
from .assessment import AssessmentAdmin
from .journal import TeacherJournalAdmin, StudentJournalAdmin
from .log import DeveloperLogAdmin

__all__ = [
    "CustomUserAdmin",
    "BrandAdmin",
    "SchoolAdmin",
    "YearAdmin",
    "TermAdmin",
    "SubjectAdmin",
    "ClassroomAdmin",
    "ActiveYearAdmin",
    "ActiveSubjectAdmin",
    "ActiveClassroomAdmin",
    "ActiveStudentAdmin",
    "MaterialAdmin",
    "AssignmentAdmin",
    "AssignmentSubmissionAdmin",
    "QuestionBankAdmin",
    "QuestionAdmin",
    "AnswerOptionAdmin",
    "QuizAdmin",
    "QuizAttemptAdmin",
    "AssessmentAdmin",
    "TeacherJournalAdmin",
    "StudentJournalAdmin",
    "DeveloperLogAdmin",
]
