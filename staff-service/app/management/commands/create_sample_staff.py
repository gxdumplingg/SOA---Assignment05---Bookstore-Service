from django.core.management.base import BaseCommand
from app.models import Staff


class Command(BaseCommand):
    help = 'Tạo nhân viên mẫu'

    def handle(self, *args, **kwargs):
        staff_data = [
            {'name': 'Nguyễn Văn A', 'email': 'staff1@bookstore.com', 'role': 'Nhân viên kho', 'department': 'Kho'},
            {'name': 'Trần Thị B', 'email': 'staff2@bookstore.com', 'role': 'Nhân viên bán hàng', 'department': 'Bán hàng'},
            {'name': 'Lê Văn C', 'email': 'staff3@bookstore.com', 'role': 'Quản lý', 'department': 'Quản lý'},
        ]
        for data in staff_data:
            staff, created = Staff.objects.get_or_create(
                email=data['email'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Đã tạo nhân viên: {staff.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Nhân viên đã tồn tại: {staff.name}'))
        self.stdout.write(self.style.SUCCESS(f'\nTổng: {Staff.objects.count()} nhân viên'))
