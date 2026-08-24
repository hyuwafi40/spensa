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
]
