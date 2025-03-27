from django.contrib import admin, messages
from django.utils.html import format_html
from .models import NetworkObject, Contact, Address, Product, Employee
from .tasks import async_data_cleaning_task

class ContactInline(admin.StackedInline):
    model = Contact
    extra = 0


class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 0


@admin.register(NetworkObject)
class NetworkObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier_link', 'hierarchy', 'level', 'debt', 'created_at', 'copy_email_button')
    list_filter = ('contacts__address__city', 'level',)
    search_fields = ('name',)

    inlines = [ContactInline, EmployeeInline]
    actions = ['clear_debt']

    def supplier_link(self, obj):
        if obj.supplier:
            return format_html('<a href="{}">{}</a>', obj.supplier.pk, obj.supplier.name)
        return "-"

    supplier_link.short_description = "Поставщик"

    def clear_debt(self, request, queryset):
        object_ids = list(queryset.values_list('id', flat=True))

        if len(object_ids) > 20:
            async_data_cleaning_task.delay(object_ids)
            self.message_user(request, "Очистка задолженности запущена в фоне.", messages.INFO)
        else:
            updated = queryset.update(debt=0)
            self.message_user(request, f"Задолженность очищена для {updated} объектов", messages.SUCCESS)

    clear_debt.short_description = "Очистить задолженность перед поставщиком"

    def copy_email_button(self, obj):
        if obj.contacts.exists():
            contact = obj.contacts.first()
            return format_html(
                f'<button class="copy-email-btn" data-email="{contact.email}">📋 Копировать Email</button>',
            )
        return "-"

    copy_email_button.short_description = "Копировать Email"

    class Media:
        js = ('admin/js/copy_email.js',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'network_object')
    search_fields = ('email',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('country', 'city', 'street', 'house_number')
    search_fields = ('country', 'city', 'street')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'model', 'release_date')
    filter_horizontal = ('network_object',)
    search_fields = ('name', 'model')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position', 'network_object')
    search_fields = ('first_name', 'last_name', 'position')
