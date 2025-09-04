from django.core.management.base import BaseCommand
from blog_v2.models import Role, CommonPermission


class Command(BaseCommand):
    help = 'Команда которая создает все предполагаемые роли и устанавливает им соответствующие разрешения'

    def handle(self, *args, **options):
        # Создаем роли
        roles_data = [
            {
                'name': 'user',
                'description': 'Regular user with basic permissions',
                'permissions': {
                    'read_all_permission': True,
                    'create_permission': False,
                    'update_all_permission': False,
                    'delete_all_permission': False
                }
            },
            {
                'name': 'editor',
                'description': 'Editor with content management permissions',
                'permissions': {
                    'read_all_permission': True,
                    'create_permission': True,
                    'update_all_permission': True,
                    'delete_all_permission': False
                }
            },
            {
                'name': 'controller',
                'description': 'Controller with moderation permissions',
                'permissions': {
                    'read_all_permission': True,
                    'create_permission': False,
                    'update_all_permission': False,
                    'delete_all_permission': True
                }
            },
            {
                'name': 'admin',
                'description': 'Administrator with full permissions',
                'permissions': {
                    'read_all_permission': True,
                    'create_permission': True,
                    'update_all_permission': True,
                    'delete_all_permission': True
                }
            }
        ]

        created_count = 0
        updated_count = 0

        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults={'description': role_data['description']}
            )

            if not created:
                role.description = role_data['description']
                role.save()
                updated_count += 1
            else:
                created_count += 1

            # Создаем или обновляем разрешения для ролей
            permission, perm_created = CommonPermission.objects.get_or_create(
                role=role,
                defaults=role_data['permissions']
            )

            if not perm_created:
                # Обновляем существующие разрешения
                for key, value in role_data['permissions'].items():
                    setattr(permission, key, value)
                permission.save()

        # выводим информацию о выполнении команды в консоль
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} and updated {updated_count} roles with permissions!'
            )
        )