from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from core.views.base import RoleDashboardMixin
from core.utils.constants import JobChoices, SubmissionStatusChoices
from core.models import (
    CustomUser,
    Year,
    Term,
    Subject,
    Classroom,
    ActiveYear,
    ActiveSubject,
    ActiveClassroom,
    ActiveStudent,
    Material,
    Assignment,
    AssignmentSubmission,
    QuestionBank,
    Quiz,
    Assessment,
    TeacherJournal,
    StudentJournal,
    DeveloperLog,
)


class IndexRedirectView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        job = request.user.job
        if job == JobChoices.DEVELOPER:
            return redirect("core:dashboard_developer")
        elif job == JobChoices.ADMINISTRATOR:
            return redirect("core:dashboard_administrator")
        elif job == JobChoices.TEACHER:
            return redirect("core:dashboard_teacher")
        elif job == JobChoices.STUDENT:
            return redirect("core:dashboard_student")
        return redirect("login")


class DeveloperDashboardView(RoleDashboardMixin, TemplateView):
    template_name = "core/index/dev.html"
    roles = [JobChoices.DEVELOPER]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "user_count": CustomUser.objects.count(),
                "developer_count": CustomUser.objects.filter(
                    job=JobChoices.DEVELOPER
                ).count(),
                "administrator_count": CustomUser.objects.filter(
                    job=JobChoices.ADMINISTRATOR
                ).count(),
                "teacher_count": CustomUser.objects.filter(
                    job=JobChoices.TEACHER
                ).count(),
                "student_count": CustomUser.objects.filter(
                    job=JobChoices.STUDENT
                ).count(),
                "year_count": Year.objects.count(),
                "term_count": Term.objects.count(),
                "subject_count": Subject.objects.count(),
                "classroom_count": Classroom.objects.count(),
                "active_year_count": ActiveYear.objects.count(),
                "active_subject_count": ActiveSubject.objects.count(),
                "active_classroom_count": ActiveClassroom.objects.count(),
                "active_student_count": ActiveStudent.objects.count(),
                "material_count": Material.objects.count(),
                "assignment_count": Assignment.objects.count(),
                "quiz_count": Quiz.objects.count(),
                "question_bank_count": QuestionBank.objects.count(),
                "assessment_count": Assessment.objects.count(),
                "teacher_journal_count": TeacherJournal.objects.count(),
                "student_journal_count": StudentJournal.objects.count(),
                "recent_logs": DeveloperLog.objects.order_by("-created_at")[:5],
            }
        )
        return context


class AdministratorDashboardView(RoleDashboardMixin, TemplateView):
    template_name = "core/index/admin.html"
    roles = [JobChoices.ADMINISTRATOR]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "user_count": CustomUser.objects.count(),
                "teacher_count": CustomUser.objects.filter(
                    job=JobChoices.TEACHER
                ).count(),
                "student_count": CustomUser.objects.filter(
                    job=JobChoices.STUDENT
                ).count(),
                "subject_count": Subject.objects.count(),
                "classroom_count": Classroom.objects.count(),
                "active_year": ActiveYear.objects.filter(is_active=True).first(),
                "active_classrooms": ActiveClassroom.objects.select_related(
                    "classroom", "teacher"
                ).all()[:5],
                "active_subjects": ActiveSubject.objects.select_related(
                    "subject", "classroom", "teacher"
                ).all()[:5],
            }
        )
        return context


class TeacherDashboardView(RoleDashboardMixin, TemplateView):
    template_name = "core/index/teacher.html"
    roles = [JobChoices.TEACHER]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.request.user
        context.update(
            {
                "teacher": teacher,
                "active_subjects": ActiveSubject.objects.filter(
                    teacher=teacher
                ).select_related("subject", "classroom")[:5],
                "active_classrooms": ActiveClassroom.objects.filter(
                    teacher=teacher
                ).select_related("classroom")[:5],
                "student_count": ActiveStudent.objects.filter(
                    classroom__teacher=teacher
                ).count(),
                "material_count": Material.objects.filter(teacher=teacher).count(),
                "assignment_count": Assignment.objects.filter(teacher=teacher).count(),
                "quiz_count": Quiz.objects.filter(teacher=teacher).count(),
                "question_bank_count": QuestionBank.objects.filter(
                    teacher=teacher
                ).count(),
                "pending_submissions_count": AssignmentSubmission.objects.filter(
                    assignment__teacher=teacher,
                    status=SubmissionStatusChoices.SUBMITTED,
                ).count(),
                "recent_journals": TeacherJournal.objects.filter(
                    teacher=teacher
                ).order_by("-created_at")[:5],
            }
        )
        return context


class StudentDashboardView(RoleDashboardMixin, TemplateView):
    template_name = "core/index/student.html"
    roles = [JobChoices.STUDENT]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user
        active_student = (
            ActiveStudent.objects.filter(student=student)
            .select_related("classroom__classroom")
            .first()
        )
        classroom = active_student.classroom if active_student else None

        context.update(
            {
                "student": student,
                "active_student": active_student,
                "classroom": classroom,
                "materials": (
                    Material.objects.filter(classroom=classroom.classroom).order_by(
                        "-created_at"
                    )[:5]
                    if classroom
                    else []
                ),
                "assignments": (
                    Assignment.objects.filter(classroom=classroom.classroom).order_by(
                        "-created_at"
                    )[:5]
                    if classroom
                    else []
                ),
                "quizzes": (
                    Quiz.objects.filter(classroom=classroom.classroom).order_by(
                        "-created_at"
                    )[:5]
                    if classroom
                    else []
                ),
                "assessments": Assessment.objects.filter(
                    student=student
                ).select_related("subject", "active_year__year", "active_year__term")[
                    :5
                ],
                "recent_journals": StudentJournal.objects.filter(
                    student=student
                ).order_by("-created_at")[:5],
            }
        )
        return context
